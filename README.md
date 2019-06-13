# crawl_image

## Introduction
- 多线程快速抓取网页所有图片资源到指定路径。
- 原理是抓取img标签的src，再整合域名成资源完整url，分发到程序线程去下载。

## Example

from crawl_image.run_factory import run_for_url_list
run_for_url_list('C:/Users/xh/Desktop/url/url.txt', img_save_path='D:/crawl/image/real', do_last_url_file_name=True)

## Features
- 高速下载
- 抓取所有图片
- 自解网页编码
- 过滤图片类型
- 重构使用class交互，并建立run_factory，提供运行工厂，简化程序调用流程。
- 增加url列表文件爬取功能。
- 去重url数组。
- 使用url最后以'/'符号结束的字符串作为图片名称，以便检查重复下载的情况。

## Communication
- 未来已来 203737026

## Copyright and License
code for everything