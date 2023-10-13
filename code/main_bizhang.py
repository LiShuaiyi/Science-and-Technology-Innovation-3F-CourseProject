# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:31:46 2020

@author: 10527
"""

import numpy as np
import cv2
import time
from func import * 
from PI import *
from driver import driver

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
delta = [0,0,0,0,0]
car = driver()
i=1
def direction(stddv_r,stddv_l):
    if stddv_r < stddv_l:
        print("Turn Left")
        return 0.0
    else:
        print("Turn Right")
        return 1.0



while True:
    i+=1
    if i%2==0:
        _, frame1 = cap1.read()
        _, frame2 = cap2.read()   
    if i%10==0:
        pic = frame2
        #cv2.imshow('roi',pic)
        gray=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
        #erode = cv2.erode(gray, None, iterations=2)
        circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=80,minRadius=30, maxRadius=100)
        if circles is not None:
            print("found the obstacle!")
            i+=1
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
            if dir==0:
                for i in range(10):
                    car.set_speed(turn_left()[1], 0)
                    time.sleep(0.1)
                #time.sleep(3)

            if dir==1:
                for i in range(10):
                    car.set_speed(0, turn_right()[0])
                    time.sleep(0.1)
                #time.sleep(3)
                    
        else:
            print("i will go along the road!")
            arr = pic_process(pic)
            [pos1, pos2, pos4, pos3] = position_extract(arr)
            #print("pos: ", [pos1, pos2, pos4, pos3])
            #pic_cut_with_point = show_point(pic_cut, pos1, pos2, pos4, pos3)
            [left_speed, right_speed] = PI_control(30, [pos1, pos2, pos4, pos3], delta)
            car.set_speed(right_speed, left_speed)
            print("speed: ", [left_speed, right_speed])
            #print(" ")
            
        i=1
        
        
    
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


