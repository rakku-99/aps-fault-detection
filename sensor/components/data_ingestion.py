from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact: #, train_file_path, test_file_path
        try:
            logging.info("Exporting collection data as pandas dataframe")
            # Exporting collection data as pandas dataframe
            df:Dataframe= utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)
            
            logging.info("save data in feature store")
            # save data in feature store 
            df.replace(to_replace='na',value=na.NAN, inplace=True)
            
            logging.info('create feature store folder')
            #create feature store folder
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True,)

            logging.info('save df to feature store folder')
            # save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            logging.info('split datasets into 2 parts Train & test set')
            #split datasets into 2 parts Train & test set
            train_df,test_df=train_test_split(df, test_size=self.data_ingestion_config.test_size)

            logging.info('create dataset directory if not available')
            # create dataset directory if not available
            dataset_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info('save df to feature stotre folder')
            #save df to feature stotre folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False)

            #prepare output- artifact
            data_ingestion_artifact=artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)
            
            logging.info("Data ingestion Component")
            return data_ingestion_artifact


        except Exception as e:
            raise SensorException(error_message=e, error_details=sys)