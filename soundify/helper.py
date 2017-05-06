import csv
import wave
import struct
import logging as log
from math import fabs

class Helper:
    def __init__(self, config):
        self.config = config
        self.rate = config.getint('Sound', 'RATE')
        self.beat = config.getfloat('Relay', 'BEAT')

    def wavToFloatArray(self, soundFilePath):
        wafFile = wave.open(soundFilePath)
        astr = wafFile.readframes(wafFile.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (wafFile.getnframes() * wafFile.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        return a

    def getLengthOfOneBeat(self):
        return self.config.getint('Sound', 'RATE') * self.config.getfloat('Relay', 'BEAT')

    def getInitialStartIndex(self, signals):
        trimStart = int(0.05 * self.rate)
        trimEnd = int(2 * self.beat * self.rate)
        trimmedSignal = signals[trimStart:trimEnd]
        for index, entry in enumerate(trimmedSignal):
            if fabs(entry) > 0.1:
                return index-200+trimStart

    def getStartIndexOfChar(self, index, delayAtStart):
        beat = self.config.getfloat('Relay', 'BEAT')
        frameRate = self.config.getint('Sound', 'RATE')
        log.debug('start index ' + str(index) + ': ' + str(delayAtStart + (beat * index)))
        return delayAtStart + (beat * index * frameRate)

    def getCharArrays(self, signals):
        signalLength = len(signals)
        charCount = 0
        lengthOfOneBeat = int(self.getLengthOfOneBeat())
        startIndex = int(self.getInitialStartIndex(signals))
        delayAtStart = startIndex/float(self.rate)
        log.debug('delay at start: ' + str(delayAtStart))
        endIndex = int(startIndex + lengthOfOneBeat)
        dict = []
        while endIndex <= signalLength:
            charVector = signals[startIndex:endIndex]
            dict.append(charVector)
            charCount += 1
            startIndex = int(self.getStartIndexOfChar(charCount, delayAtStart))
            endIndex = int(startIndex + lengthOfOneBeat)
        return dict[1::2]

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
            charVector = map(float, dictEntry[1:])
            distance = self.getDistance(inputVector, charVector)
            log.debug('looking for best match: ' + str(char) + ' = ' + str(distance))
            if distance < minDist:
                minDist = distance
                bestFitChar = char
        log.debug('best match: ' + str(bestFitChar) + ' = ' + str(minDist))
        return bestFitChar