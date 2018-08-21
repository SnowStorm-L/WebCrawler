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


# https://baike.baidu.com/item/robots/5243374?fr=aladdin
# robots.txt 文件 对搜索引擎爬虫的建议性限制吧

class JianDanImage:
    __image_url = "http://jandan.net/ooxx/"

    @staticmethod
    def url_open(url, data=None):
        request = urllib.request.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                           'Version/11.1 Safari/605.1.15')
        response = urllib.request.urlopen(request, data)
        return response.read()

    def find_image_url(self, from_page=0, to_page=45, filter_score=0):
        page_list = [self.__image_url + "page-%s#comments" % str(idx) for idx in range(from_page, to_page + 1)]
        img_url_list = []

        if filter_score < 0:
            limit = 0
        elif filter_score > 1:
            limit = 1
        else:
            limit = filter_score

        current_page_number = 0

        for url in page_list:

            html_str = self.url_open(url).decode('utf-8')

            load_page_number = int(re.findall('"current-comment-page">\[(.*?)]</span>', html_str)[0])

            if current_page_number == load_page_number:
                return img_url_list

            current_page_number = load_page_number

            support_regular = 'OO</a> \[<span>(.*?)</span>]'
            oppose_regular = 'XX</a> \[<span>(.*?)</span>]'

            support_list = [float(idx) for idx in re.findall(support_regular, html_str) if float(idx) != 0.0]

            oppose_list = [float(idx) for idx in re.findall(oppose_regular, html_str) if float(idx) != 0.0]

            score_list = list(map(lambda x, y: x / (x + y), support_list, oppose_list))

            img_hash_list = list(re.findall('img-hash">(.*?)</span>', html_str))

            if limit != 0:
                tuple_list = list(zip(img_hash_list, score_list))

                img_hash_list = [idx[0] for idx in list(filter(lambda x: x[1] > limit, tuple_list))]

            img_url = ["http:" + self.decode_hash_value(idx) for idx in img_hash_list]

            img_url_list.extend(img_url)

        return img_url_list

    def download_img(self, store_path):
        # 有空加个多线程?
        count = 0
        img_list = self.find_image_url()
        print("total - {0}".format(len(img_list)))
        for url in img_list:
            data = urllib.request.urlopen(url).read()
            img_type = "." + url.split(".")[-1]
            img_path = store_path + "/" + str(uuid.uuid4()) + img_type
            print(img_path)
            if data is not None:
                with open(img_path, "wb") as file:
                    count += 1
                    print("writing - {0}".format(count))
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
    download_path = "/Users/l/Desktop/jiandan"
    image.download_img(download_path)
