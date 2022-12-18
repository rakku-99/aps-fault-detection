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

'''
from sensor.utils import get_connection_as_dataframe
import os,sys

if __name__=="m__main__":
     try:
          get_connection_as_dataframe(database_name="aps", collection_name='sensor')
     except Exception as e:
          print(e)
'''

import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_connection_as_dataframe
from sensor.entity.config_entity import DataIngestionConfig
from sensor.components import data_ingestion

if __name__=="__main__":
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          #get_connection_as_dataframe(database_name="aps",collection_sensor="sensor")
          print(data_ingestion_config.to_dict)
          print(data_ingestion.initiate_data_ingestion())
     except Exception as e:
          print(e)
          