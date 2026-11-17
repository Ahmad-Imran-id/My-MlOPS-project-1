from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifacts
from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import MyException
import sys

class TrainingPipline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

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
            
    '''Running complete pipeline'''
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
        except Exception as e:
            raise MyException(e,sys)

