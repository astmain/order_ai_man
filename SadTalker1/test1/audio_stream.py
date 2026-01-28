import sounddevice as sd
import numpy as np
import wavio
import tempfile
from threading import Thread
import queue

class AudioStreamer:
    def __init__(self, sample_rate=16000, channels=1, chunk_duration=0.5):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = int(sample_rate * chunk_duration)
        self.q = queue.Queue()
        self.stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype="int16", callback=self._callback)

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def start(self):
        self.stream.start()
        return self

    def get_chunk(self):
        return self.q.get()

    def stop(self):
        self.stream.stop()

# 实时写入临时WAV
def stream_to_temp_wav(streamer, temp_file):
    with open(temp_file, 'wb') as f:
        wavio.write(f, np.array([]), streamer.sample_rate, sampwidth=2)
        while True:
            chunk = streamer.get_chunk()
            wavio.write(f, chunk, streamer.sample_rate, sampwidth=2)