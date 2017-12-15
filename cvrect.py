# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:47:57 2016

@author: Administrator
"""
import matplotlib.pyplot as plt
from skimage import color,morphology,io
import cv2
import numpy as np

img=io.imread('d:/cover/5.jpg')
im = cv2.imread('d:/cover/5.jpg')
img=color.rgb2gray(img)
#imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
bw=(img<0.35)*1
#ret,bw=cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
chull = morphology.convex_hull_image(bw) #获得轮廓的最大凸包图形，二值
c=np.uint8(chull)
#ret,c=cv2.threshold(c,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#canny = cv2.Canny(c, 50, 150)  
ch=c.copy();
#ch=np.uint8(ch)
image, contours, hierarchy = cv2.findContours(ch,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt = contours[0] #取点
rect = cv2.minAreaRect(cnt) # rect = ((center_x,center_y),(width,height),angle)最小面积
points = cv2.boxPoints(rect) # Find four vertices of rectangle from above rect
#im=np.uint8(img*255)   #skimage默认读取的值在0-1，polyline需要在uint8,int32上画图
cv2.polylines(im,np.int32([points]),False,(255,0,0),4)# draw rectangle in blue color 浮点数改整数

#x,y,w,h = cv2.boundingRect(contours) #正接矩形
#bw = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

plt.imshow(im,plt.cm.gray)
plt.xticks([]),plt.yticks([])
print(rect[2]) #倾斜角度