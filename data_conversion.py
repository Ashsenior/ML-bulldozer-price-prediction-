import pandas as pd 
import numpy as np 

# First read data and parse dates into pandas DateTime64 
data = pd.read_csv('../data/Test.csv',low_memory=False,parse_dates=['saledate'])

# Splitting saledate into Day, Month, Year columns
data['saleYear'] = data.saledate.dt.year 
data['saleMonth'] = data.saledate.dt.month 
data['saleDay'] = data.saledate.dt.day 
data['saleDayOfWeek'] = data.saledate.dt.dayofweek 
data['saleDayOfYear'] = data.saledate.dt.dayofyear 
data.drop('saledate',axis=1,inplace=True)

# Converting string data into pandas categories
for label,content in data.items():
    if pd.api.types.is_string_dtype(content):
        data[label] = content.astype('category').cat.as_ordered()

# Filling the numerical and categorical missing values into numeric forms
for label,content in data.items():
    if pd.api.types.is_numeric_dtype(content):
        if pd.isnull(content).sum():
            data[label+'is_missing'] = True
            data[label] = data[label].fillna(content.median())
        elif label == 'auctioneerID':
            data['auctioneerIDis_missing'] = False
    elif pd.api.types.is_categorical_dtype(content):
        data[label+'is_missing'] = pd.isnull(content)
        data[label] = pd.Categorical(content).codes + 1

# Writing the new data into a csv file
data.to_csv('../data/test_converted.csv',index=False)
