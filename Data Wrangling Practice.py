# Data Wrangling Practice 

import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib import pyplot


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
df = pd.read_csv(url, names = headers)
print(df)

# Identify and handle missing values

df.replace("?", np.nan, inplace = True)
missing_data = df.isnull()
''' #I was counting the missing values in each column

for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")   

"normalized-losses": 41 missing data
"num-of-doors": 2 missing data
"bore": 4 missing data
"stroke" : 4 missing data
"horsepower": 2 missing data
"peak-rpm": 2 missing data
"price": 4 missing data

Deal with missing values - 

"normalized-losses": 41 missing data, replace them with mean
"stroke": 4 missing data, replace them with mean
"bore": 4 missing data, replace them with mean
"horsepower": 2 missing data, replace them with mean
"peak-rpm": 2 missing data, replace them with mean
"num-of-doors": 2 missing data, replace them with "four".
"price": 4 missing data, delete the whole row
'''

avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
df["normalized-losses"].replace(np.nan, avg_norm_loss, inplace=True)
avg_bore=df['bore'].astype('float').mean(axis=0)
df["bore"].replace(np.nan, avg_bore, inplace=True)
avg_storke = df['stroke'].astype("float").mean(axis=0)
df['stroke'].replace(np.nan, avg_storke, inplace=True)
avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
df['horsepower'].replace(np.nan, avg_horsepower, inplace=True)
avg_peakrpm=df['peak-rpm'].astype('float').mean(axis=0)
df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True)
df["num-of-doors"].replace(np.nan, "four", inplace=True)
df.dropna(subset=["price"], axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

#Correct data format

#print(df.dtypes) # list the data types for each column¶
#Convert data types to proper format
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")

#Data Standardization - I will assume i am in a country that accepts the fuel consumption with L/100km standard. Formula -> L/100km = 235 / mpg

df['city-L/100km'] = 235/df["city-mpg"]
df["highway-mpg"] = 235/df["highway-mpg"]
df.rename(columns={'"highway-mpg"':'highway-L/100km'}, inplace=True)

#Data Normalization
#Target: normalize those variables so their value ranges from 0 to 1 - Approach: replace the original value by (original value)/(maximum value)

df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df["height"] = df["height"]/df["height"].max()

#Binning - i will categorize horsepower into three types: high, medium, and low horsepower
df["horsepower"]=df["horsepower"].astype(int, copy=True)
bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
group_names = ['Low', 'Medium', 'High']
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True )

#draw historgram of attribute "horsepower" with bins = 3 

plt.pyplot.hist(df["horsepower"], bins = 3)
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")
#pyplot.show()


#Indicator Variable
dummy_variable_1 = pd.get_dummies(df["fuel-type"])
dummy_variable_1.rename(columns={'gas':'fuel-type-gas', 'diesel':'fuel-type-diesel'}, inplace=True)
df = pd.concat([df, dummy_variable_1], axis=1)
df.drop("fuel-type", axis = 1, inplace=True)
dummy_aspiration = pd.get_dummies(df['aspiration'])
dummy_aspiration.rename(columns= {'std':'aspiration-std', 'turbo': 'aspiration-turbo'}, inplace=True)
df = pd.concat([df, dummy_aspiration], axis=1)
df.drop('aspiration', axis=1, inplace=True)

#Save the df to csv file
df.to_csv('Data_Wrangling_Practice.csv')

if __name__ == "__main__":
    print(df.head(10))
    print(df.tail(10))
