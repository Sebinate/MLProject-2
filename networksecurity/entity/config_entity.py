from datetime import datetime
import os
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
import sys
from networksecurity.constants import training_pipeline

print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig():
    def __init__(self, timestamp = datetime.now()):
        self.timestamp = timestamp.strftime("%M-%d-%Y-%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)

class DataIngestionConfig():
    def __init__(self, training_pipieline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_dir: str = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_FEATURE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_dir: str = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.test_dir: str = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.test_size = training_pipeline.DATA_INGESTION_TEST_SIZE
        self.random_state = training_pipeline.DATA_INGESTION_RANDOM_STATE
        self.db_name = training_pipeline.DATA_INGESTION_DB_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME