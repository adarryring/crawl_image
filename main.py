#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawl_image.run_factory import run_for_url_list

if __name__ == '__main__':
    # run()
    # run_for_url_list('C:/Users/xh/Desktop/url/1.txt', img_save_path='D:/crawl/image/1', do_last_url_file_name=True)
    run_for_url_list('C:/Users/xh/Desktop/url/url.txt', img_save_path='D:/crawl/image/real', do_last_url_file_name=True)
