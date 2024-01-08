# -*- coding: utf-8 -*-
"""ML_Course-Project_235666006(Crop-recommendation).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cl0C5FzfqXaBYrL5pBphydxn3u-bQM9g

Importing libraries packages according to our model requirement
"""

import pandas as pd
import numpy as np

"""Importing dataset for model training and testing

# **Load and Explore Data**
"""

DF=pd.read_csv('/content/Crop_recommendation.csv')

DF.head(5) #exploring dataset

DF.info()

#We can rename them so it's easier to understand
DF.rename(columns={'N': 'Nitrogen'}, inplace=True)
DF.rename(columns={'P': 'Phosphorus'}, inplace=True)
DF.rename(columns={'K': 'Potassium'}, inplace=True)
DF.rename(columns={'ph': 'value of the soil'}, inplace=True)

DF.info() #checking for null values in our dataset

print(DF['label'].value_counts())
print(DF['label'].nunique())#Fetching no of classes we have into dataset

"""So we have 100 samples from each crop type"""

DF.describe()#Here is a statistical measures of variability

#checking correlation between explanatory variables
DF_numeric = DF.drop('label', axis = 1)
DF_numeric.corr()
#as there is some correlation between independent variables which will affect  our model We can use PCA for de-correlation

"""# *Data Preprocessing*"""

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# selection features for PCA
numerical_columns = ['Nitrogen', 'Phosphorus', 'Potassium', 'temperature', 'humidity', 'value of the soil', 'rainfall']
data_for_pca = DF[numerical_columns]

# Standardize the data so that our analysis should not get dominated by large features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_for_pca)

# Apply PCA with 7 components
pca = PCA(n_components=7)
pca_result = pca.fit_transform(scaled_data)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i}' for i in range(1, 8)])

# Display the DataFrame with principal components
print("DataFrame after PCA:")
print(pca_df)

#checking correlation after PCA performed
pca_df.corr()

DF_numeric.corr()

"""#As we can observe that the correlation before and after applying PCA correlation after PCA got reduced to very small values"""

#analysis of correlation
# Plot a heatmap
import matplotlib.pyplot as plt
import seaborn as sns#importing packages for analysis
# Calculate the correlation matrix
correlation_matrix = DF_numeric.corr()

# Plot a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Correlation Matrix Heatmap')
plt.show()

