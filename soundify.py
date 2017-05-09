import argparse
import ConfigParser
import logging as log
from soundify.plotter import Plotter
from soundify.textifier import Textifier
from soundify.transformer import Transformer
from soundify.predictifier import Predictifier

parser = argparse.ArgumentParser(description='Soundify')
parser.add_argument('command', metavar='Command', type=str, help='[init|soundify|textify|textifyML|testdata]')
parser.add_argument('--verbose', '-v', action='count', help='Increase output verbosity',  default=0)
parser.add_argument('--dst', metavar='OutputFile', type=str, help='File to store the result of the command')
parser.add_argument('--src', metavar='InputFile', type=str, help='Source file to execute the command')
parser.add_argument('--rep', metavar='Repetitions', type=int, help='Number of repetitions',  default=1)

def main():
    # config for opening serial connection
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    # parse command line input
    inputArgs = parser.parse_args()

    #configure logging
    levels = [log.WARNING, log.INFO, log.DEBUG]
    level = levels[min(len(levels) - 1, inputArgs.verbose)]
    log.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

    #transformer
    transformer = Transformer(config)

    if (inputArgs.command == "init"):
        transformer.initDictonary()

    if (inputArgs.command == "soundify"):
        soundFilePath = inputArgs.dst
        inputString = open(inputArgs.src).read()
        transformer.soundify(inputString, soundFilePath)

    if (inputArgs.command == "textify"):
        soundFilePath = inputArgs.src
        text = transformer.textify(soundFilePath)
        print(text)

    if(inputArgs.command == "plot"):
        soundFilePath = inputArgs.src
        plotter = Plotter(config)
        plotter.plotSound(soundFilePath)
        plotter.plotCharsInSoundFile(soundFilePath)

    if(inputArgs.command == 'testdata'):
        count = int(inputArgs.rep)
        transformer.generateTestData(count)

    if(inputArgs.command == 'textifyML'):
        soundFilePath = inputArgs.src

        # sound to float array
        soundAsFloatArray = transformer.soundToFloatArray(soundFilePath)
        soundAsCharArrays = transformer.getCharsAsFloatArrays(soundAsFloatArray)

        predictifier = Predictifier(config).predict(soundAsCharArrays)
        predictifier.predict(soundAsCharArrays)




if __name__ == "__main__":
    main()
