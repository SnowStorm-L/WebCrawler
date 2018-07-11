#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 AM11:44
# @Author  : L
# @Email   : L862608263@163.com
# @File    : wechat.py
# @Software: PyCharm

import urllib.parse
import urllib.request
import re


from selenium.webdriver import Safari


def url_open(url, data=None):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/11.1 Safari/605.1.15')
    response = urllib.request.urlopen(request, data)
    return response.read()


def gen_search_gzh_url(keyword, page=1, search_type=1):
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


search_result = gen_search_gzh_url("广州移动")

html_string = url_open(search_result).decode('utf-8')

data_id_list = re.findall("data-id=(.*?)onerror", html_string)


article_list = list(map(lambda x: str(x).replace('amp;', "").replace('http', 'https') + "==", re.findall('href=(.*?)==', html_string)))
zhong_guo_yi_dong = str(article_list[0])[1:]


print(zhong_guo_yi_dong)

# print(url_open(zhong_guo_yi_dong).decode('utf-8'))

#executable_path='/Users/l/Desktop/accc/selenium-server-standalone-3.13.0.jar'
driver = Safari()
driver.get(zhong_guo_yi_dong)

print(driver.page_source)
driver.close()

