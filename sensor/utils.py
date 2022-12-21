import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os, sys
import yaml

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
            
    except Exception as e:
        raise SensorException(e, sys)
        
def convert_columns_float(df,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise SensorException(e, sys)
    
    