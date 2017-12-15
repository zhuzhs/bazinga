# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:22:10 2017

@author: Administrator
"""

from ctypes import *
import numpy as np
import time
globals()['tt'] = time.clock()
api = cdll.LoadLibrary('./test.dll')

n=100
dis=np.arange(n)
print dis
dis=dis.reshape(10,10)
#print dis
#api.restype = c_void_p 
bb=np.zeros((10,10), dtype=np.int) #dll输出，用参数形式代入，避免返回指针读数组
api.foo(dis.ctypes.data,bb.ctypes.data,10,c_int(10))  #数组首地址
print bb 
print((time.clock()-globals()['tt']))
del(api)

#globals()['tt'] = time.clock()
#n=100
#dis1=np.array(range(n))
#a=dis1.reshape(10,10)
#for  i in a:
#    i=i*2
#print dis1
#print((time.clock()-globals()['tt']))