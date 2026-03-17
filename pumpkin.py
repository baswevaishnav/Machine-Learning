import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

#Reading csv file
pumpkins = pd.read_csv('C:/Users/VBaswe/Practice/Machine-Learning/US-pumpkins.csv')

#Filter out rows which don't use price per bushel
pumpkins = pumpkins[pumpkins['Package'].str.contains('bushel',case=True,regex=True)]
print(pumpkins.head())

#Check the sum of null rows in each column
print(pumpkins.isnull().sum())

#Selecting columns that we need
new_columns = ['Package','Month','Variety','City Name','Low Price','High Price','Date']

#Dropping all other columns
pumpkins = pumpkins.drop([c for c in pumpkins if c not in new_columns], axis=1)
#Alternate: pumpkins = pumpkins[new_columns]

#Average price
avg_price = (pumpkins['Low Price']+pumpkins['High Price'])/2

#Get the month from the date column
month = pd.DatetimeIndex(pumpkins['Date']).month

#Day of the Year
day_of_year = pd.to_datetime(pumpkins['Date']).apply(lambda dt: (dt - datetime(dt.year,1,1)).days)

#Create a new dataframe using these columns
pumpkins_df = pd.DataFrame({'Month': month, 'Day of Year': day_of_year, 'Package': pumpkins['Package'], 'Variety':pumpkins['Variety'], 'City':pumpkins['City Name'], 'Low Price': pumpkins['Low Price'], 'High Price':pumpkins['High Price'], 'Average Price': avg_price})

#Convert average price of all row prices with 1 1/9 bushels by dividing it by 1 1/19
pumpkins_df.loc[pumpkins['Package'].str.contains('1 1/9'),'Average Price'] = avg_price/(1+1/9)
#Convert average price of all row prices with 1/2 bushels by dividing it by 1/2
pumpkins_df.loc[pumpkins['Package'].str.contains('1/2'),'Average Price'] = avg_price/(1/2)

#Print last 10 rows
print(pumpkins_df.tail(10))

#print(min(pumpkins_df['Average Price']))

#Get values to plot
price = pumpkins_df['Average Price']
month = pumpkins_df['Month']

#Create scatter plot
plt.scatter(price,month)
plt.show()

#Create bar chart
pumpkins_df.groupby(['Month'])['Average Price'].mean().plot(kind='bar')
plt.ylabel("Pumpkin Price")
plt.show()

#Scatter Plot for Month and Price
plt.scatter('Month','Average Price', data=pumpkins_df)
plt.show()

#Calculate the correlation between Month and Price
print(pumpkins_df['Month'].corr(pumpkins_df['Average Price']))

#Scatter Plot for Day of Year and Price
plt.scatter('Day of Year','Average Price', data=pumpkins_df)
plt.show()

#Calculate the correlation between Day of Year and Price
print(pumpkins_df['Day of Year'].corr(pumpkins_df['Average Price']))

#Define colors for different kinds of pumpkin
colors = ['red','blue','green','yellow']

#Scatter Plot for Day of Year and Price using a set of colors for each kind of pumpkin group
ax=None
for i, var in enumerate(pumpkins_df['Variety'].unique()):
    df = pumpkins_df[pumpkins_df['Variety']==var]
    ax = df.plot.scatter('Day of Year','Average Price', ax=ax,color=colors[i],label=var)
plt.show()

#Bar chart to see which Variety is the most expensive and cheapest
pumpkins_df.groupby('Variety')['Average Price'].mean().plot(kind='bar')
plt.show()

#Cheapest
pie_pumpkins = pumpkins_df[pumpkins_df['Variety']=='PIE TYPE']
pie_pumpkins.plot.scatter('Day of Year','Average Price')
plt.show()

#Calculate the correlation between Day of Year and Price
print(pie_pumpkins['Day of Year'].corr(pie_pumpkins['Average Price']))

#Calculate the correlation between Month and Price
print(pie_pumpkins['Month'].corr(pie_pumpkins['Average Price']))