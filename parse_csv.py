import os
import csv
import matplotlib.pyplot as plt
import numpy

times = [[] for i in range(32)]
pairs = [[[] for i in range(32)] for i in range(32)]

#Get dataset from serial port file and generate data matrix
with open(os.getcwd() + '/EIT/datasets/320s400ml.txt', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(reader, None)
  for row in reader:
    #if current rows 2nd value is equal to input, print that row
    for i in range(32): 
        if i == int(row[0]):
              #print(row)        
              times[i].append(int(row[1]))
              for x in range(32):
                pairs[i][x].append(int(row[3+x]))
            
#Normalization of all data 
pairs_outliers_norm = [[[] for i in range(32)] for i in range(32)]

for m in range(32):
  for n in range(32):
    for x in pairs[m][n]:
      if pairs[m][n][0] != 0:
        pairs_outliers_norm[m][n].append(x/pairs[m][n][0])
      else:
          pairs_outliers_norm[m][n].append(0)


#Create a .csv file compatible with EIDORS format in Octave
EIT_data = [[] for i in range(32*32)]
EIT_data.clear()
with open('eit_format.csv', 'w', newline='') as file:
  writer = csv.writer(file, delimiter=',')
  for i in range(len(pairs[0][0])):
    for m in range(32):
      for n in range(32):
        EIT_data.append(pairs[m][n][i])
    writer.writerow(EIT_data)
    EIT_data.clear()


#Remove outliers from data to visualize better the graph data
maxs = numpy.zeros((32,32))
mins = numpy.zeros((32,32))
for m in range(32):
  for n in range(32):
     elements = numpy.array( pairs_outliers_norm[m][n])
     max_ = numpy.max(elements, axis=0)
     min_ = numpy.min(elements, axis=0)
     maxs[m][n] = max_
     mins[m][n] = min_



# Change n to visualize voltages related to de excitation pair n
n=1
for m in range(32):
  if maxs[m][n] < 1.2 and mins[m][n] > 0.8:
       plt.plot(times[m], pairs_outliers_norm[m][n])


#plt.plot(times[0], pairs_outliers_norm[0][4])



plt.ylabel('ADC')
plt.xlabel('Time')
plt.show()


#print(times[0])