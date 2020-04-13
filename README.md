# Decoding-Little-Endian

Raw emg signal from the EMG-UKA Trial Corpus uses .adc (a analog to digital acquisition file extension) in its data.
The data needs to be preprocessed and visualized before developing a proper model to train using these datas.
The data is raw, uncompressed, headerless and in little endian short integer format.

For obtaining the dataset, please contact:
tanja.schultz@kit.edu
http://csl.anthropomatik.kit.edu

This repo contains the required code for effective conversion of the data into an appropriate format.
