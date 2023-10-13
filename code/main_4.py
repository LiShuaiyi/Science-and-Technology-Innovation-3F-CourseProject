# -*- coding: utf-8 -*-

from func import * 
from PI_2 import *
from recog_3 import *
from mlp_sign import *
from driver import driver
import numpy as np
import cv2

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
delta = [0,0,0,0,0]
car = driver()

vote_right=0
vote_left=0
i=1

#left=cv2.imread('left.png',cv2.IMREAD_GRAYSCALE)
#right=cv2.imread('right.png',cv2.IMREAD_GRAYSCALE)

#left_hash = calc_hash(left)
#right_hash = calc_hash(right)
    
while True:
    i+=1
    if i%2==0:
        _, frame1 = cap1.read()
        _, frame2 = cap2.read()
        
    if i%10==0:

        pic = frame2
        direction = 2.0

        mode=circle_search(pic)
        print("mode",mode)
        
        if mode==2:  #识别标识牌
            roi=cv2.imread('roi_new.png',0)
            roi = cv2.resize(roi, (20, 20))
            #gray=cv2.COLOR_BGR2GRAY(roi)
            model_name = "ckpt.yml"
            result = svm_sign(roi, model_name)
            if result==1:
                print('direction: right')
                direction=1.0
            elif result==0:
                print('direction: left')
                direction=0.0

        if mode==0:  #route
            direction = 2.0

        
        print("direction",direction)
        
        if direction==2.0: #route
            arr = pic_process(pic)
            [pos1, pos2, pos4, pos3] = position_extract(arr)
            print("pos: ", [pos1, pos2, pos4, pos3])
            #pic_cut_with_point = show_point(pic_cut, pos1, pos2, pos4, pos3)
            [left_speed, right_speed] = PI_control(40, [pos1, pos2, pos4, pos3], delta)
            car.set_speed(right_speed, left_speed)
            #print("speed: ", [left_speed, right_speed])
            
        if direction==0.0:
            vote_right=0
            vote_left=0
            for i in range(10):
                print('left!')
                car.set_speed(turn_left()[1], 0)
                time.sleep(0.1)
        
        if direction==1.0:
            vote_right=0
            vote_left=0
            for i in range(10):
                print('right!')
                car.set_speed(0, turn_right()[0])
                time.sleep(0.1)
                
        i=1
                
            
        
    
        

