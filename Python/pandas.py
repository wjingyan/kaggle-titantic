import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv', 'rU')) 
header = csv_file_object.next() 
data=[] 

for row in csv_file_object:
    data.append(row)
data = np.array(data) 

#print data
#print data[0:15, 5]
print type(data[0::,5])