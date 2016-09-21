#-*- coding:utf-8 -*-

import requests
import re
import os
import time
import cookie
import saveimg
import getids

pid = '****'  # 账号
password = '****'  # 密码
number = 5  # 下载图片数量
text = '/mnt/p/'+'cookie.txt'  # cookie位置
add='/mnt/p/img'#linux绝对地址
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取系统时间
mkpath = str(today)

filename = text
if os.path.exists(filename):
    cookies = cookie.loadcookie(text)
else:
    cookie.getcookies(pid=pid, password=password,text=text)
    cookies = cookie.loadcookie(text)  # 读取cookie


dataids=getids.getid()
saveimg.mkdir(add)#创建img文件夹
saveimg.mkdir(add+'/'+mkpath)#创建日期文件夹
mkpath=add+'/'+mkpath
saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)#保存图片