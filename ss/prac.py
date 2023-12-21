import numpy as np
import tkinter
import pygame
from tkinter import *
from tkinter import filedialog

window = Tk()
pygame.mixer.init()

window.title('Chan Jin Park')
window.geometry('640x400+100+100')
window.resizable(True, True)

count = 0
dir = 'C:\CJ\22-2\ss'


def load_wav():
    pygame.mixer.music.load(dir)
    pygame.mixer.music.play(loops=0)


def countUP():
    global count
    count += 1
    label.config(text=str(count))


label = tkinter.Label(window, text='0')
label.pack()

button1 = tkinter.Button(window, overrelief='solid', width=15, command=load_wav, repeatdelay=1000, repeatinterval=100)
button1.pack()

# label = tkinter.Label(window, text='안녕하세요')
# label.pack()

window.mainloop()
