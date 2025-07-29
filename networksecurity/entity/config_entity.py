from datetime import datetime
import os
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
import sys
from networksecurity.constants import training_pipeline

print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConig():
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%M-%d-%Y-%H-%M-%S")
        self.timestamp = timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)

class DataIngestionConfig():
    def __init__(self, training_pipieline_config):
        pass