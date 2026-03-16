import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, model_selection

# Load the diabetes dataset
x,y = datasets.load_diabetes(return_X_y=True)

#Print the shape of the data and the first row
print(x.shape)
print(x[0])

#Extract the column at index 2 and reshape it to be a 2D array
x = x[:,2]
print(x.shape)
x = x.reshape(-1,1)
print(x.shape)

#Split the data into training and testing sets
x_train, x_test, y_train, y_test = model_selection.train_test_split(x,y, test_size=0.33)

#Create a linear regression model and fit it to the training data
model = linear_model.LinearRegression()
model.fit(x_train, y_train)

#Predict using the test data
y_pred = model.predict(x_test)

#Create a scatter plot
plt.scatter(x_test, y_test, color='blue')

#Plot the predicted line
plt.plot(x_test, y_pred, color='red', linewidth=3)

#Add labels and title
plt.xlabel('Scaled BMIs')
plt.ylabel('Diabetes Progression')
plt.title('Linear Regression on Diabetes Dataset')

#Draw the plot
plt.show()


