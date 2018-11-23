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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import time


class RailwayTickets:
    username = ''
    pwd = ''
    driver = webdriver.Chrome()

    def login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        # 等100秒找元素, 0.5秒找一次
        WebDriverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.CLASS_NAME, 'login-account')))
        driver.find_element_by_xpath("//*[@class = 'login-box']/ul/li[2]").click()

        WebDriverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.ID, 'J-userName')))
        user_name = driver.find_element_by_id('J-userName')
        user_name.click()
        user_name.clear()
        user_name.send_keys(self.username)

        WebDriverWait(driver, 100, 0.5).until(ec.visibility_of_element_located((By.ID, 'J-password')))
        password = driver.find_element_by_id('J-password')
        password.click()
        password.clear()
        password.send_keys(self.pwd)

        img = driver.find_element_by_xpath("//*[@id = 'J-loginImg']")
        print(img)

        login = driver.find_element_by_xpath("//*[@id = 'J-login']")
        # login.click()

        # print(driver.page_source)
        driver.close()


if __name__ == '__main__':
    check_tickets = RailwayTickets()
    check_tickets.login()
