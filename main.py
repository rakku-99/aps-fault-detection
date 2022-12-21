'''import pymongo

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")
# Database Name
dataBase = client["neurolabDB"]

# Collection  Name
collection = dataBase['Products']

# Sample data
d = {'companyName': 'iNeuron',
     'product': 'Affordable AI',
     'courseOffered': 'Machine Learning with Deployment'}

# Insert above records in the collection
rec = collection.insert_one(d)

# Lets Verify all the record at once present in the record with all the fields
all_record = collection.find()

# Printing all records present in the collection
for idx, record in enumerate(all_record):
     print(f"{idx}: {record}")
'''


from sensor.utils import get_connection_as_dataframe
import os,sys

if __name__=="__main__":
     try:
          get_connection_as_dataframe(database_name="aps", collection_name='sensor')
     except Exception as e:
          print(e)

import pandas as pd
import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_connection_as_dataframe
from sensor.components import data_ingestion
from sensor.components.data_ingestion import DataIngestion
from sensor.entity import config_entity
from sensor.entity.config_entity import DataIngestionConfig
from sensor.components.data_validation import DataValidation

file_path="/config/workspace/aps_failure_training_set1.csv"
print(__name__)

if __name__=="__main__":
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          #print(data_ingestion.initiate_data_ingestion())
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

          data_validation_config= config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                         data_ingestion_artifact=data_ingestion_artifact)
          
          data_validation_artifact = data_validation.initiate_data_validation()

     except Exception as e:
          print(e)
          