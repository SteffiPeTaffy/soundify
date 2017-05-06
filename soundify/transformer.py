import csv
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
        allAsciiChars = "abcdefg"
        self.soundify(allAsciiChars, self.dictSoundFilePath)

        wasAsFloatArray = self.helper.wavToFloatArray(self.dictSoundFilePath)
        inputSignals = self.helper.getCharArrays(wasAsFloatArray)
        inputAsArray = list(allAsciiChars)
        with open(self.dictFilePath, 'wb') as f:
            writer = csv.writer(f)
            for index, vector in enumerate(inputSignals):
                writer.writerow([inputAsArray[index], vector])

    def textify(self, soundFilePath):
        wasAsFloatArray = self.helper.wavToFloatArray(soundFilePath)
        inputSignals = self.helper.getCharArrays(wasAsFloatArray)
        csv.field_size_limit(self.config.getint('Dictonary', 'FIELD_SIZE_LIMIT'))
        with open(self.dictFilePath, 'rb') as f:
            reader = csv.reader(f)
            dict = list(reader)
        result = ""
        for inSignal in inputSignals:
            result += self.helper.getChar(inSignal, dict)
        return result

    def soundify(self, inputString, soundFilePath):
        threadConfig = {'exitFlag': False}
        soundRecorder = SoundRecorder(soundFilePath, threadConfig, self.config)
        soundRecorder.start()

        # send input to relay board
        relayBoard = RelayBoard(self.config)
        relayBoard.writeInputString(inputString)

        # stop the recording thread
        threadConfig['exitFlag'] = True
        soundRecorder.join(10)