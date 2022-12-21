from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
# two-sample Kolmogorov-Smirnov test for goodness of fit
from scipy.stats import ks_2samp 
import os,sys
from typing import Optional
import pandas as pd
from sensor import utils
import numpy as np

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20} ")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            # validation error dictionary 
            self.validation_error=dict()

        except Exception as e:
            raise SensorException(e, sys)

    # Read dataframe, check each column has sufficient values 
    # if so many missing values then drop
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        '''
        This function will drop columns containing missing values more than specified
        df: Accepts a pd DataFrame
        threshold: Percentage criteria to drop a column
        =====================================================================================================
        returns pd DataFrame if atleast a sinle column is available after missing value column drop else None
        '''
        try:
            # 2:45 75. 3rd Dec
            threshold=self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            # selecting column name wich contains null above to {thresfold}
            logging.info(f"selecting column name wich contains null above to {threshold}")
            drop_column_names=null_report[null_report>threshold].index
            
            logging.info(f"Columns to drop: {drop_column_names}")
            self.validation_error[report_key_name]=drop_column_names
            df.drop(list(drop_column_names),axis=1,inplace=True)
            
            # Return None if no column left 
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise SensorException(e, sys)

    # count/ check all the columns available in dataset
    # comparing base_df & present_df
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns=base_df.columns
            current_columns=current_df.columns

            missing_columns=[]
            for base_columns in base_columns:
                if base_columns not in current_columns:
                    logging.info(f"Columns: {base_columns} are missing")
                    missing_columns.append(base_columns)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise e

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns=base_df.columns
            current_columns=current_df.columns
            for base_column in base_columns:
                base_data, current_data =base_df[base_column],current_df[base_column]
                # Null hypothessis - both column data drawn from same distribution
                
                logging.info(f"Hypothesis {base_column}:{base_data.dtype}, {current_data.dtype} ")
                same_distribution=ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    #same distribution - Accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":True
                    }                    
                else:
                    # different distribution
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    
            self.validation_error[report_key_name]=drift_report

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base df")
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            # base_df has na as null
            logging.info(f"Replacing na values in base df")
            base_df.replace({"na":np.NAN},inplace=True)

            logging.info(f"Drop null values columns from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")
            
            logging.info(f"Reading train df")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test df")
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null values columns from train df")
            self.drop_missing_values_columns(df=train_df, report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null values columns from test df")
            self.drop_missing_values_columns(df=test_df, report_key_name="missing_values_within_test_dataset")

            exclude_columns=["class"]
            base_df=utils.convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            train_df=utils.convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            test_df=utils.convert_columns_float(df=test_df,exclude_columns=exclude_columns)

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status= self.is_required_columns_exists(base_df=base_df, current_df=train_df, report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status= self.is_required_columns_exists(base_df=base_df, current_df=test_df, report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all columns in train df available hence  detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drip_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all columns in test df available hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drip_within_test_dataset")
            # write report
            logging.info("writing report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path, 
            data=self.validation_error)

            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact:{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)
