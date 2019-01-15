#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: crawl img tag source
@author: xiaohong
@time: 2019-01-01
@feature: crawl image for every site/multi thread to download/filter img type
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
def run_multi(folder, host, img_list, img_crawl_model_):
    threads = []
    for index, img in enumerate(img_list):
        threads.append(threading.Thread(target=run, args=(folder, index, host, img, img_suffix(img.get('src'), img_crawl_model_.default_img_suffix))))

    for th in threads:
        th.start()
    for th in threads:
        th.join()


# download image
def run(folder, img_name, host, img, default_img_suffix_):
    # noinspection PyBroadException
    try:
        path = folder + '/%s' + default_img_suffix_
        f = open(path % img_name, 'wb')
        f.write(request.urlopen(get_img_url(host, img.get('src'))).read())
        f.close()
        logging.info('下载第%s张图片' % img_name)
    except Exception as e:
        logging.error('第%s张图片下载失败 : ' + str(e) % img_name)


# save image
def save(img_crawl_model_, img_list, host):
    folder = make_unique_folder(img_crawl_model_.img_save_path)
    if img_crawl_model_.do_multi:
        run_multi(folder, host, img_list, img_crawl_model_)
    else:
        for index, img in enumerate(img_list):
            run(folder, index, host, img, img_suffix(img.get('src'), img_crawl_model_.default_img_suffix))
    logging.info('下载完毕')


# start
def crawl_start(img_crawl_model_):
    start = datetime.datetime.now()
    host = get_host(img_crawl_model_.url)
    img_list = get_img(get_html(img_crawl_model_.url))
    img_list = img_list_filter(img_list, img_crawl_model_)
    save(img_crawl_model_, img_list, host)
    logging.warning('crawl 耗时 : ' + str(datetime.datetime.now() - start))


# 是否为空
def blank(s):
    return s is None or s is ''


# img suffix
def img_suffix(src, default_img_suffix_):
    url_path = urlparse(str(src)).path
    i = url_path.rfind('.')
    return ('.' + default_img_suffix_) if -1 == i else url_path[i:]


# suffix filter
def suffix_filter(src, img_crawl_model_):
    if blank(src):
        return False
    suffix = img_suffix(src, img_crawl_model_.default_img_suffix)
    for e in img_crawl_model_.img_include_suffix:
        if suffix.endswith(e):
            return True
    for e in img_crawl_model_.img_exclude_suffix:
        if suffix.endswith(e):
            return False
    return True


# img list filter
def img_list_filter(img_list, img_crawl_model_):
    img_list_result = []
    for img in img_list:
        if suffix_filter(img.get('src'), img_crawl_model_):
            img_list_result.append(img)
    return img_list_result


# show image tag
def print_img_list(img_crawl_model_):
    img_list = get_img(get_html(img_crawl_model_.url))
    logging.info(dir(img_list[0]))

    img_list = img_list_filter(img_list, img_crawl_model_)
    for img in img_list:
        logging.info('[' + str(img.get('src')) + '] : True')
