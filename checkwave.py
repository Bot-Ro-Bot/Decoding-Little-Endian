import wave
import matplotlib.pyplot as plt
import numpy as np

audio=wave.open("e07_002_001_0100.wav",'r')
# audio=wave.open("e07_002_001_0100.adc",'r')
signal=audio.readframes(-1)
signal=np.fromstring(signal,'int16')
print(audio.getnchannels())
print(audio.getsampwidth())
print(audio.getnframes())
print(audio.getframerate())
print(audio.getcomptype())
print(audio.getparams())
print(signal.shape)
plt.plot(signal)
# plt.show()