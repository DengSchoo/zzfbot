import re

import requests
from lxml import etree

# 阿里云搜索
# https://www.alipansou.com/search?k=%E9%9A%90%E5%85%A5%E5%B0%98%E7%83%9F&s=1&t=-1

aliyun_url = 'https://www.alipansou.com'
baidu_url = 'https://www.xiongdipan.com'

proxy = '120.196.188.21:9091'

proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
}

search_url_part = '/search?k='

sort_op = {
    '默认': '0',
    '时间': '1',
    '精确': '2'
}
type_op = {
    '全部类型': '-1',
    '视频': '1',
    '音乐': '2',
    '图片': '3',
    '文档': '4',
    '压缩包': '5',
    '其它': '6',
    '文件夹': '7',
}

search_urls = {
    'aliyun': aliyun_url,
    'al': aliyun_url,
    'bd': baidu_url,
    'baidu': baidu_url,
}

# 百度网盘搜索
# https://www.xiongdipan.com/search?k=%E9%9A%90%E5%85%A5%E5%B0%98%E7%83%9F&s=1&t=-1

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'cookie': 'test_cookie=CheckForPermission; expires=Fri, 09-Sep-2022 10:08:08 GMT; path=/; domain=.doubleclick.net; Secure; HttpOnly; SameSite=none'
}

fir_sea_xpath = '/html/body/div/div[1]'

first_max_num = 3


def get_list(url: str, keyword: str) -> list:
    #result = requests.get(url + search_url_part + keyword, headers=headers, proxies=proxies)
    result = requests.get(url + search_url_part + keyword, headers=headers)
    tree = etree.HTML(result.text)
    print("text" + result.text + "\n")
    fir_sea_list = tree.xpath(fir_sea_xpath)[0]
    res_list = []
    # print(len(fir_sea_list))
    for idx in range(3, min(4 + first_max_num, len(fir_sea_list))):
        href_xpath = './a/@href'
        sub_fix = fir_sea_list[idx].xpath(href_xpath)
        # print(sub_fix)
        if (len(sub_fix) > 0):
            sec_url_sub = sub_fix[0]
            sec_url = url + sec_url_sub
            # print(sec_url)
            res_list.append(get_sec_res(sec_url))
    # print(res_list)
    return res_list


tab_str = '    '

tab_str = tab_str + tab_str


def get_sec_res(url: str) -> str:
    result = requests.get(url, headers=headers)
    tree = etree.HTML(result.text)
    # print(result.text)
    root = tree.xpath('/html/body/div/div[1]')[0]
    name = '资源名称：' + str(
        root.xpath('./van-row[4]/van-col/van-cell/@value')[0]).strip() + '\n'
    type = tab_str + '类型：' + str(
        root.xpath('./van-row[5]/van-col/van-cell/text()')[0]).strip() + '\n'
    res_type = tab_str + '类别：' + str(
        root.xpath('./van-row[6]/van-col/van-cell/text()')[0]).strip() + '\n'
    size = ''
    time = ''
    if len(root) <= 10:
        time = tab_str + '分享时间：' + str(
            root.xpath('./van-row[7]/van-col/van-cell/text()')[0]).strip() + '\n'
    elif len(root) >= 11:
        size = tab_str + '文件大小：' + str(
            root.xpath('./van-row[7]/van-col/van-cell/text()')[0]).strip() + '\n'
        times = root.xpath('./van-row[8]/van-col/van-cell/text()')
        if len(times) >= 1:
            time = tab_str + '分享时间：' + str(times[0]).strip() + '\n'
    js_shell = tree.xpath('/html/body/script[3]/text()')[0]
    url = tab_str + '资源链接：' + process_js_shell(js_shell) + '\n'
    if 'aliyun' in url:
        url = url.replace('\\', '')
    return name + type + res_type + size + time + url


def process_js_shell(js_shell: str) -> str:
    # print(str(js_shell))
    res = re.findall('window.open\(\"([^"]*)\",\"target\"\)', str(js_shell))[0]
    # print(res)
    return res


def get_search_domain(key: str):
    if key in search_urls.keys():
        return search_urls[key]
    return aliyun_url


def get_search_sort_op(key: str):
    if key in sort_op.keys():
        return '&s=' + sort_op[key]
    return ''


def get_search_type_op(key: str):
    if key in type_op.keys():
        return '&t=' + type_op[key]
    return ''


def pan_res_search(keyword: str):
    splits = keyword.strip().split(' ')
    print(''.join(splits))
    lenth = len(splits)
    search_key = ''
    if lenth == 1 or lenth == 2:
        return '搜索参数为空'
    domain = get_search_domain(splits[1])
    if lenth == 3:
        search_key = splits[2]
    if lenth == 4:
        search_key = splits[2] + get_search_sort_op(splits[3])
    if lenth == 5:
        search_key = splits[2] + get_search_sort_op(splits[3]) + get_search_type_op(splits[4])
    res = get_list(domain, search_key)
    print(domain + search_key)
    if len(res) == 0:
        return '搜索结果为空！'
    ret_msg = ''
    for idx in range(len(res)):
        ret_msg += f'\n【{idx + 1}】{res[idx]}'
    return ret_msg


url = 'http://httpbin.org/ip'
#headers = {'User-Agent': 'python-spider'}
proxy = {'http': '代理ip', 'https': '代理ip'}  #在这个字典中可以单一的使用http或是https
response = requests.get(url=url, headers=headers, proxies=proxies, timeout=6)  #timeout是请求超时设置
print(response.text)
