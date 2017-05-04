import serial
import time


class RelayBoard:
    def __init__(self, config):
        self.relayBoard = serial.Serial(port=config.get('Socket', 'TTY_PORT'),
                                        baudrate=config.get('Socket', 'BAUDRATE'),
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE)

    def soundify(self, inputStr):
        self.relayBoard.__enter__()
        for c in inputStr:
            self.clear()
            self.writeDec(ord(c))
            print(c)
        self.relayBoard.__exit__()

    def write(self, command, address, inputDec):
        time.sleep(0.2)
        checksum = command ^ address ^ inputDec
        self.relayBoard.write(bytearray([command, address, inputDec, checksum]))

    def clear(self):
        self.write(3, 0, 0)

    def writeDec(self, inputDec):
        command = 3
        address = 0
        self.write(command, address, inputDec=inputDec)
