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
signal_copy=signal[0:2]
print(len(signal_copy))
values=struct.unpack("<h",signal_copy)
print(values)

'''
-> byte array huney raixa binary maa read garda ani tesaile aba 
16 bit ko laagi 2 bytes huna paryo..bhanneley 50792/2=25396

->  "<" chai little endian ko laagi ani h bhaneko chai hex coded bytes bhaneko
'''
abc="h"*25396
values=list(struct.unpack("<"+abc,signal))
values=np.array(values)
print(values.size)
raw.close()
plt.plot(values)
plt.show()
