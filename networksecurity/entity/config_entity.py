from datetime import datetime
import os
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
import sys
from networksecurity.constants import training_pipeline

print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig():
    def __init__(self, timestamp = datetime.now()):
        self.timestamp = timestamp.strftime("%m-%d-%Y-%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
        self.model_dir = os.path.join('final_model')

class DataIngestionConfig():
    def __init__(self, training_pipieline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_dir: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_dir: str = os.path.join(
             self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.test_dir: str = os.path.join(
             self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.test_size = training_pipeline.DATA_INGESTION_TEST_SIZE
        self.random_state = training_pipeline.DATA_INGESTION_RANDOM_STATE
        self.db_name = training_pipeline.DATA_INGESTION_DB_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig():
    def __init__(self, training_pipieline_config: TrainingPipelineConfig):
        self.validation_dir = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        
        self.valid_data_dir = os.path.join(
            self.validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        self.invalid_data_dir = os.path.join(
            self.validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        self.Train_valid_data_file_path = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.Train_invalid_data_file_path = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.Test_valid_data_file_path = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        self.Test_invalid_data_file_path = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        self.drift_report_dir = os.path.join(
            training_pipieline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR
        )

        self.drift_report_file_path = os.path.join(
            self.drift_report_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

        self.schema_file_path = training_pipeline.SCHEMA_FILE_PATH

class DataTransformationConfig():
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transform_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORM_DIR
        )

        self.data_transform_train_file_path = os.path.join(
            self.data_transform_dir,
            training_pipeline.DATA_TRANSFORMED_DIR,
            training_pipeline.DATA_TRAIN_TRANSFORM_FILE_NAME
        )

        self.data_transform_test_file_path = os.path.join(
            self.data_transform_dir,
            training_pipeline.DATA_TRANSFORMED_DIR,
            training_pipeline.DATA_TEST_TRANSFORM_FILE_NAME
        )

        self.data_transform_object_file_path = os.path.join(
            self.data_transform_dir,
            training_pipeline.DATA_PREPROCESSOR_FILE_NAME
        )

class ModelTrainingConfig():
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_train_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAIN_DIR
        )

        self.model_train_saved = os.path.join(
            self.model_train_dir,
            training_pipeline.MODEL_TRAINED_DIR,
            training_pipeline.MODEL_TRAINED_FILE_NAME
        )

        self.model_final_path = os.path.join(
            training_pipeline.FINAL_DIR,
            training_pipeline.MODEL_TRAINED_FILE_NAME
        )

        self.preprocessing_final_path = os.path.join(
            training_pipeline.FINAL_DIR,
            training_pipeline.DATA_PREPROCESSOR_FILE_NAME
        )

        self.model_expected_accuracy = training_pipeline.MODEL_TRAIN_EXPECTED_ACC
        self.model_over_under_threshold = training_pipeline.MODEL_TRAIN_OVERUNDERFITTING_THRESHOLD