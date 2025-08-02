from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
from networksecurity.entity import config_entity, artifact_entity
from networksecurity.utils.main_utils.utils import save_object_as_pkl, load_from_np, load_object_from_pkl
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel, evaluate_model

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

import os 
import sys
import pandas as pd
import numpy as np

import mlflow
import dagshub
dagshub.init(repo_owner='Sebinate', repo_name='MLProject-2', mlflow=True)

class ModelTraining:
    def __init__(self,
                 data_transform_artifact: artifact_entity.DataTransformationArtifact,
                 config: config_entity.ModelTrainingConfig):
        try:
            self.data_transform_artifact = data_transform_artifact
            self.config = config

        except Exception as e:
            raise Custom_Exception(e, sys)
        
    def track_mlflow(self, best_model, classificationmetric):
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            accuracy = classificationmetric.accuracy
            recall = classificationmetric.recall
            precession = classificationmetric.precession

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("precession", precession)
            mlflow.sklearn.log_model(best_model, 'model')

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Logistic Regression": LogisticRegression(),
            "Naive Bayes": GaussianNB(),
            "Ada Boost": AdaBoostClassifier(),
            "Gradient Boost": GradientBoostingClassifier(),
            "Random Forest": RandomForestClassifier(),
            "K Nearest Neighbors": KNeighborsClassifier(),
            "XG Boost": XGBClassifier()
        }

        params = {
            "Logistic Regression": {},

            "Naive Bayes": {},

            "Ada Boost": {"n_estimators": [50, 100, 150, 200, 400],
                          "learning_rate": [5, 1, 0.1, 0.01, 0.001]},
                          
            "Gradient Boost": {"n_estimators": [50, 100, 200, 400],
                               "learning_rate": [1, 0.1, 0.001],
                               "max_depth": [1, 3, 5, 10]},

            "Random Forest": {"n_estimators": [50, 100, 150, 200, 400],
                               "max_leaf_nodes": [None, 1, 4, 8, 10]},

            "K Nearest Neighbors": {"n_neighbors": [2, 5, 7, 10]},

            "XG Boost": {}
        }

        logging.info("Initialized models and parameters")
        logging.info("Initializing model evaluation and hyper parameter tuning")
        model_report:dict = evaluate_model(X_train, y_train, X_test, y_test, models, params)

        best_model_name = max(model_report, key = lambda x:model_report[x][1])
        best_score = model_report[best_model_name][1]
        best_model = models[best_model_name]

        logging.info(f"Re-predicting on train split on {best_model_name} with r2 test score of {best_score}")
        best_model.set_params(**model_report[best_model_name][2])
        best_model.fit(X_train, y_train)

        y_train_pred = best_model.predict(X_train)

        logging.info("Calling Evaluation report")
        classification_train_metric = get_classification_score(y_train, y_train_pred)

        logging.info("Re-predicitng on test split")
        y_test_pred = best_model.predict(X_test)

        logging.info("Calling Evaluation report")
        classification_test_metric = get_classification_score(y_test, y_test_pred)

        self.track_mlflow(best_model, classification_test_metric)

        logging.info("Loading preprocessor file")
        file = load_object_from_pkl(self.data_transform_artifact.preprocessor_obj_file_path)
        directory = os.path.dirname(self.config.model_train_saved)
        os.makedirs(directory, exist_ok = True)

        Network_Model = NetworkModel(preprocessor = file, model = best_model)

        logging.info("Saving model to pickle file")
        save_object_as_pkl(self.config.model_train_saved, best_model)

        logging.info("Loading model train artifact")
        model_trainer_artifact = artifact_entity.ModelTrainingArtifact(model_saved_file_path = self.config.model_train_saved,
                                                                       train_metric_artifact = classification_train_metric,
                                                                       test_metric_artifact = classification_test_metric)

        return model_trainer_artifact


    def model_train_initiate(self):
        try:
            train_df = load_from_np(self.data_transform_artifact.transformed_train_file_path)
            test_df = load_from_np(self.data_transform_artifact.transformed_test_file_path)
            logging.info("Successfully loaded transformed Train and Test data sets")

            X_train, y_train, X_test, y_test = (
                train_df[:, :-1],
                train_df[:, -1],
                test_df[:, :-1],
                test_df[:, -1]
            )
            logging.info("Successfully split train and test data sets to input and target")

            model = self.train_model(X_train, y_train, X_test, y_test)

            return model
        except Exception as e:
            logging.error("Fatal Error has occured in initiating model training")
            raise Custom_Exception(e, sys)