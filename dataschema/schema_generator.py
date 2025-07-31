import yaml
import pandas as pd
import numpy as np

data = pd.read_csv(r"../Network_Data/phisingData.csv")

columns = list(data.columns)

columns = list(data.columns)
to_yml_dictionary = {'column': [{col: str(dtypes)} for col, dtypes in data.dtypes.items()], 
                     'numeric': [columns[i] for i in range(len(columns)) if pd.api.types.is_numeric_dtype(data[columns[i]])]}

with open("schema.yml", 'w') as file:
    yaml.dump(to_yml_dictionary, file, default_flow_style = False)