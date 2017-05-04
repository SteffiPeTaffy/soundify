import argparse
import ConfigParser
from soundify.relayBoard import RelayBoard

parser = argparse.ArgumentParser(description='Soundify stuff')
parser.add_argument('inputStr', metavar='inputStr', type=str, help='string you want to soundify')

def main():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    args = parser.parse_args()
    relayBoard = RelayBoard(config=config)
    relayBoard.soundify(args.inputStr)

if __name__ == "__main__":
    main()
