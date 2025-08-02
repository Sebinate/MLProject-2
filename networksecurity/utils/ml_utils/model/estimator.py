from networksecurity.exception.exception import Custom_Exception
from networksecurity.entity.artifact_entity import ClassificationMetricsArtifact, ModelTrainingArtifact
from networksecurity.constants.training_pipeline import SAVED_MODELS_DIR, MODEL_TRAINED_FILE_NAME
from networksecurity.logging_utils.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import numpy as np
import warnings

import os
import sys

warnings.filterwarnings('ignore')

class NetworkModel():
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model

        except Exception as e:
            logging.error("Fatal Error has occured in loading preprocessor and model")
            raise Custom_Exception(e, sys)
    
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)

            return y_pred

        except Exception as e:
            logging.error("Fatal Error has occured in predicting values")
            raise Custom_Exception(e, sys)
        
def evaluate_model(X_train:np.array, 
                   y_train:np.array, 
                   X_test:np.array, 
                   y_test:np.array, 
                   models: dict, 
                   params: dict):
    try:
        results = {}
        for name, model in list(models.items()):
            gs = GridSearchCV(estimator = model, param_grid = params[name], cv = 3, verbose = 1)
            gs.fit(X_train, y_train)
            logging.info("Successfully intialized and fitted X and Y to the grid search cv")

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            logging.info(f"Successfully intialized {name} with the best params {gs.best_params_}")

            #Predicting for train data
            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_r2_score = r2_score(y_train, y_train_pred)
            test_r2_score = r2_score(y_test, y_test_pred)

            results[name] = [train_r2_score, test_r2_score, gs.best_params_]

        return results

    except Exception as e:
        logging.error("Fatal Error has occured in evaluating models")
        raise Custom_Exception(e, sys)