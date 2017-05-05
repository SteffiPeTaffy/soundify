import serial
import time

class RelayBoard:
    def __init__(self, config):
        self.relayBoard = serial.Serial(port=config.get('Socket', 'TTY_PORT'),
                                        baudrate=config.get('Socket', 'BAUDRATE'),
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE)
        self.beat = config.getfloat('Relay', 'BEAT')

    def soundify(self, inputStr):
        self.relayBoard.__enter__()
        for c in inputStr:
            self.clear()
            self.writeDec(ord(c))
            print(c)
        time.sleep(self.beat)
        self.relayBoard.__exit__()

    def write(self, command, address, inputDec):
        time.sleep(self.beat)
        checksum = command ^ address ^ inputDec
        self.relayBoard.write(bytearray([command, address, inputDec, checksum]))
        self.relayBoard.flush()

    def clear(self):
        self.write(3, 0, 0)

    def writeDec(self, inputDec):
        self.write(3, 0, inputDec=inputDec)
