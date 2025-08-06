### End-to-End Machine Learning Project on Phising Dataset
A End-to-End Machine learning project on the Phising dataset that aims to classify whether a specific instance is considered a phising text or not. This project aims to show proficiency in ML-Operations, industry standard coding structure, and integration with different 3rd party software (MLFlow, Dagshub, and Azure).

#### Key Features
- Uses FastAPI to interact with the Model Training pipeline, and Batch Prediction
- Integrates Azure Blob storage and Azure Container Registry
- Uses Classification models including hyperparameter tuning
- Integrates a simple ETL pipeline through push_data.py, converting local csv file to MongoDB Atlas
- Complete Data ingestion, validation, transformation, and Model Training

***Azure Implementation is partially incomplete due to lack of resources to fund the Azure Virtual Machine runtime*** 

#### Project Structure
##### Push Data
- push_data.py
    - Primarly uses the libraries pymongo and pandas
    - Converts csv -> pandas dataframe -> JSON -> MongoDB Atlas collection

##### Data Ingestion
- networksecurity/components/data_ingestion.py
    - Primarly uses the libraries scikit-learn, pymongo, and pandas
    - Reads data from the MongoDB Atlas collection
    - Saves read data into feature_store artifact (raw data)
    - Utilizes scikit-learn's train_test_split to split data to train and test, and saved as artifacts

##### Data Validation
- networksecurity/components/data_validation.py
    - Primarly uses the libraries pandas and yml
    - Validates the splitted test and train datasets structure, number of columns, and column datatype from dataschema/schema.yml
    - Saves validated/invalid datasets to their respective artifacts folder as numpy arrays

##### Data Transformation
- networksecurity/components/data_transformation.py
    - Primarly uses the libraries pandas, scikit-learn, and numpy
    - Creates a preprocessor object (a K-Nearest Neighbor Imputer) to standardize the input data and is saved as a preprocessor.pkl file
    - Splits both the train and test datasets into their respective input and output (X and Y)
    - Imputes the train and test input features
    - Saves to their respective artifacts folder

##### Model Training
- networksecurity/components/model_trainer.py
    - Primarly uses the libraries numpy, and scikit-learn
    - Uses classification models namely Binary Logistic Regression, K-Nearest Neighbor, Naive Bayes, XGBoost, Gradient Boost, Adaboost, and Random Forest
    - Hyperparameter Tuning occurs with specified parameters (found at the source code) using GridSearch Cross Validation