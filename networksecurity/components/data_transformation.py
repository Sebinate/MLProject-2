from networksecurity.exception.exception import Custom_Exception
from networksecurity.logging_utils.logger import logging
from networksecurity.entity import config_entity, artifact_entity
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORM_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_object_as_pkl, save_to_np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np
import os
import sys

class DataTransformation():
    def __init__(self,
                 data_validation_artifact: artifact_entity.DataValidationArtifact,
                 config: config_entity.DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.config = config

        except Exception as e:
            raise Custom_Exception(e, sys)
        
    @staticmethod
    def read_data(file_path):
        try:
            logging.info("Reading Data")
            return pd.read_csv(file_path)

        except Exception as e:
            logging.error("Fatal Error has occured in reading file")
            raise Custom_Exception(e, sys)
        
    def get_data_transformer(self) -> Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORM_IMPUTER_PARAMS)
            logging.info(f"Initialized KNN Imputer with parameters {DATA_TRANSFORM_IMPUTER_PARAMS}")
            
            processor = Pipeline(
                [("KNNImputer", imputer)]
            )
            logging.info("Suuccessfully initialized pipeline")

            return processor
        
        except Exception as e:
            raise Custom_Exception(e, sys)

        
    def data_tranform_initiate(self) -> artifact_entity.DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Successfully Loaded train and test file for data transformation")

            X_train = train_df.drop(TARGET_COLUMN, axis = 1)
            Y_train = train_df[TARGET_COLUMN]
            Y_train = Y_train.replace(-1, 0)

            X_test = test_df.drop(TARGET_COLUMN, axis = 1)
            Y_test = test_df[TARGET_COLUMN]
            Y_test = Y_test.replace(-1, 0)
            logging.info("Successfully created inputs and outputs and changed -1 to 0")

            preprocessor_obj = self.get_data_transformer()

            transformed_X_train = preprocessor_obj.fit_transform(X_train)
            transformed_X_test = preprocessor_obj.transform(X_test)
            logging.info("Successfully Transformed X_train and X_test data")

            train_arr = np.c_[transformed_X_train, np.array(Y_train)]
            test_arr = np.c_[transformed_X_test, np.array(Y_test)]
            logging.info('Successfully concatinated augmented input and output arrays')

            save_to_np(self.config.data_transform_train_file_path, train_arr)
            save_to_np(self.config.data_transform_test_file_path, test_arr)
            logging.info("Successfully saved np arrays")

            save_object_as_pkl(self.config.data_transform_object_file_path, preprocessor_obj)
            logging.info("Successfully saved preprocessor as pkl file")

            data_transformed_artifacts = artifact_entity.DataTransformationArtifact(
                transformed_train_file_path = self.config.data_transform_train_file_path,
                transformed_test_file_path = self.config.data_transform_test_file_path,
                preprocessor_obj_file_path = self.config.data_transform_object_file_path
            )

            return data_transformed_artifacts
        except Exception as e:
            logging.error("Fatal Error has occured in intiating data transformation")
            raise Custom_Exception(e, sys)