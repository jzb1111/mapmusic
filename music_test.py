# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:45:53 2020

@author: jzb
"""

from image_tool import get_img,get_point,gen_key_time
from music_tool import read_piano_key,make_freq_dict,gen_sound,play_sound

piano_key_lis,piano_freq_lis=read_piano_key('piano_key.xlsx')

piano_dic=make_freq_dict(piano_key_lis,piano_freq_lis)

diclis=list(piano_dic.keys())

c=get_point('timg.jpg')
key=gen_key_time(c,60,547,750)

for i in key:
    freq=i[0]
    time=i[1]
    print(freq,time)
    
    test_sound=gen_sound(piano_dic[list(piano_dic.keys())[int(freq)]],time)
    play_sound(test_sound)