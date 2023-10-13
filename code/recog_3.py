# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np


def calc_hash(img):
    result = ''
    for i in range(30):
        for j in range(30):
            if img[i,j] > 100:#二值化阈值120
                result += '1'
            else:
                result += '0'
    return result #输出为900个0/1字符串

def comp_hash(hash1, hash2):
    s = 0
    for i in range(900):
        if hash1[i] == hash2[i]: #比较哈希序列的相似度
            s += 1
    return s

def img_process(pic,left_hash,right_hash):
    mid = err = num = radius = direction = 0
    center = [0,0]
    
    mid = err = num = black = 0
    i = 1
    img = pic #ret值为True或False，代表有没有读到图像
# 1,9,10,15,16,17,24,25
    ret=True
    if ret == True:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #灰度图像
        #img = cv2.flip(img,-1) #翻转图像;0沿x轴翻转;>0沿y轴翻转;<0x,y轴同时翻转。
        cv2.equalizeHist(img, img)
        cv2.imshow("origin",img)

        # sign detecting
        cir_det = img
        circles = cv2.HoughCircles(cir_det, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=60, minRadius=30, maxRadius=60)
                  
        if circles is not None:
            circles1 = circles[0,:,:] 
            circles1 = np.uint16(np.around(circles1))   
            num = len(circles)
            center = [circles[0,0][0],circles[0,0][1]]
            radius = circles[0,0][2]
        else:
            num = 0
            center = [0,0]
            radius = 0
    
        ret,img = cv2.threshold(img,100,255,0) #二值化,0黑1白    

        if num :#num不为0时
            #画出找到的圆
            for i in circles1[:]: 
                #坐标行列
                x=int(i[0])
                y=int(i[1])
                #半径
                r=int(i[2])
                #在原图用指定颜色标记出圆的位置
                
                roi = img[y-r:y+r,x-r:x+r]
                img2=img
                cv2.circle(img2,(x,y),r,(255,0,0),2) 
            print("center",x,y) 
            print("radius",r)
            cv2.imshow("img2",img2)
            cv2.imshow("roi",roi)
            #cv2.waitKey(0)

            if int(center[1]-0.7*radius) > 0 and int(center[1]+0.7*radius) < 480 and int(center[0]-0.7*radius) > 0 and int(center[0]+0.7*radius) < 640:
                #直方图均衡
                #cv2.equalizeHist(roi, roi)
                ret,roi = cv2.threshold(roi,90,255,0) #二值化,0黑1白
                cv2.imwrite("roi.png",roi)
                #sign=roi
                sign = cv2.resize(roi,(30,30))#将比较区域调整为30*30正方形
                cv2.imshow('sign',sign)
                #sign recognition
                sign_hash = calc_hash(sign)
                cmpr_l = comp_hash(sign_hash, left_hash)
                cmpr_r = comp_hash(sign_hash, right_hash)
                print("left:",cmpr_l,"  right:",cmpr_r)
                #哪张图片hash比较值越大，就与哪张图片越相似
                if (cmpr_l - cmpr_r > 10):
                    print('left sign detected!')
                    direction = 0.0
                elif (cmpr_r - cmpr_l > 10):
                    print('right sign detected!')
                    direction = 1.0
                else:
                    print('go straight!')
                    direction = 2.0

    return direction  


def circle_search(pic):
    mid = err = num = radius = direction = 0
    center = [0,0]
    
    mid = err = num = black = 0
    i = 1
    img = pic 

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #灰度图像
    cv2.equalizeHist(img, img)
    cv2.imshow("origin",img)

    # sign detecting
    cir_det = img
    circles = cv2.HoughCircles(cir_det, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=60, minRadius=30, maxRadius=60)
                
    if circles is not None:
        circles1 = circles[0,:,:] 
        circles1 = np.uint16(np.around(circles1))   
        num = len(circles)
        center = [circles[0,0][0],circles[0,0][1]]
        radius = circles[0,0][2]
        
    else:
        num = 0
        center = [0,0]
        radius = 0  

    if num :#num不为0时
        #画出找到的圆
        for i in circles1[:]: 
            #坐标行列
            x=int(i[0])
            y=int(i[1])
            #半径
            r=int(i[2])
            #在原图用指定颜色标记出圆的位置
            roi = img[y-r:y+r,x-r:x+r]
            rr=int(r*0.65)
            roi_new=pic[y-rr:y+rr,x-rr:x+rr]
            cv2.imwrite('roi_new.png',roi_new)

        print("center",x,y) 
        print("radius",r)
        
        return 2
       
    return 0

def obstacle_research(pic):#输出0左转，1右转，2没有搜索到同心圆
    pass


def main1():
    left=cv2.imread('left_3.png',cv2.IMREAD_GRAYSCALE)
    right=cv2.imread('right_3.png',cv2.IMREAD_GRAYSCALE)
    
    print('have read the sign!')
    left_hash = calc_hash(left)
    right_hash = calc_hash(right)
   
    pic=cv2.imread('roi.png')
    img_process(pic,left_hash,right_hash)
    return

def main2():
    left=cv2.imread('left_2.png',cv2.IMREAD_GRAYSCALE)
    right=cv2.imread('right_2.png',cv2.IMREAD_GRAYSCALE)
    
    print('have read the sign!')
    left_hash = calc_hash(left)
    right_hash = calc_hash(right)
   
    roi=cv2.imread('roi.png')
    ret,sign = cv2.threshold(roi,90,255,0) #二值化,0黑1白
    #sign=roi
    #sign = cv2.resize(roi,(30,30))#将比较区域调整为30*30正方形
    cv2.imshow('sign',sign)
    #sign recognition
    sign_hash = calc_hash(sign)
    cmpr_l = comp_hash(sign_hash, left_hash)
    cmpr_r = comp_hash(sign_hash, right_hash)
    print("left:",cmpr_l,"  right:",cmpr_r)
    #哪张图片hash比较值越大，就与哪张图片越相似
    if (cmpr_l - cmpr_r > 30):
        print('left sign detected!')
        direction = 1
    elif (cmpr_r - cmpr_l >30):
        print('right sign detected!')
        direction = -1
    else:
        print('go straight!')
        direction = 0
    
    print("direction",direction)
    return

if __name__ == "__main__":
    main2()




