import argparse
import ConfigParser
import logging as log
from soundify.helper import Helper
from soundify.transformer import Transformer
from soundify.plotter import Plotter

parser = argparse.ArgumentParser(description='Soundify')
parser.add_argument('command', metavar='Command', type=str, help='[init|soundify|textify]')
parser.add_argument('--verbose', '-v', action='count', help='Increase output verbosity',  default=0)
parser.add_argument('--dst', metavar='OutputFile', type=str, help='File to store the result of the command')
parser.add_argument('--src', metavar='InputFile', type=str, help='Source file to execute the command')

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


if __name__ == "__main__":
    main()
