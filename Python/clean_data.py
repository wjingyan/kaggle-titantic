############## COLUMNS 
def clean_gender(df):
	# 0 - female, 1 - male
	df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1}).astype(int)

def clean_embarked_most_common(df):
	# 0 - C, 1 - S, 2 - Q
	# 2 missing - fill with C
	df['Embarked'] = df['Embarked'].fillna('C') 
	df['EmbarkCode'] = df['Embarked'].map( {'C': 0, 'S': 1, 'Q': 2}).astype(int)

def clean_age_median_class_gender(df, pd):
	# 100+ age missing - fill with median age for class/gender
	# fill in missing age data with median age
	# and 'AgeIsNull' column
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

def clean_fare(df):
	

############# MAIN
def clean_data(path):
	df = pd.read_csv(path, header=0)

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