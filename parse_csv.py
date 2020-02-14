import os
import csv
import matplotlib.pyplot as plt
import numpy

with open(os.getcwd() + '/EIT/datasets/Natural_Bladder_fill.txt', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(reader, None)

  times = [[] for i in range(32)]
  pairs = [[[] for i in range(32)] for i in range(32)]


  for row in reader:
    #if current rows 2nd value is equal to input, print that row
    for i in range(32): 
        if i == int(row[0]):
              #print(row)        
              times[i].append(int(row[1]))
              for x in range(32):
                pairs[i][x].append(int(row[3+x]))



times_outliers = [[[] for i in range(32)] for i in range(32)]
pairs_outliers = [[[] for i in range(32)] for i in range(32)]

means = numpy.zeros((32,32))
sds = numpy.zeros((32,32))




for m in range(32):
  for n in range(32):
    elements = numpy.array(pairs[m][n])
    mean = numpy.mean(elements, axis=0)
    sd = numpy.std(elements, axis=0)
    means[m][n] = mean
    sds[m][n] = sd 
    for i, x in enumerate(pairs[m][n]):
      if x > mean - 2 * sd and x < mean + 2 * sd:
        pairs_outliers[m][n].append(x)
        times_outliers[m][n].append(times[m][i])


pairs_outliers_norm = [[[] for i in range(32)] for i in range(32)]


for m in range(32):
  for n in range(32):
    for x in pairs_outliers[m][n]:
      if means[m][n]<pairs_outliers[m][n][0]:
        pairs_outliers_norm[m][n].append(x/pairs_outliers[m][n][0])
      else:
        pairs_outliers_norm[m][n].append(x/pairs_outliers[m][n][0])




for x in range(32):
  for y in range(32):
    if sds[y][x] < 1000:
      plt.plot(times_outliers[y][x],pairs_outliers_norm[y][x])

plt.ylabel('ADC')
plt.xlabel('Time')
plt.show()
print(len(times_outliers[0][4]))
print(len(pairs_outliers_norm[0][4]))


