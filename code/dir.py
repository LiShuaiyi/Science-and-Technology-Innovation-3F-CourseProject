# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:31:46 2020

@author: 10527
"""

import numpy as np
import cv2

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

def direction(stddv_r,stddv_l):
    if stddv_r < stddv_l:
        print("Turn Left")
        return 0.0
    else:
        print("Turn Right")
        return 1.0
    
while True:
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()

    pic = frame2
    cv2.imshow('roi',pic)
    gray=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
    erode = cv2.erode(gray, None, iterations=2)
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=60,minRadius=30, maxRadius=100)
    if circles is not None:
        for circle in circles[0]:
            #圆的基本信息
            #坐标行列
            x=int(circle[0])
            y=int(circle[1])
            #半径
            r=int(circle[2])
        print(x,y,r)
        roi1 = gray[y-r:y+r,x+1*r:x+3*r]#右侧区域具体与r的倍数关系可能需要调整，这里是根据识别出红圈取得的值
        roi2 = gray[y-r:y+r,x-3*r:x-1*r]
        (mean1 , stddv1) = cv2.meanStdDev(roi1)#计算均值、方差
        (mean2 , stddv2) = cv2.meanStdDev(roi2)
        print(mean1 , stddv1)
        print(mean2 , stddv2)
        dir = direction(stddv1,stddv2)#返回方向判断，0左转，1右转
        #print(dir)
        cv2.imshow('roi.jpg',roi2)
    cv2.waitKey(3)
    
def mean():
    roi1 = gray[y-r:y+r,x+1*r:x+3*r]#右侧区域具体与r的倍数关系可能需要调整，这里是根据识别出红圈取得的值
    roi2 = gray[y-r:y+r,x-3*r:x-1*r]#左侧区域
    (mean1 , stddv1) = cv2.meanStdDev(roi1)#计算均值、方差
    (mean2 , stddv2) = cv2.meanStdDev(roi2)
    print(mean1 , stddv1)
    print(mean2 , stddv2)
    direction = direction(stddv1,stddv2)#返回方向判断，0左转，1右转
    #print(dir)
    cv2.imshow('roi.jpg',roi2)
    cv2.waitKey(0)    #测试用
    return direction

