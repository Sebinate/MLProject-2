import pandas as pd
import numpy as np

from networksecurity.entity import config_entity, artifact_entity
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
from networksecurity.utils.main_utils.utils import read_schema, write_yaml

from scipy.stats import ks_2samp
import os
import sys

class DataValidation():
    def __init__(self, 
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                 data_validation_config: config_entity.DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_schema(self.data_validation_config.schema_file_path)    

        except Exception as e:
            logging.error("Fatal Error has occured in Data Validation")
            raise Custom_Exception(e, sys)

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            logging.error("Fatal Error has occured in trying to read the data")
            raise Custom_Exception(e, sys)
        

    def validate_no_columns(self, dataframe:pd.DataFrame):
        try:
            number_of_columns = len(self.schema['column'])
            logging.info(f"Required no. of columns {number_of_columns}")
            logging.info(f"No. of columns in dataframe is {len(dataframe.columns)}")

            if number_of_columns != len(dataframe.columns):
                return False
            
            return True

        except Exception as e:
            logging.error("Fatal Error has occured in validating no. of columns")
            raise Custom_Exception(e, sys)
        
    def validate_numerical_columns(self, dataframe: pd.DataFrame):
        try:
            number_of_numerical_schema = len(self.schema['numeric'])
            number_of_numerical_dataframe = len([column for column in dataframe.columns if pd.api.types.is_numeric_dtype(dataframe[column])])
            logging.info(f'Required no. of numerical columns {number_of_numerical_schema}')
            logging.info(f'No. of columns in dataframe {number_of_numerical_dataframe}')

            if number_of_numerical_dataframe != number_of_numerical_schema:
                return False
            
            return True

        except Exception as e:
            logging.error("Fatal Error has occured in validating numerical columns")
            raise Custom_Exception(e, sys)
        
    def detect_drift(self, base_df:pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05):
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_sample_dist = ks_2samp(d1, d2)

                if is_sample_dist.pvalue <= 0.05:
                    is_found =  False
                
                else:
                    is_found = True
                    status = False
                
                report.update({column: {
                    "p-value":float(is_sample_dist.pvalue),
                    "is_similar": is_found 
                }})

            dir_path = os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(dir_path, exist_ok = True)

            write_yaml(self.data_validation_config.drift_report_file_path, report)

        except Exception as e:
            logging.error("Fatal Error has occured in detecting data drift")
            raise Custom_Exception(e, sys)

    def data_validation_initiate(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            logging.info("Loading Train and Test data from artifacts")

            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)
            logging.info("Reading data as pandas dataframe")

            #Validating number of columns
            train_status = self.validate_no_columns(train_data)
            if not train_status:
                error_message_train = f'Train data is incomplete or has too many columns. \n'

            test_status = self.validate_no_columns(test_data)
            if not test_status:
                error_message_test = f'Test data is incomplete or has too many columns. \n'

            #Validating Numerical columns
            train_status_num = self.validate_numerical_columns(train_data)
            if not train_status_num:
                error_message_train_num = f'Train data is incomplete or has too many numerical columns. \n'

            test_status_num = self.validate_numerical_columns(test_data)
            if not test_status_num:
                error_message_test_num = f'Test data is incomplete or has too many numerical columns. \n'

            #Checking Data Drift
            status = self.detect_drift(base_df = train_data, current_df = test_data)
            dir_path = os.path.dirname(self.data_validation_config.Train_valid_data_file_path)
            os.makedirs(dir_path, exist_ok = True)

            train_data.to_csv(
                self.data_validation_config.Train_valid_data_file_path, header = True, index = False
            )

            test_data.to_csv(
                self.data_validation_config.Test_valid_data_file_path, header = True, index = False
            )

            data_validation = artifact_entity.DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_validation_config.Train_valid_data_file_path,
                valid_test_file_path = self.data_validation_config.Test_valid_data_file_path,
                invalid_test_file_path = None,
                invalid_train_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )

            return data_validation
        except Exception as e:
            logging.error("Fatal Error has occured in initiating data validation")
            raise Custom_Exception(e, sys)