import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.pipeline.training_pipeline import start_training_pipeline

file_path="/config/workspace/aps_failure_training_set1.csv"
print(__name__) 

if __name__=="__main__":
     try:
          # start_training_pipeline
          start_training_pipeline()
          print("train.py file ran") 
                  
     except Exception as e:
          print(e)