import re
#coding=utf-8

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
    'cookie': '_ga=GA1.1.481167973.1667014847; __gads=ID=216fae9a67a9d5ee-224095a038d900f4:T=1673356318:RT=1673356318:S=ALNI_MYnvxvlAUNHLEe37h13I-CkWhBxrQ; Hm_lvt_02f69e0ba673e328ef49b5fb98dd4601=1677897985,1677936657,1678621279,1679834163; _bid=f34e039111870ec62cac42f73be95917; __gpi=UID=00000ba14569e8e7:T=1673356318:RT=1679834163:S=ALNI_Mb3QzLchd5HxoifHPyvpsdmqPYwxA; _ga_NYNC791BP2=GS1.1.1679834163.28.1.1679834360.0.0.0; _ga_0B2NFC7Z09=GS1.1.1679834163.26.1.1679834360.17.0.0; Hm_lpvt_02f69e0ba673e328ef49b5fb98dd4601=1679834361',
    'referer': 'https://www.alipansou.com/s/Ye8OmwQDjxXEOqMNRb3HnAZfrxVbP'
}

# headers = {
# 'Host': 'www.alipansou.com',
# 'Connection': 'keep-alive',
# 'sec-ch-ua: '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
# 'sec-ch-ua-platform': "Windows",
# 'sec-ch-ua-mobile': '?0'.
# 'Upgrade-Insecure-Requests': 1
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54,
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# 'Sec-Fetch-Site': same-origin
# 'Sec-Fetch-Mode': navigate
# 'Sec-Fetch-User': ?1
# 'Sec-Fetch-Dest': document
# 'Referer': https://www.alipansou.com/s/AdS6dklGcuwOqXtoMoWMs0VqAOPai
# 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6
# 'Cookie': '_ga=G'A1.1.481167973.1667014847; __gads=ID=216fae9a67a9d5ee-224095a038d900f4:T=1673356318:RT=1673356318:S=ALNI_MYnvxvlAUNHLEe37h13I-CkWhBxrQ; Hm_lvt_02f69e0ba673e328ef49b5fb98dd4601=1677897985,1677936657,1678621279,1679834163; _bid=f34e039111870ec62cac42f73be95917; __gpi=UID=00000ba14569e8e7:T=1673356318:RT=1679834163:S=ALNI_Mb3QzLchd5HxoifHPyvpsdmqPYwxA; _ga_NYNC791BP2=GS1.1.1679834163.28.1.1679834360.0.0.0; _ga_0B2NFC7Z09=GS1.1.1679834163.26.1.1679834360.17.0.0; Hm_lpvt_02f69e0ba673e328ef49b5fb98dd4601=1679834361
# 'Accept-Encoding': 'gzip, deflate'
# }

fir_sea_xpath = '/html/body/div/div[1]'

first_max_num = 3


def get_list(url: str, keyword: str) -> list:
    #result = requests.get(url + search_url_part + keyword, headers=headers, proxies=proxies)
    result = requests.get(url + search_url_part + keyword, headers=headers, verify=False)
    tree = etree.HTML(result.text)
    #print("text" + result.text + "\n")
    
    fir_sea_list = tree.xpath(fir_sea_xpath)[0]
    res_list = []
    # print(len(fir_sea_list))
    for idx in range(3, min(3 + first_max_num, len(fir_sea_list))):
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
    result = requests.get(url, headers=headers, verify=False)
    tree = etree.HTML(result.text)
    #print(result.text)
    root = tree.xpath('/html/body/div/div[1]')[0]

    ret_msg = ''
    name = '资源名称：' + str(
        root.xpath('./van-row[4]/van-col/van-cell/@value')[0]).strip() + '\n'
    ret_msg += name
    meta_info = root[4:len(root) - 3]
    for meta in meta_info:
        meta_name = str(meta.xpath('./van-col/van-cell/@title')[0]).strip()
        if meta_name == '密码':
            meta_val = str(meta.xpath('./van-col/van-cell/b[1]/text()')[0]).strip()
        else :
            meta_val = str(meta.xpath('./van-col/van-cell/text()')[0]).strip()
        ret_msg += f'{tab_str + meta_name + "：" + meta_val}\n'
    js_shell = tree.xpath('/html/body/script[3]/text()')[0]
    cv = process_js_shell(js_shell)
    headers_tmp = headers
    headers_tmp['referer'] = aliyun_url + cv
    TMP_URL = requests.get(aliyun_url + cv, headers=headers_tmp, verify=False).url
    url = tab_str + '资源链接：' + TMP_URL + '\n'
    return ret_msg + url




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
    #print(''.join(splits))
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



print(pan_res_search('ps al 黑化律师'))
