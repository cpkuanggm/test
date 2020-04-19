# encoding=utf8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import xlrd
import datetime

url = "https://www.sui.com/"
user = "***"
passwrod = "***"

chrome = webdriver.Chrome(r"chromedriver.exe")  # 获取浏览器对象
chrome.implicitly_wait(10)
chrome.get(url)

chrome.find_element("link text", "记账").click()
chrome.find_element("link text", "记一笔").click()

lsinput = chrome.find_element('id', "levelSelect-payout")
lsinput.click()
lsinput1 = lsinput.find_element("xpath", "//*[@title='衣服饰品']")
lsinput1.click()
lsinput1.find_element("xpath", "//*[@title='衣服裤子']").click()
