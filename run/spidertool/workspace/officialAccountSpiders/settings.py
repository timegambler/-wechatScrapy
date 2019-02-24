# coding:utf-8
import os
from datetime import datetime 
from selenium.webdriver.chrome.options import Options


########################## 手动配置项 begin #################################
# USER_INFO = ['0027010','lin8966016'] # 配置用于登录的公众号平台账号/密码，需自行申请并绑定管理员
# # 配置公众号清单，数量较多时建议分批
# NICKNAME_LIST = [
#     '湖南电信',
#     '湖南联通'
# ]
# # 配置需要爬取的起始和终止日期, 建议周期不超过3个月
# TIME_LINE = ['2018-11','2019-01']
# SLEEP_INTERVAL = 8     # 设置网页爬取时间间隔(秒)
USE_BROWSER_INTERFACE = 1   # 配置浏览器是否带界面，取值{0,1},在linux上运行必须设置为0
########################## 手动配置项 end #################################

########################## 自定义内置配置项 begin #################################
WORKSPACE_PATH = './spidertool/workspace/officialAccountSpiders' 
# 验证码图片下载路径
VERIFY_CODE_IMG_PATH = '{}/'.format(WORKSPACE_PATH)

Cookie = ''
Referer = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN'
# UA池
USER_AGENT_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/440.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/440.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/426.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/426.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/427.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/427.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/428.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/428.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/429.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/429.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/430.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/430.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/431.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/431.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/432.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/432.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/433.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/433.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/434.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/434.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/435.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/435.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/436.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/436.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/437.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/437.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/438.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/438.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/439.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/439.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/440.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/440.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/441.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/441.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/442.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/442.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/443.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/443.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/444.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/444.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/445.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/445.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/446.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/446.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/447.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/447.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/448.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/448.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/449.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/449.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/450.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/450.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/451.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/451.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/452.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/452.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/453.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/453.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/454.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/454.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/455.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/455.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/456.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/456.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/457.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/457.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/458.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/458.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/459.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/459.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/460.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/460.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/461.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/461.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/462.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/462.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/463.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/463.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/464.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/464.35 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/465.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/465.36 Edge/17.17134"
]

# 代理IP池
PROXY_POOL = [
    "122.114.82.64:16816",  
    "122.114.234.72:16816",     
    "112.74.206.133:16816",     
    "43.226.164.66:16816",     
    "43.226.164.244:16816",     
    "120.25.71.27:16816",     
    "114.67.143.3:16816",     
    "122.114.69.82:16816",     
    "112.74.108.33:16816",     
    "116.62.128.50:16816",     
    "123.56.246.33:16816",     
    "122.114.197.131:16816",    
    "114.215.174.49:16816",     
    "116.255.162.107:16816",    
    "116.255.162.165:16816",    
    "112.74.202.247:16816",     
    "101.200.185.203:16816",    
    "42.123.83.108:16816",     
    "42.51.205.96:16816",     
    "120.26.167.145:16816"     
]
# 浏览器配置
BROWSER_OPTION = Options()
if not USE_BROWSER_INTERFACE:
    BROWSER_OPTION.add_argument('--headless')    
BROWSER_OPTION.add_argument('--disable-gpu')
BROWSER_OPTION.add_argument('--no-sandbox')
BROWSER_OPTION.add_experimental_option("prefs",{"profile.default_content_setting_values":{'notifications':2}}) # 禁止弹窗和图片加载
BROWSER_OPTION.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"')
########################## 自定义内置配置项 end #################################


########################## scrapy内置配置项 begin #################################
def init_custom_settings():
    # 初始化该爬虫的scrapy配置
    custom_settings = globals()
    return custom_settings

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 5

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'mp.weixin.qq.com',
    # 'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1453156335&lang=zh_CN',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie':''
}

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'spidertool.workspace.officialAccountSpiders.middlewares.UserAgentMiddleware': 543,
    'spidertool.workspace.officialAccountSpiders.middlewares.SeleniumMiddleware': 543
}

try:
    CRAWL_FILE_PATH = os.mkdir('{}/crawl_file/'.format('../'))
except:
    pass
CRAWL_FILE_PATH ='{}/crawl_file/'.format('../')

ITEM_PIPELINES = {
   'spidertool.workspace.officialAccountSpiders.pipelines.officialAccountPipeline': 300,
}

# 日志文件输出路径
LOG_ENABLED = True
LOG_ENCODING = 'utf8'
try:
    os.mkdir('{}/log_file'.format(WORKSPACE_PATH))
except:
    pass
try:
    os.remove('{}/log_file/crawl_log.log'.format(WORKSPACE_PATH))
except:
    pass
today = datetime.now()
LOG_FILE_PATH = '{}/log_file/crawl_log.log'.format(WORKSPACE_PATH)
LOG_LEVEL = 'INFO'
LOG_FILE = LOG_FILE_PATH

########################## scrapy内置配置项 end #################################