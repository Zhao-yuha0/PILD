# -*- coding: utf-8
import os

from scrapy import cmdline
import scrapy
import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# cmdline.execute('scrapy crawl txms'.split())

# site_input1 = 'http://www.ebook80.com/education/6830.html'
# site_input2= 'http://www.hrbxflz.gov.cn/news_show.php?cid=12&id=6394'
# task_name = '1150'
# rule_list = {'身份证': '^[1-9]\\d{5}(18|19|([23]\\d))\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$'}
# domain = 'pageOnly'

# pid = os.getpid()
# print('debug', pid)

# process = CrawlerProcess(get_project_settings())
# # print('=========list:',process.spiders.list())
#
# process.crawl('txms',
#               start_urls=site_input2,
#               task_name=task_name,
#               domain=domain,
#               rule_list=rule_list)
# process.start()
rule_list = {'测试': '[1-9][0-9]{8,}'}

url = 'http://cstc.hrbeu.edu.cn/bzrgz/list.htm'  # 起始网页
spiderName = 'slave1'  # 由控制模块根据任务类型获取空闲爬虫名称，由名称启动相应爬虫

taskId = 99  # 任务ID
taskName = 'demoTask'  # 任务名称
domain = '仅本网页'  # 仅本网页 同级域名 仅本域名
taskType = '临时任务'  # 临时任务 周期增量 周期全量 站点测试 规则测试

# 连接到redis数据库，加入起始地址
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r.lpush(spiderName, url)
# r.connection_pool.disconnect()
# 启动爬虫，传入参数
process = CrawlerProcess(get_project_settings())
process.crawl(spiderName,
              taskId=taskId,
              taskName=taskName,
              domain=domain,
              url=url,
              taskType=taskType)
process.start()

# process = CrawlerProcess(get_project_settings())
# process.crawl('RuleTest')
# process.start()
# process = CrawlerProcess(get_project_settings())
# process.crawl('demoSpider')#爬虫名称
# process.start() # the script will block here until the crawling is finished
# /usr/local/lib/python3.8/site-packages
# ln -s /usr/local/lib/python3.8 /usr/bin/python3
# lpush slave:start_urls https://blog.csdn.net/lh_python/article/details/79704102
