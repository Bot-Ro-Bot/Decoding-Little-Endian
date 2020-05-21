import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import struct


file_name ="e07_002_001_0100.adc" 

raw = open(file_name,"rb")
signal= (raw.read())
print(type(signal))
print(len(signal))

#byte array huney raixa binary maa read garda ani tesaile aba 16 bit ko laagi 2 bytes huna paryo..bhanneley 50792/2=25396
#small "<" chai little endian ko laagi ani h chai hex maa encoded bhayeko ley

abc="h"*int(len(signal)/2)
values=list(struct.unpack("<"+abc,signal))
values=np.array(values)
print(values.size)
raw.close()
values=values.reshape(int(len(signal) / (2*7)),7)
print(values.shape)

#sabbai 7 otai graph c maa aaune raixa...sahi laagyo yo kura...
fig,c=plt.subplots(7,1)

#naam ko laagi matra
columns=['CHANNEL_1','CHANNEL_2','CHANNEL_3','CHANNEL_4','CHANNEL_5','CHANNEL_6','MARKER']

#a function to setup graphs of all seven channels
def showGraph():
	for i in range(7):
		c[i].plot(values[:600,i])
		c[i].set_title(columns[i],size=8)
showGraph()
plt.show()

