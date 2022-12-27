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
from sensor.entity import config_entity, artifact_entity
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
#from sensor.components.model_pusher import ModelPusher

file_path="/config/workspace/aps_failure_training_set1.csv"
print(__name__)

if __name__=="__main__":
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          print("Data Ingestion started")
          data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          #print(data_ingestion_config.to_dict())
          #print(data_ingestion.initiate_data_ingestion())
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

          print("Data Validation started")
          data_validation_config= config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                         data_ingestion_artifact=data_ingestion_artifact)
          
          data_validation_artifact = data_validation.initiate_data_validation()
          
          print("Data Transformation started")
          data_transformation_config= config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation=DataTransformation(data_transformation_config=data_transformation_config, 
                    data_ingestion_artifact=data_ingestion_artifact)       
          data_transformation_artifact = data_transformation.initiate_data_transformation()

          print("Model Training started") 
          model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, 
                              data_transformation_artifact=data_transformation_artifact)            
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          print("Model Evaluation started") 
          model_eval_config=config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval = ModelEvaluation(model_eval_config=model_eval_config, 
                                   data_ingestion_artifact=data_ingestion_artifact, 
                                   data_transformation_artifact=data_transformation_artifact, 
                                   model_trainer_artifact=model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()

     except Exception as e:
          print(e)
          