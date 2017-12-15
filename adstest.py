# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 11:06:45 2016

@author: Administrator
"""

from ctypes import *
#I've tried OleDll and windll as wel..
ADS_DLL = windll.LoadLibrary(r"C:\TwinCAT\AdsApi\TcAdsDll\TcAdsDll.dll")
class AmsNetId(Structure):
    _fields_ = [('NetId', c_ubyte*6)]
class AmsAddr(Structure):
    _fields_=[('AmsNetId',AmsNetId),('port',c_ushort)]
# DLL function working fine
version = ADS_DLL.AdsGetDllVersion()
print(version)
#DLL function working fine
errCode = ADS_DLL.AdsPortOpen()
print(errCode)
#DLL function using the AmsAddr() class, working fine
amsAddress = AmsAddr()
pointer_amsAddress = pointer(amsAddress)
errCode = ADS_DLL.AdsGetLocalAddress(pointer_amsAddress)
print(errCode)
contents_amsAddres = pointer_amsAddress.contents
amsAddress.port=801

#errCode = ADS_DLL.AdsSyncReadReq()
#print(errCode) # --> errCode = timeout error, normal because I didn't pass any arguments
# Now with arguments:
plcNetId = AmsNetId((c_ubyte*6)(172,31,96,218,1,1)) #correct adress to the PLC
plcAddress = AmsAddr(plcNetId,801) #correct port to the PLC
nIndexGroup = c_ulong(0xF020)
nIndexOffset = c_ulong(0x4)
nLength = c_ulong(0x4)
data = c_void_p()
pointer_data = pointer(data)

#I tried with an without the following 2 lines, doesn't matters
#ADS_DLL.AdsSyncReadReq.argtypes=[AmsAddr,c_ulong,c_ulong,c_ulong,POINTER(c_void_p)]
#ADS_DLL.AdsSyncReadReq.restype=None
v1=c_char_p(b"MAIN.plcint")

lHdlVarR=c_ulong()  #use name
nErr=ADS_DLL.AdsSyncReadWriteReq(pointer(amsAddress),0xF003,0x0,nLength,pointer(lHdlVarR),len(v1.value),v1)
print(nErr)  # Fetch handle for the PLC variable  #ADSIGRP_SYM_HNDBYNAME 0xF003
errCode = ADS_DLL.AdsSyncReadReq(pointer(amsAddress),0xF005,lHdlVarR,nLength,pointer_data)
print(errCode)   #ADSIGRP_SYM_VALBYHND 0xF005
print(data.value)   #Read values of the PLC variables (by handle)

errCode = ADS_DLL.AdsSyncReadReq(pointer(amsAddress),0x4020,nIndexOffset,nLength,pointer_data)
print(errCode) #use address
print(data.value)

dwdata=c_int(89)
errCode = ADS_DLL.AdsSyncWriteReq(pointer(plcAddress),0x4020,nIndexOffset,nLength,pointer(dwdata))#using plcAddress same as amsAddress
print(errCode)


## Index Group
## READ_M - WRITE_M
#INDEXGROUP_MEMORYBYTE = 0x4020  #: plc memory area (%M), offset means byte-offset
## READ_MX - WRITE_MX
#INDEXGROUP_MEMORYBIT = 0x4021  #: plc memory area (%MX), offset means the bit adress, calculatedb by bytenumber * 8 + bitnumber
## PLCADS_IGR_RMSIZE
#INDEXGROUP_MEMORYSIZE = 0x4025  #: size of the memory area in bytes
## PLCADS_IGR_RWRB
#INDEXGROUP_RETAIN = 0x4030  #: plc retain memory area, offset means byte-offset
## PLCADS_IGR_RRSIZE
#INDEXGROUP_RETAINSIZE = 0x4035  #: size of the retain area in bytes
## PLCADS_IGR_RWDB
#INDEXGROUP_DATA = 0x4040  #: data area, offset means byte-offset
## PLCADS_IGR_RDSIZE
#INDEXGROUP_DATASIZE = 0x4045  #: size of the data area in bytes
#
#
#ADSIGRP_SYMTAB = 0xF000
#ADSIGRP_SYMNAME = 0xF001
#ADSIGRP_SYMVAL = 0xF002
#
#ADSIGRP_SYM_HNDBYNAME = 0xF003
#ADSIGRP_SYM_VALBYNAME = 0xF004
#ADSIGRP_SYM_VALBYHND = 0xF005
#ADSIGRP_SYM_RELEASEHND = 0xF006
#ADSIGRP_SYM_INFOBYNAME = 0xF007
#ADSIGRP_SYM_VERSION = 0xF008
#ADSIGRP_SYM_INFOBYNAMEEX = 0xF009
#
#ADSIGRP_SYM_DOWNLOAD = 0xF00A
#ADSIGRP_SYM_UPLOAD = 0xF00B
#ADSIGRP_SYM_UPLOADINFO = 0xF00C
#
#ADSIGRP_SYMNOTE = 0xF010  # notification of named handle
#ADSIGRP_IOIMAGE_RWIB = 0xF020  # read/write input byte(s)
#ADSIGRP_IOIMAGE_RWIX = 0xF021  # read/write input bit
#ADSIGRP_IOIMAGE_RWOB = 0xF030  # read/write output byte(s)
#ADSIGRP_IOIMAGE_RWOX = 0xF031  # read/write output bit
#ADSIGRP_IOIMAGE_CLEARI = 0xF040  # write inputs to null
#ADSIGRP_IOIMAGE_CLEARO = 0xF050  # write outputs to null
#
#ADSIGRP_DEVICE_DATA = 0xF100  # state, name, etc...
#ADSIOFFS_DEVDATA_ADSSTATE = 0x0000  # ads state of device
#ADSIOFFS_DEVDATA_DEVSTATE = 0x0002  # device state