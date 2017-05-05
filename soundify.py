import argparse
import ConfigParser
import string

from soundify.relayBoard import RelayBoard
from soundify.soundRecorder import SoundRecorder
from soundify.soundTransformer import SoundTransformer

parser = argparse.ArgumentParser(description='Soundify stuff')
parser.add_argument('command', metavar='Command', type=str, help='[init|soundify|textify]')
parser.add_argument('--dst', metavar='OutputFile', type=str, help='File to store the result of the command')
parser.add_argument('--src', metavar='InputFile', type=str, help='If ommited input is read from STDIN')

def record(inputString, soundFilePath, config):
    threadConfig = {'exitFlag': False}
    soundRecorder = SoundRecorder(path=soundFilePath, threadConfig=threadConfig, config=config)
    soundRecorder.start()

    # send input to relay board
    relayBoard = RelayBoard(config=config)
    relayBoard.soundify(inputStr=inputString)

    # stop the recording thread
    threadConfig['exitFlag'] = True
    soundRecorder.join(10)


def main():
    # config for opening serial connection
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    # parse command line input
    inputArgs = parser.parse_args()

    if (inputArgs.command == "init"):
        #Record all ascii chars
        soundFilePath = "ascii.wav"
        #allAsciiChars = string.printable
        allAsciiChars = "abcdefghijklmnopqrstuvwxyz"
        record(allAsciiChars, soundFilePath=soundFilePath, config=config)

        # build dict
        soundTransformer = SoundTransformer(config=config, soundFilePath=soundFilePath)
        soundTransformer.writeDictToFile(allAsciiChars)
        print('Number of Characters detected: ' + str(len(soundTransformer.getCharArrays())))

    if (inputArgs.command == "soundify"):
        soundFilePath = inputArgs.dst
        inputString = open(inputArgs.src).read()
        record(inputString=inputString, soundFilePath=soundFilePath, config=config)

    if (inputArgs.command == "textify"):
        soundFilePath = inputArgs.src
        soundTransformer = SoundTransformer(config=config, soundFilePath=soundFilePath)
        inputSignals = soundTransformer.getCharArrays()
        print('Number of Characters detected: ' + str(len(inputSignals)))

        text = soundTransformer.textify(inputSignals)
        print('[%s]' % text)

if __name__ == "__main__":
    main()
