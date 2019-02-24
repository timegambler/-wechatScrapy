# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import options
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from pydispatch import dispatcher
from scrapy import signals
from datetime import datetime
import time
import logging
import random
import re
from spidertool.workspace.officialAccountSpiders.settings import USER_AGENT_POOL,PROXY_POOL,VERIFY_CODE_IMG_PATH,BROWSER_OPTION,Cookie,Referer


class UserAgentMiddleware(UserAgentMiddleware):
    def __init__(self,user_agent_pool):
        self.user_agent_pool = user_agent_pool

    def process_request(self,request,spider):
        user_agent = random.choice(self.user_agent_pool)
        request.headers["user-agent"] = user_agent
        request.headers["Cookie"] = Cookie
        request.headers["Referer"] = Referer
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(user_agent_pool= USER_AGENT_POOL)

class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    
    def __init__(self,proxy_pool):
        self.proxy_pool = proxy_pool

    def process_request(self,request,spider):
        proxy_ip = random.choice(self.proxy_pool)
        request.headers['Proxy-Authorization'] = proxy_ip 
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(proxy_pool=PROXY_POOL)
        
class SeleniumMiddleware():
    counter = 1 # 记录请求发起次数
    def __init__(self):
        self.chrome_option = BROWSER_OPTION
        self.browser = webdriver.Chrome(options=self.chrome_option)
        self.browser.set_window_size(1366,768)
        self.wait = WebDriverWait(self.browser, 20)
        logging.info('browser has been created')
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self,spider):
        #当爬虫退出的时候 关闭chrome
        logging.info("spider closed")
        print('数据爬取程序结束!')
        self.browser.quit()
    
    def process_request(self,request,spider):
        # logging.info('crawl url:%s'%request.url)
        # logging.info('user_agent:%s'%request.headers["User-Agent"])
        useSelenium = request.meta.get('useSelenium',False)
        if useSelenium:
            user_info = request.meta.get('user_info',False)
            parse_type = request.meta.get('parse_type',False)
            if spider.name == 'officialAccount':
                if user_info:
                    self.browser.get(request.url)
                    self.browser.implicitly_wait(10)
                    username = self.browser.find_elements_by_name('account')[0]
                    password = self.browser.find_elements_by_name('password')[0]
                    username.send_keys(user_info[0])
                    password.send_keys(user_info[1])
                    time.sleep(1)
                    self.browser.find_elements_by_class_name('btn_login')[0].click()
                    self.browser.implicitly_wait(20)
                    print('请扫面微信二维码验证登陆...')
                    time.sleep(2)
                    self.browser.save_screenshot(VERIFY_CODE_IMG_PATH+'wechat_qrcode.bmp')
                    try_times = 0
                    while 'login' in self.browser.current_url or '立即注册' in self.browser.page_source:
                        if try_times >10:
                            logging.warn('exceeded max try times..')
                            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',status=202)
                        else:
                            logging.info('暂未扫码验证,第%s次等待...'%try_times)
                            time.sleep(10)
                            try_times += 1
                    self.browser.refresh()
                    return HtmlResponse(url=request.url, body=self.browser.current_url, request=request, encoding='utf-8',status=200)
                    
                # if parse_type == 'parse_fakeid':
                else:
                    if self.counter >24:
                        logging.info('暂停15分钟')
                        time.sleep(60*15)
                        self.counter = 0
                    else:
                        self.counter += 1
                    nickname = request.meta.get('nickname',False)
                    self.browser.get(request.url)
                    self.browser.implicitly_wait(20)
                    if 'searchbiz' in request.url:
                        global Cookie
                        global Referer
                        token = str(re.findall('token=(\d*)',self.browser.current_url)[0])
                        Referer = Referer.format(token)
                        if Cookie == '':
                            for item in self.browser.get_cookies():
                                Cookie += '{}={};'.format(item['name'],item['value'])
                    return HtmlResponse(url=request.url, body=self.browser.page_source,flags=[nickname],request=request, encoding='utf-8',status=200)
