from src.entity.config_entity import DataIngestionConfig,DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import MyException
import sys
from src.components.data_validation import  Data_validation

class TrainingPipline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()

    '''starting dataingestion by creating object for DataIngestionClass while returning its artifacts'''
    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            logging.info(f'Entered the start_data_ingestion methord of TriningPipeline class')
            obj=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=obj.initiate_data_ingestion()
            logging.info(f'Exited the start_data_ingestion methord of TriningPipeline class')
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    '''starting datavalidation by creating object for Data_Validation Class while returning its artifacts'''
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            logging.info(f'Entered the start_data_validation methord of TriningPipeline class')
            obj=Data_validation(data_ingestion_artifact,self.data_validation_config)
            data_validation_artifact=obj.intiate_validation()
            logging.info(f'Exited the start_data_ingestion methord of TriningPipeline class')
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys)

    '''Running complete pipeline'''
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise MyException(e,sys)

