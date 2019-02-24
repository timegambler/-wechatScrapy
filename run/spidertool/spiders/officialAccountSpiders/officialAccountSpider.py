# -*- coding: utf-8 -*-

from scrapy import Request,Spider
from pydispatch import dispatcher
from scrapy import signals
import time
from random import random
from datetime import datetime
import re
import logging
from json import loads,dumps
import csv
from urllib.request import unquote
from spidertool.workspace.officialAccountSpiders.settings import init_custom_settings,CRAWL_FILE_PATH
from spidertool.workspace.officialAccountSpiders.items import officialAccountItem


class officialAccountSpider(Spider):
    name = 'officialAccount'
    token_pattern = re.compile('token=(\d*)')
    custom_settings = init_custom_settings()

    def __init__(self):
        dispatcher.connect(self.spider_closed,signals.spider_closed)
        # 获取已缓存的公众号账号信息
        try:
            # with open(CRAWL_FILE_PATH+'officialAccountDict.cmd','r',encoding='utf8') as f:
            with open(CRAWL_FILE_PATH+'officialAccountDict.json','r',encoding='utf8') as f:
                self.officialAccountDict = loads(f.read())
                print(self.officialAccountDict)
                print(self.officialAccountDict.get('湖南联通',False))
        except:
            self.officialAccountDict = {}

        # 获取爬取配置信息
        try:
            with open('config.json','r',encoding='utf8')as f:
                config_data = loads(f.read())
        except:
            with open('config.json','r',encoding='utf_8_sig')as f:
                config_data = loads(f.read())
        self.USER_INFO = config_data['USER_INFO']
        self.NICKNAME_LIST = config_data['NICKNAME_LIST']
        self.TIME_LINE = config_data['TIME_LINE']
        self.SLEEP_INTERVAL = config_data['SLEEP_INTERVAL']
        
        # 获取已爬取的数据情况，用于续爬
        try:
            with open(CRAWL_FILE_PATH+'crawlLog.json','r',encoding='utf8') as f:
                self.crawlLogDict = loads(f.read())
            print(self.crawlLogDict)
        except:
            self.crawlLogDict = {}
        self.crawl_task = self.crawlLogDict.get('{}-{}'.format(self.TIME_LINE[0],self.TIME_LINE[1]),{})
    def start_requests(self):
        print('数据爬取程序运行中...')
        print('爬取公众号清单：\n',self.NICKNAME_LIST)
        print('爬取周期：\n',self.TIME_LINE)
        url = 'https://mp.weixin.qq.com/'
        yield Request(url,callback=self.search_account,meta={'useSelenium':1,'user_info':self.USER_INFO})

    def search_account(self,response):
        if response.status ==200:
            try:
                logging.info('登录成功...')
                print('登录成功...')
                time.sleep(5)
                token = str(re.findall(self.token_pattern,response.text)[0])
                search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}&query={}'
                for nickname in self.NICKNAME_LIST:
                    fakeid = self.officialAccountDict.get(nickname,False)
                    if fakeid:
                        # 查看当前公众号爬取任务是否完毕，如果是则跳过该公众号，否则继续上次任务
                        officialAccount_crawlinfo = self.crawl_task.get(nickname,['crawling',0])
                        if officialAccount_crawlinfo[0] == 'crawling':
                            next_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={}&lang=zh_CN&f=json&ajax=1&random={}&action=list_ex&count=5&query=&fakeid={}&type=9&begin={}'.format(token,str(random()),fakeid,str(officialAccount_crawlinfo[1]))
                            logging.info('{}上次爬取到page<{}>'.format(nickname,officialAccount_crawlinfo[1]))
                            logging.info('next url:{}'.format(next_url))
                            print('爬取下一条链接：',next_url)
                            time.sleep(self.SLEEP_INTERVAL)
                            yield Request(next_url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':nickname})
                            # 跳出循环，顺序爬取
                            break
                        elif officialAccount_crawlinfo[0] == 'finished':
                            print('公众号<{}>已爬取完所有数据,skip...'.format(nickname))
                    else:
                        url = search_url.format(token,nickname)
                        yield Request(url,callback=self.parse_fakeid,meta={'useSelenium':1})
                        # 跳出循环，顺序爬取
                        break
                        # time.sleep(5)
            except Exception as e:
                logging.exception(e)
        elif response.status ==202:
            logging.warn('账号登录失败')
    
    def parse_fakeid(self,response):
        article_search_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={}&lang=zh_CN&f=json&ajax=1&random={}&action=list_ex&count=5&query=&fakeid={}&type=9&begin={}'
        # article_search_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={}&action=list_ex&count=5&query=&fakeid={}&type=9&begin={}'
        token = str(re.findall(self.token_pattern,response.url)[0])
        nickname = unquote(re.findall("query=(.*)",response.url)[0], encoding="utf8")
        # print(nickname)
        account_pattern = re.compile('"fakeid":"([^,]*)",{1,6}"nickname":"([^,]*)"')
        try:
            account_list = re.findall(account_pattern,response.text)
            for ac in account_list:
                # print(ac[1])
                if ac[1] == nickname:
                    account = ac
                    logging.info(account)
                    self.officialAccountDict[account[1]] = account[0]
                    # 记录公众号的fakeid，并写入文件
                    with open(CRAWL_FILE_PATH+'officialAccountDict.json','w',encoding='utf8') as f:
                        f.write(dumps(self.officialAccountDict))
                    url = article_search_url.format(token,random(),account[0],'0')
                    print('爬取下一条链接：',url)
                    yield Request(url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':account[1]})
                    time.sleep(self.SLEEP_INTERVAL)
                    return
            logging.warn('公众号<{}>可能不存在,请核实'.format(nickname))
        except Exception as e:
            logging.exception(e)
            print('操作过于频繁，请稍后再试...')

    def parse_article_link(self,response):
        fakeid_pattern = re.compile('fakeid=([^&]*)')
        nickname = list(self.officialAccountDict.keys())[list(self.officialAccountDict.values()).index(re.findall(fakeid_pattern,response.url)[0])]
        # self.officialAccountDict.get(re.findall(fakeid_pattern,response.url)[0],False)
        if 'freq control' in response.text:
            logging.warn('访问过于频繁,暂停60分钟...')
            print('访问过于频繁,暂停120分钟...')
            time.sleep(60*120)
            yield Request(response.url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':nickname},dont_filter=True)
        else:
            current_page = int(re.findall('begin=(\d*)',response.url)[0])
            # 记录当前公众号爬取页码，并写入文件
            self.crawl_task[nickname] = ['crawling',current_page]
            self.crawlLogDict['{}-{}'.format(self.TIME_LINE[0],self.TIME_LINE[1])] = self.crawl_task
            with open(CRAWL_FILE_PATH+'crawlLog.json','w',encoding='utf8') as f:
                f.write(dumps(self.crawlLogDict))
            page_num_pattern = re.compile('"app_msg_cnt":(\d*)')
            article_pattern = re.compile('"link":"([^,]*)"[^\}]*,"title":"([^\"]*)"[^\}]*,"update_time":(\d*)')
            try:
                page_num = int(re.findall(page_num_pattern,response.text)[0])
                article_list = re.findall(article_pattern,response.text)
                logging.info('max page:{}'.format(page_num))
                for article_link,article_title,update_time in article_list:
                    if datetime.fromtimestamp(int(update_time)).strftime('%Y-%m')>= self.TIME_LINE[0] and datetime.fromtimestamp(int(update_time)).strftime('%Y-%m')<= self.TIME_LINE[1]:
                        item = officialAccountItem()
                        item['nickname'] = nickname
                        item['article_title'] = article_title
                        item['article_updatetime'] = datetime.fromtimestamp(int(update_time)).strftime('%Y-%m-%d %H:%M:%S')
                        item['article_link'] = article_link.replace('amp;','')
                        yield item  
                    recent_date = datetime.fromtimestamp(int(update_time)).strftime('%Y-%m')
                if recent_date < self.TIME_LINE[0]:
                    logging.info('公众号<{}>爬取任务结束'.format(response.flags[0]))
                    print('公众号<{}>爬取任务结束'.format(response.flags[0]))
                    # 记录当前公众号爬取页码，并写入文件
                    self.crawl_task[nickname] = ['finished',current_page]
                    self.crawlLogDict['{}-{}'.format(self.TIME_LINE[0],self.TIME_LINE[1])] = self.crawl_task
                    with open(CRAWL_FILE_PATH+'crawlLog.json','w',encoding='utf8') as f:
                        f.write(dumps(self.crawlLogDict))
                    # 如果有未爬完的公众号，继续爬
                    token = str(re.findall(self.token_pattern,response.url)[0])
                    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}&query={}'
                    for nickname in self.NICKNAME_LIST:
                        logging.info(nickname)
                        fakeid = self.officialAccountDict.get(nickname,False)
                        if fakeid:
                            # 查看当前公众号爬取任务是否完毕，如果是则跳过该公众号，否则继续上次任务
                            officialAccount_crawlinfo = self.crawl_task.get(nickname,['crawling',0])
                            if officialAccount_crawlinfo[0] == 'crawling':
                                next_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={}&lang=zh_CN&f=json&ajax=1&random={}&action=list_ex&count=5&query=&fakeid={}&type=9&begin={}'.format(token,str(random()),fakeid,str(officialAccount_crawlinfo[1]))
                                logging.info('{}上次爬取到page<{}>'.format(nickname,officialAccount_crawlinfo[1]))
                                logging.info('next url:{}'.format(next_url))
                                print('爬取下一条链接：',next_url)
                                time.sleep(self.SLEEP_INTERVAL)
                                yield Request(next_url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':nickname})
                                # 跳出循环，顺序爬取
                                break
                            elif officialAccount_crawlinfo[0] == 'finished':
                                print('公众号<{}>已爬取完所有数据,skip...'.format(nickname))
                        else:
                            logging.info('正在爬取公众号<{}>'.format(nickname))
                            print('正在爬取公众号<{}>'.format(nickname))
                            url = search_url.format(token,nickname)
                            yield Request(url,callback=self.parse_fakeid,meta={'useSelenium':1})
                            # 跳出循环，顺序爬取
                            break
                            # time.sleep(5)
                elif int(current_page/5) < int(page_num/5):
                    next_url = response.url.replace('begin='+str(current_page),'begin='+str(int((current_page/5+1)*5)))
                    logging.info('next url:{}'.format(next_url))
                    print('爬取下一条链接：',next_url)
                    time.sleep(self.SLEEP_INTERVAL)
                    yield Request(next_url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':nickname})
                else:
                    logging.info('公众号<{}>爬取任务结束'.format(response.flags[0]))
                    print('公众号<{}>爬取任务结束'.format(response.flags[0]))
                    # 记录当前公众号爬取页码，并写入文件
                    self.crawl_task[nickname] = ['finished',current_page]
                    self.crawlLogDict['{}-{}'.format(self.TIME_LINE[0],self.TIME_LINE[1])] = self.crawl_task
                    with open(CRAWL_FILE_PATH+'crawlLog.json','w',encoding='utf8') as f:
                        f.write(dumps(self.crawlLogDict))
                    # 如果有未爬完的公众号，继续爬
                    token = str(re.findall(self.token_pattern,response.url)[0])
                    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={}&query={}'
                    for nickname in self.NICKNAME_LIST:
                        logging.info(nickname)
                        fakeid = self.officialAccountDict.get(nickname,False)
                        if fakeid:
                            # 查看当前公众号爬取任务是否完毕，如果是则跳过该公众号，否则继续上次任务
                            officialAccount_crawlinfo = self.crawl_task.get(nickname,['crawling',0])
                            if officialAccount_crawlinfo[0] == 'crawling':
                                next_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={}&lang=zh_CN&f=json&ajax=1&random={}&action=list_ex&count=5&query=&fakeid={}&type=9&begin={}'.format(token,str(random()),fakeid,str(officialAccount_crawlinfo[1]))
                                logging.info('{}上次爬取到page<{}>'.format(nickname,officialAccount_crawlinfo[1]))
                                logging.info('next url:{}'.format(next_url))
                                print('爬取下一条链接：',next_url)
                                time.sleep(self.SLEEP_INTERVAL)
                                yield Request(next_url,callback=self.parse_article_link,meta={'useSelenium':1,'nickname':nickname})
                                # 跳出循环，顺序爬取
                                break
                            elif officialAccount_crawlinfo[0] == 'finished':
                                print('公众号<{}>已爬取完所有数据,skip...'.format(nickname))
                        else:
                            logging.info('正在爬取公众号<{}>'.format(nickname))
                            print('正在爬取公众号<{}>'.format(nickname))
                            url = search_url.format(token,nickname)
                            yield Request(url,callback=self.parse_fakeid,meta={'useSelenium':1})
                            # 跳出循环，顺序爬取
                            break
                            # time.sleep(5)

            except Exception as e:
                logging.exception(e)

    def spider_closed(self,spider):
        self.crawlLogDict['{}-{}'.format(self.TIME_LINE[0],self.TIME_LINE[1])] = self.crawl_task
        with open(CRAWL_FILE_PATH+'crawlLog.json','w',encoding='utf8') as f:
            f.write(dumps(self.crawlLogDict))
        with open(CRAWL_FILE_PATH+'officialAccountDict.json','w',encoding='utf8') as f:
            f.write(dumps(self.officialAccountDict))





