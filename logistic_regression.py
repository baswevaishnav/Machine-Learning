import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score


full_pumpkins = pd.read_csv('C:/Users/VBaswe/Practice/Machine-Learning/US-pumpkins.csv')
print(full_pumpkins.head())

#Select columns
columns_to_select = ['City Name', 'Package', 'Variety', 'Origin', 'Item Size', 'Color']
pumpkins = full_pumpkins.loc[:, columns_to_select]

#Drop rows with missing values
pumpkins.dropna(inplace=True)

#Print first few rows
print(pumpkins.head())

#Specify colors for each values of the hue variable

palette = {
    'ORANGE': 'orange',
    'WHITE': 'wheat'
}

#Plot a bar chart
sns.catplot(
    data=pumpkins, y = 'Variety', hue = 'Color', kind = "count", palette = palette,
)
plt.show()

#Different sizes of pumpkins
sizes = pumpkins['Item Size'].unique()
print(sizes)

#Encoding Item Size column using ordinal encoder
item_size_catogories = [['sml', 'med', 'med-lge', 'lge', 'xlge', 'jbo', 'exjbo']]
ordinal_features = ['Item Size']
ordinal_encoder = OrdinalEncoder(categories=item_size_catogories)

#Encode all other features using one hot encoding
categorical_features = ['City Name', 'Package', 'Variety', 'Origin']
categorical_encoder = OneHotEncoder(sparse_output=False)

#Column transformation
ct = ColumnTransformer(transformers=[
                       ('ord', ordinal_encoder, ordinal_features),
                       ('cat', categorical_encoder, categorical_features)
                        ])

#Get the encoded features as a padas DataFrame
ct.set_output(transform='pandas')
encoded_features = ct.fit_transform(pumpkins)
print(encoded_features.head())

#Encode the Color column using label encoding
label_encoder = LabelEncoder()
encoded_label = label_encoder.fit_transform(pumpkins['Color'])
encoded_pumpkins = encoded_features.assign(Color=encoded_label)
print(encoded_pumpkins.head())

list(label_encoder.inverse_transform([0,1]))

#Encoding Item size column to use as x axis
pumpkins['Item Size'] = encoded_pumpkins['ord__Item Size']

g = sns.catplot(
    data=pumpkins,
    x='Item Size', y='Color', row='Variety',
    kind='box', orient='h',
    sharex=False, margin_titles=True,
    height=1.5, aspect=4, palette=palette,
)

#Defining axis labels
g.set(xlabel="Item Size", ylabel="").set(xlim=(0,6))
g.set_titles(row_template="{row_name}")
plt.show()

palette = {
    '0': 'orange',
    '1': 'wheat'
}
sns.swarmplot(x='Color',y='ord__Item Size', data=encoded_pumpkins,palette=palette)
plt.show()


#X is encoded deatures
X = encoded_pumpkins[encoded_pumpkins.columns.difference(['Color'])]

#Y us encoded label
Y = encoded_pumpkins['Color']

#Split data into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=0)

#Train a logistic regression model on the pupkin dataset
model = LogisticRegression()
model.fit(X_train,Y_train)
predictions = model.predict(X_test)

#Evaluate the model and print results
print(classification_report(Y_test,predictions))
print('Prediction Labels: ',predictions)
print('F1-score: ',f1_score(Y_test,predictions))


#Confusion matrix
print(confusion_matrix(Y_test,predictions))

#PROC curve
y_scores = model.predict_proba(X_test)

#Calculating ROC curve
fpr, tpr, thresholds = roc_curve(Y_test, y_score=[:,1])

#Plot ROC curve
fig = plt.figure(figsize=(6,6))
#Plot diagonal 50% line
plt.plot([0,1],[0,1],'k--')
#Plot FPR and TPR achieved by our model
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()