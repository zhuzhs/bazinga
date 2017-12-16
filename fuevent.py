#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 21:03:33 2017

@author: sme
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:19:00 2017

@author: sme
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:21:30 2017

@author: sme
"""

from multiprocessing import Manager,Process,Queue,Event
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,wait
import time,os,random
#注：###后用process开进程，后#*为future且pool开进程
def return_future(q,e):#采集和通讯
    while 1:
        time.sleep(1)
        random.seed()  
        a=random.randint(1,10)
        print('sub:',os.getpid())
        if not e.is_set():
            while  not q.empty():#queue中只保留当前值
                value = q.get(True)
            q.put([a])
        else:
            break
        #l=[a]
        print('now:',a)
        print ('queue size:',q.qsize()) 
        if a==10 :
            #pool.shutdown()
            e.set()# 后续加进去的子进程得到event的set信号就不再计算，退出
            break
    return q


if __name__=='__main__':
# 创建一个线程池
#pool = ThreadPoolExecutor(max_workers=1)
    e=Manager().Event()   #pool需用manager()
    pool= ProcessPoolExecutor(max_workers=3) #*

# 往线程池加入2个task
#f1 = pool.submit(return_future,"hello")
#    with Manager() as mgr: 
#        l = mgr.list()
#        l=[]
#        l.append(0)
    ###q =Queue()用process开子进程时，且非pool时用
    q = Manager().Queue()#pool时用 #*
#    f2 = pool.submit(return_future,q)  #*
    ###p=Process(target=return_future, args=(q,))
    ###p.start()
    #p.join()
    while 1:
        tim=time.time()
        print('c')
        print('main:',os.getpid())
        time.sleep(0.4)
        if not e.is_set():#未置位就增加一个子进程到pool
            f2 = pool.submit(return_future,q,e)
        
        if not q.empty():
            value = q.get(True)
            d=value[0]+1
            print
            print ("d=",d)
            print
            if d==11:
                break
#                pool.terminate()
        print (time.time()-tim)
