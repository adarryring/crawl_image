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


def make_unique_folder(path):
    """
    创建时间戳文件夹

    :param path: 文件路径
    :return: 文件夹路径
    """
    t = time.time()
    folder = path + '/' + str(int(t))
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def get_html(url):
    """
    获取网页源代码

    :param url: HTML网址
    :return: HTML内容
    """
    response = request.urlopen(url)
    html = response.read()
    return html.decode(chardet.detect(html)['encoding'])


def get_host(url):
    """
    获取域名+端口

    :param url: url
    :return: 域名端口
    """
    host = urlparse(url)
    return host.scheme + '://' + host.netloc


def get_img_url(host, src):
    """
    获取绝对路径

    :param host: 域名
    :param src: 资源相对地址
    :return: 资源绝对地址
    """
    return urljoin(host, src)


def get_img(html):
    """
    获取图片标签

    :param html: HTML内容
    :return: 页面所有img标签对象
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('img')


def run_multi(folder, host, img_list, img_crawl_model_):
    """
    多线程抓取

    :param folder: 本地存储文件夹
    :param host: 域名
    :param img_list: img tag对象数组
    :param img_crawl_model_: ImgCrawlModel对象
    :return: void
    """
    threads = []
    for index, img in enumerate(img_list):
        threads.append(threading.Thread(target=run, args=(folder, index, host, img, img_suffix(img.get('src'), img_crawl_model_.default_img_suffix))))

    for th in threads:
        th.start()
    for th in threads:
        th.join()


def run(folder, img_name, host, img, default_img_suffix_):
    """
    download image

    :param folder: 本地存储文件夹
    :param img_name: 图片文件名称，不带后缀
    :param host: 域名
    :param img: img tag对象
    :param default_img_suffix_: 默认图片存储文件的后缀
    :return: void
    """
    path = folder + '/%s' + default_img_suffix_
    run_by_url(path % img_name, get_img_url(host, img.get('src')))


def run_by_url(img_file_path, img_url):
    """
    download image from url

    :param img_file_path: 本地图片文件路径
    :param img_url: 图片url
    :return: void
    """
    # noinspection PyBroadException
    try:
        f = open(img_file_path, 'wb')
        f.write(request.urlopen(img_url).read())
        f.close()
        logging.info('下载第%s张图片' % f.name)
    except Exception as e:
        logging.error('第%s张图片下载失败 : %s' % (str(e), img_file_path))


def save(img_crawl_model_, img_list, host):
    """
    save image

    :param img_crawl_model_: ImgCrawlModel对象
    :param img_list: img tag对象数组
    :param host: 域名
    :return: void
    """
    folder = make_unique_folder(img_crawl_model_.img_save_path)
    if img_crawl_model_.do_multi:
        run_multi(folder, host, img_list, img_crawl_model_)
    else:
        for index, img in enumerate(img_list):
            run(folder, index, host, img, img_suffix(img.get('src'), img_crawl_model_.default_img_suffix))
    logging.info('下载完毕')


def crawl_start(img_crawl_model_):
    """
    start

    :param img_crawl_model_: ImgCrawlModel对象
    :return: void
    """
    start = datetime.datetime.now()
    host = get_host(img_crawl_model_.url)
    img_list = get_img(get_html(img_crawl_model_.url))
    img_list = img_list_filter(img_list, img_crawl_model_)
    save(img_crawl_model_, img_list, host)
    logging.warning('crawl 耗时 : ' + str(datetime.datetime.now() - start))


def blank(s):
    """
    是否为空

    :param s: string
    :return: true is empty string, else false.
    """
    return s is None or s is ''


def img_suffix(src, default_img_suffix_):
    """
    img suffix

    :param src: 图片url
    :param default_img_suffix_: 默认图片后缀
    :return: 返回默认图片后缀，如果图片url没有带图片后缀的话
    """
    url_path = urlparse(str(src)).path
    i = url_path.rfind('.')
    return ('.' + default_img_suffix_) if -1 == i else url_path[i:]


def suffix_filter(src, img_crawl_model_):
    """
    suffix filter

    :param src: 图片url
    :param img_crawl_model_: ImgCrawlModel对象
    :return: true is legal
    """
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


def img_list_filter(img_list, img_crawl_model_):
    """
    img list filter

    :param img_list: img tag对象数组
    :param img_crawl_model_: ImgCrawlModel对象
    :return: 合法的img tag对象数组
    """
    img_list_result = []
    for img in img_list:
        if suffix_filter(img.get('src'), img_crawl_model_):
            img_list_result.append(img)
    return img_list_result


def print_img_list(img_crawl_model_):
    """
    show image tag

    :param img_crawl_model_: ImgCrawlModel对象
    :return: void
    """
    img_list = get_img(get_html(img_crawl_model_.url))
    logging.info(dir(img_list[0]))

    img_list = img_list_filter(img_list, img_crawl_model_)
    for img in img_list:
        logging.info('[' + str(img.get('src')) + '] : True')
