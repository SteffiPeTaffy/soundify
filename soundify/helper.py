import random
import string
from math import fabs
import logging as log
import numpy as np
import peakutils


class Helper:
    def __init__(self, config):
        self.config = config
        self.peak_threshold_char_detection = self.config.getfloat('Textify', 'PEAK_THRESHOLD_CHAR_DETECTION')
        self.peak_distance_char_detection = self.config.getint('Textify', 'PEAK_DISTANCE_CHAR_DETECTION')
        self.peak_threshold_char_translation = self.config.getfloat('Textify', 'PEAK_THRESHOLD_CHAR_TRANSLATION')
        self.peak_distance_char_translation = self.config.getint('Textify', 'PEAK_DISTANCE_CHAR_TRANSLATION')

    def getPeakIndices(self, floatArray):
        cb = np.array(floatArray)
        return peakutils.indexes(cb, thres=self.peak_threshold_char_translation / max(cb), min_dist=self.peak_distance_char_translation)

    def getPeakIndicesForCharacterDetection(self, floatArray):
        cb = np.array(floatArray)
        indexes = peakutils.indexes(cb, thres=self.peak_threshold_char_detection / max(cb), min_dist=self.peak_distance_char_detection)
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
        return int(self.config.getint('Sound', 'RATE') * self.config.getfloat('Relay', 'BEAT'))

    def transposeLists(self, listOfLists):
        return map(list, zip(*listOfLists))

    def getRandomInputString(self):
        allAsciiChars = string.printable
        return ''.join(random.sample(allAsciiChars,len(allAsciiChars)))