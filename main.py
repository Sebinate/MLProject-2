from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
from networksecurity.entity import config_entity
import sys
import os

if __name__ == "__main__":
    try:
        train_pipelien_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(train_pipelien_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        print(data_ingestion.data_ingestion_initiate())
    except Exception as e:
        raise Custom_Exception(e, sys)