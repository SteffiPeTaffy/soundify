import logging as log
from math import fabs

import sys

from soundify.helper import Helper
from soundify.dictonary import Dictonary


class Textifier():
    def __init__(self, config):
        self.config = config
        self.helper = Helper(self.config)
        self.rate = config.getint('Sound', 'RATE')
        self.beat = config.getfloat('Relay', 'BEAT')
        self.dictonary = Dictonary(self.config)
        self.dict = self.dictonary.loadDict()

    def getModifiedHammingtonDistance(self, inputAsFloatArray, charAsFloatArray):
        if len(inputAsFloatArray) != len(charAsFloatArray):
            log.warn('to calculate the modified hammington distance the input arrays need to have the same size')
        result = []
        for index, val in enumerate(inputAsFloatArray):
            result.append(fabs(inputAsFloatArray[index] - charAsFloatArray[index]))
        return sum(result)

    def getBestFit(self, a, list):
        minDistance = sys.maxsize
        bestFitChar = ''
        for index, value in enumerate(list):
            char = self.dictonary.getCharAt(index, self.dict)
            distance = self.helper.getDistance(a, value)
            log.debug('looking for best match: ' + str(char) + ' = ' + str(distance))
            if distance<minDistance:
                minDistance = distance
                bestFitChar = char
        if bestFitChar == '':
            log.warn('Could not find anything for value ' + str(a) + ' in list ' + str(list))
        return [bestFitChar, minDistance]

    def getCharBasedOnModifiedHammingtonDistance(self, inputVector):
        minDist = sys.maxsize
        bestFitChar = ''
        for dictEntry in self.dict:
            char = dictEntry[0]
            charVector = map(float, dictEntry[5:])
            distance = self.getModifiedHammingtonDistance(inputVector, charVector)
            log.debug('looking for best match: ' + str(char) + ' = ' + str(distance))
            if distance < minDist:
                minDist = distance
                bestFitChar = char
        log.info('best match based on distance of vectors: ' + str(bestFitChar) + ' = ' + str(minDist))
        return bestFitChar

    def getCharBasedOnNumberOfPeaks(self, inputVector):
        peakIndices = self.helper.getPeakIndices(inputVector)
        numberOfPeaksInput = len(peakIndices)
        numberOfPeaksFromDict = self.dictonary.getNumberOfPeaks(self.dict)
        bestFit = self.getBestFit(numberOfPeaksInput, numberOfPeaksFromDict)
        log.info('best match based on number of peaks: ' + str(bestFit[0]) + ' = ' + str(bestFit[1]))
        return bestFit[0]


    def getCharBasedOnLowestPeak(self, inputVector):
        peaks = self.helper.getPeaks(inputVector)
        lowestPeak = min(peaks)
        lowestPeaksFromDict = self.dictonary.getMinPeaks(self.dict)
        bestFit = self.getBestFit(lowestPeak, lowestPeaksFromDict)
        log.info('best match based on lowest peak: ' + str(bestFit[0]) + ' = ' + str(bestFit[1]))
        return bestFit[0]


    def getCharBasedOnHighestPeak(self, inputVector):
        peaks = self.helper.getPeaks(inputVector)
        maxPeak = max(peaks)
        maxPeaksFromDict = self.dictonary.getMaxPeaks(self.dict)
        bestFit = self.getBestFit(maxPeak, maxPeaksFromDict)
        log.info('best match based on highest peak: ' + str(bestFit[0]) + ' = ' + str(bestFit[1]))
        return bestFit[0]

    def mostCommon(self, list):
        return max(set(list), key=list.count)

    def getBestFitOverall(self, bestMatches):
        transposedList = self.helper.transposeLists(bestMatches)
        return map(self.mostCommon, transposedList)
