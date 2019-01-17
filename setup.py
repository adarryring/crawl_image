#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: crawl img tag source
@author: xiaohong
@time: 2019-01-01
@feature: crawl image for every site/multi thread to download/
"""

import setuptools
import io

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="crawl_image",
    version="0.0.6",

    author="xiaohong2019",
    author_email="2229009854@qq.com",

    description="fast crawl web image source",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/xiaohong2019/crawl_image",
    packages=setuptools.find_packages(),
    install_requires=[
        'chardet',
        'beautifulsoup4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
