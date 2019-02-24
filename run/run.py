# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
 
# 这里是必须引入的
# import robotparser
 
import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues
 
import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle
 
import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader
 
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.chunked
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt
 
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
 
import scrapy.pipelines
 
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

from scrapy import Request,Spider
import time
from datetime import datetime
import re
import logging
from json import loads
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import options
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from pydispatch import dispatcher
from scrapy import signals
import random
import csv
import sys 
import os 
from urllib.request import unquote
sys.path.append(os.path.dirname(__file__))
# from spidertool.workspace.officialAccountSpiders.items import officialAccountItem
# from spidertool.workspace.officialAccountSpiders.settings import USER_AGENT_POOL,PROXY_POOL,VERIFY_CODE_IMG_PATH,BROWSER_OPTION,Cookie,Referer,init_custom_settings,NICKNAME_LIST,SLEEP_INTERVAL,CRAWL_FILE_PATH,TIME_LINE,USER_INFO


process = CrawlerProcess(get_project_settings())
try:
    # 'sk' is the name of one of the spiders of the project.
    process.crawl('officialAccount')
    process.start()  # the script will block here until the crawling is finished
    # time.sleep(30)
except Exception as e:
    print(e)
    time.sleep(5)
