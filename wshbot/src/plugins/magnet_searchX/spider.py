import re

import requests
from lxml import etree

main_url = 'https://clm9.me'

base_search_url = 'https://clm9.me/search?word='

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.25',
    'cookie': '_ga=GA1.1.1366630586.1656818456; challenge=3339af4017f8a8e35ceaf603cd358f2e; ex=1; _ga_W7KV15XZN0=GS1.1.1662205312.13.1.1662206526.0.0.0'

}

'//*[@id="Search_list_wrapper"]/li[1]/div[1]/div/a'

max_search = 2


def search_res(keyword):
    # gbk_key_word = keyword.decode("utf-8").encode("gbk", 'ignore')
    # print(gbk_key_word)
    html = requests.get(base_search_url + keyword.decode('utf-8'), headers=headers)

    tree = etree.HTML(html.text)

    search_list = tree.xpath('/html/body/div[1]/div[2]/div[2]/ul')
    if len(search_list) == 0:
        return None
    # print(len(search_list[0]))
    mag_list = search_list[0]
    ret_mag = []
    mag_len = len(mag_list) - 1
    if mag_len > max_search:
        mag_len = max_search
    for i in range(mag_len):
        # print('./li[' + str(i + 1) + ']/div[1]/div/a//@href')
        '/html/body/div[1]/div[2]/div[2]/ul/li[1]/div[1]/div/a'
        sec_page_url = main_url + tree.xpath(
            '/html/body/div[1]/div[2]/div[2]/ul/li[' + (i + 1).__str__() + ']/div[1]/div/a/@href')[0]
        # res_name = tree.xpath('/html/body/div[1]/div[2]/div[2]/ul/li[' + str(i + 1) + ']/div[1]/div/a/text()')[0]
        ret_mag.append('【' + ((i + 1).__str__()) + '】' + get_mag(sec_page=sec_page_url))
        # print( sec_page_url)
    if len(ret_mag) == 0:
        return "搜索结果为空！"
    return '\n'.join(ret_mag)


tab_str = '    '


def get_mag(sec_page):
    html = requests.get(sec_page, headers=headers)
    tree = etree.HTML(html.text)
    # print(html.text)
    res_name = tree.xpath('/html/body/div[1]/div[2]/div[2]/h1/text()')[0] + '\n'
    res_mag = tab_str + '资源链接：' + tree.xpath('//*[@id="down-url"]//@href')[0]
    res_file_num = tab_str + '文件数量：' + tree.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/b[1]/text()')[
        0] + '\n'
    #print(res_file_num)
    res_size = tab_str + '文件大小：' + str(
        tree.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/b[2]/text()')[0]) + '\n'
    #print(res_size)
    res_time = tab_str + '收录时间：' + tree.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/b[3]/text()')[0] + '\n'
    #print(res_time)
    res_dow_times = tab_str + '下载次数：' + tree.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/b[4]/text()')[
        0] + '\n'
    #print(res_dow_times)
    return res_name + res_file_num + res_size + res_time + res_dow_times + res_mag


print(search_res('laf-41'.encode('utf-8')))
