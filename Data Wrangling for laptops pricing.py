#Data Wrangling for laptops pricing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-Coursera/laptop_pricing_dataset_base.csv"
df = pd.read_csv(url, header=None)
headers = ["Manufacturer", "Category", "Screen", "GPU", "OS", "CPU_core", "Screen_Size_cm", "CPU_frequency", "RAM_GB", "Storage_GB_SSD", "Weight_kg", "Price"]
df.columns = headers
df.replace("?", np.nan, inplace=True)
df[['Screen_Size_cm']] = np.round(df[['Screen_Size_cm']],2)

# Evaluate the dataset for missing data
'''
missing_values = df.isnull()
for column in missing_values.columns.values.tolist():
    print(column)
    print (missing_values[column].value_counts())
    print("")  
'''
#We have four missing data in Screen_Size_cm and five in Weight_kg

#for the weight attribute, i will replace the missing values with mean value since the values in "Weight_kg" attribute are continuous in nature
avg_weight = df['Weight_kg'].astype('float').mean(axis=0)
df['Weight_kg'].replace(np.nan, avg_weight, inplace=True)

#for the secreen size attribute, i will replace the missing values with the most frequent value since the values in "Screen_Size_cm" attribute are categorical in nature,
freq_value = df['Screen_Size_cm'].value_counts().idxmax()
df['Screen_Size_cm'].replace(np.nan, freq_value, inplace=True)

#Fixing the data types, from object to float
df[["Weight_kg","Screen_Size_cm"]] = df[["Weight_kg","Screen_Size_cm"]].astype("float")

#Data Standardization
df['Weight_kg'] = df['Weight_kg']*2.205 #from kg to pounds
df.rename(columns={'Weight_kg' : 'Weight_pounds'}, inplace=True)
df["Screen_Size_cm"] = df["Screen_Size_cm"]/2.54 #from cm to inch
df.rename(columns={'Screen_Size_cm':'Screen_Size_inch'}, inplace=True)

#Data Normalization
df['CPU_frequency'] = df['CPU_frequency']/df['CPU_frequency'].max()

#Binning - i will categorize price into three types: high, medium, and low
bins = np.linspace(min(df['Price']), max(df['Price']), 4)
catg = ['Low', "Medium", "High"]
df['Price-binned'] = pd.cut(df['Price'], bins, labels=catg, include_lowest=True)

#draw bar of attribute "price" with bins = 3 
plt.bar(catg, df["Price-binned"].value_counts())
plt.xlabel("Price")
plt.ylabel('Count')
plt.title('Price bins')
#plt.show()

#Indicator variables
dummy_screen = pd.get_dummies(df['Screen'])
df.rename(columns={'IPS Panel':'Screen-IPS_panel', 'Full HD':'Screen-Full_HD'}, inplace=True)
df = pd.concat([df, dummy_screen], axis=1)
df.drop("Screen", axis = 1, inplace=True)

df.to_csv('Data_Wrangling_for_Laptops_Pricing.csv')

print(df.head(15))