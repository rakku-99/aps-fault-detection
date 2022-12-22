from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys
import pandas as pd
from sensor import utils
import numpy as np

from sklearn.preprocessing import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transormation_config= data_transormation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod 

    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer=SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler=RobustScaler()
            pipeline = Pipeline(steps=[
                        ('imputer', simple_imputer),
                        ('RobustScaler', robust_scaler)])
            return pipeline

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self,)->artifact_entity.DataTransformation:
        try:
            #reading train & test files
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            # selecting input feature for train & test df
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df =test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature train & test df
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df  = test_df[TARGET_COLUMN]

            # convert pos neg categorical into numerical - 
            label_encoder=LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            input_feature_train_arr = transformation_pipeline.transform(input_feature_test_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            # Handle imbalance - pos=1000, neg=35188
            smt = SMOTETomek(sampling_strategy="minority")
            logging.info(f"Before resampling in training set Input: {input_feature_train_arr}, Traget :{target_feature_train_arr} ")
            input_feature_train_arr,target_feature_train_arr = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr}, Traget :{target_feature_train_arr} ")

            logging.info(f"Before resampling in training set Input: {input_feature_test_arr}, Traget :{target_feature_test_arr} ")
            input_feature_test_arr ,target_feature_test_arr  = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling in training set Input: {input_feature_test_arr}, Traget :{target_feature_test_arr} ")

            # target Encoder
            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr =np.c_[input_feature_test_arr ,target_feature_test_arr] 

            # save numpy array
            # 1:10 4-Dec-22
            utils.save_numpy_array_data(file_path=self.data_transormation_config.transformed_train_path, 
                    array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transormation_config.transformed_test_path, 
                    array=test_arr)

            utils.save_object(file_path=self.data_transormation_config.transform_object_path, 
                    obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transormation_config.target_encoder_path, 
                    obj=label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)






            
            
            # can be shared with all other objects
    # class method vs instance method
        #class classmethod(f: Callable[..., Any]),
        #classmethod(function) -> method,
        #Convert a function to be a class method."""

    #A class method receives the class as implicit first argument,
    #just like an instance method receives the instance.
    #To declare a class method, use this idiom:
    ''' SimpleImputer is a class in the `sklearn.impute` module that can be used 
to replace missing values in a dataset, using a variety of input strategies.
- Here we use SimpleImputer can also be used to impute multiple columns at 
once by passing in a list of column names. SimpleImputer will then replace missing 
values in all of the specified columns.'''
            