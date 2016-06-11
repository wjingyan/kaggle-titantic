# example from https://www.kaggle.com/c/titanic/details/getting-started-with-python
# slight modification documented
import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv','rU')) # as opposed to 'rb' in tutorial, we're going for Universal mode!
header = csv_file_object.next()

data = []
for row in csv_file_object:
	data.append(row)
data = np.array(data)

fare_ceiling = 40
#modify data such that ceiling is indeed 40
data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

number_of_classes = len(np.unique(data[0::,2])) #syntax

survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes): #syntax? [1, number_of_classes]
	for j in xrange(number_of_price_brackets):
		women_only_stats = (data[			
							(data[0::,4] == "female")	#female
							& (data[0::, 2].astype(np.float) == i + 1)		# ith class
							& (data[0:, 9].astype(np.float) >= j * fare_bracket_size) # greater than this bin
							# syntax :: is the same as :
							& (data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size) # less than next bin
							, 1])
		
		men_only_stats = data[			\
							(data[0::,4] != "female")	\
							& (data[0::, 2].astype(np.float) == i + 1)		\
							& (data[0:, 9].astype(np.float) >= j * fare_bracket_size) \
							& (data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size) \
							, 1]
		survival_table[0, i, j] = np.mean(women_only_stats.astype(np.float))
		survival_table[1, i, j] = np.mean(men_only_stats.astype(np.float))

survival_table[survival_table != survival_table] = 0 #syntax? python is a weird language

survival_table[survival_table < 0.5] = 0 #syntax do something on the entire table
survival_table[survival_table >= 0.5] = 1

print survival_table

test_file_object = csv.reader(open('test.csv', 'rU'))
header = test_file_object.next()
prediction_file_object = csv.writer(open('python-genderclassmodel.csv', 'wb'))
prediction_file_object.writerow(["PassengerId", "Survived"])

for row in test_file_object:
	for j in xrange(number_of_price_brackets):
		try:
			row[8] = float(row[8])
		except:
			bin_fare = 3 - float(row[1])
			break
		if row[8] > fare_ceiling:
			bin_fare = number_of_price_brackets - 1
			break
		if row[8] >= j * fare_bracket_size and row[8] < (j + 1) * fare_bracket_size:
			bin_fare = j
			break
	pclass = float(row[1])
	if row[3] == 'female':
		prediction_file_object.writerow([row[0], "%d" % int(survival_table[0, pclass - 1, bin_fare])])
	else:
		prediction_file_object.writerow([row[0], "%d" % int(survival_table[1, pclass - 1, bin_fare])])






