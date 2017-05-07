from math import fabs
import logging as log
import numpy as np
import peakutils


class Helper:
    def __init__(self, config):
        self.config = config

    def getPeakIndices(self, floatArray):
        cb = np.array(floatArray)
        return peakutils.indexes(cb, thres=0.1 / max(cb), min_dist=1)

    def getPeakIndicesForCharacterDetection(self, floatArray):
        cb = np.array(floatArray)
        indexes = peakutils.indexes(cb, thres=0.3 / max(cb), min_dist=4000)
        log.debug('Detected ' + str(len(indexes)) + ' peaks for character detection')
        return indexes

    def getPeaks(self, floatArray):
        indexes = self.getPeakIndices(floatArray)
        return map(lambda i: floatArray[i], indexes)

    def getAvg(self, floatArray):
        return sum(floatArray) / len(floatArray)

    def getDistance(self, a, b):
        return fabs(a-b)

    def calculateLengthOfOneBeat(self):
        return self.config.getint('Sound', 'RATE') * self.config.getfloat('Relay', 'BEAT')

    def transposeLists(self, listOfLists):
        return map(list, zip(*listOfLists))