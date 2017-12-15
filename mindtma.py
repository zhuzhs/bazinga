# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 12:12:08 2017

@author: zhuzhs
"""
import time,cv2,numpy
from skimage import io,filters
from scipy import ndimage as ndi
from skimage.morphology import medial_axis
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


globals()['tt'] = time.clock()
plt.cla()
plt.close('all')

img=cv2.imread('d:/jiao/j2.png') #opencv
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#img = io.imread('d:/jiao/j2.png',as_grey=True) #skimage

#img=255-img  #invert
img=~img

img = filters.gaussian(img,sigma=1.1)    #[0,1]，模糊之后成为整体，消除杂散线段，不然会影响求中轴和距离
img=(img*255).astype("uint8")
#ret,dst=cv2.threshold(img,128,255,cv2.THRESH_BINARY) #method1
dst=((img >128) * 255).astype("uint8") #method2

#width,height=dst.shape
skel, distance = medial_axis(dst, return_distance=True)  #距离变换
dist_on_skel = distance * skel   #距离值的图，有skel的显示距离（skel=1）,相当于 与
#dos=copy.deepcopy(dist_on_skel)  #list
dos=dist_on_skel.copy()   #array

#for i in range(width): #method1
#    for j in range(height):
#        if dos[i][j]==0.0:
#            dos[i][j]=255

#ddd=[]    #method2
#for i in dos:
#    f=map(lambda x:255 if x==0 else x, i)
#    ddd.append(f)
#dos=ddd

#dos=dos.reshape(width*height,1) #method3   longest time
#dos=numpy.array(list((map(lambda x:255 if x==0 else x, dos))))
#dos=dos.reshape(width,height)

#dos=map(lambda x:255 if x==0 else x, dos.flat) #method4  #fastest
#dos=numpy.array(dos).reshape(width,height)

dos[dos==0]=255 #method5  #fastest#转换之后可以求最小值，不然最小值是0

a=ndi.minimum_position(dos)#找最小点位置并画圈
c=list(a)
c[0],c[1]=c[1],c[0]
a=tuple(c)
cir1 = Circle(a, radius=19, color='r',fill=False,alpha=0.5)

b=ndi.maximum_position(dist_on_skel)#找最大点位置并画圈
c=list(b)
c[0],c[1]=c[1],c[0]
b=tuple(c)
cir2 = Circle(b, radius=19, color='y',fill=False,alpha=0.5)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax1.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
ax1.add_patch(cir1)
ax1.add_patch(cir2)
ax1.axis('off')
ax2.imshow(dist_on_skel, cmap=plt.cm.spectral, interpolation='nearest')
ax2.contour(img, [7], colors='w')
ax2.axis('off')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
plt.show()
print((time.clock()-globals()['tt']))


