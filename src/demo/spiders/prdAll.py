# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urlparse

import scrapy
import re
import urllib
from copy import deepcopy
from demo.items import DemoItem, FileItem
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class TrueniversalCrawler(RedisCrawlSpider):

    def __init__(self, taskId=None, taskName=None, domain=None, url=None, taskType=None, **kwargs):
        super().__init__(**kwargs)

        # 初始化参数
        self.taskId = taskId
        self.taskName = taskName
        self.domain = domain
        self.taskType = taskType
        self.url = url

        # 确定任务域名
        self.allowed_domains = []
        if self.domain == '仅本域名':
            self.allowed_domains.append(urlparse(self.url).netloc)
        elif self.domain == '同级域名':
            this_str = urlparse(self.url).netloc
            up_str = this_str.split('.', 1)[1]
            self.allowed_domains.append(up_str)

    name = 'prdall'
    redis_key = 'prdall'
    spiderType = '周期全量'

    rules = (
        Rule(LinkExtractor(), callback='parse_page_link', follow=True),
        Rule(LinkExtractor(allow=('xlsx', 'xls', 'doc', 'docx'),
                           deny_extensions=""), callback='parse_file_link', follow=True)
    )

    def parse_page_link(self, response):
        html = response.text
        tree = etree.HTML(html)

        ele = tree.xpath('//script | //noscript | //style | //footer | //head')
        for e in ele:
            e.getparent().remove(e)

        content = tree.xpath('string(.)')
        content = content.replace('\n', ' ')
        content = content.replace('\r', ' ')
        content = content.replace('\t', '')
        content = content.replace('\xa0', '')
        content = content.replace('\u3000', '')
        content = content.replace(' ', '')

        # print(content)

        demoItem = DemoItem()

        demoItem['url'] = response.url
        demoItem['content'] = content
        demoItem['taskName'] = self.taskName
        demoItem['taskType'] = self.taskType
        demoItem['time'] = datetime.now().strftime('%H:%M:%S')
        demoItem['taskId'] = self.taskId

        yield demoItem

    def parse_file_link(self, response):
        print('get file url：', response.url)

    def parse_start_url(self, response):
        html = response.text
        tree = etree.HTML(html)

        ele = tree.xpath('//script | //noscript | //style | //footer | //head')
        for e in ele:
            e.getparent().remove(e)

        content = tree.xpath('string(.)')
        content = content.replace('\n', ' ')
        content = content.replace('\r', ' ')
        content = content.replace('\t', '')
        content = content.replace('\xa0', '')
        content = content.replace('\u3000', '')
        content = content.replace(' ', '')

        print(content)

        demoItem = DemoItem()

        demoItem['url'] = response.url
        demoItem['content'] = content
        demoItem['taskName'] = self.taskName
        demoItem['taskType'] = self.taskType
        demoItem['time'] = datetime.now().strftime('%H:%M:%S')
        demoItem['taskId'] = self.taskId

        yield demoItem

        if self.domain == '仅本网页':
            self.crawler.engine.close_spider(self, '仅本页面')
