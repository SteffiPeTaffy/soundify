import pyaudio
import wave
import threading
import logging as log

import time


class SoundRecorder(threading.Thread):
    def __init__(self, path, threadConfig, config):
        threading.Thread.__init__(self)
        self.path = path
        self.threadConfig = threadConfig
        self.config = config

    def run(self):
        self.record(path=self.path)

    def record(self, path):
        audio = pyaudio.PyAudio()
        format = pyaudio.paInt16
        channels = self.config.getint('Sound', 'CHANNELS')
        rate = self.config.getint('Sound', 'RATE')
        chunk = self.config.getint('Sound', 'CHUNK')

        # start Recording
        log.debug('Start recording')
        stream = audio.open(format=format,
                            channels=channels,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk)
        frames = []

        while not self.threadConfig['exitFlag']:
            data = stream.read(chunk)
            frames.append(data)

        # stop Recording
        log.debug('Stop recording')
        stream.stop_stream()
        stream.close()
        audio.terminate()

        log.debug('Write audio to wav file: ' + str(path))
        waveFile = wave.open(path, 'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
