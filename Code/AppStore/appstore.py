import urllib.request
import json
import time

input_id = 989673964


# https://weibo.com/p/23041812e1c1e0b0102wyrm
# https://www.jianshu.com/p/b8e4ee3aadbe

# https://rss.itunes.apple.com/zh-cn

# 一页50个评论, 满了换页
# 通过这个接口可以获取前500个评论
def get_reviews(app_id, pages=range(1, 4), sort_type="mostrecent", country="cn"):
    for page in pages:
        try:
            url = 'https://itunes.apple.com/%srss/customerreviews/id=%s/page=%d/sortby=%s/json' \
                  % (country + "/", app_id, page, sort_type)
            print(url)
            with urllib.request.urlopen(url) as f:
                data = json.loads(f.read().decode()).get('feed')

            entry = data.get('entry')

            if entry is None:
                break

            if type(entry) is dict:
                get_info_from(entry)
            elif type(entry) is list:
                for sub_info in entry:
                    get_info_from(sub_info)

        except Exception as error:
            print(error)
            time.sleep(1)


def get_info_from(dic):
    title = dic.get('title').get('label')
    author = dic.get('author').get('name').get('label')
    version = dic.get('im:version').get('label')
    rating = dic.get('im:rating').get('label')
    review = dic.get('content').get('label')
    vote_count = dic.get('im:voteCount').get('label')
    print("标题:%s" % title)
    print("作者:%s" % author)
    print("版本:%s" % version)
    print("内容:%s" % review)
    print("评分:%s" % rating)
    print("投票:%s" % vote_count)
    print("\n")


get_reviews(input_id)
