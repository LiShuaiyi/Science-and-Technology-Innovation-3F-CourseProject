# -*- coding: utf-8 -*-

import cv2 as cv
import os
import numpy as np

def pic_process(pic):
    #裁剪图片的下1/3
    height = len(pic)
    width = len(pic[0])
    pic1 = pic[int(height/3)*2:height,0:width]
    #图片转换为灰度图
    gray = cv.cvtColor(pic1,cv.COLOR_RGB2GRAY)
    #高斯自定义5*5的卷积核
    kernel = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],dtype = np.uint8)/25
    # 提取灰度图中0-70像素值的像素
    mask = cv.inRange(gray,0,70) 
    #膨胀
    erosion = cv.erode(mask,kernel,iterations = 1) 
    #腐蚀
    dilation = cv.dilate(erosion,kernel,iterations = 1) 
    #开运算，先腐蚀再膨胀。
    opening = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel) 
    #闭运算，先膨胀再腐蚀。
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel) 
    #直方图均衡
    cv.equalizeHist(closing, closing)
    #此时的图片里只有255和0, 把255->1
    array = closing/255
    return array

def position_extract(array):
    (row, col) = array.shape
    #取1（纵向位置为从上到下10个像素） 2（纵向中间） 3（纵向下10） 4（纵向下40）个点 
    # RANGE_X为第x个点的定位所用到的二值图横向切片的像素厚度
    RANGE_1 = 20
    RANGE_2 = 40
    RANGE_3 = 40
    RANGE_4 = 70
    #N为滤波系数 小于像素厚度/N的像素会被过滤掉
    N = 2.5
    #点1滤波
    array1 = array[10-int(RANGE_1/2):10+int(RANGE_1/2),:]
    array1[:,:110] = 0
    array1[:,col-110:] = 0
    array1 = np.sum(array1,axis=0)
    array1[array1 <= RANGE_1/N] = 0
    #点2滤波
    array2 = array[int(row/2-RANGE_2/2):int(row/2+RANGE_2/2),:]
    array2[:,:110] = 0
    array2[:,col-110:] = 0
    array2 = np.sum(array2,axis=0)
    array2[array2 <= RANGE_2/N] = 0
    #点4滤波
    array4 = array[row-40-int(RANGE_4/2):row-40+int(RANGE_4/2),:]
    array4[:,:120] = 0
    array4[:,col-120:] = 0
    array4 = np.sum(array4,axis=0)
    array4[array4 <= RANGE_4/N] = 0
    #点3滤波
    array3 = array[row-10-int(RANGE_3/2):row-10+int(RANGE_3/2),:]
    array3[:,:150] = 0
    array3[:,col-150:] = 0
    array3 = np.sum(array3,axis=0)
    array3[array3 <= RANGE_3/N] = 0
    #获取点1-4的横向位置
    pos1 = pos2 = pos4 = pos3 = 0
    if np.sum(np.sum(array1,axis=0)) > 20:
        pos1 = np.mean(np.nonzero(array1))
    if np.sum(np.sum(array2,axis=0)) > 20:
        pos2 = np.mean(np.nonzero(array2))
    if np.sum(array4) > 20:
        pos4 = np.mean(np.nonzero(array4))
    if np.sum(array3) > 20:
        pos3 = np.mean(np.nonzero(array3))

    return [pos1, pos2, pos4, pos3]

def show_point(pic1 , pos1, pos2, pos4, pos3):
    arr = np.array(pic1[:,:,0])
    (row, col) = arr.shape
    cv.circle(pic1, (int(pos1), 5), 2, (0,255,0), 4)
    cv.circle(pic1, (int(pos2), int(row/2)), 2, (0,255,0), 4)
    cv.circle(pic1, (int(pos4), row-40), 2, (0,255,0), 4)
    cv.circle(pic1, (int(pos3), row-10), 2, (0,255,0), 4)
    #cv.imshow('cut pic with points',pic1)
    #cv.waitKey(0)
    return pic1

if __name__ == "__main__":
    for i in range(31):
        pic = cv.imread('line'+ str(i+1) +'.png')
        height = len(pic)
        width = len(pic[0])
        pic_cut = pic[int(height/3)*2:height,0:width]
        arr = pic_process(pic)
        [pos1, pos2, pos4, pos3] = position_extract(arr)
        pic_cut_with_point = show_point(pic_cut, pos1, pos2, pos4, pos3)
        cv.imwrite('pic with point'+ str(i+1) +'.png', pic_cut_with_point)
        


