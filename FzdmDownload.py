# -*- coding:UTF-8 -*-
import requests
import os, time, random
from selenium import webdriver
from contextlib import closing


class FzdmDownload():
    def __init__(self):
        self.floder = '1'  # 保存路径

        # 目标网页
        self.target = 'https://manhua.fzdm.com/153/5/'
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

        # 网页元素
        self.imgtag = "//*[@id='mhpic']"
        self.imgmethod = "xpath"

    # 根据imgurl 下载图片
    def downloadimg(self, imgurl, headers, floder, i):
        with closing(
                requests.get(
                    imgurl, stream=True, verify=False, headers=headers)) as r:
            with open(os.path.join(floder, str(i) + '.jpg'), 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    def getdownloadurl(self, imgurl, path):
        with open(os.path.join(path,
                               os.path.basename(path) + '.txt'), 'w+') as f:
            for img in imgurl:
                f.write(img + '\n')

    def getimgurl(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")  #设置允许不安全证书
        options.add_argument("headless")  #添加无头参数
        chrome = webdriver.Chrome(options=options)  # 获取浏览器对象
        chrome.implicitly_wait(2)
        imgs = []
        target = self.target
        for i in range(100):
            chrome.get(target)
            chrome.implicitly_wait(3)
            elm = chrome.find_element(self.imgmethod, self.imgtag)
            imgs.append(elm.get_attribute('src'))
            try:
                a = chrome.find_element("link text", "下一页")
                target = a.get_attribute("href")
            except:
                print("共%d页" % (i + 1))
                break
            time.sleep(random.randint(0, 5))  #设置随机停顿时间
        return imgs

    def downone():
        pass


if __name__ == '__main__':    
    path = "F://鬼灭之刃//"
    down = FzdmDownload()
    imgurls = down.getimgurl()
    print(imgurls)
    os.makedirs(path + down.floder, exist_ok=True)   
    down.getdownloadurl(
        imgurls,
        path + down.floder,
    )
    
