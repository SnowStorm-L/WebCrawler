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

import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from PIL import Image

import random
import base64
import time


# class RailwayTickets:
#     username = '123123123'
#     pwd = '123123123'
#
#     # 图宽 300, 高190
#     # 刷新那个按钮 行高 30
#     # start_x 300 / 4(列) / 2(中间点) = 37.5
#     # start_y (190 - 30(刷新那个按钮 行高)) / 2(行) / 2(中间点) + 30(起始行高) = 70
#     location_list = [ "%d,%d" % (38 + 38 * x, 70 + y * 80) for x in range(0, 7, 2)
#                                                            for y in range(0, 2)]
#     """
#     1 3 5 7
#     2 4 6 8
#     """
#
#     driver = webdriver.Chrome()
#
#     handler_set = set()
#
#     def login(self):
#         driver = self.driver
#         driver.maximize_window()
#         driver.set_page_load_timeout(60)
#
#         time.sleep(5)
#
#         try:
#             driver.get("https://kyfw.12306.cn/otn/resources/login.html")
#         except selenium.common.exceptions.TimeoutException:
#             print("time out of 60 s")
#             driver.execute_script('window.stop()')
#
#         while driver.current_url != 'https://kyfw.12306.cn/otn/resources/login.html':
#             driver.refresh()
#
#         # 等100秒找元素, 0.5秒找一次
#
#         driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.CLASS_NAME, 'login-account')))
#
#         driver.find_element_by_xpath("//*[@class = 'login-box']/ul/li[2]").click()
#
#         driver.implicitly_wait(30)
#
#         driverWait(driver, 100, 0.5).until(ec.visibility_of_element_located((By.ID, 'J-userName')))
#         user_name = driver.find_element_by_id('J-userName')
#         user_name.click()
#         user_name.clear()
#         user_name.send_keys(self.username)
#
#         driverWait(driver, 100, 0.5).until(ec.visibility_of_element_located((By.ID, 'J-password')))
#         password = driver.find_element_by_id('J-password')
#         password.click()
#         password.clear()
#         password.send_keys(self.pwd)
#
#         driver.implicitly_wait(30)
#
#         # 获取验证码图片, 写入本地
#
#         # 图片元素加载
#         driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.ID, 'J-loginImg')))
#
#         # # 图片
#         login_img_src = driver.find_element_by_xpath("//*[@id = 'J-loginImg']").get_attribute("src")
#         split_index = login_img_src.find(',')
#         base64_str = login_img_src[split_index + 1:]
#
#         # 切图
#         # 切成 7份  一份标题  6份内容
#         img_data = base64.b64decode(base64_str)
#
#         origin_img_name = 'origin_img.png'
#
#         file = open(origin_img_name, 'wb')
#         file.write(img_data)
#         file.close()
#         # width 293 height 190
#
#         # 第一张 头部 width 293 30
#
#
#
#
#
#
#
#
#         # crop_list.append((0, 0, 292, 30))
#         #
#         # for index, crop_tuple in enumerate(crop_list):
#
#
#
#         time.sleep(5)
#
#         # 识别图片
#         open_google_vision_js = 'window.open("https://cloud.google.com/vision/")'
#         driver.execute_script(open_google_vision_js)
#
#         time.sleep(2)
#
#         driver.switch_to.window(driver.window_handles[-1])
#
#         # 有时换过去 页面没加载出来
#         time.sleep(2)
#
#         print(driver.current_url)
#
#         print(driver.page_source[:300])
#
#         driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.ID, 'vision_demo_section')))
#         js_code = "var a = document.documentElement.scrollTop=750"
#         driver.execute_script(js_code)
#         iframe = driver.find_element_by_xpath("//*[@id = 'vision_demo_section']").find_element_by_tag_name('iframe')
#         driver.switch_to.frame(iframe)
#         driverWait(driver, 100, 0.5).until(ec.presence_of_element_located((By.ID, 'input')))
#         input_img = driver.find_element_by_xpath("//*[@id = 'input']")
#         input_img.send_keys("/Users/l/Desktop/WebCrawler/Code/12306/login_img.jpg")
#
#         # 点击验证码
#         # for location in self.location_list:
#         #     offset_x, offset_y = location.split(',')
#         #     print('click offset_x %s offset_y %s' % (offset_x, offset_y))
#         #     ActionChains(driver).move_to_element_with_offset(login_img, offset_x, offset_y).click().perform()
#
#         # 点击登录
#         # login = driver.find_element_by_xpath("//*[@id = 'J-login']")
#         # login.click()
#
#         # print(driver.page_source)
#         # time.sleep(20)
#         # driver.close()




if __name__ == '__main__':
    # check_tickets = RailwayTickets()
    # check_tickets.login()

        clip_img = Image.open("origin_img.png")

        img_width = clip_img.size[0]
        img_height = clip_img.size[1]

        region = (0, 0, img_width, 30)

        clip_img.crop(region)

        # 裁切图片
        cropImg = clip_img.crop(region)

        # 保存裁切后的图片
        cropImg.save("0.png")

        # (0, 30, 70, (30 + 80)) 第一张

        regin1 = (0, 30, img_width, img_height)
        clip_img.crop(regin1)
        cropImg = clip_img.crop(regin1)

        # 保存裁切后的图片
        cropImg.save("1.png")

        img = Image.open("1.png")

        xx = 3
        yy = 2
        width, height = img.size

        item_width = int(width / 3) - 20
        item_height = int(height / 2)

        box_list = []

        for i in range(3):
            for j in range(2):
                # 切图区域是矩形，位置由对角线的两个点(左上和右下)确定
                # (j + 1) * (i + 1)
                box = (i * item_width, j * item_width, (i + 1) * 70, (j + 1) * 80)
                print(box)
                box_list.append(box)
                cropImg = img.crop(box)
                cropImg.save("%d_%d.png" % (i, j))


        # location_list = ["%d,%d" % (38 + 38 * x, 70 + y * 80) for x in range(0, 7, 2)
        #          for y in range(0, 2)]
        #
        #
        # for idx, element in enumerate(location_list):
        #     xy = element.split(",")
        #     x = int(xy[0])
        #     y = int(xy[1])
        #     region = (x-38, y-70+30, 70, 110)
        #     print(region)
        #     cropImg = clip_img.crop(region)
        #     cropImg.save("%d.png" % (idx+1))







