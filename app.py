import os
import sys
import certifi
import pandas as pd
from dotenv import load_dotenv
import pymongo

from networksecurity.logging_utils.logger import logging
from networksecurity.exception.exception import Custom_Exception
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object_from_pkl
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constants.training_pipeline import DATA_INGESTION_DB_NAME, DATA_INGESTION_COLLECTION_NAME

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from uvicorn import run as app_run

templates = Jinja2Templates(directory = "./templates")

ca = certifi.where()

load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL_KEY")

client = pymongo.MongoClient(mongo_db_url)
database = client[DATA_INGESTION_DB_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/', tags = ['authentication'])
async def index():
    return RedirectResponse(url = '/docs')

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return Response("Training is successful")

    except Exception as e:
        raise Custom_Exception(e, sys)
    
@app.post('/predict')
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file).drop("Unnamed: 0", axis = 1, errors = 'ignore')

        preprocessor = load_object_from_pkl("final_model/preprocessor.pkl")
        model = load_object_from_pkl("final_model/model.pkl")

        network_model = NetworkModel(preprocessor = preprocessor,
                                     model = model)

        y_pred = network_model.predict(df)

        df['predicted_column'] = y_pred

        table_html = df.to_html(classes = 'table table-striped')

        return templates.TemplateResponse('table.html', {'request': request, 'table': table_html})

    except Exception as e:
        raise Custom_Exception(e, sys)
    
if __name__ == "__main__":
    app_run(app, host = 'localhost', port = 8000)