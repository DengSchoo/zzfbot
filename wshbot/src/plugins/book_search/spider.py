import re

import requests

from lxml import etree
import urllib3

from . import config as cf

urllib3.disable_warnings()


# exp : https://zh.annas-archive.org/search?lang=zh&content=&ext=pdf&sort=&q=%E4%B8%8A%E5%B8%9D%E6%8E%B7%E7%AD%9B%E5%AD%9 %E5%9 %97

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'cookie': '_ga=GA1.1.481167973.1667014847; __gads=ID=216fae9a67a9d5ee-224095a038d900f4:T=1673356318:RT=1673356318:S=ALNI_MYnvxvlAUNHLEe37h13I-CkWhBxrQ; Hm_lvt_02f69e0ba673e328ef49b5fb98dd4601=1677897985,1677936657,1678621279,1679834163; _bid=f34e039111870ec62cac42f73be95917; __gpi=UID=00000ba14569e8e7:T=1673356318:RT=1679834163:S=ALNI_Mb3QzLchd5HxoifHPyvpsdmqPYwxA; _ga_NYNC791BP2=GS1.1.1679834163.28.1.1679834360.0.0.0; _ga_0B2NFC7Z09=GS1.1.1679834163.26.1.1679834360.17.0.0; Hm_lpvt_02f69e0ba673e328ef49b5fb98dd4601=1679834361',
    'referer': 'https://www.alipansou.com/s/Ye8OmwQDjxXEOqMNRb3HnAZfrxVbP'
}

search = 'https://zh.annas-archive.org/search?lang={}&content={}&ext=pdf{}sort={}&q={}'

book_detail = 'https://zh.annas-archive.org'

langs = {
    "语言": '',
    '中文': 'zn',
    '英文': 'en'
}

contents = {
    "内容": "",
    '期刊': 'journal_article',
    '任何类型': 'book_any',
    '小说': 'book_fiction',
    '未知类型的图书': 'book_unknown',
    '非小说类图书': 'book_nonfiction',
    '漫画': 'book_comic',
    '杂志': 'magazine',
    '标准文档': 'standards_document',
}

requests.session().keep_alive = False

exts = [
    "pdf",
    "epub",
    "cbr",
    "fb2",
    "mobi",
    "cbz",
    "djvu",
    "azw3",
    "fb2.zip",
    "txt",
    "rar",
    "zip",
    "doc",
    "lit",
    "rtf",
    "htm",
    "html",
    "lrf",
    "mht",
    "docx"
]

sorts = {
    "最相关": "",
    "最新": "newest",
    "最旧": "oldest",
    "最大": "largest",
    "最小": "smallest",
}

page_start = '/html/body/main/div[{}]'
# list_start = '/html/body/main/div[4]/div[2]'
list_start = './div[{}]'

href_xpath = './a/@href'

book_size_and_ext = './a/div[2]/div[1]/text()'

book_publish_info = './a/div[2]/div[2]/text()'

book_writer = './a/div[2]/div[3]/text()'

book_name = './a/div[2]/h3/text()'

max_size = 3


def get_url(lang: str, content: str, ext: str, sort: str, q: str) -> str:
    return search.format(lang, content, ext, sort, q)


def get_dic(choice: str, dic: dict) -> str:
    lang = ""
    for key in dic.keys():
        if choice.count(key) != 0:
            return langs[key]
    return lang


def get_ext(choice: str) -> str:
    for ext in exts:
        if ext in choice:
            return ext
    return ""


book_info = """
【{}】:《{}》
    【基本信息】：{}
    【出版社】：{}
    【作者】：{}
    【资源链接】：
"""
tab_str = '    '

tab_str = tab_str + tab_str


def build_book_info(no: str, name: str, size_ext: str, publish_info: str, writer: str, links: [str]) -> str:
    info = book_info.format(no, name, size_ext, publish_info, writer)
    for link in links:
        info = info + tab_str + link + '\n'
    return info


def check_book_not_found(text: [str]) -> bool:
    if (text == None):
        return False
    #print(text)
    return text.count('未找到文件。') != 0


def get_normal_page(book_root, index, ret):
    href = book_root.xpath(href_xpath)[0]
    name = book_root.xpath(book_name)[0]
    size_ext = get_xpath_info(book_root, book_size_and_ext)
    publish_info = get_xpath_info(book_root, book_publish_info)
    writer = get_xpath_info(book_root, book_writer)
    links = search_tar_book(book_detail + href)
    ret.append(build_book_info(index.__str__(), name, size_ext, publish_info, writer, links))

def get_xpath_info(root, xpath:str):
    x = root.xpath(xpath)
    if len(x) == 0:
        return ""
    return x[0]

def get_comment_page(book_root, index, ret):
    '/html/body/main/div[3]/div[50]/comment()'
    comment = book_root.xpath('./comment()')[0].text.strip()
    # comment = comment.replace('<!--', '')
    # comment = comment.replace('-->', '')
    tree = etree.HTML(comment)
    #print(etree.tostring(tree))
    root = tree.xpath('/html/body')[0]
    href = root.xpath(href_xpath)[0]
    name = root.xpath(book_name)[0]
    size_ext = get_xpath_info(root, book_size_and_ext)
    publish_info = get_xpath_info(root, book_publish_info)
    writer = get_xpath_info(root, book_writer)
    links = search_tar_book(book_detail + href)
    ret.append(build_book_info(index.__str__(), name, size_ext, publish_info, writer, links))

def search_first_list(q: str, choice: str) -> [str]:
    url = get_url(get_dic(choice, langs), get_dic(choice, contents), get_ext(choice), get_dic(choice, sorts), q)
    result = requests.get(url, headers=headers, verify=False)
    tree = etree.HTML(result.text)
    check_condition = '/html/body/main/div[3]/span[1]/text()'
    begin = 3
    if check_book_not_found(tree.xpath(check_condition)):
        begin = 4
    # print(result.text)
    root = tree.xpath(page_start.format(begin))[0]
    ret = []
    index = 1
    start = 2
    for i in range(start, min(cf.config_dic.get('max_links') + start, len(root[1: len(root) - 1]))):
        root_path = list_start.format(i)
        book_root = root.xpath(root_path)[0]
        # print(root_path)
        hrefs = book_root.xpath(href_xpath)
        if len(hrefs) != 0:
            get_normal_page(book_root, index, ret)
        else:
            get_comment_page(book_root, index, ret)
        index += 1
    return ret


tar_book_info = '/html/body/main/div[2]/ul'
book_link = './li[1]'
book_link_address = './a/@href'
book_link_text = './a/text()'


def build_href(no: str, href: str, desc: str):
    return f'#{no} {desc}：{href}'


def search_tar_book(url: str) -> [str]:
    # url = get_url(get_dic(choice, langs), get_dic(choice, contents), get_ext(choice), get_dic(choice, sorts), q)
    result = requests.get(url, headers=headers, verify=False)
    tree = etree.HTML(result.text)
    # print(result.text)
    links = []
    links_root = tree.xpath(tar_book_info)[0]
    index = 1
    for link in links_root:
        href = link.xpath(book_link_address)[0]
        text = link.xpath(book_link_text)[0]
        links.append(build_href(index.__str__(), href, text))
        index += 1
    return links


print(search_first_list('优化设计', '中文'))
