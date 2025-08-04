from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTraining

from networksecurity.entity import config_entity, artifact_entity

from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception

from networksecurity.cloud.az_syncher import AzureSync

import os
import sys

class TrainingPipeline():
    def __init__(self):
        self.training_pipeline_config = config_entity.TrainingPipelineConfig()
        self.az_synch = AzureSync()

    def start_data_ingestion(self):
        try:
            logging.info("Initiated Data Ingestion")
            data_ingestion_config = config_entity.DataIngestionConfig(self.training_pipeline_config)
            logging.info("Initiated Data Ingestion Config")

            data_ingestion = DataIngestion(data_ingestion_config)
            logging.info("Initiated Data Ingestion Class")
            data_ingestion_artifact = data_ingestion.data_ingestion_initiate()
            logging.info("Initiated Data Ingestion Artifact")

            return data_ingestion_artifact

        except Exception as e:
            logging.error("Fatal error has occured in data ingestion")
            raise Custom_Exception(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info("Initiated Data Validation")
            data_validation_config = config_entity.DataValidationConfig(self.training_pipeline_config)
            logging.info("Initiated Data Validation Config")

            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact, 
                                             data_validation_config = data_validation_config)
            logging.info("Initiated Data Validation Class")

            data_validation_artifact = data_validation.data_validation_initiate()
            logging.info("Initiated Data Validation Artifact")

            return data_validation_artifact

        except Exception as e:
            logging.error("Fatal Error has occured in data validation")
            raise Custom_Exception(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: artifact_entity.DataValidationArtifact):
        try:
            logging.info("Initiated Data Transformation")
            data_transformation_config = config_entity.DataTransformationConfig(self.training_pipeline_config)
            logging.info("Initiated Data Transformation Config")

            data_transformation = DataTransformation(data_validation_artifact = data_validation_artifact,
                                                     config = data_transformation_config)
            logging.info("Initiated Data Transformation Class")

            data_transformation_artifact = data_transformation.data_tranform_initiate()
            logging.info("Initiated Data Transformation")

            return data_transformation_artifact
    
        except Exception as e:
            logging.error("Fatal Error has occured in data transformation")
            raise Custom_Exception(e, sys)
        
    def start_model_training(self, data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            logging.info("Initiated Model Training")
            model_training_config = config_entity.ModelTrainingConfig(self.training_pipeline_config)
            logging.info("Initiated Model Training Config")

            model_training = ModelTraining(data_transform_artifact = data_transformation_artifact,
                                           config = model_training_config)
            logging.info("Initiated Model Training Class")
            model_training_artifact = model_training.model_train_initiate()
            logging.info("Initiated Model Training Artifact")

            return model_training_artifact

        except Exception as e:
            logging.error("Fatal Error has occured in model training")
    
    def sync_artifact_dir_to_az(self):
        try:
            self.az_synch.synch_folder_to_az(container = "artifacts", directory = self.training_pipeline_config.artifact_dir, blob_prefix = self.training_pipeline_config.timestamp)

        except Exception as e:
            raise Custom_Exception(e, sys)
        
    def sync_final_model_dir_to_az(self):
        try:
            self.az_synch.synch_folder_to_az(container = "model", directory = self.training_pipeline_config.model_dir, blob_prefix = self.training_pipeline_config.timestamp)

        except Exception as e:
            raise Custom_Exception(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_training_artifact = self.start_model_training(data_transformation_artifact)

            self.sync_artifact_dir_to_az()
            self.sync_final_model_dir_to_az()

            return model_training_artifact

        except Exception as e:
            logging.error("Fatal Error has occured in running the pipeline")
            raise Custom_Exception(e, sys)