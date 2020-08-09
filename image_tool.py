# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:07:49 2020

@author: jzb
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_img(path):
    return cv2.imread(path)

def get_point(img):
    img = get_img(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    corners = cv2.goodFeaturesToTrack(gray,100,0.01,10)#最鲁棒的角点检测方法
    #返回的结果是[[311,...250]] 两层括号的数组
    corners = np.int0(corners)
    out=[]
    for i in range(len(corners)):
        out.append([corners[i][0][1],corners[i][0][0]])
    out=sorted(out,key=lambda x:x[1])
    out_=[]
    while out!=[]:
        outtmp=[]
        if outtmp==[]:
            outtmp.append(out[0])
            out.pop(0)
        #print(out)
        if out==[]:
            out_.append(outtmp)
            break
        while out[0][1]==outtmp[-1][1]:
            #print(out[0][1])
            #print(out)
            outtmp.append(out[0])
            out.pop(0)
        out_.append(outtmp)
        
    return out_

def gen_key_time(points,alltime,chang,kuan):
    timeunit=alltime/kuan
    keyunit=88/chang
    out=[]
    for i in range(len(points)):
        for j in range(len(points[i])):
            freq=np.floor(points[i][j][0]*keyunit)
            if i!=len(points)-1:
                time=(points[i+1][0][1]-points[i][0][1])*timeunit
            else:
                time=(kuan-points[i][0][1])*timeunit
            out.append([freq,time])
    return out
        
c=get_point('timg.jpg')
key=gen_key_time(c,60,547,750)
