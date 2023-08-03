import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing.context import Process
from scrapy import cmdline
import os
import redis


def set_new_path(path):
    os.chdir(path)


def set_old_path(path):
    os.chdir(path)


# 启动网页测试爬虫
def startPageTestSpider(spiderName, taskId, taskName, domain, url, taskType):
    os.chdir('/root/demo/project/testSpider/testSpider/')
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiderName,
                  taskId=taskId,
                  taskName=taskName,
                  domain=domain,
                  url=url,
                  taskType=taskType)
    process.start()
    os.chdir('/root/demo/project')


# 启动规则测试爬虫
def startRuleTestSpider(spiderName, taskId, taskName, domain, url, taskType):
    os.chdir('/root/demo/project/testSpider/testSpider/')
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiderName,
                  taskId=taskId,
                  taskName=taskName,
                  domain=domain,
                  url=url,
                  taskType=taskType)
    process.start()
    os.chdir('/root/demo/project')


def startTestSpider(spiderName, site_input, task_name, domain, rule_list, taskNum):
    os.chdir('/root/demo/project/testSpider/testSpider/')
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiderName,
                  start_urls=site_input,
                  task_name=task_name,
                  domain=domain,
                  rule_list=rule_list,
                  taskNum=taskNum)
    process.start()
    os.chdir('/root/demo/project')


# 启动任务爬虫-redisSpiders
def startRedisSpider(spiderName, taskId, taskName, domain, url, taskType):
    # 向redis写入url
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.lpush(spiderName, url)
    r.connection_pool.disconnect()

    os.chdir('/root/demo/project/demo')
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiderName,
                  taskId=taskId,
                  taskName=taskName,
                  domain=domain,
                  url=url,
                  taskType=taskType)
    process.start()
    os.chdir('/root/demo/project')


# 根据任务类型启动任务爬虫
def start_spider_threads(spiderName, taskId, taskName, domain, url, taskType):
    # 在进程中启动爬虫
    crawl_threads = Process(target=startRedisSpider,
                            args=(spiderName, taskId, taskName, domain, url, taskType))
    crawl_threads.start()


# 根据任务类型启动任务爬虫和测试爬虫
def start_Test_threads(spiderName, site_input, task_name, domain, rule_list, taskNum):
    # 在进程中启动测试爬虫
    crawl_threads = Process(target=startTestSpider,
                            args=(spiderName, site_input, task_name, domain, rule_list, taskNum))
    crawl_threads.start()
