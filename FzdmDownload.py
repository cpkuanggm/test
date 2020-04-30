# -*- coding:UTF-8 -*-
import requests
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from contextlib import closing


class FzdmDownload():
    def __init__(self):
        self.floder = 'fzdm'  # 保存路径

       # 目标网页
        self.target = 'https://www.fzdm.com/manhua/132/174//index_21.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

       # 网页元素
        self.imgtag = "//*[@id='mhpic']"
        self.imgmethod = "xpath"

    # 根据imgurl 下载图片
    def downloadimg(self,imgurl, headers, floder, i):
        with closing(requests.get(imgurl, stream=True, verify=False, headers=headers)) as r:
            with open(os.path.join(floder, str(i)+'.jpg'), 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    def getimgurl(self):
        chrome = webdriver.Chrome(r"chromedriver.exe")  # 获取浏览器对象
        chrome.implicitly_wait(10)
        imgs = []
        target=self.target
        for i in range(100):
            chrome.get(target)
            chrome.implicitly_wait(10)
            last=chrome.find_element("xpath","//*[@id='pjax-container']/div[2]")
            print(last.text.find("最后一页了"))
            elm = chrome.find_element(self.imgmethod, self.imgtag)
            imgs.append(elm.get_attribute('src'))
            try: 
                a = chrome.find_element("link text", "下一页")
                target = a.get_attribute("href")
            except:
                print("共%d页" % (i+1)) 
                break
        return imgs

    def downone():
        pass


if __name__ == '__main__':
    down = FzdmDownload()
    imgurls = down.getimgurl()

    os.makedirs(down.floder, exist_ok=True)
    i = 0
    for img in imgurls:
        i += 1
        down.downloadimg(img, down.headers, down.floder, i)
