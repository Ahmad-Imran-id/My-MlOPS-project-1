from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataIngestionConfig,DataTranformationConfig
from src.entity.artifact_entity import DataIngestionArtifacts,DataTransformationArifacts,DataValidationArtifacts
import pandas as pd
import os
import sys
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder,TargetEncoder,StandardScaler,RobustScaler
from src.utils.main_utils import *
from src.constants import SCHEMA_FILE_PATH,TARGET_COLUMN
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN

class DataTransformation:
    def __init__(self,data_ingetion_artifacts:DataIngestionArtifacts,
                 data_transformation_config:DataTranformationConfig,
                 data_validation_artifact:DataValidationArtifacts):
        try:
            self.data_ingetion_artifacts=data_ingetion_artifacts
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)

    def map_text_cols(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            logging.info('Mapping Gender and Vehicle_Damage collums to 1s and 0s')
            df['Gender']=df['Gender'].map({'Female':0,'Male':1}).astype(int)
            df['Vehicle_Damage']=df['Vehicle_Damage'].map({'No': 0,'Yes': 1}).astype(int)

            return df

        except Exception as e:
            raise MyException(e,sys)


    def drop_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            to_drop = self.schema_config['drop_columns']

            if isinstance(to_drop, str):
                cols = [to_drop]
            else:
                cols = to_drop

            df.drop(columns=cols, inplace=True, errors='ignore')
            logging.info(f'Dropped columns (if present): {cols}')

            return df
        
        except Exception as e:
            raise MyException(e,sys)

    def scaling_encoding_pipline(self)->Pipeline:
        try:
            logging.info('Entered scaling_encoding_pipeline methord of data transformation')
            ss_cols=self.schema_config['ss_cols']
            rs_cols=self.schema_config['rs_cols']
            target_encoding_cols=self.schema_config['target_encoding_cols']
            oe_cols=self.schema_config['ordinal_encoding_cols']
            vehicle_age_order = [['< 1 Year', '1-2 Year', '> 2 Years']]

            preprocessor=ColumnTransformer(
                transformers=[
                    ('ordinal_encoder',OrdinalEncoder(categories=vehicle_age_order),oe_cols),
                    ('target_encoding',TargetEncoder(target_type='binary'),target_encoding_cols),
                    ('standard_scaler',StandardScaler(),ss_cols),
                    ('robust_scaler',RobustScaler(),rs_cols)
                ],
                remainder='passthrough'
            )
            logging.info('Encoders Initialized')
            logging.info(f'({oe_cols}) were ordinally encoded,\n({target_encoding_cols} were target encoded)\n ({ss_cols} were standard scaled)\n ({rs_cols} were robust scaled)')
            
            #wrapping everything in a single pipline for future proofing
            final_pipeline=Pipeline(steps=[('preprocessor',preprocessor)])
            logging.info('final_pipeline ready')
            logging.info('Exited scaling_encoding_pipeline methord of data transformation')

            return final_pipeline
            

        except Exception as e:
            raise MyException(e,sys)


    def start_data_transformation(self)->DataTransformationArifacts:
        try:
            logging.info('Data transformation started')
            validation_status=self.data_validation_artifact.validation_status
            if not validation_status:
                raise Exception(self.data_validation_artifact.error_message)

            logging.info('getting train and test dataframes from data_ingestion_artifacts')
            train_df:pd.DataFrame=read_pd_csv(self.data_ingetion_artifacts.trained_file_path)
            test_df:pd.DataFrame=read_pd_csv(self.data_ingetion_artifacts.test_file_path)

            
            X_train=train_df.drop(columns=[TARGET_COLUMN])
            y_train=train_df[TARGET_COLUMN]

            X_test=test_df.drop(columns=[TARGET_COLUMN])
            y_test=test_df[TARGET_COLUMN]
            logging.info('Input and target collum defined for both train and test df')

            #perfroming small transformations on train features
            X_train=self.drop_cols(X_train)
            X_train=self.map_text_cols(X_train)
            #perfroming small transformations on test features
            X_test=self.drop_cols(X_test)
            X_test=self.map_text_cols(X_test)
            logging.info('required collums droped and text columns mapped to numeric')

            logging.info('getting object for main transforamtion')
            transformation_pipeline=self.scaling_encoding_pipline()

            X_train_arr=transformation_pipeline.fit_transform(X_train,y_train)
            X_test_arr=transformation_pipeline.transform(X_test)
            logging.info('Main transformation completed for both train and test features')

            logging.info('Applying smoteen to handle imbalnced dataset')
            smt=SMOTEENN(sampling_strategy='minority')

            X_train_final,y_train_final=smt.fit_resample(X_train_arr,y_train)
            X_test_final,y_test_final=smt.fit_resample(X_test_arr,y_test)
            logging.info('SMOTEEN aplied to both train and test datasets')

            train_arr=np.c_[X_train_final,np.array(y_train_final)]
            test_arr=np.c_[X_test_final,np.array(y_test_final)]

            logging.info('Saving objects and transformed data to required filepaths')
            save_object(self.data_transformation_config.obj_file_path,transformation_pipeline)
            save_numpy_array_data(self.data_transformation_config.train_transformed_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.test_transformed_file_path,array=test_arr)
            logging.info('Saved objects and transformed data to required filepaths')

            logging.info('Data transformation completed')

            return DataTransformationArifacts(train_transformed_file_path=self.data_transformation_config.train_transformed_file_path,
                                              obj_transformed_file_path=self.data_transformation_config.obj_file_path,
                                              test_transformed_file_path=self.data_transformation_config.test_transformed_file_path)

        except Exception as e:
            raise MyException(e,sys)
    

      