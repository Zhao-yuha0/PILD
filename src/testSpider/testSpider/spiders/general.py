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
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider


class TrueniversalCrawler(RedisSpider):

    name = 'slave2'
    redis_key = 'slave1'

    def parse(self, response, **kwargs):
        html = response.text
        tree = etree.HTML(html)  # 创建一个etree实例对象

        tableText = tree.xpath('//table//text()')
        tableStr = ",".join(tableText)
        # print(tableStr)

        ele = tree.xpath('//script | //noscript | //style | //footer | //head | //table')
        for e in ele:
            e.getparent().remove(e)

        content = tree.xpath('string(.)')
        content = content + tableStr

        content = content.replace('\n', '')
        content = content.replace('\r', '')
        content = content.replace('\t', '')
        content = content.replace('\xa0', '')
        content = content.replace('\u3000', '')
        content = content.replace(' ', '')

        # print(content)

        demoItem = DemoItem()

        demoItem['url'] = response.url
        demoItem['content'] = content
        demoItem['time'] = datetime.now().strftime('%H:%M:%S')

        print(demoItem['url'], demoItem['time'], demoItem['content'][0:10])
