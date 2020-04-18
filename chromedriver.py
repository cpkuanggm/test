# -*- coding:utf-8 -*-
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait

url = "https://login.sui.com/"
user = "***"
passwrod = "****"

chrome = webdriver.Chrome(r"chromedriver.exe")
chrome.implicitly_wait(10) 
chrome.get(url)

input = chrome.find_element_by_id("email")
input.send_keys(user)
input = chrome.find_element_by_id("pwd")
input.send_keys(passwrod)
button = chrome.find_element_by_id('loginSubmit')
button.click()


tally = chrome.find_element_by_link_text('记一笔')
tally.click()


#金额
input = chrome.find_element_by_id("tb-outMoney-1")
input.send_keys(123)


#成员
chrome.find_element_by_id("tb-member_text").click()
input = chrome.find_element_by_id("ul_tb-member")
input.find_element_by_id("tb-member_v_2032594115044").click()

#时间
input = chrome.find_element_by_id("tb-datepicker")
input.clear()
input.send_keys("2019.11.05 22:56")

#分类
chrome.find_element_by_id("levelSelect-payout").click()

input = chrome.find_element_by_id("ls-li-payout-2032594114994")
hover = ActionChains(chrome).move_to_element(input)  #找到元素
hover.perform()  #悬停

chrome.find_element_by_id("ls-li-payout-2032594114995").click()
