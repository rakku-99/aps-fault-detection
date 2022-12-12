import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os, sys
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
        logging.info(f"Reading data from database:{database} and collection: {collection_name} ")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found column:{df.columns} ")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop('_id',axis=1)
        logging.info(f"Row and col in df: {df.shape}")
        return df
    except Exception as e:
        raise SensorException(e, sys)