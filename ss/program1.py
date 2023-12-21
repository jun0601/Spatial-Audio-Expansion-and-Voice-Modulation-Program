import os
import numpy as np
import tkinter
from tkinter import *
import tkinter.ttk  # 콤보박스 사용시 필요
import pygame
from tkinter import filedialog
from tkinter.messagebox import showinfo
import librosa
import soundfile as sf
import tkinter.font
from PIL import ImageTk, Image
import samplerate

# 전역 변수 선언
global speech_wav
global speech_impulse
global echo_np


# wave 파일 load하고 play
def play_echo_wav():
    pygame.mixer.music.load('./echo_1.wav')
    pygame.mixer.music.play(loops=0)


def play_pitch_wav():
    pygame.mixer.music.load('./pitch_1.wav')
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

    ##파일 선택시 경로 뜨는 메시지 박스
    message = tkinter.Message(window, text=filename, width=350, relief="solid")
    message.place(x=200, y=60)

    ##선택 파일 재생
    button_play = tkinter.Button(window, text='play', command=load_wav)
    button_play.place(x=540, y=60)

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
        initialdir='/',
        filetypes=filetypes)

    ##파일 선택시 경로 뜨는 메시지 박스
    message = tkinter.Message(window, text=filename, width=350, relief="solid")
    message.place(x=300, y=100)

    ##선택 파일 재생
    button_play = tkinter.Button(window, text='play', command=play_wav)
    button_play.place(x=540, y=100)

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )

    global speech_impulse
    speech_impulse, fs = librosa.load(filename, sr=16000)


# wave 파일이랑 impulse response 파일 convolution
def convolution():
    global echo_np
    try:
        echo_np = np.convolve(speech_wav, speech_impulse, "full")[:len(speech_wav)] * 30
        tkinter.messagebox.showinfo(title="generate echo wav", message="합성에 성공하였습니다")

    except:
        tkinter.messagebox.showinfo(title="generate echo wav", message="합성에 실패하였습니다\n파일을 선택했는지 확인해주세요")


# ser에 따른 에코 생성하는 함수
def generate_echo_wav():
    check = -1
    try:
        # Compute the power of speech and noise after removing DC bias.
        dc_speech = np.mean(speech_wav)
        dc_echo = np.mean(echo_np)
        pow_speech = np.mean(np.power(speech_wav - dc_speech, 2.0))
        pow_echo = np.mean(np.power(echo_np - dc_echo, 2.0))

        # Compute the scale factor of noise component depending on the target SER.
        alpha = np.sqrt(10.0 ** (float(10) / 10.0) * pow_speech / (pow_echo + 1e-6))
        echo_wav = (speech_wav + (alpha * echo_np))

        sf.write('./echo_1.wav', echo_wav, 16000)
        tkinter.messagebox.showinfo(title="generate echo wav", message="생성에 성공하였습니다")
    except:
        tkinter.messagebox.showinfo(title="generate echo wav", message="생성에 실패하였습니다\n파일을 선택했는지 확인해주세요")


def pitch_high():
    hi_pitch = samplerate.resample(speech_wav, 0.5, 'sinc_best')
    sf.write('./pitch_high_wav', hi_pitch, 16000)


def pitch_low():
    low_pitch = samplerate.resample(speech_wav, 1.5, 'sinc-best')
    sf.write('./pitch_low_wav', low_pitch, 16000)


# tkinter 정의
window = tkinter.Tk()
pygame.mixer.init()

# tkinter 기본 설정
window.title('Voice Modulation Program')
window.geometry('640x400')
window.resizable(False, False)

# 배경 설정
img = Image.open("./background.jpg")
img_resized = img.resize((640, 400))
bg = ImageTk.PhotoImage(img_resized)
bg_label = Label(window, image=bg)
bg_label.place(x=-2, y=-2, width=640, height=400)

##제목 라벨 설정
font = tkinter.font.Font(family="HY동녘B", size=10)
font2 = tkinter.font.Font(family="HY동녘B", size=20)
label_title = tkinter.Label(window, text="<Voice Modulation Program>", font=font2, width=25, height=2, fg="white",
                            bg="black")
label_title.pack()

