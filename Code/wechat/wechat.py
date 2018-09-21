#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 AM11:44
# @Author  : L
# @Email   : L862608263@163.com
# @File    : wechat.py
# @Software: PyCharm

import time
import urllib.parse
import urllib.request
import re
import os

from selenium.webdriver import PhantomJS

# 微信公众号 广州移动 12点左右会发流量(9月21号更新, 活动已经变了)


# 问题
# 1,从weixinsogou网址获取的消息并不及时, 比在手机App里的消息慢了20分钟
# 2,验证码, 防止访问过于频繁的


def url_open(url, data=None):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/11.1 Safari/605.1.15')
    response = urllib.request.urlopen(request, data)
    return response.read()


class WeChat:
    index = 0
    china_mobile = "http://mp.weixin.qq.com/profile?src=3&timestamp=1531369031&ver=1&" \
                   "signature=pC*0jwF4JiQV2sA6P4zu5EBD*Y8x41r6edcCBwz8NoiJPgrh9cwZEzwyxcfh44nULjresODAsv5zZFkgrvKvaQ=="

    @staticmethod
    def wechat_sogou_search_info(keyword, page=1, search_type=1):
        """拼接搜索 公众号 URL

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1

        search_type : int, optional, default is 1
            1  # 公众号
            2  # 文章

        Returns
        -------
        str
            search_gzh_url
        """
        assert isinstance(page, int) and page > 0

        qs_dict = dict()
        qs_dict['type'] = search_type
        qs_dict['page'] = page
        qs_dict['ie'] = 'utf8'
        qs_dict['query'] = keyword

        return 'http://weixin.sogou.com/weixin?{}'.format(urllib.parse.urlencode(qs_dict))

    def wechat_article_info(self):

        # print('广州移动文章列表 ', china_mobile)

        # http://phantomjs.org/download.html 下载phantomjs可执行文件, 指定路径
        # 设置不输出运行日志
        driver = PhantomJS(executable_path='/Users/l/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs',
                           service_log_path=os.path.devnull)

        driver.get(self.china_mobile)

        page_source = driver.page_source

        data_list = list(re.findall('2018年7月12', page_source))

        print(data_list)

        if len(data_list) == 0:
            print("空数据")
            search_result = self.wechat_sogou_search_info("广州移动")

            html_string = url_open(search_result).decode('utf-8')

            # data_id_list = re.findall("data-id=(.*?)onerror", html_string)

            article_list = list(
                map(lambda x: str(x).replace('amp;', "").replace('http', 'https') + "==",
                    re.findall('href=(.*?)==', html_string)))

            self.china_mobile = str(article_list[0])[1:]
            print("新的 ", self.china_mobile)
            self.wechat_article_info()
            driver.close()
            return

        driver.close()

        self.index += 1

        while "2018年7月13日" not in page_source:
            print("没找到", self.index)
            time.sleep(30)
            self.wechat_article_info()
        else:
            print("拿流量了````````````````````````````````````")
            exit()


if __name__ == "__main__":
    wechat = WeChat()
    wechat.wechat_article_info()
