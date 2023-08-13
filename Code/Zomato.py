#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:18:10 2023

@author: sindhu19s

"""
# import packages
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
pd.set_option('display.max_columns', None)
data= pd.read_csv("/Users/apple/desktop/Datasets/Datasets/Zomato.csv")
print(data.info())

"""
#   Column                 Non-Null Count  Dtype  
---  ------                 --------------  -----  
 0   Unnamed: 0.1           7105 non-null   int64  
 1   Unnamed: 0             7105 non-null   int64  
 2   restaurant name        7105 non-null   object 
 3   restaurant type        7105 non-null   object 
 4   rate (out of 5)        7037 non-null   float64
 5   num of ratings         7105 non-null   int64  
 6   avg cost (two people)  7048 non-null   float64
 7   online_order           7105 non-null   object 
 8   table booking          7105 non-null   object 
 9   cuisines type          7105 non-null   object 
 10  area                   7105 non-null   object 
 11  local address          7105 non-null   object 

"""

# data.to_csv('/Users/apple/desktop/Datasets/Datasets/rat.csv', columns=['rate (out of 5)'])

# data.to_csv('/Users/apple/desktop/Datasets/Datasets/avg.csv', columns=['avg cost (two people)'])

# Drop the below to columns
data.drop('Unnamed: 0',axis=1,inplace=True)
data.drop('Unnamed: 0.1',axis=1,inplace=True)

# Print unique number of values for each column
print((data.nunique()))
"""
restaurant name          7105 (has funky values)
restaurant type            81 
rate (out of 5)            31 (has nan)
num of ratings            935
avg cost (two people)      65 (has nan)
online_order                2 ['No' 'Yes']
table booking               2 ['No' 'Yes']
cuisines type            2175 (no funky values)
area                       30 (no funky values)
local address              90 (no funky values)
"""
# Print total number of rows

print(data.shape) # (7105, 10)

# Get unique values for column online_order , table booking
print(sorted(pd.unique(data['area'])))
print(sorted(pd.unique(data['table booking']))) # ['No' 'Yes']
print(sorted(pd.unique(data['rate (out of 5)']))) 
print(sorted(pd.unique(data['avg cost (two people)']))) 
print(sorted(pd.unique(data['restaurant type']))) 


#list count of nan values 
count_nan_in_df = data.isnull().sum()
print (count_nan_in_df)

"""
restaurant name           0
restaurant type           0
rate (out of 5)          68
num of ratings            0
avg cost (two people)    57
online_order              0
table booking             0
cuisines type             0
area                      0
local address             0 = 125
"""

# Check for NaN under an entire DataFrame:
print(data.isnull().values.any()) # RETURNED TRUE

# Count the NaN under an entire DataFrame:
print(data.isnull().sum().sum()) # 125

"""
# Drop all the rows that have all the columns as NAN
data1=data.dropna(how='any')  
data1.dropna(how='any', inplace=True) # (6984, 10)

# Print unique number of values for each column
print((data1.nunique()))

restaurant name          6984
restaurant type            81
rate (out of 5)            31
num of ratings            932
avg cost (two people)      64
online_order                2
table booking               2
cuisines type            2155
area                       30
local address              90 """

# Describe mean and basic details
print(data.describe())

"""
         rate (out of 5)   num of ratings        avg cost (two people)
count      7037.000000     7105.000000            7048.000000
mean          3.514253      188.921042             540.286464
std           0.463249      592.171049             462.902305
min           1.800000        1.000000              40.000000
25%           3.200000       16.000000             300.000000
50%           3.500000       40.000000             400.000000
75%           3.800000      128.000000             600.000000
max           4.900000    16345.000000            6000.000000
"""
# While we can always drop rows which have nan values , we will fill it with mean values . 

data['rate (out of 5)'].fillna(3.51,inplace=True)
data['avg cost (two people)'].fillna(540.286,inplace=True)

# Calculate average price for 2 people by area 
print(data.groupby(['area'],as_index=False)['avg cost (two people)'].mean())

# Print Graph
x=(sorted(pd.unique(data['area'])))
y=data.groupby(['area'],as_index=False)['avg cost (two people)'].mean()
print(y) # this is 2 columns , so select 1 column) 
plt.bar(x,y['avg cost (two people)'])
plt.xlabel('Area')
plt.ylabel('Average price for 2 people')
plt.xticks(x, rotation='vertical' , size=8)
plt.grid()
plt.show(block=True)

# Change boolean values to integer
print(sorted(pd.unique(data['online_order'])))
print(data[['restaurant name']].head(10))
data['online_order'] =data['online_order'].map({'Yes': 1, 'No': 0})
data['table booking'] = data['table booking'].map({'Yes': 1, 'No': 0})

# Calculate Average Number of times online_orders are booked by area

y1=data.groupby(['area'],as_index=False)[['online_order' ,'table booking']].sum()
print(y1)

# Print Graph
plt.plot(x,y1['table booking'],marker='D')
plt.xlabel('Area')
plt.ylabel('Sum Of Table Order in Area')
plt.xticks(x, rotation='vertical' , size=8)
plt.grid()
plt.show(block=True)

# Print Graph
# https://queirozf.com/entries/add-labels-and-text-to-matplotlib-plots-annotation-examples 

fig, ax1 = plt.subplots()
ax1.bar(x, y1['online_order'])
ax1.set_xlabel('Area')
ax1.set_ylabel('Sum of Orders Online')
plt.xticks(x,rotation='vertical' , size=8 , ha='right')
ax1.grid()
ax2 = ax1.twinx()
ax2.plot(x,y1['table booking'],'r-',marker='.')
for i,j in zip(x,y1['table booking']):
    label=format(j)
    plt.annotate(label,
                 (i,j),
                 ha='center') # Prints labels for each data point
ax2.set_ylabel('Sum of Table Booking', color='r')
fig.show()

print(data[['cuisines type']].head(10))

# Removing Updating the encoded Formats
def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')

data['restaurant name']= data['restaurant name'].apply(remove_accents)
data['cuisines type']= data['cuisines type'].apply(remove_accents)
rest_type = data['restaurant type'].value_counts(ascending=False).head(5).reset_index(name='count')
print(rest_type)

# Plot Pie Chart
plt.pie(rest_type['count'],
        autopct='%.1f%%',
        startangle=90,
        labels=rest_type['restaurant type'] ,
        labeldistance=1.2)
#plt.title('Restaurant Type Distribution')
plt.axis('equal')
plt.show()

# Least 10 areas of restaurants 
data["area"].value_counts(ascending=True).head(10).plot(kind="bar", xlabel="area", ylabel="Count", title="top 10 areas of restaurants")
plt.xticks(rotation=85)
plt.show()

# TOP 10 areas of restaurants 
data["area"].value_counts.head(10).plot(kind="bar", xlabel="area", ylabel="Count", title="top 10 areas of restaurants")
plt.xticks(rotation=85)
plt.show()

# TOP 10 cuisines type of restaurants 
print(data["cuisines type"].value_counts(ascending=False).head(10))
data["cuisines type"].value_counts(ascending=False).head(10).plot(kind="bar", xlabel="cuisines type", ylabel="Count", title="top 10 areas of restaurants")
plt.xticks()
plt.show()

# Average num of ratings by area
p1=data.groupby(['area'],as_index=False)[['num of ratings']].mean()
print(p1)
# Plot a Graph
plt.bar(x,p1['num of ratings'])
plt.xlabel('Area')
plt.ylabel('Average num of ratings')
plt.xticks(x, rotation='vertical' , size=8)
plt.grid()
plt.show(block=True)


