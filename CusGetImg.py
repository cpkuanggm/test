# -*- coding:UTF-8 -*-
import requests
import bs4
import os
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import closing
import urllib3


class CusGetImg():
    def __init__(self):
        # 目标网页
        self.coute = 2
        self.index = 'https://manhua.fzdm.com/'

        self.page = self.index+'1/brc30/index_8.html'
        self.target = self.index+'1/brc30/index_' + str(
            self.coute)+'.html'
        self.title = "1"

        # selenium 网页元素
        self.imgtag = "image-big-text"
        self.imgmethod = "class"

        # requests网页元素
        self.pagetag = 'a'
        self.pagetagstr = 'readlink'
        self.imgtag = 'span'
        self.imgtagstr = 'f12'

        # re匹配
        self.pattern = ""

        self.USER_AGENT_LIST = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.36",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
    # 设置页面

    def settarget(self):
        self.target = self.index+'thread-htm-fid-45-page-' + str(
            self.coute)+'.html'
    # 设置随机headers

    def setheaders(self):
        self.headers = {
            'User-Agent':
            random.choice(self.USER_AGENT_LIST)
        }

    # 根据imgurl 下载图片
    def downloadimg(self, imgurl, floder, i):
        with closing(
                requests.get(
                    imgurl, stream=True, verify=False,
                    headers=self.headers)) as r:
            with open(os.path.join("1", str(i) + '.jpg'), 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    # 一页imgurls写入文件
    def getdownloadurl(self, imgurl, path, floder):
        with open(os.path.join(path, floder + '.txt'), 'w+') as f:
            for img in imgurl:
                f.write(img + '\n')

    # selenium方法驱动imgurls
    def getimgurl(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")  # 设置允许不安全证书
        options.add_argument("headless")  # 添加无头参数
        chrome = webdriver.Chrome(options=options)  # 获取浏览器对象
        chrome.implicitly_wait(2)
        imgs = []
        chrome.get(self.page)
        print(chrome.page_source)
        chrome.implicitly_wait(3)
        # chrome.execute_script('window.scrollTo(0,1000000)')#模拟鼠标滚轮
        elms = chrome.find_elements(self.imgmethod, self.imgtag)
        for elm in elms:
            imgs.append(elm.get_attribute('title'))
        return imgs

    # 论坛requests，re和bs4取得imgurls
    def getimgurlre(self, page, headers):
        res = requests.get(page, stream=True, verify=False, headers=headers)
        res.raise_for_status()
        #print(res.encoding)#取response内容的编码
        #print(res.apparent_encoding)#取headers里设置的编码
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        self.title = soup.find_all("h1")[0].text.encode("ISO-8859-1").decode('GBK')  # 内容转换编码
        print(self.title)
        # 查找<img 包含file属性的元素
        elms = soup.find_all(self.imgtag, class_=self.imgtagstr)
        imgs = []
        # pattern = 'http://pic.workgreat\d+?.live' #正则表达式替换参数
        for elm in elms:
            imgs.append(elm.span.img.get('src'))
        return imgs

# 论坛返回每个主题页面url
    def getpage(self):
        res = requests.get(
            self.target, stream=True, verify=False, headers=self.headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        # 查找td class='folder'
        elms = soup.find_all(self.pagetag, attrs={'name': True})
        pages = []
        for elm in elms:
            pages.append(self.index +
                         elm.get('href'))  # 取其中的子项a的href属性            
        return pages

    # 一页每个url添加<img src="..."></img>
    def imgs2html(self, imgurls, path, floder):
        with open(os.path.join(path, floder + '.html'), 'w+', encoding='GBK') as f:
            f.write(self.title+"\n")
            for img in imgurls:
                f.write("<img src='" + img + "'></img>\n")
# 取99论坛 img   不包括end页


def get99img(start, end):
    urllib3.disable_warnings()
    path = "F://pw//"  # 下载目录
    # 判断是否存在path目录
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    down = CusGetImg()
    for i in range(start, end):
        down.coute = i
        down.settarget()        
        pages = down.getpage()
        
        for page in pages:
            #floder = re.search(".*?tid=(.*?)&extra", page).group(1)  # 取文件夹名
            floder=down.title
            imgurls = down.getimgurlre(page, down.headers)  # 取得下载列表
            # os.makedirs(path + floder, exist_ok=True)  #建立图片目录
            down.imgs2html(imgurls, path, floder)  # 每页imgurl重新生成html页面
            print(floder)
            #time.sleep(random.randint(0, 3))  # 设置随机停顿时间
            down.setheaders()  # 设置随机headers


if __name__ == '__main__':
    get99img(2, 3)
