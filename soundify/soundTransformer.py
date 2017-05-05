import csv
import string
import wave
import struct

class SoundTransformer:
    def __init__(self, config, soundFilePath):
        self.config = config
        self.soundFilePath = soundFilePath
        self.rate = config.getint('Sound', 'RATE')

    # convert sound to vector
    def wavToFloatArray(self):
        wafFile = wave.open(self.soundFilePath)
        astr = wafFile.readframes(wafFile.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (wafFile.getnframes() * wafFile.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        return a

    def getLengthOfChar(self):
        return self.config.getint('Sound', 'RATE') * self.config.getfloat('Relay', 'BEAT')

    def getStartIndexOfChar(self, index):
        delayAtStart = self.config.getfloat('Relay', 'BEAT') - 0.05
        beat = self.config.getfloat('Relay', 'BEAT')
        frameRate = self.config.getint('Sound', 'RATE')
        return delayAtStart + (beat * index * frameRate)

    def getCharArrays(self):
        signals = self.wavToFloatArray()
        signalLength = len(signals)
        charCount = 1
        startIndex = int(self.getStartIndexOfChar(charCount))
        lengthOfOneChar = int(self.getLengthOfChar())
        endIndex = int(startIndex + lengthOfOneChar) if int(
            startIndex + lengthOfOneChar) < signalLength else signalLength - 1
        dict = []
        while startIndex < signalLength:
            dict.append(signals[startIndex:endIndex])
            charCount += 1
            startIndex = int(self.getStartIndexOfChar(charCount))
            endIndex = int(startIndex + lengthOfOneChar) if int(startIndex + lengthOfOneChar) >= signalLength else signalLength - 1
        return dict[::2]

    def writeDictToFile(self, inputString):
        allSciiSignals = self.getCharArrays()
        with open('soundifyDict.csv', 'wb') as f:
            w = csv.writer(f)
            w.writerow(list(inputString))
            w.writerow(allSciiSignals)

    def __str__(self):
        return "\n".join(self.wavToFloatArray())