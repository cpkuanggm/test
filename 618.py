# -*- coding: utf-8 -*-
# 2018/09/05
# 淘宝秒杀脚本，扫码登录版
import os
from selenium import webdriver
import datetime
import time
from os import path
from selenium.webdriver.common.action_chains import ActionChains

d = path.dirname(__file__)
abspath = path.abspath(d)

driver = webdriver.Chrome()
#driver.maximize_window()
driver.implicitly_wait(10)
#账号密码
acc = "13928510457"
pwd = "06840018"

#2480显示器
carid1 = "//*[@id='product_1131222']/div[1]/div[1]/div/input"


def login():
    # 打开淘宝登录页，并进行扫码登录
    driver.get("https://www.jd.com")    
    if driver.find_element_by_link_text("你好，请登录"):
        driver.find_element_by_link_text("你好，请登录").click()

    if driver.find_element_by_link_text("账户登录"):
        driver.find_element_by_link_text("账户登录").click()

    driver.find_element_by_id("loginname").send_keys(acc)
    driver.find_element_by_id("nloginpwd").send_keys(pwd)

    print("请在10秒内完成扫码")
    time.sleep(10)

def getcar(carid):
    js = "window.open('https://cart.jd.com/cart.action')"
    driver.execute_script(js)
    driver.implicitly_wait(10)
    # 点击购物车里全选按钮

    try: 
       driver.find_element_by_xpath(carid).click()
    except:
        print('购物车没有id:{0}'.format(carid))
    #if driver.find_element_by_id("J_CheckBox_939558169627"):
    #     driver.find_element_by_id("J_CheckBox_939558169627").click()
    #if driver.find_element_by_name("toggle-checkboxes"):
    #    driver.find_element_by_name("toggle-checkboxes").click()
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(buytime):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now > buytime:
            try:
                # 点击结算按钮
                if driver.find_element_by_id("J_Go"):
                    driver.find_element_by_id("J_Go").click()
                driver.find_element_by_link_text('提交订单').click()
            except:
                time.sleep(0.1)
        print(now)
        time.sleep(0.1)


if __name__ == "__main__":
    #  times = input("请输入抢购时间：")
    # 时间格式："2018-09-06 11:20:00.000000" 
    login()
    getcar(carid1)
    #buy("2020-06-18 00:00:00.000000")
