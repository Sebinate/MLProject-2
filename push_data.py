import os
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
import sys
import json
import certifi
from dotenv import load_dotenv

load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL_KEY")
print(mongo_db_url)

#Creates a secure and valid request line
ca = certifi.where()

class NetworkExtract():
    def __init__(self, db, collection):
        try:
            self.db = db
            self.collection = collection

        except Exception as e:
            raise Custom_Exception(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path, index_col = False)
            logging.info("Loading Data")

            # Converting the pandas data frame into a json
            
            records = data.to_dict(orient = 'records')

            return records

        except Exception as e:
            raise Custom_Exception(e, sys)
        
    def insert_to_mongo(self, records):
        try:
            logging.info("Initializing Records")
            self.records = records

            logging.info("Initializing MongoDB client")
            self.client = pymongo.MongoClient(mongo_db_url)
            
            logging.info("Accessing collection")
            self.db= self.client[self.db]
            self.collection = self.db[self.collection]

            logging.info("Inserting records into database")
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'
    db = "SEBAI"
    collection = "NetworkData"
    networkobj = NetworkExtract(db, collection)

    records = networkobj.csv_to_json(FILE_PATH)
    print(records)
    no_rec = networkobj.insert_to_mongo(records)
    print(no_rec)