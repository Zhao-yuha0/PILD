import json
from scrapy import cmdline
import os, redis

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# site_input1 = 'http://cstc.hrbeu.edu.cn/2021/0413/c3688a267228/page.htm'
# site_input2 = 'http://cstc.hrbeu.edu.cn/3688/list.htm'
# task_name = 'ruleFinder'
# rule_list = {'身份证': '^[1-9]\\d{5}(18|19|([23]\\d))\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$'}
# domain = 'this'
#
# process = CrawlerProcess(get_project_settings())
# process.crawl('geng',
#               start_urls=site_input2,
#               task_name=task_name,
#               domain=domain,
#               rule_list=rule_list)
# process.start()

# process = CrawlerProcess(get_project_settings())
# process.crawl('general', start_urls='http://sec.hrbeu.edu.cn/2017/1220/c227a177569/page.htm', allowed_domains=['sec.hrbeu.edu.cn'])
# process.start()

# allowed_domains = ['https://baijiahao.baidu.com/s?id=1715188026568423850&wfr=spider&for=pc']


rule_list = {'测试': '[1-9][0-9]{8,}'}

url = 'http://cstc.hrbeu.edu.cn/2021/0519/c11981a270292/page.htm'  # 起始网页
spiderName = 'slave2'  # 由控制模块根据任务类型获取空闲爬虫名称，由名称启动相应爬虫

taskId = 999  # 任务ID
taskName = 'demoTask'  # 任务名称
domain = '网页'  # 仅本网页 同级域名 仅本域名
taskType = '临时任务'  # 临时任务 周期增量 周期全量 站点测试 规则测试

# 连接到redis数据库，加入起始地址
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r.lpush(spiderName, url)
# r.connection_pool.disconnect()
# 启动爬虫，传入参数
# os.chdir('/root/demo/project/demo')
process = CrawlerProcess(get_project_settings())
process.crawl(spiderName)
process.start()
os.chdir('/root/demo/project')
