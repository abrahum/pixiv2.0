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
number = 6  # 下载图片数量
text = 'cookie.txt'  # cookie位置
ceiling=4#防止下载到漫画，每个id图片上限
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取系统时间
mkpath = str(today)

filename = text
if os.path.exists(filename):
    cookies = cookie.loadcookie(text)
else:
    cookie.getcookies(pid=pid, password=password,text=text)
    cookies = cookie.loadcookie(text)  # 读取cookie


dataids=getids.getid()
saveimg.mkdir('img')# 调用函数
saveimg.mkdir('img'+'\\'+mkpath)
mkpath='img'+'\\'+mkpath
saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)

