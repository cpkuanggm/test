# -*- coding:UTF-8 -*-
import requests, bs4
import os, time, random, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import closing
import urllib3


class QQManHua():
    def __init__(self):
        # 目标网页
        self.coute = 3
        self.target = 'https://f.wonderfulday28.live/forumdisplay.php?fid=21&page=' + str(
            self.coute)
        self.page = 'https://f.wonderfulday28.live/viewthread.php?tid=373570&extra=page%3D1'
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

        #selenium 网页元素
        self.imgtag = "image-big-text"
        self.imgmethod = "class"

        #requests网页元素
        self.tag = "div"
        self.tagstr = "class_"

        #re匹配
        self.pattern = "file="
    
    #设置随机headers
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

    #一页imgurls写入文件
    def getdownloadurl(self, imgurl, path, floder):
        with open(os.path.join(path, floder + '.txt'), 'w+') as f:
            for img in imgurl:
                f.write(img + '\n')

    #selenium方法驱动imgurls
    def getimgurl(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")  #设置允许不安全证书
        options.add_argument("headless")  #添加无头参数
        chrome = webdriver.Chrome(options=options)  # 获取浏览器对象
        chrome.implicitly_wait(2)
        imgs = []
        chrome.get(self.page)
        print(chrome.page_source)
        chrome.implicitly_wait(3)
        #chrome.execute_script('window.scrollTo(0,1000000)')#模拟鼠标滚轮
        elms = chrome.find_elements(self.imgmethod, self.imgtag)
        for elm in elms:
            imgs.append(elm.get_attribute('title'))
        return imgs

    #requests，re和bs4取得imgurls
    def getimgurlre(self, page, headers):
        res = requests.get(page, stream=True, verify=False, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        elms = soup.find_all("img", attrs={'file': True})  #查找<img 包含file属性的元素
        imgs = []
        pattern = 'http://pic.workgreat\d+?.live'
        for elm in elms:
            imgs.append(
                re.sub(pattern, 'https://f.wonderfulday28.live/',
                       elm.get('file')))
        return imgs

    def getpage(self):
        res = requests.get(
            self.target, stream=True, verify=False, headers=self.headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        elms = soup.find_all("td", class_='folder')  #查找td class='folder'
        pages = []
        for elm in elms:
            pages.append('https://f.wonderfulday28.live/' +
                         elm.a.get('href'))  #取其中的子项a的href属性
        return pages

    #一页每个url添加<img src="..."></img>
    def imgs2html(self, imgurls, path, floder):
        with open(os.path.join(path, floder + '.html'), 'w+') as f:
            for img in imgurls:
                f.write("<img src='" + img + "'></img>\n")


if __name__ == '__main__':
    urllib3.disable_warnings()
    path = "F://pw//"  #下载目录
    down = QQManHua()
    pages = down.getpage()
    for i in range(7, 10):
        down.coute = i
        for page in pages:
            floder = re.search(".*?tid=(.*?)&extra", page).group(1)
            imgurls = down.getimgurlre(page, down.headers)  #取得下载列表
            #os.makedirs(path + floder, exist_ok=True)  #建立图片目录
            down.imgs2html(imgurls, path, floder)  #每页imgurl重新生成html页面
            print(floder)
            time.sleep(random.randint(0, 5))  #设置随机停顿时间
            down.setheaders()#设置随机headers
