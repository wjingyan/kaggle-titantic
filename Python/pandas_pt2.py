import pandas as pd
import numpy as np
import pylab as P # for histogram!

# For .read_csv, always use header=0 when you know row 0 is the header row
df = pd.read_csv('../Data/train.csv', header=0)

#print df
#print df.head(3) # first 3 rows
#print df.tail(3) # last 3 rows
#print type(df) #pandas.core.frame.DataFrame
#print df.dtypes # Yay, panda interprets data types intelligently
#print df.info()
#print df.describe()
#print df['Age'][0:10] # first 10 rows of age column
#print df.Age[0:10]
#print type(df['Age']) #pandas.core.series.Series
#print df['Age'].mean()
#print df[ ['Sex', 'Pclass', 'Age']] # show only sex, pclass, age columns
#print df[df['Age'] > 60]
#print df[df['Age'] > 60][['Sex','Pclass','Age', 'Survived']]
#print df[df['Age'].isnull()][['Sex','Pclass','Age', 'Survived']]

# male in each class
#for i in range(1, 4):
#	print i, len(df[(df['Sex'] == 'male') & (df['Pclass'] == i)])

# histogram
#df['Age'].hist()
#df['Age'].dropna().hist(bins=16, range=(0,80), alpha = 1) # alpha is just the prettiness of the hist
#P.show()

#df['Gender'] = 4
#df['Gender'] = df['Sex'].map( lambda x: x[0].upper()) # lambda generate a function
df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1}).astype(int)
# 0, 1 or 2 (Cherbourg, Southamption and Queenstown)
# ('Cannot convert NA to integer')
df['Embarked'] = df['Embarked'].fillna('C') #just fill the two missing with most common
df['EmbarkCode'] = df['Embarked'].map( {'C': 0, 'S': 1, 'Q': 2}).astype(int) 

# fill in missing age data
median_ages = np.zeros((2,3))
df['AgeFill'] = df['Age']

for i in range(0, 2):
	for j in range(0, 3):
		median_ages[i, j] = df[(df['Gender'] == i) & (df['Pclass'] == j + 1)]['Age'].dropna().median()
#print median_ages

for i in range (0, 2): # gender
	for j in range(0, 3): #Pclass
		df.loc[(df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j + 1), 'AgeFill'] = median_ages[i,j]


# only print rows missing ages 
#print df[df['Age'].isnull()] [['Gender', 'Pclass', 'Age', 'AgeFill']].head(10)

# AgeIsNull column
df['AgeIsNull'] = pd.isnull(df.Age).astype(int)
print df[df['Age'].isnull()] [['Gender', 'Pclass', 'Age', 'AgeFill', 'AgeIsNull', 'Embarked', 'EmbarkCode']].head(10)



