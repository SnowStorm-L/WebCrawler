#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/14 PM6:18
# @Author  : L
# @Email   : L862608263@163.com
# @File    : ishadow.py
# @Software: PyCharm

import re
import urllib.request
import urllib.response
from biplist import *


class AutoChangeServer:
    url = "https://my.ishadowx.net/#"
    # 桌面复制的配置文件路径,在这个路径的文件读取 把代码写完成在换正式路径
    # 否则可能损坏配置文件
    preference_plist_path = "/Users/l/Desktop/com.jumboapps.shadowsocksx.plist"

    # 这个是配置文件路径
    # "/Users/l/Library/Preferences/com.jumboapps.shadowsocksx.plist"

    def open_preference_plist(self):
        try:
            plist = readPlist(self.preference_plist_path)
            # print(plist)
        except Exception as e:
            print("Not a plist:", e)

        relation_dict = plist
        server_list = relation_dict["key.server.list"]
        for each_line in server_list:
            # 这里是个数组
            # 数组里面每个data,都可以通过Xcode,ObjC的writeToFile函数,写入一个plist文件里面,打开查看
            print(each_line)

    def run(self):
        response_html = self.url_open(self.url).decode('utf-8')

        ip_list = re.findall('IP Address:<span id="ip[a-z]{3,4}">(.*?)</span>', response_html)

        print(ip_list)

        port_list = re.findall('Port:<span id="port[a-z]{3,4}">([0-9]{5})', response_html)

        print(port_list)

        password_list = re.findall('<span id="pw[a-z]{3,4}">([a-z.\-0-9]{1,17})', response_html)

        print(password_list)

    @staticmethod
    def url_open(url, data=None):
        request = urllib.request.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                           'Version/11.1 Safari/605.1.15')
        response = urllib.request.urlopen(request, data)
        return response.read()


if __name__ == "__main__":
    auto_change_server = AutoChangeServer()
    auto_change_server.open_preference_plist()
