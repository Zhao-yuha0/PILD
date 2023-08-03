from urllib.parse import urlparse

import scrapy
import pymysql
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class JsSpider(CrawlSpider):

    def __init__(self, start_urls=None, task_name=None, rule_list=None, domain=None,taskNum=None, **kwargs):
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

        self.rules = rule_list
        self.spiderName = '规则测试1'
        self.spiderType = '周期全量'

    name = 'ruletest'

    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'testSpider.middlewares.SeleniumDownloadMiddleware': 543,
            'testSpider.middlewares.TestSpiderMiddleware': 543,
        }
    }

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=False),
    )


    def parse_item(self, response):
        pass


    def parse_start_url(self, response):

        html = response.xpath("//html").xpath('string(.)').extract()[0]

        res = html.replace('\n', '')
        res = res.replace('\r', '')
        res = res.replace('\t', '')
        res = res.replace('\u3000', '')
        res = res.replace('\xa0', '')
        res = res.replace(' ', '')

        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        cursor.execute("delete from test_result ;")
        db.commit()
        db.close()

        ruleDict = self.rules  # 规则字典
        for key in ruleDict:
            resFind = re.findall(ruleDict[key], res)
            if len(resFind) != 0:
                # 匹配到内容
                count = len(resFind)
                page = 1
                content = ','.join(resFind)

                db = pymysql.connect(user="root", passwd="123456", db="ConTest")
                cursor = db.cursor()

                sql = "insert into test_result(rule, content, page, count, url) VALUES (%s,%s,%s,%s,%s) "
                val = (ruleDict[key],content,page,count,response.url)
                cursor.execute(sql, val)
                db.commit()
                db.close()

        self.crawler.engine.close_spider(self, '仅本页面测试')

