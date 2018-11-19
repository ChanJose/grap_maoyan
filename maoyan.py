# -*- coding: utf-8 -*-
# 提取猫眼电影TOP100的电影名称、时间、评分和图片等信息，存到文件中

import requests
import re
import json
from requests.exceptions import RequestException
import time


# 爬取页面
def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)  # 获取页面
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 分析页面
def parse_page(html):
    # 1.提取排名信息
    # pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>', re.S)

    # 2.随后提取电影图片
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"', re.S)

    # 3.接着提取电影名称
    # pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>', re.S)

    # 4.然后，提取主演
    # pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>', re.S)

    # 5.接着，提取发布时间
    # pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>', re.S)

    # 6. 提取评分的整数部分和小数部分
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)

    # 7.整理数据
    for item in items:
        yield {  # 返回一个生成器对象
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }


# 写入到文件中
def write_to_file(content):
    with open('result3.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


# 爬取TOP100
def craw(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)  # 目标站点
    html = get_page(url)  # 抓取页面
    for item in parse_page(html):  # 分析页面,返回一个生成器对象,写入到文件中
        write_to_file(item)


if __name__ == "__main__":
    for i in range(10):
        craw(i*10)
        time.sleep(1)  # 增加一个延时等待，防止速度太快，猫眼反爬虫导致没反应
