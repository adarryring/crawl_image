#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: crawl img tag source
@author: xiaohong
@time: 2019-01-01
@feature: crawl image for every site/multi thread to download/
"""

from setuptools import setup, find_packages

setup(
    name="crawl_image",
    version="0.0.1",
    keywords='pip crawl web img image crawl_image',
    description="crawl web image source",
    long_description="crawl web image source, simple and fast!",
    license="MIT Licence",

    url="https://github.com/xiaohong2019/crawl_image",
    author="xiaohong2019",
    author_email="2229009854@qq.com",

    packages=find_packages(),
    platforms="any",
    install_requires=["BeautifulSoup"]
)
