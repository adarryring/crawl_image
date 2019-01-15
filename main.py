#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawl_image.model.img_crawl_model import ImgCrawlModel
from crawl_image.img_crawl import crawl_start, print_img_list

"""run"""
if __name__ == '__main__':
    img_crawl_model = ImgCrawlModel()
    print_img_list(img_crawl_model)
    crawl_start(img_crawl_model)
