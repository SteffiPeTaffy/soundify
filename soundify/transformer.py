import csv
import logging as log
import string

from soundify.helper import Helper
from soundify.soundRecorder import SoundRecorder
from soundify.relayBoard import RelayBoard


class Transformer:
    def __init__(self, config):
        self.config = config
        self.helper = Helper(self.config)
        self.dictFilePath = self.config.get('Dictonary', 'DICT_FILE_NAME')
        self.dictSoundFilePath = self.config.get('Dictonary', 'DICT_SOUND_FILE_PATH')

    def initDictonary(self):
        #allAsciiChars = string.printable
        allAsciiChars = "abcde"
        self.soundify(allAsciiChars, self.dictSoundFilePath)

        wasAsFloatArray = self.helper.wavToFloatArray(self.dictSoundFilePath)
        inputSignals = self.helper.getCharArrays(wasAsFloatArray)
        inputAsArray = list(allAsciiChars)
        with open(self.dictFilePath, 'wb') as f:
            writer = csv.writer(f)
            log.info('writing dict to csv ' + str(self.dictFilePath))
            for index, vector in enumerate(inputSignals):
                char = inputAsArray[index]
                row = [char] + vector
                log.debug('writing row for char ' + str(char) + ' with length ' + str(len(vector)) + ' to dict')
                writer.writerow(row)

    def textify(self, soundFilePath):
        # sound to float array
        wasAsFloatArray = self.helper.wavToFloatArray(soundFilePath)
        inputSignals = self.helper.getCharArrays(wasAsFloatArray)

        # load dict
        with open(self.dictFilePath, 'rb') as f:
            reader = csv.reader(f)
            dict = list(reader)
        log.info('loading dict from ' + str(self.dictFilePath) + ' with ' + str(len(dict)) + ' entries')

        # look up result from dict
        result = ""
        for inSignal in inputSignals:
            result += self.helper.getChar(inSignal, dict)
            log.info('result: [%s]' % result)
        return result

    def soundify(self, inputString, soundFilePath):
        # start the recording thread
        relayBoard = RelayBoard(self.config)
        relayBoard.init()

        threadConfig = {'exitFlag': False}
        soundRecorder = SoundRecorder(soundFilePath, threadConfig, self.config)
        soundRecorder.start()

        # send input to relay board
        relayBoard.writeInputString(inputString)

        # stop the recording thread
        threadConfig['exitFlag'] = True
        soundRecorder.join(10)
