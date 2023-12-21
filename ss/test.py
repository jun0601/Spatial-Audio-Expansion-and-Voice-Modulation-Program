import numpy as np
import tkinter
import pygame
from tkinter import filedialog
from tkinter.messagebox import showinfo
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import samplerate

# 전역 변수 선언
global speech_wav
global speech_impulse
global echo_np
# global image_path


# wave 파일 load하고 play
def load_wav():
    pygame.mixer.music.load('./result.wav')
    pygame.mixer.music.play(loops=0)


# wave 파일 불러오기
def select_file_wave():
    filetypes = (
        ('wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='C:\CJ\22-2\ss',
        filetypes=filetypes)

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )
    global speech_wav
    speech_wav, fs = librosa.load(filename, sr=16000)


# impulse response 파일 불러 오기
def select_file_impulse():
    filetypes = (
        ('wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='C:\CJ\22-2\ss',
        filetypes=filetypes)

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )
    global speech_impulse
    speech_impulse, fs = librosa.load(filename, sr=16000)


# wave 파일이랑 impulse response 파일 convolution
def convolution():
    global echo_np
    # global image_path
    echo_np = np.convolve(speech_wav, speech_impulse, "full")[:len(speech_wav)] * 30
    plt.figure(figsize=(12,3))
    # path = './image_path.jpg'
    librosa.display.waveshow(echo_np, 16000)
    # plt.savefig(path)


# ser에 따른 에코 생성하는 함수
def generate_echo_wav():
    # Compute the power of speech and noise after removing DC bias.
    dc_speech = np.mean(speech_wav)
    dc_echo = np.mean(echo_np)
    pow_speech = np.mean(np.power(speech_wav - dc_speech, 2.0))
    pow_echo = np.mean(np.power(echo_np - dc_echo, 2.0))

    # Compute the scale factor of noise component depending on the target SER.
    alpha = np.sqrt(10.0 ** (float(10) / 10.0) * pow_speech / (pow_echo + 1e-6))
    echo_wav = (speech_wav + (alpha * echo_np))

    sf.write('./result.wav', echo_wav, 16000)


# tkinter 정의
window = tkinter.Tk()
pygame.mixer.init()

# tkinter 기본 설정
window.title('Voice Modulation Program')
window.geometry('640x400')
window.resizable(False, False)

# wave 파일 불러 오는 버튼
button_wave = tkinter.Button(window, text='select wave file', command=select_file_wave)
button_wave.place(x=100, y=100)
# button_wave.pack(expand=True)
# button_wave.grid(row=0, column=0)

# impulse response 파일 불러 오는 버튼
button_impulse = tkinter.Button(window, text='select impulse response wave file', command=select_file_impulse)
button_impulse.place(x=200, y=100)
# button_impulse.pack(expand=True)
# button_impulse.grid(row=0, column=1)

# convolution 버튼
button_conv = tkinter.Button(window, text='convolution', command=convolution)
button_conv.place(x=150, y=200)

# photo = tkinter.PhotoImage(file='./sample_image.png')
#pLabel = tkinter.Label(window, image=photo)
# pLabel.place(x=150, y=250)
# button_conv.pack(expand=True)
# button_conv.grid(row=1, column=0)

# echo generator 버튼
button_gene = tkinter.Button(window, text='generate echo wave',
                             command=generate_echo_wav)
button_gene.place(x=300, y=200)
# button_gene.pack(expand=True)
# button_gene.grid(row=1, column=1)

# 저장된 에코 입혀진 wave 파일 play 버튼
button_play = tkinter.Button(window, text='play', command=load_wav)
button_play.place(x=200, y=300)
# button_play.pack(expand=True)
# button_play.grid(row=2, column=0)

window.mainloop()
