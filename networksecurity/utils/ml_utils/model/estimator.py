from networksecurity.exception.exception import Custom_Exception
from networksecurity.logging_utils.logger import logging
from networksecurity.entity import artifact_entity
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import numpy as np
import sys

def get_classification_score(y_true: np.array, y_pred: np.array):
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_accuracy_score = accuracy_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)

        classification_metric = artifact_entity.ClassificationMetricsArtifact(
            f1_score = model_f1_score,
            accuracy = model_accuracy_score,
            recall = model_recall_score,
            precession = model_precision_score
        )
        logging.info("Successfully generated classification metric artifact")
        return classification_metric
    
    except Exception as e:
        raise Custom_Exception(e, sys)