from src.logger import logging
from src.exception import MyException
import yaml
import sys
import os

def read_yaml_file(filepath:str):
    try:
        with open(filepath,'rb') as file:
            return yaml.safe_load(file)

    except Exception as e:
        raise MyException(e,sys)

def write_yaml_file(filepath:str,content:str,replace:bool=False)->None:
    try:
        if replace==True:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)

        with open(filepath,'w') as file:
            return yaml.dump(content,file)

    except Exception as e:
        raise MyException(e,sys)
