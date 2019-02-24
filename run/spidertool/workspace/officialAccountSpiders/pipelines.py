# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spidertool.workspace.officialAccountSpiders.settings import CRAWL_FILE_PATH
from spidertool.workspace.officialAccountSpiders.items import officialAccountItem
import csv
from datetime import datetime
from json import loads
import os

class officialAccountPipeline():
    def __init__(self):
        try:
            with open('config.json','r',encoding='utf8')as f:
                config_data = loads(f.read())
        except:
            with open('config.json','r',encoding='utf_8_sig')as f:
                config_data = loads(f.read())
        44 = config_data['TIME_LINE']
        self.filename = 'officialAccount_data_{}_{}.csv'.format(TIME_LINE[0],TIME_LINE[1])
        self.crawl_date = datetime.now().strftime('%Y-%m-%d')
        self.file =  open(CRAWL_FILE_PATH+self.filename,'a',encoding='utf_8_sig',newline='')
        with open(CRAWL_FILE_PATH+self.filename,'r',encoding='utf_8_sig')as f:
            if len(f.readlines()) == 0:
                self.writer = csv.writer(self.file)
                self.writer.writerow(('公众号名称','文章标题','发布时间','文章链接','爬取时间'))
                self.file.close() 



    def process_item(self,item,spider):
        if isinstance(item,officialAccountItem):
            with open(CRAWL_FILE_PATH+self.filename,'a',encoding='utf_8_sig',newline='')as wf:
                self.writer = csv.writer(wf)
                self.writer.writerow((item['nickname'],item['article_title'],item['article_updatetime'],item['article_link'],self.crawl_date))
        return item

    def close_spider(self,spider):
        pass
        # self.file.close() 

