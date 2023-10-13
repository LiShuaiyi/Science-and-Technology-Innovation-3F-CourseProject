import numpy as np
import cv2
from func import *

def PI_control(base_speed, pos, d):
    height = 480
    width = 640+50
    kp = 1.5
    ki = 0.15
    # [pos1, pos2, pos4, pos3] = pos
    dp = 0
    a = 0
    di = 0
    for j in range(4):
        if pos[j]>10:
            a = a+1
            dp = dp+(pos[j]-width/2)
    if a>0:
        dp = dp/a
    else:
        dp = 0
    for i in range(len(d)-1):
        d[i] = d[i+1]
        di = di + d[i]
    d[len(d)-1] = dp
    di = di + dp
    control = (kp*dp + ki*di)*0.05
    left_speed = base_speed + control
    right_speed = base_speed - control

    return left_speed, right_speed

def go_straight(base_speed=30):
    x = base_speed
    y = base_speed
    return x, y

def turn_left(base_speed=40):
    x = base_speed
    y = base_speed*2
    return x, y

def turn_right(base_speed=40):
    x = base_speed*2
    y = base_speed
    return x, y

if __name__ == "__main__":
    pic = cv.imread('line4' +'.png')
    height = len(pic)
    width = len(pic[0])
    pic_cut = pic[int(height/3)*2:height,0:width]
    arr = pic_process(pic)
    [pos1, pos2, pos4, pos3] = position_extract(arr)
    print([pos1, pos2, pos4, pos3])
    pic_cut_with_point = show_point(pic_cut, pos1, pos2, pos4, pos3)
    delta = [10.0,20.5,15.2,3.7]
    [left_speed, right_speed] = PI_control(30, [pos1, pos2, pos4, pos3], delta)
    print([left_speed, right_speed])