from datetime import datetime
from urllib.parse import urlparse

import scrapy
import pymysql
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from testSpider.items import StrItem,FileItem
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
        self.spiderName = '周期增量1'
        self.spiderType = '周期增量'

        db = pymysql.connect(user="root", passwd="", db="ConTest")
        cursor = db.cursor()
        cursor.execute("select url from url_history where name = %s", self.task_name)
        self.urls = cursor.fetchall()
        self.urlHistory = []
        for urlTuple in self.urls:
            self.urlHistory.append(urlTuple[0])

        db.close()

    name = '周期增量1'

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('xlsx','xls','doc','docx'),
                           deny_extensions = ""),callback='parse_file_link',follow=True)
    )


    def parse_item(self, response):

        # 在监测历史中
        if response.url in self.urlHistory:
            pass
        else:

            html = response.xpath("//html").xpath('string(.)').extract()[0]

            res = html.replace('\n', '')
            res = res.replace('\r', '')
            res = res.replace('\t', '')
            res = res.replace('\xa0', '')
            res = res.replace('\u3000', '')
            res = res.replace(' ', '')
            resItem = StrItem()
            resItem['url'] = response.url
            resItem['content'] = res
            resItem['file_name'] = None

            db = pymysql.connect(user="root", passwd="", db="ConTest")
            cursor = db.cursor()
            sql = "insert into url_history (name, task_id, url, time) values (%s, %s, %s, %s)"
            val = (self.task_name, self.taskNum, response.url, datetime.now().strftime('%Y-%m-%d %H:%M'))
            cursor.execute(sql,val)
            db.commit()
            db.close()

            yield resItem

    def parse_file_link(self, response):

        if response.url in self.urlHistory:
            pass
        else:
            db = pymysql.connect(user="root", passwd="", db="ConTest")
            cursor = db.cursor()
            sql = "insert into url_history (name, task_id, url, time) values (%s, %s, %s, %s)"
            val = (self.task_name, self.taskNum, response.url, datetime.now().strftime('%Y-%m-%d %H:%M'))
            cursor.execute(sql, val)
            db.commit()
            db.close()

            fileItem = FileItem()
            fileItem['file_urls'] = [response.url]
            fileItem['file_name'] = str(response.meta['link_text'])
            fileItem['file_type'] = response.url.split('.')[-1]
            yield fileItem

    def parse_start_url(self, response):

        # 在监测历史中
        if response.url in self.urlHistory:
            pass
        else:

            html = response.xpath("//html").xpath('string(.)').extract()[0]

            res = html.replace('\n', '')
            res = res.replace('\r', '')
            res = res.replace('\t', '')
            res = res.replace('\xa0', '')
            res = res.replace('\u3000', '')
            res = res.replace(' ', '')
            resItem = StrItem()
            resItem['url'] = response.url
            resItem['content'] = res
            resItem['file_name'] = None

            db = pymysql.connect(user="root", passwd="", db="ConTest")
            cursor = db.cursor()
            sql = "insert into url_history (name, task_id, url, time) values (%s, %s, %s, %s)"
            val = (self.task_name, self.taskNum, response.url, datetime.now().strftime('%Y-%m-%d %H:%M'))
            cursor.execute(sql, val)
            db.commit()
            db.close()

            yield resItem



        if self.domain == '仅本网页':
            self.crawler.engine.close_spider(self, '仅本页面')

