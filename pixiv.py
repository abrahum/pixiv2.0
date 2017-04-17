# -*- coding:utf-8 -*-

import requests
import re
import sys
import os
import time
import cookie
import saveimg
import daily
import painter
import threading
import tqdm
import getopt
import db
import sqlite3

user_agent = 'User-Agent,Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers1 = ({
    'Referer': 'http://www.pixiv.net/',
    'User-Agent': user_agent
})

if sys.platform == 'win32':
    path_break = '\\'
else:
    path_break = '/'


def get_cookies(pid, password, login=False):
    filename = 'cookie.txt'
    if login:
        cookie.get_cookies(pid=pid, password=password, text=filename)
        cookies = cookie.loadcookie(filename)  # 读取cookie
        return cookies
    elif os.path.exists(filename):
        cookies = cookie.loadcookie(filename)
        return cookies
    else:
        print("load cookie false")


def r18word(key):
    if key:
        return 'r18'
    else:
        return ''  


def keyword_swich(keyword):
    byte = keyword.encode('utf-8')
    dbytedir = {b'\x00': '%00', b'\x01': '%01', b'\x02': '%02', b'\x03': '%03',
                b'\x04': '%04', b'\x05': '%05', b'\x06': '%06', b'\x07': '%07',
                b'\x08': '%08', b'\x09': '%09', b'\x0a': '%0A', b'\x0b': '%0B',
                b'\x0c': '%0C', b'\x0d': '%0D', b'\x0e': '%0E', b'\x0f': '%0F',
                b'\x10': '%10', b'\x11': '%11', b'\x12': '%12', b'\x13': '%13',
                b'\x14': '%14', b'\x15': '%15', b'\x16': '%16', b'\x17': '%17',
                b'\x18': '%18', b'\x19': '%19', b'\x1a': '%1A', b'\x1b': '%1B',
                b'\x1c': '%1C', b'\x1d': '%1D', b'\x1e': '%1E', b'\x1f': '%1F',
                b'\x20': '%20', b'\x21': '%21', b'\x22': '%22', b'\x23': '%23',
                b'\x24': '%24', b'\x25': '%25', b'\x26': '%26', b'\x27': '%27',
                b'\x28': '%28', b'\x29': '%29', b'\x2a': '%2A', b'\x2b': '%2B',
                b'\x2c': '%2C', b'\x2d': '%2D', b'\x2e': '%2E', b'\x2f': '%2F',
                b'\x30': '%30', b'\x31': '%31', b'\x32': '%32', b'\x33': '%33',
                b'\x34': '%34', b'\x35': '%35', b'\x36': '%36', b'\x37': '%37',
                b'\x38': '%38', b'\x39': '%39', b'\x3a': '%3A', b'\x3b': '%3B',
                b'\x3c': '%3C', b'\x3d': '%3D', b'\x3e': '%3E', b'\x3f': '%3F',
                b'\x40': '%40', b'\x41': '%41', b'\x42': '%42', b'\x43': '%43',
                b'\x44': '%44', b'\x45': '%45', b'\x46': '%46', b'\x47': '%47',
                b'\x48': '%48', b'\x49': '%49', b'\x4a': '%4A', b'\x4b': '%4B',
                b'\x4c': '%4C', b'\x4d': '%4D', b'\x4e': '%4E', b'\x4f': '%4F',
                b'\x50': '%50', b'\x51': '%51', b'\x52': '%52', b'\x53': '%53',
                b'\x54': '%54', b'\x55': '%55', b'\x56': '%56', b'\x57': '%57',
                b'\x58': '%58', b'\x59': '%59', b'\x5a': '%5A', b'\x5b': '%5B',
                b'\x5c': '%5C', b'\x5d': '%5D', b'\x5e': '%5E', b'\x5f': '%5F',
                b'\x60': '%60', b'\x61': '%61', b'\x62': '%62', b'\x63': '%63',
                b'\x64': '%64', b'\x65': '%65', b'\x66': '%66', b'\x67': '%67',
                b'\x68': '%68', b'\x69': '%69', b'\x6a': '%6A', b'\x6b': '%6B',
                b'\x6c': '%6C', b'\x6d': '%6D', b'\x6e': '%6E', b'\x6f': '%6F',
                b'\x70': '%70', b'\x71': '%71', b'\x72': '%72', b'\x73': '%73',
                b'\x74': '%74', b'\x75': '%75', b'\x76': '%76', b'\x77': '%77',
                b'\x78': '%78', b'\x79': '%79', b'\x7a': '%7A', b'\x7b': '%7B',
                b'\x7c': '%7C', b'\x7d': '%7D', b'\x7e': '%7E', b'\x7f': '%7F',
                b'\x80': '%80', b'\x81': '%81', b'\x82': '%82', b'\x83': '%83',
                b'\x84': '%84', b'\x85': '%85', b'\x86': '%86', b'\x87': '%87',
                b'\x88': '%88', b'\x89': '%89', b'\x8a': '%8A', b'\x8b': '%8B',
                b'\x8c': '%8C', b'\x8d': '%8D', b'\x8e': '%8E', b'\x8f': '%8F',
                b'\x90': '%90', b'\x91': '%91', b'\x92': '%92', b'\x93': '%93',
                b'\x94': '%94', b'\x95': '%95', b'\x96': '%96', b'\x97': '%97',
                b'\x98': '%98', b'\x99': '%99', b'\x9a': '%9A', b'\x9b': '%9B',
                b'\x9c': '%9C', b'\x9d': '%9D', b'\x9e': '%9E', b'\x9f': '%9F',
                b'\xa0': '%A0', b'\xa1': '%A1', b'\xa2': '%A2', b'\xa3': '%A3',
                b'\xa4': '%A4', b'\xa5': '%A5', b'\xa6': '%A6', b'\xa7': '%A7',
                b'\xa8': '%A8', b'\xa9': '%A9', b'\xaa': '%AA', b'\xab': '%AB',
                b'\xac': '%AC', b'\xad': '%AD', b'\xae': '%AE', b'\xaf': '%AF',
                b'\xb0': '%B0', b'\xb1': '%B1', b'\xb2': '%B2', b'\xb3': '%B3',
                b'\xb4': '%B4', b'\xb5': '%B5', b'\xb6': '%B6', b'\xb7': '%B7',
                b'\xb8': '%B8', b'\xb9': '%B9', b'\xba': '%BA', b'\xbb': '%BB',
                b'\xbc': '%BC', b'\xbd': '%BD', b'\xbe': '%BE', b'\xbf': '%BF',
                b'\xc0': '%C0', b'\xc1': '%C1', b'\xc2': '%C2', b'\xc3': '%C3',
                b'\xc4': '%C4', b'\xc5': '%C5', b'\xc6': '%C6', b'\xc7': '%C7',
                b'\xc8': '%C8', b'\xc9': '%C9', b'\xca': '%CA', b'\xcb': '%CB',
                b'\xcc': '%CC', b'\xcd': '%CD', b'\xce': '%CE', b'\xcf': '%CF',
                b'\xd0': '%D0', b'\xd1': '%D1', b'\xd2': '%D2', b'\xd3': '%D3',
                b'\xd4': '%D4', b'\xd5': '%D5', b'\xd6': '%D6', b'\xd7': '%D7',
                b'\xd8': '%D8', b'\xd9': '%D9', b'\xda': '%DA', b'\xdb': '%DB',
                b'\xdc': '%DC', b'\xdd': '%DD', b'\xde': '%DE', b'\xdf': '%DF',
                b'\xe0': '%E0', b'\xe1': '%E1', b'\xe2': '%E2', b'\xe3': '%E3',
                b'\xe4': '%E4', b'\xe5': '%E5', b'\xe6': '%E6', b'\xe7': '%E7',
                b'\xe8': '%E8', b'\xe9': '%E9', b'\xea': '%EA', b'\xeb': '%EB',
                b'\xec': '%EC', b'\xed': '%ED', b'\xee': '%EE', b'\xef': '%EF',
                b'\xf0': '%F0', b'\xf1': '%F1', b'\xf2': '%F2', b'\xf3': '%F3',
                b'\xf4': '%F4', b'\xf5': '%F5', b'\xf6': '%F6', b'\xf7': '%F7',
                b'\xf8': '%F8', b'\xf9': '%F9', b'\xfa': '%FA', b'\xfb': '%FB',
                b'\xfc': '%FC', b'\xfd': '%FD', b'\xfe': '%FE', b'\xff': '%FF'}
    result = ''
    for i in range(len(byte)):
        target = byte[i:i+1]
        result = result + dbytedir.get(target)
    return result


