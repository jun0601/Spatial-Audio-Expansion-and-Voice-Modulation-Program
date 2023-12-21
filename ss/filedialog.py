import numpy as np
import tkinter
import pygame
from tkinter import filedialog
from tkinter.messagebox import showinfo
import librosa
import soundfile as sf

global speech_wav
global speech_impulse
global echo_np


def load_wav():
     pygame.mixer.music.load('./echo_1.wav')
     pygame.mixer.music.play(loops=0)

# def countUP():
#     global count
#     count += 1
#     label.config(text=str(count))

def select_file_wave():
    filetypes = (
        ('wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    global speech_wav
    speech_wav, fs = librosa.load(filename, sr=16000)


def select_file_impulse():
    filetypes = (
        ('wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    global speech_impulse
    speech_impulse, fs = librosa.load(filename, sr=16000)


def convolution():
    global echo_np
    echo_np = np.convolve(speech_wav, speech_impulse, "full")[:len(speech_wav)] * 30


def generate_echo_wav():
    # Compute the power of speech and noise after removing DC bias.
    dc_speech = np.mean(speech_wav)
    dc_echo = np.mean(echo_np)
    pow_speech = np.mean(np.power(speech_wav - dc_speech, 2.0))
    pow_echo = np.mean(np.power(echo_np - dc_echo, 2.0))

    # Compute the scale factor of noise component depending on the target SER.
    alpha = np.sqrt(10.0 ** (float(10) / 10.0) * pow_speech / (pow_echo + 1e-6))
    echo_wav = (speech_wav + (alpha * echo_np))

    sf.write('./echo_1.wav', echo_wav, 16000)

    #
    # path_speech = filedialog.askopenfilename(filetypes=[('Wave File', '.wav')])
    # speech, fs = librosa.load(path_speech, sr=16000)
    #
    # path_IR = filedialog.askopenfilename(filetypes=[('Wave File', '.wav')])
    # IR, fs = librosa.load(path_IR, sr=16000)
    #
    # echo_np = np.convolve(speech, IR, "full")[:len(speech)] * 30
    # wav_echo_0 = generate_echo_wav(speech, echo_np, -20)

    # sf.write('./echo.wav', wav_echo_0, fs)

    # label = tkinter.Label(window, text='0')
    # label.pack()


window = tkinter.Tk()
pygame.mixer.init()

window.title('Voice Modulation Program')
window.geometry('640x400')
window.resizable(False, False)

button_wave = tkinter.Button(window, text='select wave file', command=select_file_wave)
button_wave.place(x=100, y=100)
button_wave.pack(expand=True)

button_impulse = tkinter.Button(window, text='select impulse response wave file', command=select_file_impulse)
button_impulse.place(x=200, y=100)
button_impulse.pack(expand=True)

button_conv = tkinter.Button(window, text='convolution', command=convolution)
button_conv.place(x=150, y=200)
button_conv.pack(expand=True)

button_gene = tkinter.Button(window, text='generate echo wave',
                             command=generate_echo_wav)
button_gene.place(x=150, y=300)
button_gene.pack(expand=True)

button_play = tkinter.Button(window, text='play', command=load_wav)
button_play.place(x=150, y=400)
button_play.pack(expand=True)

window.mainloop()

# wav_echo_0 = generate_echo_wav(speech_wav, echo_np, -20)

# button_impulse = tkinter.Button(window, text='select impulse response file', command=select_file)
# # IR, fs = librosa.load(path[1], sr=16000)
# button_impulse.pack(expand=True)
# button1 = tkinter.Button(window, overrelief='solid', width=15, command=load_wav('./echo.wav'), repeatdelay=1000,
#                          repeatinterval=100)
# button1.pack()

# label = tkinter.Label(window, text='안녕하세요')
# label.pack()

window.mainloop()
