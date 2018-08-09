#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/14 PM6:18
# @Author  : L
# @Email   : L862608263@163.com
# @File    : free_vpn.py
# @Software: PyCharm

import re
import urllib.request
import urllib.response
from biplist import *
from urllib import error
import base64


def url_open(url, data=None):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/11.1 Safari/605.1.15')
    try:
        response = urllib.request.urlopen(request, data)
        return response.read().decode('utf-8')
    except error.URLError as e:
        print(e.reason)


class Ishadowx:
    # 2018,8,8 这个网址被封了
    __url = "https://my.ishadowx.net/#"
    # 桌面复制的配置文件路径,在这个路径的文件读取 把代码写完成在换正式路径
    # 否则可能损坏配置文件
    __preference_plist_path = "/Users/l/Desktop/com.jumboapps.shadowsocksx.plist"

    # 这个是配置文件路径
    # "/Users/l/Library/Preferences/com.jumboapps.shadowsocksx.plist"

    def open_preference_plist(self):
        try:
            plist = readPlist(self.__preference_plist_path)
            # print(plist)
        except Exception as e:
            print("Not a plist:", e)

        server_list = plist["key.server.list"]
        for each_line in server_list:
            # 这里是个数组
            # 数组里面每个data,都可以通过Xcode,ObjC的writeToFile函数,写入一个plist文件里面,打开查看
            # 剩下的工作就是怎么把数据替换进去了.
            # 我看其它端的配置文件都是json构造的, mac上plist文件存储,稍微不同 有空再继续研究
            print(each_line)

    def run(self):
        response_html = url_open(self.__url)

        if response_html is not None:
            ip_list = re.findall('IP Address:<span id="ip[a-z]{3,4}">(.*?)</span>', response_html)

            print(ip_list)

            port_list = re.findall('Port:<span id="port[a-z]{3,4}">([0-9]{5})', response_html)

            print(port_list)

            password_list = re.findall('<span id="pw[a-z]{3,4}">([a-z.\-0-9]{1,17})', response_html)

            print(password_list)


class Blog:

    def fetch_page(self):
        # 就不全部页拿了, 旧的估计也失效了
        # https://www.hinwen.com/page/2/?s=ssr
        html_string = url_open("https://www.hinwen.com/?s=ssr")

        if html_string is not None:
            detail_list = re.findall('href="(.*?)" rel="bookmark">免费SS/SSR分享', html_string)
            for detail_url in detail_list:
                detail_info = url_open(detail_url)
                re_ss_list = re.findall('ss://(.*?)</p>', detail_info)
                re_ssr_list = re.findall('ssr://(.*?)</p>', detail_info)
                # print(re_ssr_list)

                ss_list = self.remake_ss_list(re_ss_list)
                print(ss_list)

    def remake_ss_list(self, re_ss_list):
        decode_list = [self.decode_base64(x) for x in re_ss_list if self.decode_base64(x) is not None]
        sub_list = [re.sub("[:@]", " ", x) for x in decode_list]
        key_list = ["method", "password", "server", "server_port"]
        value_list = list(map(lambda x: x.split(), sub_list))
        remake_result = [{key: value for key, value in zip(key_list, x)} for x in value_list]
        return remake_result

    @staticmethod
    def decode_base64(data):
        """Decode base64, padding being optional.

        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.

        """
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += '=' * missing_padding
        try:
            return base64.b64decode(data).decode('utf-8').replace("\n", "")
        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    # # ishadow的
    # ishadow = Ishadowx()
    # ishadow.run()

    # 某人博客的
    blog = Blog()
    blog.fetch_page()
    #
    # tt = "aes-256-cfb:isx.yt-05379585@c.isxc.top:17568"
    # jj =
    # print()

    # print([x.split(":") for x in str.split("@")])
