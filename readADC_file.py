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
signal=signal[0:2]
print(len(signal))
values=struct.unpack("<h",signal)
print(values)
