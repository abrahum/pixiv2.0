#-*- coding:utf-8 -*-

import requests
import re
import os


def getcookies(pid,password,text):

    s = requests.session()

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers1 = ({
       'Referer':'https://accounts.pixiv.net/login?return_to=http%3A%2F%2Fwww.pixiv.net%2Franking.php%3Fmode%3Ddaily&source=pc&view_type=page',
       'User-Agent': user_agent
    })

    shouUrl='https://accounts.pixiv.net/login?return_to=http%3A%2F%2Fwww.pixiv.net%2Franking.php%3Fmode%3Ddaily&source=pc&view_type=page'
    url1 = 'https://accounts.pixiv.net/api/login?lang=zh'

    res1 = s.get(shouUrl, headers=headers1)

    content = res1.text.encode('utf-8')
    pattern = re.compile('(?<=<input type="hidden" name="post_key" value=")\w*(?=">)')
    items = re.findall(pattern,content)
    if not items:
        print 'postkey is not found'
        exit()
    postkey=items[0]

    data=({
     'pixiv_id':str(pid),
     'password':str(password),
     'captcha':'',
     'g_recaptcha_response':'',
     'post_key':str(postkey),
     'source':'pc'
     })

    res2 = s.post(url1, data=data)#登录页
    cookies = s.cookies
    fp = open(text,'wb')
    fp.write('; '.join(['='.join(item) for item in cookies.items()]))
    fp.close()#保存cookies
    print 'save cookies is Success'


def loadcookie(text):
     loadcookies = {}
     f = open(text,'r')
     for line in f.read().split(';'):
         name,value=line.strip().split('=',1)
         loadcookies[name]=value
     f.close()
     print 'load cookies is Success'
     return loadcookies



