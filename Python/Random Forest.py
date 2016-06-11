import pandas as pd
import numpy as np
import pylab as P # for histogram!

df = pd.read_csv('../Data/train.csv', header=0)

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

df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked', 'Age'], axis = 1)

df = df.dropna()

train_data = df.values

print train_data


