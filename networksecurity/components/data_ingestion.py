import os
import sys

from networksecurity.entity import config_entity, artifact_entity
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL_KEY')

class DataIngestion():
    def __init__(self, config: config_entity.DataIngestionConfig):
        try:
            self.config = config
            logging.info("Data Ingestion Config Successfull")

        except Exception as e:
            logging.error("Fatal Error has occured in Data Ingestion Config initialization")
            raise Custom_Exception(e, sys)
        
    def export_collection(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            logging.info(f"Successfully Connected to MongoDB client")

            database = self.mongo_client[self.config.db_name]
            collection = database[self.config.collection_name]
            logging.info("Successfully initialized collection")

            df = pd.DataFrame(list(collection.find()))
            logging.info("Successfully Converted to CSV")

            if "_id" in df.columns.to_list():
                df.drop("_id", inplace = True, axis = 1)

            df.replace({"na":np.nan}, inplace = True)

            return df
        
        except Exception as e:
            logging.error("Fatal Error has occured in converting MongoDB to Dataframe")
            raise Custom_Exception(e, sys)
        
    def export_to_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_dir = self.config.feature_store_dir
            dir_path = os.path.dirname(feature_store_dir)
            logging.info("Initializing feature store directory")

            os.makedirs(dir_path, exist_ok = True)
            logging.info("Feature store directory successfully created")

            dataframe.to_csv(feature_store_dir, index = False, header = True)
            logging.info("Dataframe exported to CSV in feature_store successfully done")

            return dataframe

        except Exception as e:
            logging.error('Fatal Error has occured in exporting raw data to feature_store directory')
            raise Custom_Exception(e, sys)
        
    def export_train_test_split(self, dataframe: pd.DataFrame):
        try:
            train_split, test_split = train_test_split(
                dataframe,
                test_size = self.config.test_size,
                random_state = self.config.random_state
                )
            logging.info("Train-Test split successfully created")

            dir_path = os.path.dirname(self.config.training_dir)

            os.makedirs(dir_path, exist_ok = True)
            logging.info("Directory for Train-Test split successfully made")

            train_split.to_csv(
                self.config.training_dir, index = False, header = True
            )
            logging.info(f"Train dataset has successfully been exported at {self.config.random_state} random state and {1 - self.config.test_size} train sample size")

            test_split.to_csv(
                self.config.test_dir, index = False, header = True
            )
            logging.info(f"Test dataset has successfully been exported at {self.config.random_state} random state and {self.config.test_size} test sample size")

        except Exception as e:
            logging.error("Fatal Error has occured in exporting data into train and test split")
            raise Custom_Exception(e, sys)
   
    def data_ingestion_initiate(self):
        try:
            logging.info("Exporting Collection to CSV")
            dataframe = self.export_collection()

            logging.info("Exporting to Raw Data")
            dataframe = self.export_to_feature_store(dataframe)

            logging.info("Performing Train-Test split")
            self.export_train_test_split(dataframe)
            
            logging.info("Storing Artifact directories")
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                train_file_path = self.config.training_dir,
                test_file_path = self.config.test_dir
            )

            return data_ingestion_artifact

        except Exception as e:
            logging.error("Fatal Error has occured in Initializing Data Ingestion")
            raise Custom_Exception(e, sys)