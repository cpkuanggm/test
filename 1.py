from selenium import webdriver
import time

chrome = webdriver.Chrome(r"chromedriver.exe")  # 获取浏览器对象
print("chrome成功")
chrome.get('http://www.baidu.com/')
time.sleep(3)