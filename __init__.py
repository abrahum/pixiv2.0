#-*- coding:utf-8 -*-

import requests
import re
import os
import time
import cookie
import saveimg
import daily
import highlike

pid = ''  # 账号
password = ''  # 密码
number = 40  # 下载图片数量
text = 'cookie.txt'  # cookie位置
ceiling=4  # 防止下载到漫画，每个id图片上限
keyword=u'akasa' # 高赞关键字
r18=False # r18
leastlikes=1000 # 高赞爬虫最少赞数
leastpages=100 # 高赞页数

today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取系统时间
mkpath = str(today)

filename = text
if os.path.exists(filename):
    cookies = cookie.loadcookie(text)
else:
    cookie.getcookies(pid=pid, password=password,text=text)
    cookies = cookie.loadcookie(text)  # 读取cookie

def dailydownload(mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time()))),
                    Number=number,text=text,cookies=cookies):
    dataids = daily.getid()
    saveimg.mkdir('dailyimg')# 调用函数
    saveimg.mkdir('dailyimg'+'\\'+mkpath)
    mkpath = 'dailyimg'+'\\'+mkpath
    saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)
    print 'Daily Done'

def HighLinkDownload(keyword=keyword,cookies=cookies,r18=r18,leastpages=leastpages,
                    leastlikes=leastlikes,Number=number,text=text,mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time())))):
    dataids = highlike.getid(keyword=keyword,cookies=cookies,r18=r18,
                    leastpages=leastpages,leastlikes=leastlikes)
    saveimg.mkdir('highlikeimg')
    saveimg.mkdir('highlikeimg'+'\\'+keyword+str(leastlikes)+'like'+mkpath)
    mkpath = 'highlikeimg'+'\\'+keyword+str(leastlikes)+'like'+mkpath
    saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)
    print 'HighLike Done'

dailydownload()
#HighLinkDownload()