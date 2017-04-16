# -*- coding:utf-8 -*-

import requests
import re
import time
user_agent = 'User-Agent,Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

headers1 = ({
    'Referer': 'http://www.pixiv.net/',
    'User-Agent': user_agent
})


def getid(r18=False, date='', cookies=''):
    if r18:
        if cookies!='':
            if date == '': 
                url1 = 'http://www.pixiv.net/ranking.php?mode=daily_r18'  # 每日排行榜
            else:
                url1 = 'http://www.pixiv.net/ranking.php?mode=daily_r18&date=' + str(date)
        else:
            print('no cookies')
            exit()
    elif date == '':
        url1 = 'http://www.pixiv.net/ranking.php?mode=daily'
    else:
        url1 = 'http://www.pixiv.net/ranking.php?mode=daily&date=' + str(date)        
    res1 = requests.get(url1, cookies=cookies, headers=headers1)

    content2 = res1.text
    pattern2 = re.compile('(?<=data-id=")\S*(?="data-tags)')
    dataids = re.findall(pattern2, content2)  # 寻找id
    if not dataids:
        print('getids is error')
        #print(url1,'\n',cookies)
        exit()
        # 判断是否成功
    print('getids is Success')
    time.sleep(2)  # 防止太快被反
    print(dataids)
    return dataids
