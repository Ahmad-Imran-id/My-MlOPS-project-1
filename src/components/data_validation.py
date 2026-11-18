from src.constants import SCHEMA_FILE_PATH
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataValidationConfig,DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
import os
import sys
from src.utils.main_utils import read_yaml_file,write_yaml_file
import pandas as pd
import json

class Data_validation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_valdation_config=data_validation_config
            self.schema_yaml=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise MyException(e,sys)

    '''
    methord checks to see required colllum lenght is same as actual column length in dataframe
    '''
    def validate_collum_length(self,df:pd.DataFrame)->bool:
        try:
            
            collum_len_validation=len(df.columns)==len(self.schema_yaml['columns'])
            logging.info(f'Are all required colums present {collum_len_validation}')  
            return collum_len_validation
                
        except Exception as e:
            raise MyException(e,sys)

    '''
    mehtord checks to see if all the required collums exist in actual dataframe
    '''
    def validate_all_collums(self,dataframe:pd.DataFrame)->tuple:
        try:
            missing_collums=[] #will store all the missing cols in dataframe compared to required columns
            for col in self.schema_yaml['columns']:
                col_name = list(col.keys())[0]
                if col_name not in dataframe.columns:
                    missing_collums.append(col)

            col_validation=len(missing_collums)==0
            if not col_validation:
                logging.info(f'Data gives in missing these collums: {missing_collums}')

            return col_validation,missing_collums
                
        except Exception as e:
            raise MyException(e,sys)

    '''
    methord to read pandas dataframe from path
    '''
    @staticmethod
    def read_df(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise MyException(e,sys)

    '''
    methord call all the required methords in sequence
    '''
    def intiate_validation(self)->DataValidationArtifacts:
        try:
            #getting train and test as pandas dataframe
            train_df=Data_validation.read_df(self.data_ingestion_artifact.trained_file_path)
            test_df=Data_validation.read_df(self.data_ingestion_artifact.test_file_path)

            validation_error_msg="" #this will store all the error messages that we get if any 

            #len validation call
            train_len_val=self.validate_collum_length(train_df)
            test_len_val=self.validate_collum_length(test_df)

            #appending validation_error message if len validation result is false for both train and test
            if train_len_val==False:
                validation_error_msg+='All required collums are not present in train_dataframe'
                logging.info(f'error all reuired collums are not present in train_dataframe, train_df_validation={train_len_val} ')
            else:
                logging.info(f'length of required collums is equal to len of actual collums in train_df: {train_len_val}')

            if test_len_val==False:
                validation_error_msg+='All required collums are not present in test dataframe'
                logging.info(f'error all reuired collums are not present in train_dataframe, train_df_validation={test_len_val} ')
            else:
                logging.info(f'length of required collums is equal to len of actual collums in test_df: {test_len_val}')      

            #column validation check
            train_col_val,train_missing_col=self.validate_all_collums(train_df)
            test_col_val,test_missing_col=self.validate_all_collums(test_df)

            #appending validation_error message if columns validation result is false
            if train_col_val==False:
                validation_error_msg+=f'columns missing in train_df: {train_missing_col}'
                logging.info(f'error all reuired collums are not present in train_dataframe, train_df_validation:{train_len_val} missing cols:{train_missing_col}')
            else:
                logging.info(f'All required columns are present in train dataframe {train_len_val}')

            if test_col_val==False:
                validation_error_msg+=f'columns missing in test_df: {train_missing_col}'
                logging.info(f'error all required collums are not present in test_dataframe, train_df_validation:{test_len_val} missing cols:{test_missing_col}')
            else:
                logging.info(f'All required columns are present in test dataframe {test_len_val}')

            validation_status=len(validation_error_msg)==0

            #storing all validation artifacts which we will return
            validation_artifact=DataValidationArtifacts(
                validation_status=validation_status
                ,error_message=validation_error_msg
                ,report_file_path=self.data_valdation_config.report_file_path)

            report_dir=os.path.dirname(self.data_valdation_config.report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            #dictionary which we will show in report
            validation_report={
                'validation_status':validation_status,
                'error_messages':validation_error_msg.strip()
            }

            #dumping report in report file
            with open(self.data_valdation_config.report_file_path,'w') as file:
                json.dump(validation_report,file,indent=4)

            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {validation_artifact}")

            return validation_artifact #returning validation artifacts
            
        except Exception as e:
            raise MyException(e,sys)