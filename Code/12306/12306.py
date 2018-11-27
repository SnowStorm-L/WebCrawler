#!/usr/local/bin/python3.6.5
# -*- coding: utf-8 -*-
# @Time    : 2018/11/13 PM2:54
# @Author  : L
# @Email   : L862608263@163.com
# @File    : 12306.py
# @Software: PyCharm

# 登录
# https://kyfw.12306.cn/otn/resources/login.html

# 单程
# https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=广州,GZQ&ts=深圳北,IOQ&date=2018-11-13&flag=N,N,Y

# 往返

# https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=wf&fs=广州南,IZQ&ts=北京,BJP&date=2018-11-13,2018-11-14&flag=N,N,Y

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import random

import time


class RailwayTickets:
    username = '123123123'
    pwd = '123123123'

    # 图宽 300, 高190
    # 刷新那个按钮 行高 30
    # start_x 300 / 4(列) / 2(中间点) = 37.5
    # start_y (190 - 30(刷新那个按钮 行高)) / 2(行) / 2(中间点) + 30(起始行高) = 70
    location_list = [ "%d,%d" % (38 + 38 * x, 70 + y * 80) for x in range(0, 7, 2)
                                                           for y in range(0, 2)]
    """
    1 3 5 7
    2 4 6 8
    """

    driver = webdriver.Chrome()

    def login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        # 等100秒找元素, 0.5秒找一次

        driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.CLASS_NAME, 'login-account')))

        driver.find_element_by_xpath("//*[@class = 'login-box']/ul/li[2]").click()

        driver.implicitly_wait(30)

        driverWait(driver, 100, 0.5).until(ec.visibility_of_element_located((By.ID, 'J-userName')))
        user_name = driver.find_element_by_id('J-userName')
        user_name.click()
        user_name.clear()
        user_name.send_keys(self.username)

        driverWait(driver, 100, 0.5).until(ec.visibility_of_element_located((By.ID, 'J-password')))
        password = driver.find_element_by_id('J-password')
        password.click()
        password.clear()
        password.send_keys(self.pwd)

        driver.implicitly_wait(30)

        login_img = driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.ID, 'J-loginImg')))

        get_captcha = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&%d" % random.uniform(1, 0)

        


        # for location in self.location_list:
        #     offset_x, offset_y = location.split(',')
        #     print('click offset_x %s offset_y %s' % (offset_x, offset_y))
        #     ActionChains(driver).move_to_element_with_offset(login_img, offset_x, offset_y).click().perform()

        # login = driver.find_element_by_xpath("//*[@id = 'J-login']")
        # login.click()

        # print(driver.page_source)
        # time.sleep(20)
        driver.close()


if __name__ == '__main__':
    check_tickets = RailwayTickets()
    check_tickets.login()
