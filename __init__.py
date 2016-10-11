#-*- coding:utf-8 -*-

import requests
import re
import os
import time
import cookie
import saveimg
import daily
import highlike
import painter

pid = ''  # 账号
password = ''  # 密码
number = 0  # 下载图片数量 0表示全部下载
text = 'cookie.txt'  # cookie位置
ceiling=4  # 防止下载到漫画，每个id图片上限
keyword=u'' # 高赞关键字
r18=False # r18daily暂时无效
leastlikes=100 # 高赞爬虫最少赞数
leastpages=10 # 高赞页数
id='' #画手id

today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取系统时间
mkpath = str(today)

filename = text
if os.path.exists(filename):
    cookies = cookie.loadcookie(text)
else:
    cookie.getcookies(pid=pid, password=password,text=text)
    cookies = cookie.loadcookie(text)  # 读取cookie

def r18word(key):
    if key:
        return 'r18'
    else:
        return ''        

def dailydownload(mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time()))),
                    Number=number,text=text,cookies=cookies,r18=r18):
    dataids = daily.getid(r18=r18)
    saveimg.mkdir('dailyimg')# 调用函数
    saveimg.mkdir('dailyimg'+'\\'+mkpath+r18word(r18))
    mkpath = 'dailyimg'+'\\'+mkpath+r18word(r18)
    saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)
    print 'Daily Done'

def HighLinkDownload(keyword=keyword,cookies=cookies,r18=r18,leastpages=leastpages,
                    leastlikes=leastlikes,Number=number,text=text,mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time())))):
    dataids = highlike.getid(keyword=keyword,cookies=cookies,r18=r18,
                    leastpages=leastpages,leastlikes=leastlikes)
    saveimg.mkdir('highlikeimg')
    saveimg.mkdir('highlikeimg'+'\\'+keyword+str(leastlikes)+'like'+mkpath+r18word(r18))
    mkpath = 'highlikeimg'+'\\'+keyword+str(leastlikes)+'like'+mkpath+r18word(r18)
    saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)
    print 'HighLike Done'

def PainterDownload(id=id,cookies=cookies,text=text,Number=number):
    dataids = painter.getid(id=id,cookies=cookies)
    saveimg.mkdir('painters')
    saveimg.mkdir('painters\\'+str(id))
    mkpath = 'painters\\'+str(id)
    saveimg.save(Number=number,dataids=dataids,text=text,cookies=cookies,path=mkpath)

#dailydownload()
HighLinkDownload()
#PainterDownload()