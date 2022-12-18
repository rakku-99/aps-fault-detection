import os
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime

FILE_NAME="sensor.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

class TrainingPipelineConfig:
    def __init__(self):
        self.artifact.dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%H%S')}")

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name='aps'
        self.collection_name='sensor'
        self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,'data_ingestion')
        self.feature_store_dir=os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
        self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.test_file_name=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
        self.test_size= 0.2
    
    def to_dict()->dict:
        try:
            return self.__dict
        except Exception as e:
            return SensorException(e,sys)

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
