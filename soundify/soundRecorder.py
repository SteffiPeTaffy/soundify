import pyaudio
import wave
import threading

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
        format = self.config.get('Sound', 'FORMAT')
        channels = self.config.get('Sound', 'CHANNELS'),
        rate = self.config.get('Sound', 'RATE'),
        chunk = self.config.get('Sound', 'CHUNK')

        # start Recording
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
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(path, 'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()