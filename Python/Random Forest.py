import pandas as pd
import numpy as np
import pylab as P # for histogram!
import csv as csv
from sklearn.ensemble import RandomForestClassifier 

def clean_data(path):
	df = pd.read_csv(path, header=0)
	print df.info()

	#Gender column female 0, male 1
	df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1}).astype(int)

	#just fill the two missing values with most common embark
	df['Embarked'] = df['Embarked'].fillna('C') 
	# 0, 1 or 2 (Cherbourg, Southamption and Queenstown)
	df['EmbarkCode'] = df['Embarked'].map( {'C': 0, 'S': 1, 'Q': 2}).astype(int) 

	# fill in missing age data with median age
	median_ages = np.zeros((2,3))
	df['AgeFill'] = df['Age']

	for i in range(0, 2):
		for j in range(0, 3):
			median_ages[i, j] = df[(df['Gender'] == i) & (df['Pclass'] == j + 1)]['Age'].dropna().median()

	for i in range (0, 2): # gender
		for j in range(0, 3): #Pclass
			df.loc[(df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j + 1), 'AgeFill'] = median_ages[i,j]

	# AgeIsNull column
	df['AgeIsNull'] = pd.isnull(df.Age).astype(int)
	#print df[df['Age'].isnull()] [['Gender', 'Pclass', 'Age', 'AgeFill', 'AgeIsNull', 'Embarked', 'EmbarkCode']].head(10)


	# All the missing Fares -> assume median of their respective class
	if len(df.Fare[ df.Fare.isnull() ]) > 0:
	    median_fare = np.zeros(3)
	    for f in range(0,3):                                              # loop 0 to 2
	        median_fare[f] = df[ df.Pclass == f+1 ]['Fare'].dropna().median()
	    for f in range(0,3):                                              # loop 0 to 2
	        df.loc[ (df.Fare.isnull()) & (df.Pclass == f+1 ), 'Fare'] = median_fare[f]

	df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked', 'Age', 'PassengerId'], axis = 1)

	print df.info()

	#df = df.dropna() # not great idea - you can't drop test data 

	return df.values

def clean_data_sample(path):
	# use data cleaning from sample
	train_df = pd.read_csv('../Data/train.csv', header=0)

train_data = clean_data("../Data/train.csv")
test_data = clean_data("../Data/test.csv")

print train_data

#TODO it's a terrible idea to open the csv file twice, passing back two references in Python?
test_df = pd.read_csv('../Data/test.csv', header=0)
ids = test_df['PassengerId'].values

forest = RandomForestClassifier(n_estimators = 100) #Syntax?

# Fit the training data to the Survived labels and create the decision trees
forest = forest.fit(train_data[0::,1::],train_data[0::,0]) #Syntax?

# Take the same decision trees and run it on the test data
output = forest.predict(test_data).astype(int) # Not converting to int caused a 0.000 submission...

predictions_file = open("Random Forest Result.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output)) #Syntax?
predictions_file.close()

print "Done."