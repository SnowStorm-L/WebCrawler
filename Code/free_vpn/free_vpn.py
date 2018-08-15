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


# NOTE Base64解码

# 在解码前，如果字符串中有包含 – 和 _ 的字符，要先分别替换为 + 和 /

# NOTE ss 链接构成

# 在 Base64 编码之前，ss链接的格式是这样的：
# ss://method:password@server:port
# 也就是说，一般我们见到的链接就是 ss://Base64编码字段
# 其中 method:password@server:port 这部分被进行了 Base64 编码

# demo
# 例如有一个这样的ss链接 ss://Y2hhY2hhMjA6ZG91Yi5pby9zc3poZngvKmRvdWIuYmlkL3NzemhmeC8qMjk4N0A2NC4xMzcuMjI5LjE1NDoyOTg3

# 那么以下的这部分字符串就是经过 Base64 编码生成的：
# Y2hhY2hhMjA6ZG91Yi5pby9zc3poZngvKmRvdWIuYmlkL3NzemhmeC8qMjk4N0A2NC4xMzcuMjI5LjE1NDoyOTg3

# 上面的字符串，base64解码出来就是（相对应的就是加密方法、密码、ip、端口:(以:或@分割)
# chacha20 : doub.io/sszhfx/*doub.bid/sszhfx/*2987 @ 64.137.229.154 : 2987

# NOTE ssr 链接构成

# 在 Base64 编码之前，ssr链接的格式是这样的：
# ssr://server:port:protocol:method:obfs:password_base64/?params_base64

# demo
# ssr://NjQuMTM3LjIwMS4yNDY6Mjk4NzphdXRoX3NoYTFfdjQ6Y2hhY2hhMjA6dGxzMS4yX3RpY2tldF9hdXRoOlpHOTFZaTVwYnk5emMzcG9abmd2S21SdmRXSXVZbWxrTDNOemVtaG1lQzhxTWprNE53Lz9yZW1hcmtzPTVweXM2TFNtNVktMzVwMmw2SWVxT21SdmRXSXVhVzh2YzNONmFHWjRMLW1Wbk9XRGotV2ZuLVdRalRwa2IzVmlMbUpwWkM5emMzcG9abmd2

# 没有需要替换的(_和-符号), 直接base64解码, 得到如下字符串

# 其中这些都已经很明显了 server:port:protocol:method:obfs:   (obfs: 混淆模式)

# 64.137.201.246:2987:auth_sha1_v4:chacha20:tls1.2_ticket_auth:ZG91Yi5pby9zc3poZngvKmRvdWIuYmlkL3NzemhmeC8qMjk4Nw/?remarks=5pys6LSm5Y-35p2l6IeqOmRvdWIuaW8vc3N6aGZ4L-mVnOWDj-Wfn-WQjTpkb3ViLmJpZC9zc3poZngv

# 混淆模式之后就是密码了  (/?之前, obfs: 之后的这段)
# ZG91Yi5pby9zc3poZngvKmRvdWIuYmlkL3NzemhmeC8qMjk4Nw base64解码后得到 doub.io/sszhfx/*doub.bid/sszhfx/*2987

# params_base64 是协议参数、混淆参数、备注及Group对应的参数值被 base64编码 后拼接而成的字符串。
# 即 params_base64为这些字段的拼接：
# obfsparam=obfsparam_base64&protoparam=protoparam_base64&remarks=remarks_base64&group=group_base64

# 因为该字段只包含 remarks ，说明其余参数都为空
# 先把remarks不符合规则的 - 字符替换为 +
# 5pys6LSm5Y-35p2l6IeqOmRvdWIuaW8vc3N6aGZ4L-mVnOWDj-Wfn-WQjTpkb3ViLmJpZC9zc3poZngv

# base64_remarks 字符串如下
# 5pys6LSm5Y+35p2l6IeqOmRvdWIuaW8vc3N6aGZ4L+mVnOWDj+Wfn+WQjTpkb3ViLmJpZC9zc3poZngv

# base64解码后的内容如下
# 本账号来自:doub.io/sszhfx/镜像域名:doub.bid/sszhfx/

# 以上内容, 参考文章 https://coderschool.cn/2498.html

class Ishadowx:

    __url = "https://us.ishadowx.net"

    # 我用的是macbook, 所以替换方法是接下来的处理
    # 桌面复制的配置文件路径,在这个路径的文件读取 把代码写完成在换正式路径
    # 否则可能损坏配置文件
    __preference_plist_path = "/Users/l/Desktop/com.jumboapps.shadowsocksx.plist"

    # 这个是配置文件路径
    # "/Users/l/Library/Preferences/com.jumboapps.shadowsocksx.plist"

    def open_preference_plist(self):

        plist = readPlist(self.__preference_plist_path)

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
            port_list = re.findall('Port:<span id="port[a-z]{3,4}">([0-9]{5})', response_html)
            password_list = re.findall('<span id="pw[a-z]{3,4}">([a-z.\-0-9]{1,17})', response_html)
            print([{"ip": x, "port": y, "password": z} for x in ip_list for y in port_list for z in password_list])


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

                self.remake_ssr_list(re_ssr_list)
                self.remake_ss_list(re_ss_list)

    def remake_ss_list(self, re_ss_list):
        decode_list = [self.decode_base64(x) for x in re_ss_list if self.decode_base64(x) is not None]
        sub_list = [re.sub("[:@]", " ", x) for x in decode_list]
        key_list = ["method", "password", "server", "server_port"]
        value_list = list(map(lambda x: x.split(), sub_list))
        remake_result = [{key: value for key, value in zip(key_list, x)} for x in value_list]
        print(remake_result)

    def remake_ssr_list(self, re_ssr_list):
        decode_list = [self.decode_base64(x) for x in re_ssr_list if self.decode_base64(x) is not None]
        # /?后面都是些辅助参数, 例如混淆参数这些, 对实际获取连接ssr没太大作用
        # 如果非要解析出来, 可以按照ssr的构造说明去解析
        split_list = [x[:str(x).find("/?")] for x in decode_list]
        sub_list = [re.sub("[:]", " ", x) for x in split_list]
        value_list_with_encode_password = list(map(lambda x: x.split(), sub_list))
        decode_password_list = list(map(lambda x: self.decode_base64(x[-1]), value_list_with_encode_password))
        value_list = [x[:-1] for x in value_list_with_encode_password]
        key_list = ["server", "port", "protocol", "method", "obfs", "password"]
        for idx, element in enumerate(value_list):
            element.append(decode_password_list[idx])
        remake_result = [{key: value for key, value in zip(key_list, x)} for x in value_list]
        print(remake_result)

    @staticmethod
    def decode_base64(data):
        origin_data = data
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += '=' * missing_padding
        try:
            data = str(data).replace("–", "+").replace("_", "/")
            return base64.b64decode(data).decode('utf-8').replace("\n", "")
        except Exception as e:
            print('解密: %s 失败 \n失败原因: %s\n原始数据: %s' % (data, e, origin_data))
            return None


if __name__ == "__main__":
    # # ishadow的
    ishadow = Ishadowx()
    ishadow.run()

    # 某人博客的
    # blog = Blog()
    # blog.fetch_page()

    pass
