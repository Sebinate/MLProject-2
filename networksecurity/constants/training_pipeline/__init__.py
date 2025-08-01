import os
import sys
import pandas as pd
import numpy as np

TARGET_COLUMN = 'Result'
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

TEST_FILE_NAME = 'test.csv'
TRAIN_FILE_NAME = 'train.csv'

SCHEMA_FILE_PATH = os.path.join("dataschema", "schema.yml")

DATA_INGESTION_DB_NAME = "SEBAI"
DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TEST_SIZE = 0.2
DATA_INGESTION_RANDOM_STATE = 42

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yml"

DATA_TRANSFORM_DIR = "data_transform"
DATA_TRANSFORMED_DIR = "transformed"
DATA_TRAIN_TRANSFORM_FILE_NAME = "train.npy"
DATA_TEST_TRANSFORM_FILE_NAME = "test.npy"
DATA_PREPROCESSOR_FILE_NAME = "preprocessor.pkl"

#For KNN imputer
DATA_TRANSFORM_IMPUTER_PARAMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}