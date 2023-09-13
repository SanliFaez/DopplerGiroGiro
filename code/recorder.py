"""
This code records the sound using the PC microphone and the PyAudio library.
Check the [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/) for the class properties and API.

"""
import matplotlib
matplotlib.use('TkAgg')
import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt


# ------------ Audio Setup ---------------
# constants
CHUNK = 4096  # 2^12, roughly 100 ms of recording at 48k sample rate
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 48000  # samples per second, this value works for Mac, but can be different for other PCs running on MS Windos or Linux.
# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
# AMPLITUDE_LIMIT = 4096

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

fig, (ax1) = plt.subplots(1, figsize=(15, 7))
lsam = 80 # number of buffer chunks to be recorded
x = np.arange(0, 2 * lsam * CHUNK, 2)  # samples (waveform), not sure why 2x is necessary

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_xlim(0, 2 * lsam * CHUNK)

data = stream.read(lsam * CHUNK, exception_on_overflow=False)
data_np = np.frombuffer(data, dtype='h')
plt.plot(x, data_np)
plt.show()

np.save("record.npy", data_np)