# wave 파일 불러 오는 버튼
button_wave = tkinter.Button(window, text='select wave file', command=select_file_wave, font=font)
button_wave.place(x=100, y=60)
# button_wave.pack(expand=True)
# button_wave.grid(row=0, column=0)

# impulse response 파일 불러 오는 버튼
button_impulse = tkinter.Button(window, text='select impulse response wave file', command=select_file_impulse,
                                font=font)
button_impulse.place(x=100, y=100)
# button_impulse.pack(expand=True)
# button_impulse.grid(row=0, column=1)

##선택 리스트 박스 예제
# listbox1 = tkinter.Radiobutton(window, text="공간음향", font=font)
# listbox2 = tkinter.Radiobutton(window, text="목소리변조")
# listbox1.place(x=100, y=150)
# listbox2.place(x=200, y=150)

##메시지 박스 예제
# message=tkinter.Message(window, text="파일경로확인: ", relief="solid")
# message.place(x=100, y=130)

# ##콤보 박스
# value1 = ["노래방", "오페라홀", "동굴", "야외"]
# value2 = ["외계인", "헬륨가스", "남녀변환"]

# combobox1 = tkinter.ttk.Combobox(window, height=15, values=value1, font=font)
# combobox1.pack()
#
# combobox1.set("공간음향")
#
# combobox2 = tkinter.ttk.Combobox(window, height=15, values=value2, font=font)
# combobox2.pack()
#
# combobox2.set("목소리변조")
#
# combobox1.place(x=100, y=150)
# combobox2.place(x=370, y=150)

# convolution 버튼
button_conv = tkinter.Button(window, text='convolution', command=convolution, font=font)
button_conv.place(x=285, y=190)
# button_conv.pack(expand=True)
# button_conv.grid(row=1, column=0)

# echo generator 버튼
button_gene = tkinter.Button(window, text='generate echo wave',
                             font=font, command=generate_echo_wav)
button_gene.place(x=150, y=300)
# button_gene.pack(expand=True)
# button_gene.grid(row=1, column=1)

button_high = tkinter.Button(window, text='high_pitch',
                             font=font, command=pitch_high)
button_high.place(x=200, y=300)

button_low = tkinter.Button(window, text='low_pitch',
                            font=font, command=pitch_low)
button_low.place(x=400, y=300)

##프로그래스 바
progressbar = tkinter.ttk.Progressbar(window, maximum=100, mode="determinate")
progressbar.place(x=370, y=300)

progressbar.start(50)
progressbar.step(1)
# progressbar.stop()


# convolution play,stop,restrat,cancel
c_button_play = tkinter.Button(window, text="재생", font=font)
c_button_play.place(x=200, y=230)

s_button_play = tkinter.Button(window, text="중지", font=font)
s_button_play.place(x=270, y=230)

r_button_play = tkinter.Button(window, text="재개", font=font)
r_button_play.place(x=340, y=230)

ca_button_play = tkinter.Button(window, text="취소", font=font)
ca_button_play.place(x=410, y=230)

# 저장된 에코 입혀진 wave 파일 play 버튼
p_photo = Image.open("C:/Users/HYUNJI_16G/PycharmProjects/pythonProject5/play.jpg")
resized = p_photo.resize((30, 30), Image.ANTIALIAS)
play_photo = ImageTk.PhotoImage(resized)
button_play = tkinter.Button(window, image=play_photo, command=load_wav)
button_play.place(x=220, y=350)
s_photo = Image.open("C:/Users/HYUNJI_16G/PycharmProjects/pythonProject5/save.png")
s_resized = s_photo.resize((30, 30), Image.ANTIALIAS)
save_photo = ImageTk.PhotoImage(s_resized)
button_save = tkinter.Button(window, image=save_photo)  # , command=save_wav
button_save.place(x=305, y=350)
sh_photo = Image.open("C:/Users/HYUNJI_16G/PycharmProjects/pythonProject5/share.jpg")
sh_resized = sh_photo.resize((30, 30), Image.ANTIALIAS)
share_photo = ImageTk.PhotoImage(sh_resized)
button_share = tkinter.Button(window, image=share_photo)  # , command=share_wav
button_share.place(x=390, y=350)
# button_play.pack(expand=True)
# button_play.grid(row=2, column=0)


window.mainloop()
print(os.getcwd())
