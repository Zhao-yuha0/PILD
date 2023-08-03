from urllib.parse import urlparse

import scrapy
import pymysql
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class JsSpider(CrawlSpider):

    def __init__(self, start_urls=None, task_name=None, rule_list=None, domain=None, taskNum=None, **kwargs):
        super().__init__(**kwargs)
        self.taskNum = taskNum
        self.start_urls = []
        self.start_urls.append(start_urls)

        self.allowed_domains = []
        self.domain = domain
        if self.domain == '仅本域名':
            self.allowed_domains.append(urlparse(self.start_urls[0]).netloc)
        elif self.domain == '同级域名':
            this_str = urlparse(self.start_urls[0]).netloc
            up_str = this_str.split('.', 1)[1]
            self.allowed_domains.append(up_str)

        self.task_name = task_name

        self.rules = 'no rule'
        self.spiderName = '网页测试1'
        self.spiderType = '周期全量'
        self.pageCount = 0
        self.fileCount = 0

    name = 'sitetest'

    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'testSpider.middlewares.SeleniumDownloadMiddleware': 543,
            'testSpider.middlewares.TestSpiderMiddleware': 543,
        }
    }

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        self.pageCount += 1

        if self.domain == '仅本网页':
            self.allowed_domains = self.start_urls[0]

        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        sql = "update test_result SET rule = %s,content = %s, page = %s, count = %s, url = %s"
        val = ('无规则', '无内容', self.pageCount, 0, str(self.allowed_domains))
        cursor.execute(sql, val)

        sql1 = "update spiders SET state='free' WHERE name = %s"
        val1 = '网页测试1'
        cursor.execute(sql1, val1)

        db.commit()
        db.close()

        if self.domain == '仅本网页':
            self.crawler.engine.close_spider(self, '仅本页面')
