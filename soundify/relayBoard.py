import serial
import time
import logging as log

class RelayBoard:
    def __init__(self, config):
        self.relayBoard = serial.Serial(port=config.get('Socket', 'TTY_PORT'),
                                        baudrate=config.get('Socket', 'BAUDRATE'),
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE)
        self.beat = config.getfloat('Relay', 'BEAT')

    def writeInputString(self, inputStr):
        self.relayBoard.__enter__()
        for c in inputStr:
            self.clear()
            self.writeChar(c)
        time.sleep(self.beat)
        self.relayBoard.__exit__()

    def write(self, command, address, inputDec):
        time.sleep(self.beat)
        checksum = command ^ address ^ inputDec
        log.debug('Writing to relay board: ' + str(command) + ' ' + str(address) + ' ' + str(inputDec) + ' ' + str(checksum))
        self.relayBoard.write(bytearray([command, address, inputDec, checksum]))
        self.relayBoard.flush()

    def clear(self):
        log.info('Clear relay board')
        self.write(3, 0, 0)

    def init(self):
        log.info('Init relay board')
        self.write(3, 0, 255)

    def writeChar(self, char):
        log.info('Writing char to relay board: ' + str(char))
        self.write(3, 0, ord(char))
