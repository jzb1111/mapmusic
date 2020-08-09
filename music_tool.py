# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:58:25 2020

@author: jzb
"""

import xlrd
import numpy as np
import simpleaudio as sa

def read_piano_key(file_name):
    piano_key_lis=[]
    piano_freq_lis=[]

    data = xlrd.open_workbook(file_name)
    table = data.sheet_by_name('Sheet1')
    #name = table.name
    rowNum = table.nrows
    #colNum = table.ncols
    
    for i in range(rowNum):
        #print(i)
        key=table.cell(i,0).value
        freq=table.cell(i,1).value
        piano_key_lis.append(key)
        piano_freq_lis.append(freq)
    for i in range(rowNum):
        #print(i)
        key=table.cell(i,4).value
        freq=table.cell(i,5).value
        piano_key_lis.append(key)
        piano_freq_lis.append(freq)
    return piano_key_lis,piano_freq_lis

def make_freq_dict(keylis,freqlis):
    dic={}
    for i in range(len(keylis)):
        dic[keylis[i]]=freqlis[i]
    return dic

def gen_sound(freq,seconds):
    seconds=seconds
    fs = 44100  # 44100 samples per second
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * fs, False)    
    # Generate a 440 Hz sine wave
    note = np.sin(freq * t * 2 * np.pi)    
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

def play_sound(sound):
    fs = 44100  # 44100 samples per second
    play_obj = sa.play_buffer(sound, 1, 2, fs)    
    # Wait for playback to finish before exiting
    play_obj.wait_done()

piano_key_lis,piano_freq_lis=read_piano_key('piano_key.xlsx')

piano_dic=make_freq_dict(piano_key_lis,piano_freq_lis)

'''for i in list(piano_dic.keys()):
    print(i)
    test_sound=gen_sound(piano_dic[i],1)
    play_sound(test_sound)'''