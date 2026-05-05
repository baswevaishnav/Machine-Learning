import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

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

#Get the day of the year and price in separte arrays
X = pie_pumpkins['Day of Year'].to_numpy().reshape(-1,1)
Y = pie_pumpkins['Average Price']

#Print the shape
print(X.shape)

#Split the data into training and testing data 
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=0)

#Create a linear regression object
lin_reg = LinearRegression()

#Train the model using our training data
lin_reg.fit(X_train,Y_train)

#Test the model using our test data
prediction = lin_reg.predict(X_test)
print(prediction)

#Calculate mean squared error
mse = np.sqrt(mean_squared_error(Y_test,prediction))

#Print the mean squared error in an easy format to read
print(f'Mean error: {mse:3.3} ({mse/np.mean(prediction)*100:3.3}%)')

#Calculate the coefficient of determination
score = lin_reg.score(X_train,Y_train)
print(f'Model Determination: ',score)

#Create a scatter plot using our test data
plt.scatter(X_test,Y_test)

#Add a line to the plot with predictions
plt.plot(X_test,prediction)

#Print the slopr and intercept
print(f'y = {lin_reg.coef_[0]}x + {lin_reg.intercept_}')
plt.show()

lin_reg.predict([[256]])

#Build polynomial regression pipeline
pipeline = make_pipeline(PolynomialFeatures(2), LinearRegression())

#Use the pipeline to build the model
pipeline.fit(X_train, Y_train)

#Test model with our test data
prediction = pipeline.predict(X_test)

#Calculate mean squared error
mse = np.sqrt(mean_squared_error(Y_test,prediction))
print(f'Mean error: {mse:3.3} ({mse/np.mean(prediction)*100:3.3}%)')

#Plot the results
plt.scatter(X_test,Y_test)
plt.plot(sorted(X_test),pipeline.predict(sorted(X_test)))
plt.show()

#Score the model
score = pipeline.score(X_train,Y_train)
print('Model Determination: ',score)