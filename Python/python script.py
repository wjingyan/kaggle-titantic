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

################### ANALYSIS START ###################
# print data[-1] #-1 for last one
number_passengers = np.size(data[0::,1].astype(np.float)) # syntax conversion is not necessary
#number_passengers = np.size(data[0::,1])
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers
# syntax so python also supports string formatting, what about concatenation? +
# syntax can't do math here
# syntax "" and '' are interchangeable
print 'Total number survived is %s' % proportion_survivors 

women_only_stats = data[0::,4] == "female" # syntax? women_only_stats is like a filter I guess
men_only_stats = data[0::,4] != "female"

women_onboard = data[women_only_stats, 1].astype(np.float)
men_onboard = data[men_only_stats, 1].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard) # syntax of \ - joion two lines
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who surived is %s' % proportion_women_survived
print 'Proportion of men who surived is %s' % proportion_men_survived

################### ANALYSIS END ###################

# write into test.csv
test_file_object = csv.reader(open('test.csv', 'rU'))
header = test_file_object.next()

prediction_file_object = csv.writer(open("python-genderbasedmodel.csv", "wb"))

prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object:
	if row[3] == 'female':
		prediction_file_object.writerow([row[0], '1']) # predict 1 - survived
	else:
		prediction_file_object.writerow([row[0], '0']) # predict 0 - deceased
#test_file.close() but I don't need to do it? syntax? python io close file
