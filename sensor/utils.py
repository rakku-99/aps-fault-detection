import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os, sys
import yaml
import dill
import numpy as np

def get_connection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    ''' Description : This function returns collection as dataframe
    ===============================================================
    Params:
    databse_name:database_name
    collection_name:collectin_name
    ===============================================================
    return Pandas dataframe of a collection
    '''
    try:
        logging.info(f"Reading data from database:{database_name} and collection: {collection_name} ")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found column:{df.columns} ")

        # useless formed '_id' column in all Mongo db
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop('_id',axis=1)
        logging.info(f"Row and col in df: {df.shape}")
        return df
        
    except Exception as e:
        raise SensorException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir=os.path.dirname(file_path)

        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data, file_writer)
        logging.info("Executed the write_yaml_file method of utils")
    except Exception as e:
        raise SensorException(e, sys)
        
def convert_columns_float(df,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        logging.info("Executed the convert_columns_float method of utils")
        return df
    except Exception as e:
        raise e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Executed the save_object method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e

def load_object(file_path: str, ) -> object:
    try:
        logging.info("Entered the load_object method of utils")
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
        logging.info("Executed the load_object method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e
        
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        logging.info("Entered the save_numpy_array_data method of utils")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info("Executed the save_numpy_array_data method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        logging.info("Entered the load_numpy_array_data method of utils")
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
        logging.info("Executed the load_numpy_array_data method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e