import yaml
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
import os
import sys
import pickle
import numpy as np

def read_schema(file_path):
    try:
        logging.info("Reading schema.yml file")
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
        
    except Exception as e:
        logging.error("Fatal Error has occured in reading schema file")
        raise Custom_Exception(e, sys)
    
def write_yaml(file_path, data):
    try:
        logging.info("Writing yaml file")
        with open(file_path, 'w') as file:
            return yaml.dump(data, file)
        
    except Exception as e:
        logging.error("Fatal Error has occured in writing yaml file")
        raise Custom_Exception(e, sys)
    
def save_to_np(file_path, array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, "wb") as file:
            np.save(file, array)

    except Exception as e:
        logging.error("Fatal Error has occured in saving file to numpy array")
        raise Custom_Exception(e, sys)
    
def save_object_as_pkl(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)

    except Exception as e:
        logging.error("Fatal Error has occured in saving file as a pkl")
        raise Custom_Exception(e, sys)