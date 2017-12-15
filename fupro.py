#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:21:30 2017

@author: sme
"""

from multiprocessing import Manager,Process,Queue
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,wait
import time,os,random
#注：###后用process开进程，后#*为future且pool开进程
def return_future(q):#采集和通讯
    while 1:
        time.sleep(1)
        random.seed()  
        a=random.randint(1,10)
        print('sub:',os.getpid())
        if not q.empty():#queue中只保留当前值
            value = q.get(True)
        q.put([a])
        print 'now:',a
        print 'queue size:',q.qsize() 
        if a==10 :
            #pool.shutdown()
            break
    return q


if __name__=='__main__':
# 创建一个线程池
#pool = ThreadPoolExecutor(max_workers=1)
    #*pool= ProcessPoolExecutor(max_workers=2) #*

# 往线程池加入2个task

    ###q =Queue()  #用process开子进程时，且非pool时用   ###
    q = Manager().Queue()#pool时或非pool时都可用 #*
    #*f2 = pool.submit(return_future,q)  #*
    p=Process(target=return_future, args=(q,))   ###
    p.start() ###
    p.join()
    while 1:
        tim=time.time()
        print('c')
        print('main:',os.getpid())
        time.sleep(2)
        if not q.empty():
            value = q.get(True)
        d=value[0]+1
        print
        print "d=",d
        print
        if d==11:
            break
        #    if f2.done()==1:
        #        print(f2.result())
        print time.time()-tim
