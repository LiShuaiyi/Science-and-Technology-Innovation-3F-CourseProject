# -*- coding: utf-8 -*-

from func import * 
from PI_2 import *
from recog_3 import *


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
        
    if i%6==0:

        pic = frame2
        direction = 2.0

        mode=circle_search(pic)
        print("mode",mode)
        
        if mode==2:  #识别标识牌
            roi=cv2.imread('roi_new.png',0)
            #roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            #cv2.equalizeHist(roi, roi)
            
            erode1 = cv2.erode(roi, None, iterations=1)
            dilate1= cv2.dilate(erode1,None,iterations=1)
            
            ret, binary = cv2.threshold(dilate1,150,255,cv2.THRESH_BINARY)
            binary = np.clip(binary, 0, 255)
            binary = np.array(binary, np.uint8)
            cv2.imwrite('binary.jpg',binary)
            binary , contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
            print(len(contours))
            if len(contours)==3:
                vote_right+=1
            if len(contours)==2:
                vote_left+=1
            
            if vote_left==2:
                direction=0.0   #turn left
            elif vote_right==2:
                direction=1.0   #turn right
            else:
                direction=2.0   #go straight
                

        if mode==0:  #route
            direction = 2.0

        
        print("direction",direction)
        
        if direction==2.0: #route
            arr = pic_process(pic)
            [pos1, pos2, pos4, pos3] = position_extract(arr)
            print("pos: ", [pos1, pos2, pos4, pos3])
            #pic_cut_with_point = show_point(pic_cut, pos1, pos2, pos4, pos3)
            [left_speed, right_speed] = PI_control(45, [pos1, pos2, pos4, pos3], delta)
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
                
            
        
    
        