def r18c(url, r18=False):
    if r18:
        url += '&r18=1'
        return url
    else:
        url += '&r18=0'
        return url    


class Pixiv(object):
    
    def __init__(self):
        self.pid = ''  # 账号
        self.password = ''  # 密码
        self.number = 0  # 下载图片数量 0表示全部下载
        self.text = 'cookie.txt'
        self.cookies = ''  # cookie
        self.ceiling = 20  # 防止下载到漫画，每个id图片上限
        self.keyword = ''  # 高赞关键字
        self.r18 = False  # r18daily暂时无效
        self.least_likes = 500  # 高赞爬虫最少赞数
        self.least_pages = 1000  # 高赞页数
        self.start_page = 0  # 搜索的关键字开始爬取页数
        self.id = ''  # 画手id
        self.type = 'daily'  #主页模式选择  默认 daily 1.daily 2.weekly 3.male 4.female
        self.date = ''  # daily的日期
        self.sdate = self.date  # daily保存使用的日期
        self.threads = False  # 是否允许多线程
        self.dataids = []  # imgurl的保存lists
        self.async_able = False  # 是否允许异步（多线程优先级高于异步）
        self.runing = []  # 还在运行的线程
        self.done = 0  # 已完成的下载数量

    # 几种爬取方式

    def db_download(self):
        con = sqlite3.connect('pixiv.db')
        cur = con.cursor()
        cur.execute('SELECT COUNT(1)')
        acom = 'SELECT * FROM IMGS WHERE LIKENUM > ' + str(self.least_likes) + ' AND TAG LIKE "%' + self.keyword + '%"'
        cur.execute(acom)
        tem = cur.fetchall()
        for i in tem:
            self.dataids.append(i[0])
        saveimg.mkdir('dbimg')
        saveimg.mkdir('dbimg' + path_break + self.keyword + str(self.least_likes) + 'like')
        mkpath = 'dbimg' + path_break + self.keyword + str(self.least_likes) + 'like'
        if self.threads:
            self.new_threadsave(mkpath)
        elif self.async_able:
            saveimg.async_save(self.dataids, self.cookies, mkpath)
        else:
            saveimg.save(number=self.number, dataids=self.dataids, cookies=self.cookies, path=mkpath)
        print('DB Done')

    def daily_download(self):
        if self.sdate == '':
            mkpath = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        else:
            mkpath = str(self.sdate[0:4]+'-'+self.sdate[4:6]+'-'+self.sdate[6:])
        self.dataids = daily.getid(r18=self.r18, date=self.date, cookies=self.cookies)
        saveimg.mkdir('dailyimg')  # 调用函数
        saveimg.mkdir('dailyimg'+path_break+mkpath+r18word(self.r18))
        mkpath = 'dailyimg'+path_break+mkpath+r18word(self.r18)
        if self.threads:
            self.new_threadsave(mkpath)
        elif self.async_able:
            saveimg.async_save(self.dataids, self.cookies, mkpath)
        else:
            saveimg.save(number=self.number, dataids=self.dataids, cookies=self.cookies, path=mkpath, ceiling=self.ceiling)
        print('Daily Done')

    def super_daily_download(self):
        date = 20161000
        self.sdate = '201610'
        while date < 20161031:
            date += 1
            self.date = str(date)
            self.daily_download()

    def highlink_download(self):
        mkpath = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        if self.least_pages > 40:
            threads = []
            for i in range(self.least_pages//40):
                t = threading.Thread(target=self.highlikegetid, args=(i*40, (i+1)*40))
                threads.append(t)
            for t in threads:
                t.start()
            for t in tqdm.tqdm(threads):
                t.join(180)
        else:
            self.highlikegetid()
        saveimg.mkdir('highlikeimg')
        saveimg.mkdir('highlikeimg'+path_break+self.keyword+str(self.least_likes)+'like'+mkpath+r18word(self.r18))
        mkpath = 'highlikeimg'+path_break+self.keyword+str(self.least_likes) + 'like' + mkpath + r18word(self.r18)
        if self.threads:
            self.new_threadsave(mkpath)
        elif self.async_able:
            saveimg.async_save(self.dataids, self.cookies, mkpath)
        else:
            saveimg.save(number=self.number, dataids=self.dataids, cookies=self.cookies, path=mkpath)
        print('HighLike Done')

    def painter_download(self):
        self.dataids = painter.getid(img_id=self.id, cookies=self.cookies)
        saveimg.mkdir('painters')
        saveimg.mkdir('painters'+path_break+str(self.id))
        mkpath = 'painters'+path_break+str(self.id)
        if self.threads:
            self.new_threadsave(mkpath)
        elif self.async_able:
            saveimg.async_save(self.dataids, self.cookies, mkpath)
        else:
            saveimg.save(number=self.number, dataids=self.dataids, cookies=self.cookies, path=mkpath, ceiling=self.ceiling)
        print('Painter Done')

    def painter_bookmark_download(self):
        self.dataids = painter.getid2(img_id=self.id, cookies=self.cookies)
        saveimg.mkdir('painters')
        saveimg.mkdir('painters'+path_break+str(self.id)+'bookmark')
        mkpath = 'painters'+path_break+str(self.id)+'bookmark'
        if self.threads:
            self.new_threadsave(mkpath)
        elif self.async_able:
            saveimg.async_save(self.dataids, self.cookies, mkpath)
        else:
            saveimg.save(number=self.number, dataids=self.dataids, cookies=self.cookies, path=mkpath, ceiling=self.ceiling)
        print('Painter\'s Bookmrak Done')

    def highlikegetid(self, startpage=0, leastpages=1000):  # 关键字爬取函数
        base_url = r18c('http://www.pixiv.net/search.php?word=' + keyword_swich(self.keyword), self.r18)
        for i in range(startpage, leastpages):
            myurl = base_url + '&p=' + str(i+1)
            html = requests.get(url=myurl, cookies=self.cookies, headers=headers1).text
            target_list = re.findall(u'<a href="/bookmark_detail\.php\?illust_id=\d+" class="bookmark-count _ui-to'
                                     u'oltip" data-tooltip="[0-9,]+', html)
            if not target_list:
                '''print('Page %d is Empty' % (i+1))'''
                return self.dataids
            for j in target_list:
                img_id = re.search('id=\d+', j).group()[3:]
                likenumber = int(re.search('"[0-9,]+', j).group()[1:].replace(',', ''))
                if likenumber >= self.least_likes:
                    self.dataids.append(img_id)
            '''print('Page %d is Done' % (i+1))'''
        return self.dataids

    def threadsave(self, mkpath):  # 旧版多线程下载方式
        threads = []
        each_size = len(self.dataids)//19
        for i in range(19):
            t = threading.Thread(target=self.save, args=(self.dataids[i*each_size:(i+1)*each_size],
                                                         self.cookies, mkpath))
            threads.append(t)
        t = threading.Thread(target=self.save, args=(self.dataids[19*each_size:], self.cookies, mkpath))
        threads.append(t)
        threads.append(threading.Thread(target=self.progress_bar))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def new_threadsave(self, mkpath):  # 新的多线程下载
        threads = []
        progarss_thread = threading.Thread(target=self.progress_bar)
        threads.append(progarss_thread)
        for i in self.dataids:
            t = threading.Thread(target=self.save, args=([i], self.cookies, mkpath))
            threads.append(t)
        for t in threads:
            t.start()
            while threading.active_count() > 20:
                pass
        progarss_thread.join()

    def progress_bar(self):  # 简易进度条
        print('0/'+str(len(self.dataids)), end='')
        done = 0
        timelock = time.time()
        while True:
            if self.done > done:
                print('\r'+str(self.done)+'/'+str(len(self.dataids)), end='')
                done = self.done
                timelock = time.time()
            elif self.done == len(self.dataids) or time.time()-timelock > 30:
                sys.exit()
            else:
                pass

    def save(self, dataids, cookies, path):  # 单线程保存
        s = requests.session()
        s.cookies = requests.utils.cookiejar_from_dict(cookies)
        s.headers = headers1
        self.runing.append(threading.current_thread())
        if len(dataids) > 30:
            print('All Download')
        for i in dataids:
            b = 0
            dataidurl = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(i)
            #res1 = s.get(dataidurl)  # 相应id网站
            res1 = saveimg.reget(dataidurl,s)
            content1 = res1.text
            pattern1 = re.compile('(?<= data-src=")\S*(?=" class="original-image">)')
            originaltus = re.findall(pattern1, content1)
            if not originaltus:
                dataidurl = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=' + str(i)
                #res2 = s.get(dataidurl)  # 相应id网站
                res2 = saveimg.reget(dataidurl,s)
                content2 = res2.text
                pattern2 = re.compile('(?<=data-filter="manga-image" data-src=")\S*(?=" data-index)')
                originaltus = re.findall(pattern2, content2)
                if not originaltus:
                    #print(str(i) + 'not found')
                    print(str(i) + ' may gif')
                    ft = open(path+'\\'+'gifid.txt','a')    #将gif图 id号输出到txt，以便自行查看
                    ft.write(str(i)+'\n')
                    ft.close
                    self.done += 1
                    continue

            for originaltu in originaltus:
                b += 1
            if b >= self.ceiling:
                #print(str(i) + ' is too long')
                print(str(i)+' is too long')
                ft = open(path+'\\'+'long picid.txt','a')    #将过长的组图id号输出到txt，以便自行查看
                ft.write(str(i)+'\n')
                ft.close
                self.done += 1
                continue
            else:
                b = 0  # 判断id图片是否过多

            for originaltu in originaltus:
                content3 = originaltu
                pattern3 = re.compile('png')
                ifpng = re.findall(pattern3, content3)
                if not ifpng:
                    str1 = 'jpg'
                else:
                    str1 = 'png'  # 判断后缀是jpg还是png
                '''print(i +'-'+str(b)+ ' is downloading')'''
                string = 'pixiv' + str(i) + '-' + 'p' + str(b) + '.' + str1
                is_exists = os.path.exists(path + path_break + string)
                '''if is_exists:
                    filesize = os.path.getsize(path+'\\'+string)
                    if filesize == 0:
                        os.remove(path+'\\'+string)
                        is_exists = False
                    elif str1 == 'jpg':
                        f = open(path+'\\'+string, 'rb')
                        f.seek(-2, 2)
                        if f.read() != '\xff\xd9':
                            f.close()
                            os.remove(path+'\\'+string)
                            is_exists = False
                        else:
                            f.close()
                    else:
                        pass'''
                if not is_exists:
                    try:
                        pic = s.get(originaltu, timeout=180)
                        fp = open(path + path_break + string, 'wb')
                        fp.write(pic.content)
                        fp.close()  # 保存图片
                        print(i+'-'+str(b) + ' download is Success')
                        b += 1
                    except requests.exceptions.ConnectionError:
                        print('Read timed out.')
                else:
                    b += 1
            self.done += 1
        self.runing.remove(threading.current_thread())


if __name__ == "__main__":
    p = Pixiv()
    help_message = "BBBBBBBBBBBBBBBBBBBBBBBBBBBB\n"\
                   "BBBBBBBB              BBBBBB\n"\
                   "BBBBB    BBBBBBBBBBB    BBBB\n"\
                   "BBB     BBBBBBBBBBBBBB   BBB\n"\
                   "B   B#  BBBBBBBBBBBBBBB   BB\n"\
                   "B  BB#  BBBBBBBBBBBBBBB    B\n"\
                   "BB#BB#  BBBBBBBBBBBBBBB#   B\n"\
                   "BBBBB#  BBBBBBBBBBBBBBB-   B\n"\
                   "BBBBB#  BBBBBBBBBBBBBBB    B\n"\
                   "BBBBB#  BBBBBBBBBBBBBB    BB\n"\
                   "BBBBB#  BBBBBBBBBBBBB    BBB\n"\
                   "BBBBB#    BBBBBBBBB    BBBBB\n"\
                   "BBBBB#  BB          BBBBBBBB\n"\
                   "BBBBB#  BBBBBBBBBBBBBBBBBBBB\n"\
                   "BBBBB#  BBBBBBBBBBBBBBBBBBBB\n"\
                   "BBBB      BBBBBBBBBBBBBBBBBB\n"\
                   "BBBBBBBBBBBBBBBBBBBBBBBBBBBB"\
                   "\n\npixiv.py -m <mod> -i <inform>\n         -r <r18>    enable r18(disable for daily mod)\n" \
                   "         -t <thread> enable threads\nmod:\nlogin    login to pixiv     -i:pid        " \
                   "-p <password>\nnormal    daily download     -i:date\nhighlike keyword download   -i:keyword    " \
                   "-l <leastlike>\ndatabase database download  -i:keyword    -l <leastlike> (need builded database)" \
                   "\npainter  painter download   -i:painterid\nbookmark bookmark download  -i:painterid"

    mod = ""
    type = ""
    inform = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrtam:i:l:p:",
                                   ["help", "r18", "thread", "async", "type=" 
                                   "mod=", "inform=", "leastlike=", "password="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == ('-h', "help"):
            print(help_message)
            sys.exit()
        elif opt in ("-m", "--mod"):
            mod = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-i", "--inform"):
            inform = arg
        elif opt in ("-l", "--leastlike"):
            p.least_likes = int(arg)
        elif opt in ("-r", "--r18"):
            p.r18 = True
        elif opt in ("-a", "--async"):
            p.async_able = True
        elif opt in ("-t", "--thread"):
            p.threads = True
        elif opt in ("-p", "--password"):
            p.password = arg
        
    p.cookies = get_cookies(p.pid, p.password)
            
    if mod == "normal":
        p.type = type
        p.date = inform
        p.sdate = p.date
        p.daily_download()
    elif mod == "highlike":
        p.keyword = inform
        p.highlink_download()
    elif mod == 'database':
        p.keyword = inform
        p.db_download()
    elif mod == 'bdb':
        s = db.BookmarkSpider(p.cookies)
        s.build_pool()
        s.run()
    elif mod == "painter":
        p.id = inform
        p.painter_download()
    elif mod == "bookmark":
        p.id = inform
        p.painter_bookmark_download()
    elif mod == "login":
        p.pid = inform
        get_cookies(p.pid, p.password, login=True)
    else:
        print(help_message)
    
    sys.exit(2)
