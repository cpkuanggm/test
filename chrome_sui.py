# encoding=utf8

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import xlrd
import datetime


# 日期数据转换  datatime ->2019.01.30 15:29
def datetime2str(dt):
    str_c = datetime.datetime.strftime(dt, '%Y.%m.%d %H:%M')
    return str_c


def fitem2(menu1=[], data="早午晚餐"):
    for item2 in menu1:
        if item2[0] == data:
            break
    return item2


def fitem1(menu1=[], item2_2="1"):
    for item1 in menu1:
        if item1[2] == item2_2:
            break
    return item1


class excel_read:
    def __init__(self,
                 excel_path=r'suiinput\twomenu.xls',
                 encoding='utf-8',
                 index=0):

        self.data = xlrd.open_workbook(excel_path)  # 获取文本对象
        self.table = self.data.sheets()[index]  # 根据index获取某个sheet
        self.rows = self.table.nrows  # 3获取当前sheet页面的总行数,把每一行数据作为list放到 list


# 数据转为列表

    def get_data(self):
        result = []
        for i in range(self.rows):
            col = self.table.row_values(i)  # 获取每一列数据

            result.append(col)
        # print(result)
        return result


class input_pay:
    def __init__(self):
        self.chrome = webdriver.Chrome(r"chromedriver.exe")  # 获取浏览器对象
        print("chrome成功")


# 分类

    def input_levelSelect(self,
                          id="levelSelect-payout",
                          menu1="ls-li-payout-2032594114994",
                          menu2=" ls-li-payout-2032594114979"):
        self.chrome.find_element_by_id(id).click()
        input = self.chrome.find_element_by_id(menu1)
        hover = ActionChains(self.chrome).move_to_element(input)  # 找到元素
        hover.perform()  # 悬停
        self.chrome.find_element_by_id(menu2).click()

    def sendkeys_byid(self, id, keys, *args):
        input = self.chrome.find_element_by_id(id)
        input.clear()
        input.send_keys(str(keys))

    def click_byid(self, id, *args):
        self.chrome.find_element_by_id(id).click()

    def click_bylinktext(self, a='首页', *args):
        self.chrome.find_element_by_link_text(a).click()

    def onemenu(self, id='tb-member_text', *args):
        self.chrome.find_element_by_id(id).click()
        # time.sleep(1)
        self.chrome.find_element_by_id("tb-member_v_2032594115044").click()

    def types(self, data3):
        if data3 == 'sendkeys':
            return self.sendkeys_byid
        if data3 == 'onemenu':
            return self.onemenu
        if data3 == 'twomenu':
            return self.input_levelSelect

if __name__ == '__main__':

    url = "https://login.sui.com/"
    user = "156875464@qq.com"
    passwrod = "a82867049"

    chrome = input_pay()
    chrome.chrome.implicitly_wait(10)
    chrome.chrome.get(url)

    chrome.sendkeys_byid("email", user)
    chrome.sendkeys_byid("pwd", passwrod)

    chrome.click_byid('loginSubmit')

    chrome.click_bylinktext('记一笔')

    # 导入控制流（）
    ctrls = excel_read(excel_path=r'suiinput\ctrls.xls').get_data()
    # print(ctrls)

    # 导入分类菜单
    menu1 = excel_read().get_data()
    menu2 = excel_read(index=1).get_data()

    # 导入datas
    datas = excel_read(excel_path=r'suiinput\datas.xls').get_data()
    # print(datas)

    # 创建日志文件
    t_str = time.strftime("%Y%m%d%H%M", time.localtime())
    filename = 'suioutput\\' + t_str + '.log'
    filelog = open(filename, 'a')
    i = 1
    for data in datas:

        chrome.sendkeys_byid(id=ctrls[0][1], keys=data[0])  # 日期
        chrome.sendkeys_byid(ctrls[1][1], data[1])  # 金额

        # 查找分类一级目录
        for item2 in menu2:
            if item2[0] == data[2]:
                break
        for item1 in menu1:
            if item1[2] == item2[2]:
                break

        chrome.input_levelSelect(id=ctrls[2][1],
                                 menu1=item1[1],
                                 menu2=item2[1])  # 分类

        chrome.onemenu()  # 成员
        chrome.sendkeys_byid(ctrls[3][1], data[3])  # 备注
        # 保存
        #chrome.click_byid('tb-save')
        # 保存成功，写入日志
        filelog.write(str(i) + ',' + data[0] + '\n')
        i = i + 1

    filelog.close()
