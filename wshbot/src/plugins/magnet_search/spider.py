import re

import requests

from lxml import etree

from bs4 import BeautifulSoup

# 首先导入模块requests
url = 'https://www.baidu.com/'
# url为https://www.baidu.com
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Cookies': ''
}


def put_header(key, value):
    headers[key] = value


# 首页域名
base_url = 'https://www.xiaopian.com/'
# 二级页面域名
sec_page_url = 'https://m.xiaopian.com'

# 搜索url
search_url = 'https://m.xiaopian.com/e/search/index.php'
re_search_url = 'https://m.xiaopian.com/e/search/'
# 首页字段设置
home_res_dict = {
    '2022新片精品': '//*[@id="header"]/div/div[3]/div[5]/div[1]/div[2]/ul',
    '2022必看大片': '//*[@id="header"]/div/div[3]/div[5]/div[2]/div[2]/ul',
    '迅雷电影资源': '//*[@id="header"]/div/div[3]/div[6]/div[1]/div[2]/ul',
    '经典大片': '//*[@id="header"]/div/div[3]/div[6]/div[2]/div[2]/ul',
    '华语电视剧': '//*[@id="header"]/div/div[3]/div[7]/div[1]/div[2]/ul',
    '欧美剧': '//*[@id="header"]/div/div[3]/div[7]/div[2]/div[2]/ul',
    '日韩剧': '//*[@id="header"]/div/div[3]/div[8]/div[1]/div[2]/ul',
    '综艺': '//*[@id="header"]/div/div[3]/div[8]/div[2]/div[2]/ul',
}

# request = requests.get(base_url, headers=headers)
#
# request.encoding = "gbk"
# //*[@id="downlist"]/table[1]
# //*[@id="downlist"]

test_url = 'https://m.xiaopian.com/html/tv/oumeitv/20220420/117404.html'

sec_search_path = '//*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]'
# //*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]/ul
sec_inner_path = '//*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]/ul/table[1]/tbody/tr[2]/td[2]/b/a'


# //*[@id="Zoom"]/span/table/tbody/tr/td/a
# //*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]/ul/table[1]/tbody/tr[2]/td[2]/b/a
# //*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]/ul/table[2]/tbody/tr[2]/td[2]/b/a
# //*[@id="downlist"]/table[1]/tbody/tr/td/a  //*[@id="downlist"]/table[2]/tbody/tr/td/a

# //*[@id="header"]/div/div[3]/div[2]/div[1]/div[5]/div[2]/ul

def search_res(keyword):
    submit = "立即搜索"
    gbk_key_word = keyword.decode("utf-8").encode("gbk", 'ignore')
    search_data = {
        "show": "title",
        "tempid": "1",
        "keyboard": gbk_key_word,
        "submit": submit.encode("gbk")
    }
    post = requests.post(search_url, data=search_data, headers=headers)
    post.encoding = "gbk"
    # print(post.text)
    # if '没有搜索到相关的内容' in post.text
    magnet = sec_search_page(post.text, keyword)
    # print(magnet)
    mag_str = "\n"
    for k, v in magnet.items():
        mag_str += k + ":\n"
        if v is None:
            mag_str += "搜索结果为空。"
            continue
        for idx in range(len(v)):
            mag_str += f'【{idx + 1}】' + v[idx] + "\n"
        mag_str += "\n"
    # print(mag_str)
    return mag_str


def sec_search_page(html, keyword):
    ret = {}
    res = re.findall(r'/html/.*.html', html)[11:]
    title = re.findall('title=\"([^"]*)\"', html)
    length = len(res)
    if length > 3:
        length = 3
    for i in range(length):
        print(sec_page_url + res[i])
        ret[title[i]] = get_res_magnet(sec_page_url + res[i], keyword.decode("utf-8").encode("gbk"))
    # print(ret)
    return ret


def filter(str: str) -> str:
    filter_strs = ['[电影天堂www.dytt89.com]', '电影天堂www.dy2018.com.mkv', '[电影天堂www.dy2018.com]']
    for item in filter_strs:
        if item in str:
            splits = str.split(item)
            return splits[0] + splits[1]
    # if filter_str in str:
    #     splits = str.split(filter_str)
    #     return splits[0] + splits[1]
    return str


def get_res_magnet(url, keyword):
    request = requests.get(url, headers=headers)
    request.encoding = "gbk"
    tree = etree.HTML(request.text)
    # print(request.text)
    maglist = tree.xpath('//*[@id="downlist"]')
    if len(maglist) == 0:
        return
    maglist = maglist[0]
    ret_mag = []
    length = int(len(maglist) / 2)
    start = 0
    # if length > 50:
    #     start = 15
        # length = 45
    if length != 0:
        for i in range(start, length):
            ret_mag.append(filter(maglist.xpath('./table[' + (i + 1).__str__() + ']/tbody/tr/td/a//@href')[0]))
            # print(ret_mag[i])
            # print(maglist.xpath('./table[' + (i + 1).__str__() + ']/tbody/tr/td/a//@href'))
    else:
        # ret_mag = re.findall('href=\"(ftp://[^"]*)\"', request.text)
        ret_mag.append(keyword + "当前资源存在 但是无磁链")
        # print(ret_mag)
    # print(ret_mag)
    if length > 40:
        return ret_mag[:45]
    return ret_mag


def get_home_html():
    request = requests.get(base_url, headers=headers)
    request.encoding = "gbk"
    return request.text


testurl = 'https://m.xiaopian.com/e/search/result/?searchid=106204'


def testUrl(url):
    request = requests.get(url, headers=headers)
    request.encoding = "gbk"
    tree = etree.HTML(request.text)
    # print(request.text)
    res = re.findall(r'/html/.*.html', request.text)[11:]
    title = re.findall('title=\"([^"]*)\"', request.text)
    print(title)
    print(res)
    new_url = sec_page_url + res[0]
    print(new_url)
    print(get_res_magnet(new_url))


def get_home_tree():
    request = requests.get(base_url, headers=headers)
    request.encoding = "gbk"
    return etree.HTML(request.text)


def get_all_magnet(divs, re_path, ):
    pass


def get_single_magnet():
    pass


def get_home_list(tree, path):
    pass


# div_list=tree.xpath('//*[@id="header"]/div/div[3]/div[5]/div[1]/div[2]/ul')


# lis = div_list[0]
# for i in range(len(lis)):
#     # print(div.xpath('//*[@id="header"]/div/div[3]/div[5]/div[1]/div[2]/ul/li[1]/a'))
#     title = lis.xpath('./li/a//text()')[i]
#     sub_url = lis.xpath('./li/a//@href')[i]
#
#     print(sec_page_url + sub_url)
#     sec_page = requests.get(sec_page_url + sub_url, headers=headers)
#     sec_page.encoding = 'gbk'
#     if i == 2:
#         break
#     print(sec_page.text)

# search_res('铁血战士'.encode("utf-8"))

# get_res_magnet(test_url)

# testUrl('https://m.xiaopian.com/e/search/result/?searchid=96965')
print('中文')
# print(request.text)
