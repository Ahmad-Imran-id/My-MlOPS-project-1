import os
import pymongo
from src.logger import logging
from src.exception import MyException
from src.constants import DATABASE_NAME,MONGODB_URL_KEY
import certifi
import sys
from dotenv import load_dotenv

load_dotenv()

ca=certifi.where()


'''We make a class where we make connection with mogodb till database then we import that class and make 
its object inside another class in data_acess proj1_data.py and make collection and create df inside there'''

class MongoDBClient:
    client=None #varable in class

    def __init__(self,database_name=DATABASE_NAME): #create constructor
        
        try:
            if MongoDBClient.client is None: #we set client to none beforehand outside constructor
                mongodb_url=os.getenv('MONGODB_URL_KE') #importing url from env
                if mongodb_url is None: 
                    raise Exception(f'Variable {mongodb_url} is empty')
                    
                MongoDBClient.client=pymongo.MongoClient(mongodb_url,tlsCAFile=ca) #initilizing client

            self.client=MongoDBClient.client
            self.database=self.client[database_name] #initialize database
            self.database_name=database_name
            logging.info('MongoDB connection succesful')
            
        except Exception as e:
            raise MyException(e,sys)



