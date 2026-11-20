from src.entity.config_entity import *
from src.entity.artifact_entity import *
from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import MyException
import sys
from src.components.data_validation import  Data_validation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainingPipline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTranformationConfig()
        self.model_trainer_config=ModelTrainerConfing()
        

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

    def start_data_transformation(self,data_ingetion_artifacts:DataIngestionArtifacts,data_validation_artifact:DataValidationArtifacts)->DataTransformationArifacts:
        logging.info('Starting data transformation')
        obj=DataTransformation(data_validation_artifact=data_validation_artifact,
                               data_ingetion_artifacts=data_ingetion_artifacts,
                               data_transformation_config=self.data_transformation_config)
        data_transformation_artifact=obj.start_data_transformation()
        return data_transformation_artifact


    def start_model_training(self,data_transformation_artifacts:DataTransformationArifacts):
        obj=ModelTrainer(self.model_trainer_config,data_transformation_artifacts)

        model_trainer_artifacts=obj.initiate_model_training()

        return model_trainer_artifacts

    '''Running complete pipeline'''
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact= self.start_data_transformation(data_ingestion_artifact,data_validation_artifact)
            model_trainer_artifacts=self.start_model_training(data_transformation_artifacts=data_transformation_artifact)
        
        except Exception as e:
            raise MyException(e,sys)

