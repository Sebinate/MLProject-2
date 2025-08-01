from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
from networksecurity.entity import config_entity, artifact_entity
import sys
import os

if __name__ == "__main__":
    try:
        train_pipelien_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(train_pipelien_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.data_ingestion_initiate()
        print(data_ingestion_artifacts)

        data_validation_config = config_entity.DataValidationConfig(train_pipelien_config)
        data_validation = DataValidation(data_ingestion_artifacts, data_validation_config)

        data_validation_artifacts = data_validation.data_validation_initiate()
        print(data_validation_artifacts)

        data_transform_config = config_entity.DataTransformationConfig(train_pipelien_config)
        data_transform = DataTransformation(data_validation_artifacts, data_transform_config)

        data_transform_artifacts = data_transform.data_tranform_initiate()
        print(data_transform_artifacts)
    except Exception as e:
        raise Custom_Exception(e, sys)