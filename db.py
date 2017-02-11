import sqlite3
import time
import asyncio
import requests
import re
from random import choice


now_time = time.localtime()
year = now_time.tm_year
mon = now_time.tm_mon
day = now_time.tm_mday
if mon < 10:
    smon = '0'+str(mon)
else:
    smon = str(mon)
if day < 10:
    sday = '0'+str(day)
else:
    sday = str(day)
mytime = str(year)+smon+sday


class BookmarkSpider(object):
    def __init__(self, cookies):
        self.pool = []
        self.con = sqlite3.connect('pixiv.db')
        self.cur = self.con.cursor()
        self.loop = asyncio.get_event_loop()
        self.s = requests.session()
        self.s.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.s.headers = ({'Referer': 'http://www.pixiv.net/',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/50.0.2661.102 Safari/537.36'})
        self.limit = 80

    def run(self):
        tasks = []
        for i in range(self.limit):
            tasks.append(self.bookmark())
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.cur.close()
        self.con.close()
        self.loop.close()
        return 0

    async def bookmark(self):
        p = Painter()
        while self.pool:
            p.id = choice(self.pool)
            targets = []
            self.pool.remove(p.id)
            try:
                bookmark_html = await self.get(p.bookmark())
            except:
                print('ERROR')
                continue
            lis = re.findall('<li class="image-item"[^收]+', bookmark_html.text)
            page = 2
            while lis and page < 32:
                for i in lis:
                    targets.append(i)
                try:
                    bookmark_html = await self.get(p.bookmark() + '&p=' + str(page))
                except:
                    continue
                lis = re.findall('<li class="image-item" id="li_\d+"><a href="member_illust.php?[^收]+',
                                 bookmark_html.text)
                page += 1
                print('\c' + str(p.id), page, len(lis))
            for i in targets:
                img = PixivImg()
                uper = Painter()
                try:
                    img.id = int(re.search('illust_id=\d+', i).group()[10:])
                    img.title = re.search('title="">[^<]+', i).group()[9:]
                    uper.name = re.search('data-user_name="[^"]+', i).group()[16:]
                    uper.id = int(re.search('data-user_id="\d+', i).group()[14:])
                    img.like_num = int(re.search('data-tooltip="[^件]+', i).group()[14:].replace(',', ''))
                    img.tag = re.search('data-tags="[^"]+', i).group()[11:].split(' ')
                    img.painter_id = uper.id
                    img.url = re.search('data-filter="thumbnail-filter lazy-image"data-src="[^"]+', i).group()[51:]
                except AttributeError:
                    img.tag = []
                img.write(self.cur)
                uper.write(self.cur)
            acom = 'UPDATE painters SET BOOKMARK = ' + mytime + ' WHERE ID = ' + str(p.id)
            self.cur.execute(acom)
            self.con.commit()
            print(len(targets))
        return 0

    def get(self, url):
        return self.loop.run_in_executor(None, self.set_timeout_get, url)

    def set_timeout_get(self, url):
        return self.s.get(url, timeout=30)

    def build_pool(self):
        self.cur.execute("SELECT ID FROM painters WHERE BOOKMARK IS NULL")
        for i in self.cur.fetchall():
            self.pool.append(i[0])
        print(len(self.pool))


class Painter(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.update_time = int(mytime)

    def bookmark(self):
        return 'http://www.pixiv.net/bookmark.php?id='+str(self.id)

    def member_illust(self):
        return 'http://www.pixiv.net/member_illust.php?id='+str(self.id)

    def write(self, cur):
        acom = 'SELECT * FROM painters WHERE ID=' + str(self.id)
        cur.execute(acom)
        if not cur.fetchall():
            acom = 'INSERT INTO painters VALUES('+str(self.id)+',"'+str(self.name)+'",'+\
                   str(self.update_time)+',NULL,NULL)'
            cur.execute(acom)
        else:
            pass
        return 0


class PixivImg(object):
    def __init__(self):
        self.id = 0
        self.title = ''
        self.like_num = 0
        self.painter_id = 0
        self.update_time = int(mytime)
        self.tag = []
        self.url = ''

    def write(self, cur):
        acom = 'SELECT * FROM imgs WHERE ID=' + str(self.id)
        cur.execute(acom)
        if not cur.fetchall():
            if self.tag:
                tag = '&'.join(self.tag)
                acom = 'INSERT INTO imgs VALUES('+str(self.id)+',"'+str(self.title)+'",'+str(self.like_num)+',' + \
                       str(self.painter_id)+','+str(self.update_time)+',"'+tag+'","'+self.url+'")'
                cur.execute(acom)
            else:
                acom = 'INSERT INTO imgs VALUES('+str(self.id)+',"'+str(self.title)+'",'+str(self.like_num)+',' + \
                       str(self.painter_id)+','+str(self.update_time)+',NULL,"'+self.url+'")'
                cur.execute(acom)
            return 0
        else:
            acom = 'UPDATE IMGS SET LIKENUM = ' + str(self.like_num) + ', URL = "' + self.url + '", UPDATETIME = ' + \
                   str(self.update_time) + ' WHERE ID = ' + str(self.id)
            cur.execute(acom)
            return 0
