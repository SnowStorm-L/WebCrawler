#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 PM4:59
# @Author  : L
# @Email   : L862608263@163.com
# @File    : google.py
# @Software: PyCharm

import json
import urllib
import urllib.request
import urllib.parse
import re


def url_open(url, data=None):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/11.1 Safari/605.1.15')
    response = urllib.request.urlopen(request, data)
    return response.read()


class TranslateGoogle:
    _tkk_url = "http://translate.google.cn/"
    _translate_url = "https://translate.google.cn/translate_a/single"

    def translate_word(self, translate_string):

        tk = self.get_tk(translate_string)
        print('请求需要的tk参数 ', tk)
        # 这里的字典有很多个dt的key, 按理说请求前就会被覆盖, 不知道有什么用
        # 'dt': 'bd', 'dt': 'ex', 'dt': 'ld', 'dt': 'md', 'dt': 'qca', 'dt': 'rw', 'dt': 'rm', 'dt': 'ss', 'dt': 't'
        data = {'client': 't', 'sl': 'auto', 'tl': 'en', 'hl': 'zh - CN', 'dt': 'at',
                'ie': 'UTF - 8',
                'oe': 'UTF - 8', 'source': 'bh', 'ssel': '0', 'tsel': '0', 'kc': '1', 'tk': str(tk),
                'q': translate_string}
        data = urllib.parse.urlencode(data).encode('utf-8')

        result = url_open(self._translate_url, data).decode('utf-8')
        print('翻译结果: ', json.loads(result))

    def get_tk(self, input_str):

        a = 4211913557
        b = -4140706334
        number = 422392

        e = "{0}.{1}".format(number, a + b).split('.')

        h = int(e[0]) or 0
        g = []
        for f in range(0, len(input_str)):
            c = ord(input_str[f])
            if 128 > c:
                g.append(c)
            else:
                if 2048 > c:
                    g.append(c >> 6 | 192)
                else:
                    if (0xd800 == (c & 0xfc00)) and \
                            (f + 1 < len(input_str)) and \
                            (0xfc00 == (ord(input_str[f + 1]) & 0xdc00)):
                        f += 1
                        c = 0x10000 + ((c & 0x3ff) << 10) + (ord(input_str[f]) & 0x3ff)
                        g.append(c >> 18 | 240)
                        g.append(c >> 12 & 63 | 128)
                    else:
                        g.append(c >> 12 | 224)
                        g.append(c >> 6 & 63 | 128)
                g.append(c & 63 | 128)

        input_str = h
        for d in range(len(g)):
            input_str += g[d]
            input_str = self.operation(input_str, '+-a^+6')
        input_str = self.operation(input_str, '+-3^+b+-f')
        input_str ^= int(e[1]) or 0
        if 0 > input_str:
            input_str = (input_str & (pow(2, 31) - 1)) + pow(2, 31)
        input_str %= pow(10, 6)
        return "%d.%d" % (input_str, input_str ^ h)

    # noinspection PyMethodMayBeStatic
    def operation(self, a, b):
        for d in range(0, len(b) - 2, 3):
            c = b[d + 2]
            c = ord(c[0]) - 87 if 'a' <= c else int(c)
            c = a >> c if '+' == b[d + 1] else a << c
            a = a + c & (pow(2, 32) - 1) if '+' == b[d] else a ^ c
        return a


# 谷歌翻译
# 重点是翻译时候的header里面需要tk这个键的值, 如果这个值不正确的话翻译请求是会被禁止的
# 这个tk的值的生成算法 可以在 https://translate.google.cn 审查元素 找到以下js代码
# go jfk-button-action 翻译按钮id
#    谷歌翻译 TKK 转换源js代码
#     sr = function(a, b)
#     {
#     for (var c = 0; c < b.length - 2; c += 3) {
#         var d = b.charAt(c + 2);
#     d = "a" <= d ? d.charCodeAt(0) - 87: Number(d);
#     d = "+" == b.charAt(c + 1) ? a >> > d: a << d;
#     a = "+" == b.charAt(c) ? a + d & 4294967295: a ^ d
#     }
#     return a
#     }, tr = null, ur = function(a)
#     {
#     if (null !== tr) var b = tr; else {
#     b = rr(String.fromCharCode(84));
#     var c = rr(String.fromCharCode(75));
#     b =[b(), b()];
#     b[1] = c();
#     b = (tr = window[b.join(c())] | | "") | | ""
#     }
#     var
#     d = rr(String.fromCharCode(116));
#     c = rr(String.fromCharCode(107));
#     d = [d(), d()];
#     d[1] = c();
#     c = "&" + d.join("") + "=";
#     d = b.split(".");
#     b = Number(d[0]) | | 0;
#     for (var e =[], f = 0, g = 0; g < a.length; g++) {
#         var l = a.charCodeAt(g);
#     128 > l ? e[f++] = l: (2048 > l ? e[f++] = l >> 6 | 192: (55296 == (l & 64512) & & g + 1 < a.length & & 56320 == (
#                 a.charCodeAt(g + 1) & 64512) ? (l = 65536 + ((l & 1023) << 10) + (a.charCodeAt(++g) & 1023), e[
#         f + +] = l >> 18 | 240, e[f + +] = l >> 12 & 63 | 128):
# e[f + +] = l >> 12 | 224, e[f + +] = l >> 6 & 63 | 128),
#     e[f + +] = l & 63 | 128)
#     }
#     a = b;
#     for (f = 0; f < e.length; f++) a += e[f], a = sr(a, "+-a^+6");
#     a = sr(a, "+-3^+b+-f");
#     a ^= Number(d[1]) | | 0;
#     0 > a & & (a = (a & 2147483647) + 2147483648);
#     a %= 1E6;
#     return c + (a.toString() + "." +
#                 (a ^ b))
#
# };

if __name__ == "__main__":
    translate = TranslateGoogle()
    translate.translate_word("我爱你")
