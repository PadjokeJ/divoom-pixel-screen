import pyaudio
import numpy as np
from PIL import Image
from time import sleep

p = pyaudio.PyAudio()
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 4000

stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output= False,
            input_device_index= 1,
            frames_per_buffer = CHUNK)

def update_line():
    try:
        data = np.fft.rfft(np.fromstring(
            stream.read(CHUNK), dtype=np.float32)
        )
    except IOError:
        pass
    #data = np.log10(np.sqrt(
    #    np.real(data)**2+np.imag(data)**2) / CHUNK) * 10
    data = np.real(data)
    return data

img = Image.new('RGBA', (16, 16), (0, 0, 0, 255))

def plot_visualizer():
    data = update_line()
    

    
    
    pixels = img.load()

    for x in range(16):
        for y in range(16):
            pixels[x, y] = (pixels[x, y][0] // 2,
                            pixels[x, y][1],
                            pixels[x, y][0] // 4,
                            pixels[x, y][3])


    chunk_width =  20 #int(1001 / 16.0)
    for i in range(16):
        h = 0
        chunk_width = int(2 ** (i / 3))
        chunk_start = i * chunk_width
        for j in range(chunk_width):
            dat = (data[j + chunk_start + 100])
            if dat >= 0.02:
                h += dat
        for y in range(int(h / chunk_width * 8 * i )):
            pixels[i, max(min(15 - y, 15), 0)] = (255, 0, 0, 255)
    
    return img

if __name__ == "__main__":
    while True:
        plot_visualizer()
        sleep(0.1)