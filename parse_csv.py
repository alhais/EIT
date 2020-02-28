import os
import csv
import matplotlib.pyplot as plt
import numpy


file_name = '310s300ml'

gains = [[] for i in range(32)]
gains.clear
#Get dataset from serial port file and generate data matrix
with open(os.getcwd() + '/EIT/datasets/'+file_name+'_Gains'+'.txt', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  #next(reader, None)
  for idx, row in enumerate(reader):
    for x in range(32):
      gains[idx].append(int(row[1+x]))

#print(gains[31])



times = [[] for i in range(32)]
pairs = [[[] for i in range(32)] for i in range(32)]

#Get dataset from serial port file and generate data matrix
with open(os.getcwd() + '/EIT/datasets/'+file_name+'.txt', newline='') as csvfile:
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


#AD5292 Potentiometer 1024 Positions 20K Nominal resistance, Formula Vw=(D/1024)*Vin
#Vin=Vw*1024/D
#Gains: 50.5 -> (D/1024) -> 100
#11 bits ADC 1.024 reference


#uV result
EIT_voltages_ADC = [[[] for i in range(32)] for i in range(32)]

for m in range(32):
  for n in range(32):
    for i in range(len(pairs[m][n])):
      EIT_voltages_ADC[m][n].append(1000*pairs[m][n][i]*1024/2048)


EIT_voltages_atElectrodes = [[[] for i in range(32)] for i in range(32)]

for m in range(32):
  for n in range(32):
    for i in range(len(EIT_voltages_ADC[m][n])):
      if gains[m][n]!= 0:
        EIT_voltages_atElectrodes[m][n].append((EIT_voltages_ADC[m][n][i]/(100*50.5))*(1024/gains[m][n]))
      else:
        EIT_voltages_atElectrodes[m][n].append(0)

#print(EIT_voltages_atElectrodes[0][6])

#Create a .csv file compatible with EIDORS format in Octave in V
EIT_data = [[] for i in range(32*32)]
EIT_data.clear()
with open('eit_format_V.csv', 'w', newline='') as file:
  writer = csv.writer(file, delimiter=',')
  for i in range(len(EIT_voltages_atElectrodes[0][0])):
    for m in range(32):
      for n in range(32):
        EIT_data.append(EIT_voltages_atElectrodes[m][n][i]/1000000)
    writer.writerow(EIT_data)
    EIT_data.clear()



#Normalization of all data 
pairs_mV_norm = [[[] for i in range(32)] for i in range(32)]

for m in range(32):
  for n in range(32):
    for x in EIT_voltages_atElectrodes[m][n]:
      if EIT_voltages_atElectrodes[m][n][0] != 0:
        pairs_mV_norm[m][n].append(x/EIT_voltages_atElectrodes[m][n][0])
      else:
          pairs_mV_norm[m][n].append(0)


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


bad_pairs = [[]]
bad_pairs.clear
# Change n to visualize voltages related to de excitation pair n
m=31
#for n in range(32):
#for n in range(32):
#  if maxs[m][n] < 1.2 and mins[m][n] > 0.8:
#    plt.plot(times[m], pairs_outliers_norm[m][n])
#  else:
#    if maxs[m][n] != 0:
#      bad_pairs.append([m,n])

m=10
#for n in range(32):
  #plt.plot(times[m], EIT_voltages_atElectrodes[m][n])

plt.plot(times[m], EIT_voltages_atElectrodes[10][1])
plt.plot(times[m], EIT_voltages_atElectrodes[1][11])
#plt.plot(times[0], pairs_outliers_norm[0][4])



plt.ylabel('uV')
plt.xlabel('Time')
plt.show()


print(bad_pairs)