# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class officialAccountItem(scrapy.Item):
    nickname = scrapy.Field()   # 公众号名称
    article_title = scrapy.Field()  # 文章标题
    article_updatetime = scrapy.Field() # 发布时间
    article_link = scrapy.Field()   # 文章链接
    crawl_time = scrapy.Field() # 爬取时间

