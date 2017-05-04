import wave
import struct

class SoundTransformer:
    def __init__(self, config, filePath):
        self.config = config
        self.filePath = filePath

    # convert sound to vector
    def wavToFloatArray(self):
        wafFile = wave.open(self.filePath)
        astr = wafFile.readframes(wafFile.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (wafFile.getnframes() * wafFile.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        return a

    def filterCharacters(self, signals):
        pass

