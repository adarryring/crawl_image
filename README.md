# crawl_image

## Introduction
多线程快速抓取网页所有图片资源到指定路径，原理是抓取img标签的src，再整合域名成资源完整url，分发到程序线程去下载。

## Example
```py
from crawl_image.img_crawl import crawl_start

URL = 'http://huaban.com/'
IMG_SAVE_PATH = 'D:/crawl/image'
crawl_start(URL, IMG_SAVE_PATH, False)
```

## Features
- 高速下载
- 抓取所有图片
- 自解网页编码

## Communication
- 未来已来 203737026

## Copyright and License
code for you