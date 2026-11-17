from src.configuration.mongo_db_connection import MongoDBClient
import os
import pymongo
import pandas as pd
from typing import Optional
import numpy as np
from src.exception import MyException
import sys

'''Creates an obj for MongoDBclient (i.e inilizing database_name) then creates retives collection and converts 
it into dataframe'''

class Proj1Data:

    def __init__(self):
        self.mongo_client=MongoDBClient()

    def convert_to_df(self,collection_name:str,database_name: Optional[str]=None):
        try:
            if database_name==None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client.client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.tolist():
                df.drop(columns=['_id'],inplace=True)
            df.replace({'na':np.nan},inplace=True)
            return df

        except Exception as e:
            raise MyException(e,sys)
            


        

