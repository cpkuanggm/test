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
import threading


class QQManHua():
    def __init__(self):
        # 目标网页
        self.coute = 2
        self.index = 'https://f.wonderfulday28.live/'

        self.page = self.index + 'forumdisplay.php?fid=21&page=2'
        self.target = self.index + 'forumdisplay.php?fid=21&page={0}'.format(
            str(self.coute))
        self.title = ""

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

        # selenium 网页元素
        self.imgtag = "image-big-text"
        self.imgmethod = "class"

        # requests网页元素
        self.tag = "div"
        self.tagstr = "class_"

        # re匹配
        self.pattern = "file="

    def settarget(self):
        self.target = self.index + 'forumdisplay.php?fid=21&page={0}'.format(
            str(self.coute))

    # 设置随机headers
    def setheaders(self):
        self.headers = {'User-Agent': random.choice(self.USER_AGENT_LIST)}

    # 根据imgurl 下载图片
    def downloadimg(self, imgurl, floder, i):
        with closing(
                requests.get(
                    imgurl, stream=True, verify=False,
                    headers=self.headers)) as r:
            with open(os.path.join(floder, str(i) + '.jpg'), 'ab+') as f:
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
        #++print(chrome.page_source)
        chrome.implicitly_wait(3)
        # chrome.execute_script('window.scrollTo(0,1000000)')#模拟鼠标滚轮
        elms = chrome.find_elements(self.imgmethod, self.imgtag)
        for elm in elms:
            imgs.append(elm.get_attribute('title'))
        return imgs

    # requests，re和bs4取得imgurls
    def getimgurlre(self, page, headers):
        res = requests.get(page, stream=True, verify=False, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        self.title = soup.find_all("h1")[0].text.encode("ISO-8859-1").decode(
            'UTF-8')  # 内容转换编码
        #print(self.title)
        elms = soup.find_all("img", attrs={'file': True})  # 查找<img 包含file属性的元素
        imgs = []
        pattern = 'http://pic.workgreat\d+?.live'
        for elm in elms:
            try:
                imgs.append(re.sub(pattern, self.index, elm.get('file')))
            except:
                print("没有img")

        return imgs

    def getpage(self):
        res = requests.get(
            self.target, stream=True, verify=False, headers=self.headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        elms = soup.find_all("td", class_='folder')  # 查找td class='folder'
        pages = []
        for elm in elms:
            try:
                pages.append(self.index + elm.a.get('href'))  # 取其中的子项a的href属性
            except:
                print("没有链接")
                continue
        return pages

    # 一页每个url添加<img src="..."></img>
    def imgs2html(self, imgurls, path, floder, page):
        with open(os.path.join(path, floder + '.html'), 'w+') as f:
            f.write("<a href='{0}'>{1}</a><p></p>".format(page, self.title))
            for img in imgurls:
                f.write("<img src='" + img + "'></img><p></p>")


def get99img(start, end):
    urllib3.disable_warnings()
    path = "F://pw//"  # 下载目录
    # 判断是否存在path目录
    os.makedirs(path, exist_ok=True)
    down = QQManHua()
    for i in range(start, end):
        down.coute = i
        down.settarget()
        pages = down.getpage()
        if pages != None:
            for page in pages:
                # floder = re.search(".*?tid=(.*?)&extra", page).group(1)  # 取文件夹名
                imgurls = down.getimgurlre(page, down.headers)  # 取得下载列表
                floder = down.title.replace('\t', '')
                os.makedirs(path + floder, exist_ok=True)  #建立图片目录
                down.imgs2html(imgurls, path, floder,page)  # 每页imgurl重新生成html页面
                i = 1
                for imgurl in imgurls:
                    down.downloadimg(imgurl, path + floder, i)
                    i += 1
                #print(floder)
                time.sleep(random.randint(0, 3))  # 设置随机停顿时间
                down.setheaders()  # 设置随机headers


if __name__ == '__main__':

    threads = []
    b = 1 #步长
    for i in range(1, 3, b):
        t = threading.Thread(target=get99img, args=(i, i + b))
        threads.append(t)
        t.start()
