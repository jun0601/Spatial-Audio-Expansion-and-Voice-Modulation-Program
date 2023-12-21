import os
import numpy as np
import tkinter
from tkinter import *
import tkinter.ttk
import pygame
from tkinter import filedialog
import librosa
import soundfile as sf
import tkinter.font
from PIL import ImageTk, Image
import samplerate

global speech, impulse_response, result, echo_np


# play result
def play_result():
    pygame.mixer.music.load('./result.wav')
    pygame.mixer.music.play(loops=0)


# download result
def download_result():
    global result
    sf.write('./result.wav', result, 16000)


# pause result
def pause_result():
    pygame.mixer.music.load('./result.wav')
    pygame.mixer.music.pause()


# speech wave select
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
    message = tkinter.Message(window, text=filename, width=350, relief="solid")
    message.place(x=250, y=100)
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

    ##파일 선택시 경로 뜨는 메시지 박스
    message2 = tkinter.Message(window, text=filename, width=350, relief="solid")
    message2.place(x=250, y=150)

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )
    global speech_impulse
    speech_impulse, fs = librosa.load(filename, sr=16000)


# wave 파일이랑 impulse response 파일 convolution
def convolution():
    global echo_np
    echo_np = np.convolve(speech_wav, speech_impulse, "full")[:len(speech_wav)] * 30


# ser에 따른 에코 생성하는 함수
def generate_echo_wav():
    # Compute the power of speech and noise after removing DC bias.
    dc_speech = np.mean(speech_wav)
    dc_echo = np.mean(echo_np)
    pow_speech = np.mean(np.power(speech_wav - dc_speech, 2.0))
    pow_echo = np.mean(np.power(echo_np - dc_echo, 2.0))

    # Compute the scale factor of noise component depending on the target SER.
    alpha = np.sqrt(10.0 ** (float(5) / 10.0) * pow_speech / (pow_echo + 1e-6))
    echo_wav = (speech_wav + (alpha * echo_np))

    sf.write('./result.wav', echo_wav, 16000)


# high pitch resampling
def pitch_high():
    global result
    result = samplerate.resample(speech_wav, 0.5, 'sinc_best')
    sf.write('./result.wav', result, 16000)


# low pitch resampling
def pitch_low():
    global result
    result = samplerate.resample(speech_wav, 1.5, 'sinc_best')
    sf.write('./result.wav', result, 16000)


# tkinter 정의
window = tkinter.Tk()
pygame.mixer.init()

window.title('Voice Modulation Program')
window.geometry('640x400')
window.resizable(False, False)

# 배경 설정
img = Image.open("./background.jpg")
img_resized = img.resize((640, 400))
bg = ImageTk.PhotoImage(img_resized)
bg_label = Label(window, image=bg)
bg_label.place(x=-2, y=-2, width=640, height=400)

# 제목 라벨 설정
font = tkinter.font.Font(family="HY동녘B", size=10)
font2 = tkinter.font.Font(family="HY동녘B", size=20)
label_title = tkinter.Label(window, text="<Voice Modulation Program>", font=font2, width=25, height=2, fg="white",
                            bg="black")
label_title.place(x=125, y=0)

# music wave gif 출력
# img_wave = Image.open('./music.png')
# img_wave_resized = img_wave.resize((200, 50))
# music_wave = ImageTk.PhotoImage(img_wave_resized)
# music_label = Label(image=music_wave)
# music_label.place(x=250, y=50, width=100, height=50)

# wave 파일 불러 오는 버튼
button_wave = tkinter.Button(window, text='Select Wave File', command=select_file_wave, font=font)
button_wave.place(x=100, y=100)

# 공간 음향 라벨
# ir_title = tkinter.Label(window, text='[Spatial Acoustics]', font=font2, fg='white', bg='black')
# ir_title.place(x=100, y=150, width=10, height=2)
# ir_title.pack()

# impulse response 파일 불러 오는 버튼
button_impulse = tkinter.Button(window, text='Select IR File', command=select_file_impulse,
                                font=font)
button_impulse.place(x=100, y=150)

# convolution 파일 불러 오는 버튼
button_conv = tkinter.Button(window, text='CONV', command=convolution,
                             font=font)
button_conv.place(x=200, y=200)

# 공간 음향 생성 함수
button_gene = tkinter.Button(window, text='Generate Sound', command=generate_echo_wav,
                             font=font)
button_gene.place(x=300, y=200)

# 목소리 변조 라벨
# ir_title = tkinter.Label(window, text='Pitch Conversion', font=font2, fg='white', bg='black')
# ir_title.place(x=100, y=250, width=10, height=2)

# low pitch 생성 버튼
button_low = tkinter.Button(window, text='Low Pitch', command=pitch_low,
                            font=font)
button_low.place(x=200, y=250)

# high pitch 생성 버튼
button_high = tkinter.Button(window, text='High Pitch', command=pitch_high,
                             font=font)
button_high.place(x=300, y=250)

# play 버튼
p_photo = Image.open("./play.jpg")
resized = p_photo.resize((30, 30), Image.ANTIALIAS)
play_photo = ImageTk.PhotoImage(resized)
button_play = tkinter.Button(window, image=play_photo, command=play_result)
button_play.place(x=250, y=300)

# pause 버튼
p_photo2 = Image.open("./pause.png")
resized2 = p_photo2.resize((30, 30), Image.ANTIALIAS)
play_photo2 = ImageTk.PhotoImage(resized2)
button_pause = tkinter.Button(window, image=play_photo2, command=pause_result)
button_pause.place(x=350, y=300)

window.mainloop()
# print(os.getcwd())
