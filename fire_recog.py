'''
Author       : Gehrychiang
LastEditTime : 2022-06-13 11:20:46
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import numpy as np
import cv2
from loguru import logger
import time
def contrast_brightness_demo(image, c, b):  #其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = np.zeros(image.shape, image.dtype)   #创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv2.addWeighted(image, c, blank, 1-c, b) #c为加权值，b为每个像素所加的像素值
    ret, dst = cv2.threshold(dst, 25, 255, cv2.THRESH_BINARY)#调整二值化阈值
    return dst
    
# 伽马校正
def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)
    
    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    
    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    
    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)






def predict_fire(fire_que,vid_que_for_fire):

    redThre = 135#红色阈值
    saturationTh = 45#饱和度阈值
    logger.debug('<检测> 开始检测火灾')
    while True:#循环读取摄像头的图像
        if not vid_que_for_fire.empty():#如果队列不为空，则读取队列中的图像
            frame = vid_que_for_fire.get()
            # cv2.imshow('frame', frame)#显示摄像头的图像
            B = frame[:, :, 0]#获取B通道
            G = frame[:, :, 1]#获取G通道
            R = frame[:, :, 2]#获取R通道
            minValue = np.array(np.where(R <= G, np.where(G <= B, R, np.where(R <= B, R, B)), np.where(G <= B, G, B)))#获取最小值
            S = 1 - 3.0 * minValue / (R + G + B + 1)#获取饱和度
            fireImg = np.array(np.where(R > redThre, np.where(R >= G, np.where(G >= B, np.where(S >= 0.2, np.where(S >= (255 - R)*saturationTh/redThre, 255, 0), 0), 0), 0), 0))#获取火焰图像
            gray_fireImg = np.zeros([fireImg.shape[0], fireImg.shape[1], 1], np.uint8)#创建灰度图像
            gray_fireImg[:, :, 0] = fireImg#将火焰图像赋值给灰度图像
            gray_fireImg = cv2.GaussianBlur(gray_fireImg, (7, 7), 0)#高斯滤波
            gray_fireImg = contrast_brightness_demo(gray_fireImg, 5.0, 25)#对比度和亮度调整
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))#获取结构元素
            gray_fireImg = cv2.morphologyEx(gray_fireImg, cv2.MORPH_CLOSE, kernel)#闭运算
            dst = cv2.bitwise_and(frame, frame, mask=gray_fireImg)#将火焰图像和摄像头图像进行位运算
            if (np.sum(dst)/np.sum(frame))>0:
                fire_que.put((True,dst))
            else:
                fire_que.put((False,dst))
            time.sleep(2)

            # cv2.imshow("gray_fireImg", gray_fireImg)#显示灰度图像
            # key=cv2.waitKey(1)
            # if key!=-1:
            #     break

if __name__ == "__main__":
    pass
