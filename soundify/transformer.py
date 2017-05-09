import csv
import string
import struct
import time
import logging as log
import uuid
import wave
from math import fabs
from soundify.helper import Helper
from soundify.soundRecorder import SoundRecorder
from soundify.relayBoard import RelayBoard
from soundify.dictonary import Dictonary
from soundify.textifier import Textifier


class Transformer:
    def __init__(self, config):
        self.config = config
        self.helper = Helper(self.config)
        self.dictFilePath = self.config.get('Dictonary', 'DICT_FILE_NAME')
        self.dictSoundFilePath = self.config.get('Dictonary', 'DICT_SOUND_FILE_PATH')

    def initDictonary(self):
        #allAsciiChars = string.printable
        allAsciiChars = "abcdef"
        self.soundify(allAsciiChars, self.dictSoundFilePath)

        soundAsFloatArray = self.soundToFloatArray(self.dictSoundFilePath)
        soundAsCharArrays = self.getCharsAsFloatArrays(soundAsFloatArray)

        dictonary = Dictonary(self.config, self.dictFilePath)
        dictonary.writeDict(soundAsCharArrays, allAsciiChars)


    def textify(self, soundFilePath):
        textifier = Textifier(self.config)

        # sound to float array
        soundAsFloatArray = self.soundToFloatArray(soundFilePath)
        soundAsCharArrays = self.getCharsAsFloatArrays(soundAsFloatArray)

        # load dict
        with open(self.dictFilePath, 'rb') as f:
            reader = csv.reader(f)
            dict = list(reader)
        log.info('loading dict from ' + str(self.dictFilePath) + ' with ' + str(len(dict)) + ' entries')

        # look up result from dict
        resultModifiedHammingtonDistance = []
        resultNumberOfPeaks = []
        resultLowestOfPeaks = []
        resultHighestfPeaks = []
        resultOverAll = []
        for charAsFloatArray in soundAsCharArrays:
            resultModifiedHammingtonDistance.append(textifier.getCharBasedOnModifiedHammingtonDistance(charAsFloatArray))
            resultNumberOfPeaks.append(textifier.getCharBasedOnNumberOfPeaks(charAsFloatArray))
            resultLowestOfPeaks.append(textifier.getCharBasedOnLowestPeak(charAsFloatArray))
            resultHighestfPeaks.append(textifier.getCharBasedOnHighestPeak(charAsFloatArray))
            resultOverAll = textifier.getBestFitOverall([resultModifiedHammingtonDistance, resultNumberOfPeaks, resultLowestOfPeaks, resultHighestfPeaks])
            log.info('result modified hammington distance:  %s' % resultModifiedHammingtonDistance)
            log.info('result #peaks:                        %s' % resultNumberOfPeaks)
            log.info('result lowest peak:                   %s' % resultLowestOfPeaks)
            log.info('result highest peak:                  %s' % resultHighestfPeaks)
            log.info('result overall:                       %s' % resultOverAll)
        return ''.join(resultOverAll)

    def soundify(self, inputString, soundFilePath):
        # start the recording thread
        relayBoard = RelayBoard(self.config)
        relayBoard.init()
        time.sleep(0.5)

        threadConfig = {'exitFlag': False}
        soundRecorder = SoundRecorder(soundFilePath, threadConfig, self.config)
        soundRecorder.start()

        # send input to relay board
        relayBoard.writeInputString(inputString)

        # stop the recording thread
        threadConfig['exitFlag'] = True
        soundRecorder.join(10)

    def generateTestData(self, count):
        for _ in range(count):
            randomInput = self.helper.getRandomInputString()
            filePath = 'testdata/input-' + str(uuid.uuid4())

            soundFilePath = filePath + '.wav'
            self.soundify(randomInput, soundFilePath)

            soundAsFloatArray = self.soundToFloatArray(soundFilePath)
            soundAsCharArrays = self.getCharsAsFloatArrays(soundAsFloatArray)

            dictFilePath = filePath + '.csv'
            dictonary = Dictonary(self.config, dictFilePath)
            dictonary.writeDict(soundAsCharArrays, randomInput)

    def soundToFloatArray(self, soundFilePath):
        wavFile = wave.open(soundFilePath)
        astr = wavFile.readframes(wavFile.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (wavFile.getnframes() * wavFile.getnchannels()), astr)
        a = [float(fabs(val)) / pow(2, 15) for val in a]
        return a

    def getCharsAsFloatArrays(self, inputSoundAsFloatArray):
        reversedInputSoundAsFloatArray = inputSoundAsFloatArray[::-1]
        peakIndices = self.helper.getPeakIndicesForCharacterDetection(reversedInputSoundAsFloatArray)
        shift = self.helper.calculateLengthOfOneBeat() / 2

        charArraysWithClearingSound = []
        for peakIndex in peakIndices:
            startIndex = int(peakIndex - shift)
            endIndex = int(peakIndex + shift)
            reversedCharVector = self.getCharArrayWithHighestPeakCentered(peakIndex, reversedInputSoundAsFloatArray)
            log.debug('vector [' + str(startIndex) + ', ' + str(endIndex) + ']')
            charArraysWithClearingSound.append(reversedCharVector[::-1])
        charArrays = charArraysWithClearingSound[::2][::-1]
        if len(charArraysWithClearingSound) % 2:
            return charArrays[1:]
        else:
            return charArrays

    def getCharArrayWithHighestPeakCentered(self, charPeak, soundAsFloatArray):
        shift = self.helper.calculateLengthOfOneBeat() / 2
        candidate = soundAsFloatArray[charPeak - shift:charPeak + shift]
        peakIndices = self.helper.getPeakIndices(candidate)
        highestPeakValue = 0
        highestPeakIndex = -1
        for index in peakIndices:
            currentPeak = candidate[index]
            if currentPeak > highestPeakValue:
                highestPeakValue = currentPeak
                highestPeakIndex = index

        offset = highestPeakIndex - int(len(candidate)/2)
        highestPeakIndexForSoundAsFloatArray = charPeak - offset
        return soundAsFloatArray[highestPeakIndexForSoundAsFloatArray-(shift+1500):highestPeakIndexForSoundAsFloatArray+(shift-1500)]


