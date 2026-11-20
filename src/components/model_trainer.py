import pandas as pd
import os,sys
import numpy as np
from src.logger import logging
from src.exception import MyException
from typing import Tuple
from src.utils.main_utils import *
from src.entity.config_entity import ModelTrainerConfing
from src.entity.artifact_entity import DataTransformationArifacts,ModelTrainerArtifact,ClassificationMetricArtifact

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score
from src.entity.estimator import MyModel


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfing,data_transformation_artifacts:DataTransformationArifacts):
        try:
            self.mt_config=model_trainer_config
            self.dt_artifact=data_transformation_artifacts
            self.model_yaml_config= read_yaml_file(ModelTrainerConfing.model_config_yaml_path)

        except Exception as e:
            raise MyException(e,sys)

        
    '''
    Creates model fits data inside it and performs some evaluations returns both metrics and actual trained model
    '''
    def create_model(self,train:np.array,test:np.array)->Tuple[object,ClassificationMetricArtifact]:
        
        try:
            #splitting into features and target
            X_train,y_train,X_test,y_test=train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            logging.info('train_test_split into features and targets done')

            #loading params from moel.yaml file in config
            rf_params=self.model_yaml_config['model_selection']['params']

            #model creation and fitting data into model
            model=RandomForestClassifier(**rf_params)
            model.fit(X_train,y_train)

            #Making predictions and getting evaluation metrics then saving them in artifacts
            y_pred=model.predict(X_test)
            accuracy=accuracy_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            precison=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)

            metric_artifact=ClassificationMetricArtifact(accuracy_score=accuracy,f1_score=f1,
                                                    precision_score=precison,recall_score=recall)

            return model,metric_artifact


        except Exception as e:
            raise MyException(e,sys)

    def initiate_model_training(self):
        try:
            #loading transforemed train and test
            train_arr=load_numpy_array_data(self.dt_artifact.train_transformed_file_path)
            test_arr=load_numpy_array_data(self.dt_artifact.test_transformed_file_path)
            logging.info('Train test transformed array loaded for model training')

            #getting trained model and some evaluations 
            trained_model,metric_artifact=self.create_model(train_arr,test_arr)
            logging.info('Model object and its metrics loaded')

            #loading preprocessor object that we got from data_transformation step 
            preprocessing_obj=load_object(self.dt_artifact.obj_transformed_file_path)
            logging.info(f'Preprocessor object loaded from: {self.dt_artifact.obj_transformed_file_path}')

            if metric_artifact.accuracy_score<self.model_yaml_config['model_evaluation']['expected_score']:
                logging.info('No model found with accuracy above base score')
                raise Exception('No model found with accuracy above base score')

            #Wrapping trained Model preprocessor object in MYModel class so that they can both be done simultaniously by making 1 call MyModel.predict
            my_model=MyModel(preprocessing_object=preprocessing_obj,trained_model_object=trained_model)

            #Saving model object and saving model_artifacts
            save_object(self.mt_config.trained_model_file_path,my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            model_artifact=ModelTrainerArtifact(self.mt_config.trained_model_file_path,metric_artifact=metric_artifact)

            logging.info(f'Model trainer artifacts: {model_artifact}')

            return model_artifact

        except Exception as e:
            raise MyException(e,sys)

        

        
        