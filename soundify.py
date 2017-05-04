import argparse
import ConfigParser
from soundify.relayBoard import RelayBoard
from soundify.soundRecorder import SoundRecorder
from soundify.soundTransformer import SoundTransformer

parser = argparse.ArgumentParser(description='Soundify stuff')
parser.add_argument('inputStr', metavar='inputStr', type=str, help='string you want to soundify')


def main():
    # config for opening serial connection
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    # parse command line input
    args = parser.parse_args()

    # start the recording thread
    threadConfig = {'exitFlag': False}
    soundFilePath = 'relay.wav'
    soundRecorder = SoundRecorder(path=soundFilePath, threadConfig=threadConfig, config=config)
    soundRecorder.start()

    # send input to relay board
    relayBoard = RelayBoard(config=config)
    relayBoard.soundify(args.inputStr)

    # stop the recording thread
    threadConfig['exitFlag'] = True
    soundRecorder.join(10)

    soundTransformer = SoundTransformer(config=config, filePath=soundFilePath)
    signal = soundTransformer.wavToFloatArray()
    print "read " + str(len(signal)) + " frames"

if __name__ == "__main__":
    main()
