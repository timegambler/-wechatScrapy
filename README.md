# -wechatScrapy
公众号爬虫
1.	安装目录下的chrome浏览器:70.0.3538.67_chrome_installer.exe
注意：如果电脑已经有安装chrome浏览器，请查看版本号https://blog.csdn.net/yoyocat915/article/details/80580
并下载http://npm.taobao.org/mirrors/chromedriver/
匹配版本的chromedriver,并按照2.配置

2.	配置chromedriver.exe
 
 
右键选择”打开文件所在的位置”,将安装目录下的chromedriver.exe 置入该目录下
右键复制目录路径，如：C:\Users\vikky\AppData\Local\Google\Chrome\Application
 
3.	设置环境变量： 
“此电脑”->右键选择->属性->高级系统设置->环境变量->系统变量->path
 
将步骤二中的路径粘贴进来
 
点击”确定”保存设置

4.	微信公众号平台https://mp.weixin.qq.com/申请注册订阅号
 
5.	爬虫配置：打开run/config.json 自行配置(注意，保存时请另存为utf8格式！！！)，主要修改USER_INFO文件，第一个为账号，第二个为密码。
 
 

6.	运行爬虫
 
用管理员微信扫描二维码登录
 

7.	 查看爬取结果
 
 

说明：微信反爬监控比较严格，如有数据爬取不到，请调整爬虫配置项


重要！！！：
位于crawl_file目录下的所有文件为程序配置和输出文件，在程序未完成爬取任务前，输出的csv文件只能查看，务必不要编辑（存在编码转换，导致爬虫续爬时程序无法读取文件）
