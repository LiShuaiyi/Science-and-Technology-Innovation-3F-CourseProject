# -*- coding:utf-8 -*-

import cv2 as cv
import numpy as np
import random
# import matplotlib as plt

def normalization(data):
    #归一化
    # _range = np.max(data) - np.min(data)
    # return (data - np.min(data)) / _range
    data = data.astype(np.float32)
    data -= np.mean(data)
    return data / np.std(data)

def label_extract(filename):
    #从filename的txt里提取[[pic_name, label_number],[],...]
    data_label = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        # print(lines)
    for line in lines:
        # print(line)
        n = line.split(' ')[0].replace('\\', '/')
        l = int(line.split(' ')[1].replace('\n', ''))
        data_label.append([n,l])
    return data_label

def data_preprocess(data_label):
    #预处理 取圆的内接正方形 得到data和label列表
    # left = 0 right = 1
    data = []
    label = []
    for i in range(len(data_label)):
        pic = cv.imread(data_label[i][0], 0)
        pic_cut = pic[5:25,5:25]
        pic_cut = normalization(pic_cut)
        dat = pic_cut.flatten().tolist()
        lab = data_label[i][1]
        data.append(dat)
        if lab == 0:
            label.append([1, 0])
        else:
            label.append([0, 1])
    return data, label

def train_svm(data, label, model_name):
    model = cv.ml.ANN_MLP_create()#建立模型
    #设置激活函数为SIGMOID，其实就这一个可以选
    model.setLayerSizes(np.array([400,100,16,2], dtype=np.float32))
    model.setActivationFunction(cv.ml.ANN_MLP_SIGMOID_SYM)
    #设置终止条件
    model.setTermCriteria((cv.TERM_CRITERIA_COUNT | cv.TERM_CRITERIA_EPS, 10000, 0.01))
    model.setTrainMethod(cv.ml.ANN_MLP_BACKPROP)#设置训练方式为反向传播
    model.setBackpropWeightScale(0.001)  #设置反向传播中的一些参数
    model.setBackpropMomentumScale(0.0) #设置反向传播中的一些参数

    # model = cv.ml.ANN_MLP_load(model_name)
    # model.setTermCriteria((cv.TERM_CRITERIA_COUNT | cv.TERM_CRITERIA_EPS, 10000, 0.0001))
    model.train(data, cv.ml.ROW_SAMPLE, label)
    model.save(model_name)

def load_and_predict(name, data):
    #预测
    model = cv.ml.ANN_MLP_load(name)
    result = model.predict(data)
    return result

def svm_sign(pic, model_name):
    '''
    pic size should be 30*30
    '''
    #封装好的svm 训练好之后实际使用的函数
    # pic_cut = pic[5:25,5:25]
    pic_cut = normalization(pic)
    data = [pic_cut.flatten().tolist()]
    result = load_and_predict(model_name, np.array(data, dtype = np.float32))
    print(result)
    return np.argmax(result[1][0])

if __name__ == "__main__":
    # data_label = label_extract("label/label.txt")
    # random.shuffle(data_label)
    # train_data_label = data_label[:300]
    # vali_data_label = data_label[300:]
    # train_data, train_label = data_preprocess(train_data_label)
    # vali_data, vali_label = data_preprocess(vali_data_label)
    # # print(len(train_label))
    # # print(len(train-data))
    # model_name = "ckpt.yml"
    # train_svm(np.array(train_data, dtype=np.float32),
              # np.array(train_label, dtype=np.float32), model_name)
    # _,result = load_and_predict(model_name, np.array(vali_data, dtype=np.float32))
    # print(result)
    # print(vali_label)

    pic = cv.imread("roi_new.png", 0)
    model_name = "ckpt.yml"
    result = svm_sign(pic, model_name)
    print(result)

