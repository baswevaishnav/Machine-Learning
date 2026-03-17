import pandas as pd
import matplotlib.pyplot as plt

#Reading csv file
pumpkins = pd.read_csv('C:/Users/VBaswe/Practice/Machine-Learning/US-pumpkins.csv')

#Filter out rows which don't use price per bushel
pumpkins = pumpkins[pumpkins['Package'].str.contains('bushel',case=True,regex=True)]
print(pumpkins.head())

#Check the sum of null rows in each column
print(pumpkins.isnull().sum())

#Selecting columns that we need
new_columns = ['Package','Month','Low Price','High Price','Date']

#Dropping all other columns
pumpkins = pumpkins.drop([c for c in pumpkins if c not in new_columns], axis=1)
#Alternate: pumpkins = pumpkins[new_columns]

#Average price
avg_price = (pumpkins['Low Price']+pumpkins['High Price'])/2

#Get the month from the date column
month = pd.DatetimeIndex(pumpkins['Date']).month

#Create a new dataframe using these columns
pumpkins_df = pd.DataFrame({'Month': month, 'Package': pumpkins['Package'], 'Low Price': pumpkins['Low Price'], 'High Price':pumpkins['High Price'], 'Average Price': avg_price})

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
