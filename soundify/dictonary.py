import csv

import logging as log
from soundify.helper import Helper


class Dictonary():
    def __init__(self, config):
        self.config = config
        self.helper = Helper(self.config)
        self.dictFilePath = self.config.get('Dictonary', 'DICT_FILE_NAME')

    def loadDict(self):
        log.info('reading dict from csv ' + str(self.dictFilePath))
        with open(self.dictFilePath, 'rb') as f:
            reader = csv.reader(f)
            dict = list(reader)
        return dict[1:]

    def writeDict(self, inputSoundAsCharArrays, inputString):
        if len(inputSoundAsCharArrays) != len(inputString):
            log.error('number of detected chars need to be equal to number of input strings [' + str(len(inputSoundAsCharArrays)) + ', ' + str(len(inputString)) + ']')

        inputStringAsArray = list(inputString)
        with open(self.dictFilePath, 'wb') as f:
            log.info('writing dict to csv ' + str(self.dictFilePath))
            writer = csv.writer(f)
            writer.writerow(['CHAR', 'AVG', '#PEAKS', 'MIN PEAK', 'MAX PEAK', 'VECTOR'])
            for index, vector in enumerate(inputSoundAsCharArrays):
                char = inputStringAsArray[index]
                avg = sum(vector)/len(vector)
                peaks = self.helper.getPeaks(vector)
                numberOfPeaks = len(peaks)
                maxPeak=max(peaks)
                minPeak=min(peaks)
                row = [char, avg, numberOfPeaks, minPeak, maxPeak] + vector
                log.debug('writing row for char: ' + str(char) +
                          ',    avg: ' + str(avg) +
                          ',    #peaks: ' + str(numberOfPeaks) +
                          ',    min peak: ' + str(minPeak) +
                          ',    max peak: ' + str(maxPeak) +
                          ',    length: ' + str(len(vector)) +
                          ' to dict')
                writer.writerow(row)

    def getChars(self, dict):
        return zip(*dict)[0]

    def getAvgs(self, dict):
        avgs = zip(*dict)[1]
        return map(float, avgs)

    def getNumberOfPeaks(self, dict):
        numberOfPeaks = zip(*dict)[2]
        return map(int, numberOfPeaks)

    def getMinPeaks(self, dict):
        minPeaks = zip(*dict)[3]
        return map(float, minPeaks)

    def getMaxPeaks(self, dict):
        maxPeaks = zip(*dict)[4]
        return map(float, maxPeaks)

    def getRowAt(self, index, dict):
        return dict[index]

    def getCharAt(self, index, dict):
        return self.getChars(dict)[index]

    def getFloatArrays(self, dict):
        floatArrays = []
        for row in dict:
            floatArrays.append(map(float, row[5:]))
        return floatArrays




