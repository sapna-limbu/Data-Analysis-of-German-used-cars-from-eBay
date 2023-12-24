#!/usr/bin/env python
# coding: utf-8

# In[37]:


# importing required libraries
import os
import subprocess
import stat
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


# In[2]:


# Replace 'your_file.csv' with the actual path to your CSV file
file_path = r"C:\Users\RATNADEEP\autos.csv"

# Try reading the CSV file with a different encoding
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    # If reading with utf-8 fails, try other encodings
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        # If 'ISO-8859-1' also fails, try 'utf-16'
        df = pd.read_csv(file_path, encoding='utf-16')

# Continue with the rest of your data processing using the 'df' DataFrame


# In[3]:


df #Raw Data


# In[4]:


df.isnull().sum()


# In[5]:


df.info()


# In[96]:


df.describe().T


# ## Changing str to datetime

# In[7]:


df['dateCreated']=pd.to_datetime(df['dateCreated']) #Changing str to datetime


# In[8]:


df['dateCrawled']=pd.to_datetime(df['dateCrawled']) #Changing str to datetime


# In[10]:


df['lastSeen']=pd.to_datetime(df['lastSeen']) #Changing str to datetime


# In[ ]:





# ## Translating German to English

# In[11]:


# checking the different types of values in the column seller
df.seller.unique()


# In[12]:


#changing values of seller  privat to private and  gewerblich to commercial
df['seller'].replace({"privat" : "private", "gewerblich" : "commercial"}, inplace=True)


# In[13]:


df.seller.unique()


# In[14]:


# checking the different types of values in the column offerType
df.offerType.unique()


# In[15]:


# changing values of offerType Gesuch to Request and Angebot to Offer
df['offerType'].replace({'Angebot':'Offer', 'Gesuch': 'Request'}, inplace = True)


# In[16]:


df.offerType.unique()


# In[18]:


# checking the different types of values in the column gearbox
df.gearbox.unique()


# In[19]:


# changing values of gearbox to manuell to manual and automatik to automatic
df['gearbox'].replace({'manuell': 'manual', 'automatik': 'automatic'}, inplace =True)


# In[20]:


df.gearbox.unique()


# In[22]:


# checking the different types of values in the column fueltype
df.fuelType.unique()


# In[23]:


# changing values of fueltype to benzin to petrol, andere to  other,and elektro to electric
df['fuelType'].replace({'benzin': 'petrol', 'andere': 'other','elektro': 'electric'}, inplace =True)


# In[24]:


df.fuelType.unique()


# In[25]:


# checking the different types of values in the column notRepairedDamage
df.notRepairedDamage.unique()  


# In[26]:


# changing values of notRepairedDamage to  ja to yes and nein  to no
df['notRepairedDamage'].replace({'ja': 'yes', 'nein': 'no' } ,inplace =True)


# In[31]:


df.notRepairedDamage.unique()  


# In[ ]:





# ## Removing Null Values

# In[43]:


# checking the column vehicleType for null values 
df["vehicleType"].isnull().values.sum()


# In[44]:


# changing the vehicleType from NaN to Others
df["vehicleType"].fillna("Other", inplace=True)


# In[45]:


# checking if there are any null values in the column brand
df["brand"].isnull().value_counts()


# In[46]:


# checking if there are any null values in the column seller
df["seller"].isnull().value_counts()


# In[47]:


# checking if there are any null values in the offerType 
df["offerType"].isnull().value_counts()


# In[48]:


# checking if there are any null values in the yearOfRegistration
df["yearOfRegistration"].isnull().value_counts()


# In[49]:


# checking if the gearbox column has null values
df["gearbox"].isnull().value_counts()


# In[50]:


# setting the NaN gearbox types to Unspecified
df["gearbox"].fillna("Unspecified", inplace=True)


# In[51]:


# checking if the fuelType has null values
df["fuelType"].isnull().value_counts()


# In[52]:


# setting the NaN fuelType types to other
df["fuelType"].fillna("other",inplace=True)


# In[53]:


# deleting the column noOfPictures since all of them are Zero
del df["nrOfPictures"]


# In[54]:


# checking for null values in powerPS column
df["powerPS"].isnull().value_counts()


# In[55]:


# checking for unique values in notRepairedDamage
df["notRepairedDamage"].isnull().value_counts()


# In[56]:


# setting nan in notRepairedDamage to other
df["notRepairedDamage"].fillna("other",inplace=True)


# In[57]:


# checking for unique values in model column
df["model"].isnull().value_counts()


# In[58]:


# setting nan in model column to Other
df["model"].fillna("Other",inplace=True)


# In[99]:


# checking for null values in abtest column
df["abtest"].isnull().value_counts()


# In[112]:


df['monthOfRegistration'].replace(0,1,inplace=True) ## Replacing 0 with 1 since 0 doesn't refer to any month.


# In[113]:


df['monthOfRegistration'].replace({1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'},inplace=True)


# In[101]:


# checking if postal code values are null
df["postalCode"].isnull().value_counts()


# In[63]:


df.isnull().sum()


# ## Removing underscores

# In[64]:


def substitution(x):
    return re.sub(r'[_]','',x)


# In[65]:


df['name']=df['name'].apply(substitution)    #Removing '_' in name column.


# In[66]:


df['name'].unique()


# In[67]:


df['brand']=df['brand'].apply(substitution)  #Removing '_' in name column.


# In[68]:


df['brand'].unique()


# In[69]:


def sub_model(x):
    return re.sub(r'[_]+?','',x)


# In[73]:


df['model']=df['model'].apply(sub_model) ## Removing '_' from model column.


# ## Removing Duplicates

# In[71]:


df[df.duplicated()]


# In[74]:


df.duplicated().sum()


# In[75]:


df.drop_duplicates(inplace=True)


# In[76]:


df.duplicated().sum()


# ## Changing the column order

# In[77]:


column_order=['name','seller','model','brand','offerType','price','yearOfRegistration','monthOfRegistration','vehicleType','gearbox','fuelType','kilometer','notRepairedDamage','abtest','powerPS','postalCode','dateCrawled','dateCreated','lastSeen']


# In[78]:


df=df[column_order]


# In[79]:


df.head()


# ## Saving the dataframe in a pickle file

# In[117]:


import pickle as pkl


# In[118]:


with open('german_df.pkl','wb') as f:
    pkl.dump(df,f)


# In[119]:


with open("german_df.pkl","rb") as f:
    ebay_cars = pkl.load(f)


# In[120]:


df=ebay_cars.copy()


# In[121]:


df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




