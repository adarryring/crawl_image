#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: crawl img tag source
@author: xiaohong
@time: 2019-01-01
@feature: crawl image for every site/multi thread to download/
"""

import time
import os
import threading
import chardet
import datetime
from urllib.parse import urlparse, urljoin
from urllib import request
from bs4 import BeautifulSoup

from crawl_image.config.setting import *


# 创建时间戳文件夹
def make_unique_folder(path):
    t = time.time()
    folder = path + '/' + str(int(t))
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


# 获取网页源代码
def get_html(url):
    response = request.urlopen(url)
    html = response.read()
    return html.decode(chardet.detect(html)['encoding'])


# 获取域名+端口
def get_host(url):
    host = urlparse(url)
    return host.scheme + '://' + host.netloc


# 获取绝对路径
def get_img_url(host, src):
    return urljoin(host, src)


# 获取图片标签
def get_img(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('img')


# 多线程抓取
def run_multi(folder, host, img_list):
    threads = []
    for index, img in enumerate(img_list):
        threads.append(threading.Thread(target=run, args=(folder, index, host, img)))

    for th in threads:
        th.start()
    for th in threads:
        th.join()


# download image
def run(folder, img_name, host, img):
    # noinspection PyBroadException
    try:
        f = open(folder + '/%s.jpg' % img_name, 'wb')
        f.write(request.urlopen(get_img_url(host, img.get('src'))).read())
        f.close()
        logging.info('下载第%s张图片' % img_name)
    except Exception:
        logging.error('第%s张图片下载失败' % img_name)


# save image
def save(img_save_path, img_list, host, do_multi):
    folder = make_unique_folder(img_save_path)
    if do_multi:
        run_multi(folder, host, img_list)
    else:
        for index, img in enumerate(img_list):
            run(folder, index, host, img)
    logging.info('下载完毕')


# show image tag
def print_img_list(url):
    img_list = get_img(get_html(url))
    for img in img_list:
        logging.info(img.get('src'))


# start
def crawl_start(url, img_save_path, do_multi):
    start = datetime.datetime.now()
    host = get_host(url)
    img_list = get_img(get_html(url))
    save(img_save_path, img_list, host, do_multi)
    logging.warning('crawl 耗时 : ' + str(datetime.datetime.now() - start))


"""run"""
if __name__ == '__main__':
    crawl_start(URL, IMG_SAVE_PATH, DO_MULTI)
    # print_img_list(URL)
