from src.logger import logging
from src.exception import MyException
from sklearn.model_selection import train_test_split
import pandas as pd
from src.data_access.proj1_data import Proj1Data
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifacts
import sys
import os

class DataIngestion:

    '''gets all the filepaths for dataingestion defined in config.entity by creating an object of its dataclass'''
    def __init__(self,data_ingestion_config=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
            
        except Exception as e:
            raise MyException(e,sys)

    
    '''
    retireves data from MOngoDB and converts it into pd.Dataframe by creating an object for 
    Proj1Data class defined in data_access, and saves this dataframe at feature_store_path (defined in
    config_entity.py)
    '''
    def export_data_into_feature_store(self)->pd.DataFrame:
        try:
            logging.info('Exporting data from MongoDB')
            data=Proj1Data()
            df=data.convert_to_df(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f'SHape of dataframe {df.shape}')
            feature_store_path=self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path),exist_ok=True)

            logging.info(f'saving dataframe to feature store {feature_store_path}')
            df.to_csv(feature_store_path,index=False,header=True)
            
            return df
        except Exception as e:
            raise MyException(e,sys)

    '''Performes train_test_split on df and saves train_set and test_set in train_file and test_file_path'''
    def split_save(self,dataframe:pd.DataFrame)->None:
        try:
            logging.info('Performing train_test_split')
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            train_file_path=self.data_ingestion_config.training_file_path
            testing_file_path=self.data_ingestion_config.testing_file_path
            os.makedirs(os.path.dirname(train_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(testing_file_path),exist_ok=True)

            logging.info(f'saving train_set to {train_file_path} and test_set to {testing_file_path}')
            train_set.to_csv(train_file_path,index=False,header=True)
            test_set.to_csv(testing_file_path,index=False,header=True)

        except Exception as e:
            raise MyException(e,sys)

    '''Calls both functions and saves train_set and test_set save path in an object of DataIngestionArtifacts '''
    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        try:
            df=self.export_data_into_feature_store()
            logging.info('Got data from MongoDB')

            self.split_save(dataframe=df)
            logging.info('Saved train and test data to respective datapaths')

            data_ingestion_artifact=DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f'Data_ingestion_artifact: {data_ingestion_artifact}')

            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e,sys)





        