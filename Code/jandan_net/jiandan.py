#!/usr/local/bin/python3.6.5
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 PM6:48
# @Author  : L
# @Email   : L862608263@163.com
# @File    : jiandan.py
# @Software: PyCharm

import urllib.request
import urllib.response
import re
import uuid
import base64
import datetime

""" 使用代理
import random

   @staticmethod
   def url_open(url, data=None):
       try:
           proxy_collection = [{'http': '39.137.77.66:8080'}, {'http': '43.239.79.55:3128'},
                               {'http': '185.22.174.65:1448'}, {'http': '117.191.11.78:8080'}]
           proxy = random.choice(proxy_collection)
           proxy_support = urllib.request.ProxyHandler(proxy)
           opener = urllib.request.build_opener(proxy_support)
           print(proxy)
           USER_AGENTS = random.choice([
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
               "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
               "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
               "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
               "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
               "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
               "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
               "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
           ])
           print(USER_AGENTS)
           opener.addheaders = [('User-Agent', USER_AGENTS)]
           response = opener.open(url, data=data)
           return response.read()
       except Exception as err:
           print(err)
           return None
       """


# https://baike.baidu.com/item/robots/5243374?fr=aladdin
# robots.txt 文件 对搜索引擎爬虫的建议性限制吧(君子协议, 该爬的还是照样爬)

class JianDanImage:
    __ooxx_url = "http://jandan.net/ooxx/"
    __pic_url = "http://jandan.net/pic/"
    download_counter = 0

    @staticmethod
    def url_open(url, data=None):
        try:
            request = urllib.request.Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                               'Version/11.1 Safari/605.1.15')
            response = urllib.request.urlopen(request, data)
            return response.read()
        except Exception as e:
            print("url_open error", e)
            return None

    def fetch_image(self, from_page=1, to_page=300, filter_score=0, store_path="/Users/l/Desktop/jiandan"):
        page_list = [self.__pic_url + str(base64.b64encode(
            ("%s-%s#comments" % (datetime.datetime.now().strftime('%Y-%m-%d').replace("-", ""), str(idx))).encode(
                'utf-8')), 'utf-8')
                     for idx in range(from_page, to_page + 1)]
        self.download_counter = 0
        if filter_score < 0:
            limit = 0
        elif filter_score > 1:
            limit = 1
        else:
            limit = filter_score

        current_page_number = 0

        for idx, url in enumerate(page_list):

            content = self.url_open(url)

            if content is None:
                continue

            print("第:" + str(idx + 1) + "页 链接:" + url)

            html_str = content.decode('utf-8')

            load_page_number = int(re.findall('"current-comment-page">\[(.*?)]</span>', html_str)[0])

            if current_page_number == load_page_number:
                return

            current_page_number = load_page_number

            support_regular = 'OO</a> \[<span>(.*?)</span>]'
            oppose_regular = 'XX</a> \[<span>(.*?)</span>]'

            support_list = [float(idx) for idx in re.findall(support_regular, html_str) if float(idx) != 0.0]

            oppose_list = [float(idx) for idx in re.findall(oppose_regular, html_str) if float(idx) != 0.0]

            score_list = list(map(lambda x, y: x / (x + y), support_list, oppose_list))

            # img_hash_list = list(re.findall('img-hash">(.*?)</span>', html_str))

            img_hash_list = list(re.findall('wx3(.*?)"', html_str))

            # print(img_hash_list)

            if limit != 0:
                tuple_list = list(zip(img_hash_list, score_list))

                img_hash_list = [idx[0] for idx in list(filter(lambda x: x[1] > limit, tuple_list))]

            img_url = ["http://wx3" + idx for idx in img_hash_list]
            img_url = list(filter(lambda index: "mw600" not in index, img_url))
            for element in img_url:
                pass
                #print(img_url)
                #self.download_img(element, store_path)

    def download_img(self, url, store_path):
        # 有空加个多线程?
        data = self.url_open(url)
        if data is None:
            self.download_counter += 1
            print("writing - {0}".format(self.download_counter))
            return
        img_type = "." + url.split(".")[-1]
        img_path = store_path + "/" + str(uuid.uuid4()) + img_type
        print(img_path)
        with open(img_path, "wb") as file:
            self.download_counter += 1
            print("writing - {0}".format(self.download_counter))
            file.write(data)

    def decode_hash_value(self, hash_value):
        return self.base64_decode(hash_value)

    @staticmethod
    def base64_decode(input_value):
        return str(base64.b64decode(input_value), "utf-8")

    # 下面这些都是源js代码,转换成py的,校验图片的(对于这次爬虫来说,作用并不大)
    # 可以研究一下实现过程

    # 固定的值
    # t = "cPUY9gzQmFTubb1z4qdRFw7PQaN63Kgg"

    # t = self.md5_encryption(t)
    #
    # p = self.md5_encryption(t[:16])
    # o = self.md5_encryption(t[16:])
    #
    # r = 4
    #
    # m = hash_value[:r]
    #
    # c = p + self.md5_encryption(p + m)
    #
    # hash_value = hash_value[r:]
    #
    # l = self.base64_decode(hash_value)
    #
    # k = list(range(0, 256))
    #
    # b = [ord(c[idx % len(c)]) for idx in k]
    #
    # g = h = 0
    #
    # for _ in list(range(0, 256)):
    #     g = (g + k[h] + b[h]) % 256
    #     temp = k[h]
    #     k[h] = k[g]
    #     k[g] = temp
    #     h += 1
    # print(k)
    #
    # u = ""
    #
    # l = list(l)
    #
    # q = g = h = 0
    #
    # for _ in range(0, len(l)):
    #     q = (q + 1) % 256
    #     g = (g + k[q]) % 256
    #     tmp = k[q]
    #     k[q] = k[g]
    #     k[g] = tmp
    #     u += chr(ord(l[h]) ^ (k[(k[q] + k[g]) % 256]))
    #     h += 1
    #
    # u = u[26:]

    # @staticmethod
    # def md5_encryption(input_value):
    #     md5_tool = hashlib.md5()
    #     md5_tool.update(input_value.encode("utf-8"))
    #     return md5_tool.hexdigest()


if __name__ == "__main__":
    image = JianDanImage()
    image.fetch_image()
