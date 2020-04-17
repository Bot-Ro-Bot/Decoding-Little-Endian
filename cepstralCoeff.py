#source : https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html

import numpy as np
import matplotlib.pyplot as plt 
import scipy.io.wavfile
from scipy.fftpack import dct

class SignalFeature:
	'''
	class SignalFeature  
		contains the function for signal processing, for extracting freatures"
	usage :
		SignalFeature(self,filename, timeframe, preEmphasis = 0.97, frameSize = 0.025, frameStride = 0.01, NFFT = 512)	


	Methods
	------------------------------------------------------
	coefficient(self,coff="filterbank",nfilt = 40, plot = False, spectrum = False):
		coefficient of the selected feature i.e."filterbank" or "MFCC"
	'''
	def __init__(self, filename, timeframe, preEmphasis = 0.97, frameSize = 0.025, frameStride = 0.01, NFFT = 512):
		'''
		Parameters
		------------------------------------------
		filename 	: str
			full name of the wave file
		timeframe	: int
		first amount of timeframe in seconds of the passed file"
		pre-emphasis: int (= 0.97 (default)) 
			apply a pre-emphasis on the signal to amplify the high frequecy.
			A pre-emphasis filter is useful in several ways: 
				(1) balance the frequency spectrum since high frequencies usually have smaller magnitudes compared to lower frequencies, 
				(2) avoid numerical problems during the Fourier transform operation 
				(3) may also improve the Signal-to-Noise Ratio (SNR)."
			pre-emphasis = 0.97 (default) . as typical values for the filter coefficient are 0.95 or 0.97
		frameSize 	: int (= 0.025 (default))
			size of frame. Typical frame sizes in speech processing range from 20 ms to 40 ms with 50% (+/-10%) overlap between consecutive frames
		frameStride	: int (= 0.01 (default))
			frame stride . usually taken as 10ms stride 
		NFFT		: int (= 512 (default))
			N -point FFT on each frame to calculate the frequency spectrum, which is also called Short-Time Fourier-Transform (STFT),
			where N is typically 256 or 512
		'''
		self.timeframe = timeframe
		sampleRate, signal = scipy.io.wavfile.read(filename)
		signal = signal[0:int(timeframe * sampleRate)] #keep the first amount of timeframe (seconds)
		self.sampleRate = sampleRate
		self.signal = signal
		self.NFFT = NFFT
		#pre-emphasis
		self.emphasizedSignal = np.append(signal[0],signal[1:] - preEmphasis * signal[:-1])
		
		#framing
		frameLength, frameStep = frameSize * sampleRate, frameStride * sampleRate #convert from seconds to samples
		signalLength = len(self.emphasizedSignal)
		frameLength = int(round(frameLength))
		frameStep = int(round(frameStep))
		numFrames = int(np.ceil(float(np.abs(signalLength - frameLength)) / frameStep )) #make sure that we have at least 1 frame

		padSignalLength = numFrames * frameStep + frameLength
		z = np.zeros((padSignalLength - signalLength))
		padSignal = np.append(self.emphasizedSignal,z) #pad signal to make sure the at all frames have equal number of samples without truncating any samplese from the original signal

		indices = np.tile(np.arange(0, frameLength), (numFrames, 1)) + np.tile(np.arange(0, numFrames * frameStep, frameStep), (frameLength, 1)).T
		frames = padSignal[indices.astype(np.int32, copy=False)]

		#window
		frames *= np.hamming(frameLength)
		# frames *= 0.54 - 0.46 * numpy.cos((2 * numpy.pi * n) / (frame_length - 1))  # Explicit Implementation **

		#fourierTransform and power spectrum
		#NFFT = 512	# N- point FFT on each frame to calculate frequecy spectrum (STFT) N is typically 256 or 512
		magFrames = np.absolute(np.fft.rfft(frames, NFFT)) 	#magnitude of FFT
		self.powFrames = ((1.0 / NFFT) * ((magFrames) ** 2))		#power spectrum


	def coefficient(self,coff="filterbank",nfilt = 40, plot = False, spectrum = False):
		'''
		coefficient of the selected feature i.e."filterbank" or "MFCC"
		
		Parameters
		----------
		coff 	: str (= "filterbank" (default))
			choose the feature. They are:-
			coff = "filterbank" 
				for selecting filterbank
			coff =  "MFCC"
				for selecting the Mel-Frequecy Cepstral Coefficient

		nfilt	: int (= 40 (default))
			no of triangular filters, typically 40 filters, on a mel-scale to the power spectrum to extract freq. bands

		plot 	: bool (= False (default))
			plots raw data of the signal. 
			plot = True for plotting the signal( uses matplot)

		spectrum: bool (= False (default))
			plots the spectrogram of the signal
			spectrum = True for plotting the spectrogram of the signal


		Returns
		---------
			numpy.ndarray . Mean-normalized value of feature.
		'''
		#nfilt = 40 , i.e. applying triangular filter, triangular filter, typically 40 filters
		lowFreqMel = 0
		highFreqMel = (2595 * np.log10(1+ (self.sampleRate / 2) / 700))  #converting Hz to mel
		melPoints = np.linspace(lowFreqMel, highFreqMel, nfilt + 2) #equally spaced in mel scale
		hzPoints = (700 * (10 ** (melPoints / 2595) - 1)) #converting Mel to Hz
		bin = np.floor((self.NFFT + 1) * hzPoints / self.sampleRate)

		fbank = np.zeros((nfilt, int(np.floor(self.NFFT / 2 +1 ))))
		for m in range(1, nfilt+1):
			f_m_minus = int(bin[m-1]) 	#left
			f_m = int(bin[m])			#center
			f_m_plus = int(bin[m+1])	#right

			for k in range(f_m_minus, f_m):
				fbank[m-1, k] = (k-bin[m-1]) / (bin[m] - bin[m-1])
			for k in range(f_m, f_m_plus):
				fbank[m-1,k] = (bin[m+1] - k) / (bin[m+1] - bin[m])

		filterBanks = np.dot(self.powFrames, fbank.T)
		filterBanks = np.where(filterBanks == 0, np.finfo(float).eps, filterBanks) #numerical stability
		filterBanks = 20 * np.log10(filterBanks) #dB

		if "filterbank" in coff:
			#mean normalization
			filterBanks -= (np.mean(filterBanks, axis=0) + 1e-8)
			filcoeff = filterBanks
		elif "MFCC" in coff:
			#MFCCs 
			num_ceps = 12 #resulting cepstral coefficient 2-13 are retained and the rest are discarded
			mfcc = dct(filterBanks, type = 2, axis = 1, norm='ortho')[:,1:(num_ceps+1)] 
			#mean normalization of MFCCs
			mfcc -= (np.mean(mfcc, axis = 0) + 1e-8)
			filcoeff = mfcc

		if plot == True:
			X_grid = np.arange(0, self.timeframe, self.timeframe/len(self.signal))
			X_grid = X_grid.reshape((len(X_grid), 1))
			print(X_grid.size)
			self.emphasizedSignal = self.emphasizedSignal.reshape((len(self.emphasizedSignal),1 ))
			
			if X_grid.size != self.emphasizedSignal.size :
				times = self.emphasizedSignal.size / X_grid.size
				X_grid = np.arange(0, self.timeframe, self.timeframe/(len(self.signal) * times))
				X_grid = X_grid.reshape((len(X_grid), 1))

			plt.plot(X_grid, self.emphasizedSignal, color = 'red')
			# plt.plot(X_grid, regressor.predict(X_grid), color = 'blue')
			plt.title('Signal ')
			plt.xlabel('time')
			plt.ylabel('adc')
			plt.show()

		if spectrum == True:
			plt.subplot(312)
			filcoeff -= (np.mean(filcoeff,axis=0) + 1e-8)
			plt.imshow(filcoeff.T, cmap=plt.cm.jet, aspect='auto')
			#need to work in xticks but its cool to visualize it for now...
			# plt.xticks(np.arange(0, (filcoeff.T).shape[1], int((filcoeff.T).shape[1] / 4)),['0s', '0.5s', '1s', '1.5s','2.5s','3s','3.5'])
			# plt.xticks(np.arange(0, (filterBanks.T).shape[1], int((filterBanks.T).shape[1] / 4)),['0s', '0.5s', '1s', '1.5s','2.5s','3s','3.5'])
			ax = plt.gca()
			ax.invert_yaxis()
			plt.title('the spectrum image')
			plt.show()

		return filcoeff