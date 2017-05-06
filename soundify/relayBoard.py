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
            log.info('Writing char to relay board: ' + str(c))
            self.clear()
            self.writeDec(ord(c))
        time.sleep(self.beat)
        self.relayBoard.__exit__()

    def write(self, command, address, inputDec):
        time.sleep(self.beat)
        checksum = command ^ address ^ inputDec
        self.relayBoard.write(bytearray([command, address, inputDec, checksum]))
        log.debug('Writing to relay board: ' + str(command) + ' ' + str(address) + ' ' + str(inputDec) + ' ' + str(checksum))
        self.relayBoard.flush()

    def clear(self):
        self.write(3, 0, 0)

    def writeDec(self, inputDec):
        self.write(3, 0, inputDec=inputDec)
