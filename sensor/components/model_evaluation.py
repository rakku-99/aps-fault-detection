from sensor.predictor import ModelResolver
from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys

class ModelEvaluation:
    def __init__(self, 
                model_eval_config:config_entity.ModelEvaluationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} 5. Model Evaluation {'<<'*20}")
            self.model_eval_config:config.entity.ModelEvaluationConfig
            self.data_ingestion_artifact:artifact_entity.DataIngestionArtifact
            self.data_transformation_artifact:artifact_entity.DataTransformationArtifact
            self.model_trainer_artifact:artifact_entity.ModelTrainerArtifact
            self.model_resolver=ModelResolver()
            
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # if model in saved model folder - 
            # -> compare best trained or model from saved folder
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(
                                    is_model_accepted=True, 
                                    improve_accuracy=None)
            
                return model_eval_artifact
                logging.info(f"Model Evaluation Artifact:{model_eval_artifact} ")

        except Exception as e:
            raise SensorException(e,sys)

