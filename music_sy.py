# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:01:24 2020

@author: jzb
"""

import wave
 
import numpy as np
import math
import matplotlib.pyplot as plt

import pyaudio 


# TO DO: reform it into piano
#-----------------------------------------
#生成正弦波
def gen_sin(amp, f, fs, tau):
    #（开始值，结束值，个数）
    nT = np.linspace(0,tau, round(tau/(1.0/fs)))#根据步长生成数组，在指定的间隔内返回均匀间隔的数字，返回num个均匀分布的样本，在[start, stop]。
    signal =np.array([amp*np.cos(2*np.pi*f*t) for t in nT])
    return signal

def play(mudata,width,channels,rate,):
    # 用文本文件记录wave模块解码每一帧所产生的内容。注意这里不是保存为二进制文件
    #dump_buff_file=open(r"Ring01.dup", 'w')
    dump_buff_file=mudata
    chunk=1                                       # 指定WAV文件的大小
    wf=wave.open(r"Ring01.wav",'rb')              # 打开WAV文件
    p=pyaudio.PyAudio()                                   # 初始化PyAudio模块
    
    # 打开一个数据流对象，解码而成的帧将直接通过它播放出来，我们就能听到声音啦
    stream=p.open(format=p.get_format_from_width(width), channels=channels, rate=rate, output=True)
 
    data = wf.readframes(chunk)      # 读取第一帧数据
    print(data)                        # 以文本形式打印出第一帧数据，实际上是转义之后的十六进制字符串

    # 播放音频，并使用while循环继续读取并播放后面的帧数
    # 结束的标志为wave模块读到了空的帧
    while data != b'':   
        stream.write(data)                # 将帧写入数据流对象中，以此播放之
        data = wf.readframes(chunk)            # 继续读取后面的帧
        dump_buff_file.write(str(data) + "\n---------------------------------------\n")                    # 将读出的帧写入文件中，每一个帧用分割线隔开以便阅读
        
    stream.stop_stream()            # 停止数据流
    stream.close()                        # 关闭数据流
    p.terminate()                          # 关闭 PyAudio
    print('play函数结束！')
#model the harmonic feature in frequency domain
#1~15谐波与基频的比例关系
Amp=[1,0.340,0.102,0.085,0.070,0.065,0.028,0.085,0.011,0.030,0.010,0.014,0.012,0.013,0.004]
numharmonic=len(Amp)#谐波个数
 
wave_data=np.array([0 for i in range(0,40000)])
wave_data = np.reshape(wave_data,[40000,1]).T
pianomusic=[0 for x in range(0,len(wave_data[0]))]
startpoint=0
 
#model the piano note attenuation feature in the time domain
#对每个钢琴音的时域衰减建模
attenuation=[0 for x in range(0, 8000)]
#the attack stage
for i in range(0,200):
    attenuation[i]=i*0.005
#the attenuate stage
#衰减阶段
for i in range(200,800):
    attenuation[i]=1-(i-200)*0.001
#the maintain stage
#保持阶段    
for i in range(800,4000):
    attenuation[i]=0.4-(i-800)*0.000078
for i in range(4000,8000):
    attenuation[i]=0.15-(i-4000)*0.0000078
 
#compose each note in each time quantum
nomalizedbasicfreq=[261.63,261.63,261.63,261.63,293.665,293.665,293.665,293.665,329.628,329.628,329.628,329.628,349.228,349.228,349.228,349.228,391.995,391.995,391.995,391.995,440,440,440,440,493.883,493.883,493.883,493.883,523.251,523.251,523.251,523.251,587.33,587.33,587.33,587.33,659.255,659.255,659.255,659.255]
ampli=[(math.pow(2,2*8-1)-1) for i in range(0,40)]
#40个/4=10
notestime=[4,4,4,4,4,4,4,4,4,4]#10个
windowsize=1000
for w in range(0,len(notestime)):
    #计算音符时长
    #初始化音符为0
    pianonote = [0 for x in range(0, windowsize*notestime[w])] #get the length according to the time of the note
    #计算每一个谐音并累加
    for i in range(0, numharmonic): #get the note by add each harmonic by the amplitude comparatively with the basic frequency
        #产生谐波,参数：幅度，频率，8000 ，结束=0.5
        pianonote = pianonote + gen_sin(ampli[startpoint] /50* Amp[i], nomalizedbasicfreq[startpoint] * (i + 1), 8000, 0.125*notestime[w])
        #矢量加法
    #attenuate the note with the time domain feature
    #进行衰减
    for k in range(0,windowsize*notestime[w]):#k:0---4000
        pianomusic[startpoint*windowsize+k]=pianonote[k]*attenuation[k]
        #0--4000 startpoint=0
        #4000-8000   =4
        #8000-12000  =8
        #36*1000---36*1000+4000（40000）4万
    startpoint=startpoint+notestime[w] #record the start point of the next note
    #startpoint变化规律：0,4,8,12，...32，36
 
for i in range(0,len(wave_data[0])):
    wave_data[0][i]=pianomusic[i]
 
 
#get a wave file
f = wave.open(r"pianomusic.wav", "wb")
#get the channel, sampling width and sampling frequency information
#see details in 2.9 of my report
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(8000)
f.writeframes(wave_data[0].tostring()) #put the data into the wave file
f.close()


 
print("STEP 9: please see in figure and listen the pianomusic.wav file")
plt.figure()
plt.subplot(211)
plt.plot(Amp)
plt.title(r'frequency domain harmonic feature')
plt.subplot(212)
plt.plot(attenuation)
plt.title(r'time domain attenuation feature')
plt.figure()
plt.plot(pianomusic)
plt.title(r'STEP 9:reform it into piano')
plt.show()