#After applying PCA plotting heatmap
PCA_correlation_matrix = pca_df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(PCA_correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('PCA Correlation Matrix Heatmap')
plt.show()

#anylizing distribution of all features in order to handel missing values if any
plt.figure(figsize=(10,8))
plt.subplot(3,2,1)
sns.distplot(DF['Nitrogen'])

plt.subplot(3,2,2)
sns.distplot(DF['Phosphorus'])

plt.subplot(3,2,3)
sns.distplot(DF['Potassium'])

plt.subplot(3,2,4)
sns.distplot(DF['temperature'])

plt.subplot(3,2,5)
sns.distplot(DF['value of the soil'])

plt.subplot(3,2,6)
sns.distplot(DF['humidity'])

plt.show()

#Now analyzing distribution of each features after applying PCA
plt.figure(figsize=(10,8))
plt.subplot(3,2,1)
sns.distplot(pca_df['PC1'])

plt.subplot(3,2,2)
sns.distplot(pca_df['PC2'])

plt.subplot(3,2,3)
sns.distplot(pca_df['PC3'])

plt.subplot(3,2,4)
sns.distplot(pca_df['PC4'])

plt.subplot(3,2,5)
sns.distplot(pca_df['PC5'])

plt.subplot(3,2,6)
sns.distplot(pca_df['PC6'])

plt.show()
print("\n","We can observe the distribution after applying PCA get approximated to almost normal distrubution")

"""## For classification we required classes in form of categorical variables(integar) but here we have names of crops so we have to encode it to numerical values"""

#encodding our classes into numerical numbers
from sklearn.preprocessing import LabelEncoder #importing encoding package

# Initialize(creating object) LabelEncoder
label_encoder = LabelEncoder()
DF['encoded_label'] = label_encoder.fit_transform(DF['label'])

DF['encoded_label'].unique() #converted labels

DF.drop('label',axis=1,inplace=True) #deleting old column of label

DF.head()#final dataset which we have to work on

"""Now Spliting Data into Features and Target(crops)"""

Features=DF.drop('encoded_label', axis=1)#splitted Features
Target=DF['encoded_label'] #splitted targets

"""## Split Data into Training and Testing Sets"""

from sklearn.model_selection import train_test_split #importing package for splitting data into test and train data

Features_train, Features_test, Target_train, Target_test = train_test_split(Features,Target, test_size=0.2, random_state=55)

"""Now we have prepared data in desirable format from raw dataset now time to build up a machine learning model

# MODEL-1 Perceptron
"""

from sklearn.linear_model import Perceptron #Creating a Perceptron model

perceptron_model=Perceptron()

# Train the Perceptron model
perceptron_model.fit(Features_train, Target_train)

# Make predictions on the test set
preceptron_pred = perceptron_model.predict(Features_test)

#predictions of perceptron model
preceptron_pred

"""Evaulating accuracy of our multi-output model"""

#importing required packages to evaluate perfomance of our model
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
print(classification_report(Target_test,preceptron_pred))
perceptron_accuracy=accuracy_score(Target_test,preceptron_pred)

print(f"The accuracy of our perceptron model is = {accuracy_score(Target_test,preceptron_pred)}")

con_mat=confusion_matrix(Target_test,preceptron_pred)

print(con_mat)

#
plt.figure(figsize=(12, 8))
sns.heatmap(con_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()

"""## Model-2(Support vector machine)"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
# You can choose different kernel functions, such as 'linear', 'rbf', 'poly', etc.
# The choice of the kernel depends on your specific problem and data.
param_grid={'C' : [0.1,1,10,100,1000],
            'gamma':[1,0.1,0.01,0.001,0.0001],
            'kernel':['linear','rbf','poly']
}
#initialize our model
grid=GridSearchCV(SVC(),param_grid=param_grid,refit=True,cv=5,verbose=True)
#training our model
grid.fit(Features_train,Target_train)
#making predictions
SVM_pred=grid.predict(Features_test)
# Evaluate the model
# accuracy = accuracy_score(Features_test, SVM_pred)
# print(f"Accuracy: {accuracy:.2f}")

print(grid.best_params_)
print()
SVM_pred

#importing required packages to evaluate perfomance of our model
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
print(classification_report(Target_test,SVM_pred))
SVM_accuracy=accuracy_score(Target_test,SVM_pred)

cnf_mat=confusion_matrix(Target_test,SVM_pred)

plt.figure(figsize=(12, 8))
sns.heatmap(con_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()
print()

print(f"Accuracy of SVM model={accuracy_score(Target_test,SVM_pred)}")

"""Model-3(Decision trees)"""

from sklearn.tree import DecisionTreeClassifier
# Split the dataset into training and testing sets

# Initialize the Decision Tree classifier
tree_classifier = DecisionTreeClassifier(random_state=42,max_depth=8)

# Train the Decision Tree classifier
tree_classifier.fit(Features_train, Target_train)

# Make predictions
DT_pred = tree_classifier.predict(Features_test)

from sklearn import tree
plt.figure(figsize=(15,10))
tree.plot_tree(tree_classifier,filled=True)

DT_pred

#importing required packages to evaluate perfomance of our model
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
print(classification_report(Target_test,DT_pred))
cn_mat=confusion_matrix(Target_test,DT_pred)

plt.figure(figsize=(12, 8))
sns.heatmap(cn_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()
print()
DT_score=accuracy_score(Target_test,DT_pred)
print(f"Accuracy of DT model={accuracy_score(Target_test,DT_pred)}")

"""model-4(Random-forest)"""

from sklearn.ensemble import RandomForestClassifier
# Initialize the Decision Tree classifier
rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)

# Train the Decision Tree classifier
tree_classifier.fit(Features_train, Target_train)

# Make predictions
RF_pred = tree_classifier.predict(Features_test)

RF_pred

#importing required packages to evaluate perfomance of our model
print(classification_report(Target_test,RF_pred))
conf_mat=confusion_matrix(Target_test,RF_pred)

plt.figure(figsize=(12, 8))
sns.heatmap(conf_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()
print()
RF_score=accuracy_score(Target_test,RF_pred)
print(f"Accuracy of RF model={accuracy_score(Target_test,RF_pred)}")

"""## model-5(Naive-Bayes)"""

from sklearn.naive_bayes import GaussianNB
# Initialize the Gaussian Naive Bayes classifier
nb_classifier = GaussianNB()

nb_classifier.fit(Features_train, Target_train)

NB_pred=nb_classifier.predict(Features_test)

NB_pred

#importing required packages to evaluate perfomance of our model
print(classification_report(Target_test,NB_pred))
confu_mat=confusion_matrix(Target_test,NB_pred)

plt.figure(figsize=(12, 8))
sns.heatmap(confu_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()
print()
NB_score=accuracy_score(Target_test,NB_pred)
print(f"Accuracy of NB model={accuracy_score(Target_test,NB_pred)}")

"""## model-6(Logistic-Regression)"""

from sklearn.linear_model import LogisticRegression
# Initialize the Logistic Regression model
logreg_classifier = LogisticRegression(random_state=42)

logreg_classifier.fit(Features_train, Target_train)

LR_pred=logreg_classifier.predict(Features_test)

LR_pred

#importing required packages to evaluate perfomance of our model
print(classification_report(Target_test,LR_pred))
LR_accuracy=accuracy_score(Target_test,LR_pred)
confus_mat=confusion_matrix(Target_test,LR_pred)

plt.figure(figsize=(12, 8))
sns.heatmap(confu_mat, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Confusion Matrix Heatmap')
plt.show()
print()
print(f"Accuracy of LR model={accuracy_score(Target_test,LR_pred)}")

"""# Comparision all used models"""

Accuracy_collection={
    "Model_algo":['perceptron','SVM','Decision_Tree','Random_forest','Naive Bayes','Logistic_regression'],
    "Accuracy":[perceptron_accuracy,SVM_accuracy,DT_score,RF_score,NB_score,LR_accuracy]
}

DF_accuracy_collection=pd.DataFrame(Accuracy_collection)

# Plot a bar graph
DF_accuracy_collection.plot(kind='bar', x='Model_algo', y='Accuracy', legend=False,color=['blue', 'green', 'red', 'purple','yellow','orange'],rot=30)
plt.title('Accuracy wise comparision of models')
plt.xlabel('Model_algo')
plt.ylabel('Accuracy')
plt.show()

print(perceptron_accuracy,SVM_accuracy,DT_score,RF_score,NB_score,LR_accuracy)

