import matplotlib.pyplot as plt
from soundify.transformer import Transformer


class Plotter():
    def __init__(self, config):
        self.config = config
        self.transformer = Transformer(self.config)

    def plotSoundVector(self, soundVector):
        plt.figure(1)
        plt.title('Soundify')
        plt.plot(soundVector, 'b')
        plt.show()

    def plotSound(self, soundFilePath):
        signal = self.transformer.soundToFloatArray(soundFilePath)
        self.plotSoundVector(signal)

    def plotCharsInSoundFile(self, soundFilePath):
        dictArray = self.transformer.soundToFloatArray(soundFilePath)
        charArrays = self.transformer.getCharsAsFloatArrays(dictArray)
        for charArry in charArrays:
            self.plotSoundVector(charArry)