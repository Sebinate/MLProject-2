import os
import sys
import pandas as pd
import numpy as np

TARGET_COLUMN = 'Result'
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

DATA_INGESTION_DB_NAME = "SEBAI"
DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TEST_SIZE = 0.2