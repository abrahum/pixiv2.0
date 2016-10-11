#-*- coding:utf-8 -*-

import requests
import re
import sys
import os
import time
import cookie
import saveimg
import daily
import highlike
import painter

today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取系统时间
mkpath = str(today)

def getcookies(pid,password,text = 'cookie.txt'):
    filename = text
    if os.path.exists(filename):
        cookies = cookie.loadcookie(text)
        return cookies
    else:
        cookie.getcookies(pid=pid, password=password,text=text)
        cookies = cookie.loadcookie(text)  # 读取cookie
        return cookies

def r18word(key):
    if key:
        return 'r18'
    else:
        return ''      

class pixiv(object):
    
    def __init__(self):
        self.pid = ''  # 账号
        self.password = ''  # 密码
        self.number = 0  # 下载图片数量 0表示全部下载
        self.text = 'cookie.txt'
        self.cookies = getcookies(self.pid,self.password)  # cookie
        self.ceiling=4  # 防止下载到漫画，每个id图片上限
        self.keyword=u'' # 高赞关键字
        self.r18=False # r18daily暂时无效
        self.leastlikes=100 # 高赞爬虫最少赞数
        self.leastpages=10 # 高赞页数
        self.id='' #画手id  

    def dailydownload(self):
        mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        dataids = daily.getid(r18=self.r18)
        saveimg.mkdir('dailyimg')# 调用函数
        saveimg.mkdir('dailyimg'+'\\'+mkpath+r18word(self.r18))
        mkpath = 'dailyimg'+'\\'+mkpath+r18word(self.r18)
        saveimg.save(Number=self.number,dataids=dataids,text=self.text,cookies=self.cookies,path=mkpath)
        print 'Daily Done'

    def HighLinkDownload(self):
        mkpath=str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        dataids = highlike.getid(keyword=self.keyword,cookies=self.cookies,r18=self.r18,leastpages=self.leastpages,leastlikes=self.leastlikes)
        saveimg.mkdir('highlikeimg')
        saveimg.mkdir('highlikeimg'+'\\'+keyword+str(self.leastlikes)+'like'+mkpath+r18word(self.r18))
        mkpath = 'highlikeimg'+'\\'+keyword+str(self.leastlikes)+'like'+mkpath+r18word(self.r18)
        saveimg.save(Number=self.number,dataids=dataids,text=self.text,cookies=self.cookies,path=mkpath)
        print 'HighLike Done'

    def PainterDownload(self):
        dataids = painter.getid(id=self.id,cookies=self.cookies)
        saveimg.mkdir('painters')
        saveimg.mkdir('painters\\'+str(self.id))
        mkpath = 'painters\\'+str(self.id)
        saveimg.save(Number=self.number,dataids=dataids,text=self.text,cookies=self.cookies,path=mkpath)
        print 'Painter Done'

if __name__ == "__main__":
    test = pixiv()
    #test.dailydownload()
    #test.HighLinkDownload()
    #test.PainterDownload()