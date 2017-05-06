import csv
import wave
import struct
import logging as log
from math import fabs


class Helper:
    def __init__(self, config):
        self.config = config
        self.rate = config.getint('Sound', 'RATE')

    def wavToFloatArray(self, soundFilePath):
        wafFile = wave.open(soundFilePath)
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

    def getCharArrays(self, signals):
        signalLength = len(signals)
        charCount = 1
        lengthOfOneChar = int(self.getLengthOfChar())
        startIndex = int(self.getStartIndexOfChar(charCount))
        endIndex = int(startIndex + lengthOfOneChar)
        dict = []
        while endIndex < signalLength:
            charVector = signals[startIndex:endIndex]
            dict.append(charVector)
            charCount += 1
            startIndex = int(self.getStartIndexOfChar(charCount))
            endIndex = int(startIndex + lengthOfOneChar)
        return dict[::2]

    def writeDictToFile(self, inputAsArray):
        inputSignals = self.getCharArrays()
        inputAsArray = list(inputAsArray)
        with open(self.config.get('Dictonary', 'DICT_FILE_NAME'), 'wb') as f:
            writer = csv.writer(f)
            for index, vector in enumerate(inputSignals):
                writer.writerow([inputAsArray[index], vector])

    def getDistance(self, inputVector, charVector):
        result = []
        for index, val in enumerate(inputVector):
            result.append(fabs(inputVector[index] - charVector[index]))
        return sum(result)

    def getChar(self, inputVector, dict):
        minDist=999999999999999
        bestFitChar = ''
        for dictEntry in dict:
            char = dictEntry[0]
            charVector = map(float, dictEntry[1][1:-1].split(','))
            distance = self.getDistance(inputVector, charVector)
            if distance < minDist:
                minDist = distance
                bestFitChar = char
        return bestFitChar

    def textify(self, inputSignals):
        csv.field_size_limit(self.config.getint('Dictonary', 'FIELD_SIZE_LIMIT'))
        with open(self.config.get('Dictonary', 'DICT_FILE_NAME'), 'rb') as f:
            reader = csv.reader(f)
            dict = list(reader)
        result = ""
        for inSignal in inputSignals:
            result += self.getChar(inSignal, dict)
        return result

    def slidingWindow(self, sequence, winSize, step=1):
        # Pre-compute number of chunks to emit
        numOfChunks = ((len(sequence) - winSize) / step) + 1

        # Do the work
        for i in range(0, numOfChunks * step, step):
            yield sequence[i:i + winSize]