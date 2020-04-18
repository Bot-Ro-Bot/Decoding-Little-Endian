'''
literature : http://archive.oreilly.com/oreillyschool/courses/Python3/Python3-08.html
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import struct

def ADC2arr(filename):
	'''
	Parameters
	----------------------------------------------
	filename 	: str
		full name of the .adc file


	Returns
	----------------------------------------------
		list of values with rows = 7 and column int(len(signal)/(2*7)) 
	'''
	raw = open(filename,"rb")
	signal = (raw.read())
	'''
	Note 
	---------------------------------------------
	- byte array huney raixa binary maa read garda ani tesaile aba 
		16 bit ko laagi 2 bytes huna paryo..bhanneley
		(calculation for test file) 
		total bytes = 50792
		byte of each data = 2
		no of data : 50792/2=25396
		the no of rows of every .adc file = 7 (kind of constant for all file)
		no of columns for .adc file = int(len(signal)/(2*7)) 
	- "<" chai little endian ko laagi ani h bhaneko chai hex coded bytes bhaneko
	'''
	cols = int(len(signal)/(2*7)) 	#no of cols  
	rows = 7						#no of rows
	values = [[0] * cols for i in range(rows)]
	for i in range(cols):
		for j in range(rows):
			temp = ((i*7)+j)*2
			signal_copy = signal[temp:temp+2]
			values[j][i] = struct.unpack("<h",signal_copy)[0]
			# print(values[j][i])
	# print(len(values)
	raw.close()
	return values



# print(sys.getfilesystemencoding())
# raw = open("e07_002_001_0100.adc","rb")
# signal= (raw.read())
# print(type(signal))
# print(len(signal))
# signal_copy=signal[0:2]
# signal_copy1 = signal[2:4]
# print(len(signal_copy))
# values=struct.unpack("<h",signal_copy)
# values1=struct.unpack("<h",signal_copy1)
# print(values)
# print(values1)

'''
-> byte array huney raixa binary maa read garda ani tesaile aba 
16 bit ko laagi 2 bytes huna paryo..bhanneley 50792/2=25396

->  "<" chai little endian ko laagi ani h bhaneko chai hex coded bytes bhaneko
'''
# abc="h"*25396
# values=list(struct.unpack("<"+abc,signal))
# values=np.array(values)
# print(values.size)
# raw.close()
# plt.plot(values)
# plt.show()




#reading the data from .adc file

# file = "e07_002_001_0100.adc"
# val = ADC2arr(file)


# #plotting data for channel 1
# print(len(val[0][:]))
# x_grid = np.arange(0,len(val[0][:]),step=1)
# x_grid = x_grid.reshape((len(x_grid), 1))
# plt.plot(x_grid, val[0][:], color="red")
# plt.title('Signal')
# plt.xlabel('time')
# plt.ylabel('adc')
# plt.show()