from src.constants import *
from dataclasses import dataclass
from datetime import datetime
import os

'''This is a file where we difine all the paths where we need to store data'''


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    artifact_dir:str=os.path.join(ARTIFACT_DIR,TIMESTAMP)
    pipeline_name:str=PIPELINE_NAME
    timestamp:str=TIMESTAMP

train_config_obj=TrainingPipelineConfig()

'''
map:
-artifact/01-01-2026/data_ingestion
-/feature_store/data.csv
-/ingested/train.csv
-/ingested/test.csv 
'''
@dataclass 
class DataIngestionConfig:
    data_ingestion_dir:str=os.path.join(train_config_obj.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    collection_name:str=COLLECTION_NAME
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

'''
data validation will create a file report.yaml (which contains report of our validation tests) and it will be
stored in following path path defined below:
map:
artifact/timestamp/data_validation/report.yaml
'''
@dataclass 
class DataValidationConfig:
    data_validation_dir:str=os.path.join(train_config_obj.artifact_dir,DATA_VALIDATION_DIR_NAME)
    report_file_path:str=os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass 
class DataTranformationConfig:
    data_tranformation_dir:str=os.path.join(train_config_obj.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    data_tansfromed_dir:str=os.path.join(data_tranformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
    train_transformed_file_path:str=os.path.join(data_tansfromed_dir,'train_transformed.npy')
    test_transformed_file_path:str=os.path.join(data_tansfromed_dir,'test_transformed.npy')
    obj_file_path:str=(os.path.join(data_tansfromed_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                    PREPROCSSING_OBJECT_FILE_NAME))


@dataclass 
class ModelTrainerConfing:
    model_dir:str=os.path.join(train_config_obj.artifact_dir,MODEL_TRAINER_DIR_NAME)
    trained_model_file_path:str=os.path.join(model_dir,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME)
    model_config_yaml_path:str=MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    
