import os, sys
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime

FILE_NAME="sensor.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

REPORT_FILE_NAME="report.yaml"
BASE_FILE_NAME="aps_failure_training_set1.csv"

TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"

MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%d%m%Y__%H%M%S')}")
        except Exception as e:
            raise SensorException(e,sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name='aps'
            self.collection_name='sensor'
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size= 0.2
            
        except Exception as e:
            raise SensorException(e,sys)

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            return SensorException(e,sys)
            
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")
             # To save report of validation- create report in yaml/ json file
            self.report_file_path=os.path.join(self.data_validation_dir,REPORT_FILE_NAME)
             # after missing values colum cehck
            self.missing_threshold:float=0.2
            self.base_file_path=os.path.join(BASE_FILE_NAME)

        except Exception as e:
            raise SensorException(e,sys)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
            self.transform_object_path=os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)            
            self.transformed_train_path=os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
            self.transformed_test_path=os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
            self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)
                        
        except Exception as e:
            raise SensorException(e,sys)
            
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
