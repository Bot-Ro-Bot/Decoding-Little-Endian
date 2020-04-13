'''
literature : http://archive.oreilly.com/oreillyschool/courses/Python3/Python3-08.html

'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import struct

raw = open("e07_002_001_0100.adc","rb")
signal= (raw.read())
print(type(signal))
print(len(signal))

#byte array huney raixa binary maa read garda ani tesaile aba 16 bit ko laagi 2 bytes huna paryo..bhanneley 50792/2=25396
#small "<" chai little endian ko laagi ani h chai hex maa encoded bhayeko ley

abc="h"*25396
values=list(struct.unpack("<"+abc,signal))
values=np.array(values)
print(values.size)
raw.close()
values=values.reshape(3628,7)
print(values.shape)

fig,c=plt.subplots(7,1)
columns=['CHANNEL_1','CHANNEL_2','CHANNEL_3','CHANNEL_4','CHANNEL_5','CHANNEL_6','MARKER']


def showGraph():
	for i in range(7):
		c[i].plot(values[:,i])
		c[i].set_title(columns[i],size=8)

showGraph()
plt.show()

