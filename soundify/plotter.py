import matplotlib.pyplot as plt
import numpy as np
import wave
from soundify.helper import Helper


class Plotter():
    def __init__(self, config):
        self.config = config
        self.helper = Helper(self.config)

    def plotSoundVector(self, soundVector):
        plt.figure(1)
        plt.title('Soundify')
        plt.plot(soundVector, 'b')
        plt.show()

    def plotSound(self, soundFilePath):
        signal = self.helper.wavToFloatArray(soundFilePath)
        self.plotSoundVector(signal)

    def plotCharsInSoundFile(self, soundFilePath):
        dictArray = self.helper.wavToFloatArray(soundFilePath)
        charArrays = self.helper.getCharArrays(dictArray)
        for charArry in charArrays:
            self.plotSoundVector(charArry)