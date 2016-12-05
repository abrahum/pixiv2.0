import requests
import re

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

headers1= ({
    'Referer': 'http://www.pixiv.net/',
    'User-Agent': user_agent
})

def getid(id,cookies):
    url = 'http://www.pixiv.net/member_illust.php?id=' + str(id)
    dataids = []
    empty = False
    p = 1
    while not empty:
        myurl = url + '&p=' + str(p)
        html = requests.get(url=myurl,cookies=cookies,headers=headers1).text
        targetlist = re.findall(u'<a href="/member_illust\.php\?mode=medium&amp;illust_id=\d+" class="work  _work ">',html)
        if not targetlist:
            print('Page %d is Empty' % (p))
            empty = True
        else:
            print('Page %d is Done' % (p))
        for j in targetlist:
            imgid = re.search('id=\d+',j).group()[3:]
            dataids.append(imgid)
        p = p+1
    return dataids
