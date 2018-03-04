# -*- coding:utf-8 -*-

import requests
import re
user_agent = 'User-Agent,Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

headers1 = ({
    'Referer': 'http://www.pixiv.net/',
    'User-Agent': user_agent
})


def getid(r18=False, date='', cookies='', types=''):
    if r18:
        if (types == 'daily') or (types =='weekly'):
            if cookies!='':
                if date == '': 
                    url1 = 'http://www.pixiv.net/ranking.php?mode='+types+'_r18'  # 排行榜
                else:
                    url1 = 'http://www.pixiv.net/ranking.php?mode='+types+'_r18&date=' + str(date)
            else:
                print('no cookies')
                exit()
        else:
            print('types error,r18 only enabled for daily and weekly')
            exit()
    elif (types == 'daily') or (types =='weekly') or (types =='monthly') or (types =='male') or (types =='female'):
        if date == '':
            url1 = 'http://www.pixiv.net/ranking.php?mode='+types
        else:
            url1 = 'http://www.pixiv.net/ranking.php?mode='+types+'&date=' + str(date)  
    else:
        print('types error')
        exit()
    try:          
        res1 = requests.get(url1, cookies=cookies, headers=headers1)
    except:
        return []

    content2 = res1.text
    pattern2 = re.compile('(?<=data-id=")\S*(?="data-tags)')
    dataids = re.findall(pattern2, content2)  # 寻找id
    if not dataids:
        print('getids is error')
        print(url1)
        exit()
        # 判断是否成功
    print('getids is Success')
    #print(dataids)
    return dataids
