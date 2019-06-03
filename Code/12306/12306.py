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

import os
import re
from PIL import Image
import base64


class RailwayTickets:
    username = '123123123'
    pwd = '123123123'

    url_of_12306 = "https://kyfw.12306.cn/otn/resources/login.html"

    # 图宽 300, 高190
    # 刷新那个按钮 行高 30
    # start_x 300 / 4(列) / 2(中间点) = 37.5
    # start_y (190 - 30(刷新那个按钮 行高)) / 2(行) / 2(中间点) + 30(起始行高) = 70
    location_list = ["%d,%d" % (38 + 38 * x, 70 + y * 80) for x in range(0, 7, 2)
                     for y in range(0, 2)]
    """
    1 3 5 7
    2 4 6 8
    """

    splitted_img_list = []
    img_content_list = []

    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-site-isolation-trials")

        # service_args=["--verbose", "--log-path=/Users/l/desktop/log.log"] 桌面输出Chrome运行的log
        self.browser = webdriver.Chrome(options=options)

        self.browser.maximize_window()

        self.wait = driverWait(self.browser, 100, 0.5)

    def get_verify_img(self):
        self.browser.get(self.url_of_12306)
        self.browser.find_element_by_xpath("//*[@class = 'login-box']/ul/li[2]").click()

        # 等待验证码图片加载
        self.wait.until(ec.visibility_of_element_located((By.ID, 'J-loginImg')))

        # 图片
        login_img_src = self.browser.find_element_by_id("J-loginImg").get_attribute("src")

        img_data = self.get_img_base64_data(login_img_src)

        origin_img_name = 'origin_img.png'

        with open(origin_img_name, 'wb') as origin_img:
            origin_img.write(img_data)
            origin_img.close()
            self.crop_img(origin_img_name)

    def img_recognition(self):
        open_google_vision_js = 'window.open("https://cloud.google.com/vision/")'

        self.browser.execute_script(open_google_vision_js)

        self.wait.until(ec.number_of_windows_to_be(2))

        self.browser.switch_to.window(self.browser.window_handles[-1])

        self.wait.until(ec.visibility_of_element_located((By.ID, 'vision_demo_section')))

        self.browser.execute_script("window.scrollTo(0, 750)")

        iframe = self.browser.find_element_by_xpath("//iframe[contains(@height,'150px')]")

        self.browser.switch_to.frame(iframe)

        self.wait.until(ec.presence_of_element_located((By.ID, 'input')))

        input_img = self.browser.find_element_by_id("input")

        input_img.send_keys(self.splitted_img_list[0])

        self.wait.until(ec.visibility_of_element_located((By.ID, "exit")))

        text_list = list(re.findall('"symbol style-scope vs-document">(.*?)</span>', self.browser.page_source))
        discern_result = ''.join(text_list)[9:]

        print(discern_result)

        # self.browser.find_element_by_xpath("//*[@id = 'exit']").click()

        # span class word style-scope vs-document
        # for idx in self.splitted_img_list:
        #     input_img.send_keys(self.splitted_img_list[0])

    def crop_img(self, img_path):
        current_work_path = os.getcwd() + "/"

        origin_img = Image.open(current_work_path + img_path)

        img_width, img_height = origin_img.size

        top_rect = (0, 0, img_width, 30)

        rect_list = [(5 * (x + 1) + 67 * x, 40 + y * 72, 72 * (x + 1), 107 + y * 72) for y in range(0, 2)
                     for x in range(0, 4)]
        rect_list.insert(0, top_rect)

        for idx, element in enumerate(rect_list):
            img = origin_img.crop(element)
            img_name = "%d.png" % idx
            img.save(img_name)
            self.splitted_img_list.append(current_work_path + img_name)

    @staticmethod
    def get_img_base64_data(origin_str):
        split_index = origin_str.find(',')

        base64_str = origin_str[split_index + 1:]

        return base64.b64decode(base64_str)

    def login(self):
        self.wait.until(ec.visibility_of_element_located((By.ID, "J-userName")))
        self.wait.until(ec.visibility_of_element_located((By.ID, "J-password")))

        # user_name = browser.find_element_by_id('J-userName')
        # user_name.send_keys(self.username)
        #
        # password = browser.find_element_by_id('J-password')
        # password.send_keys(self.pwd)

        # # 点击验证码
        # for location in self.location_list:
        #     offset_x, offset_y = location.split(',')
        #     print('click offset_x %s offset_y %s' % (offset_x, offset_y))
        #     ActionChains(driver).move_to_element_with_offset(login_img, offset_x, offset_y).click().perform()
        #
        # # 点击登录
        # login = driver.find_element_by_xpath("//*[@id = 'J-login']")
        # login.click()
        #
        # print(driver.page_source)
        # time.sleep(20)

        # browser.quit()


if __name__ == '__main__':
    check_tickets = RailwayTickets()
    check_tickets.get_verify_img()
    check_tickets.img_recognition()
