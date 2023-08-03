from urllib.parse import urlparse

import scrapy
from lxml import etree
from html.parser import HTMLParser
from testSpider.items import DemoItem


class DemoSpider(scrapy.Spider):

    def __init__(self, start_urls=None, task_name=None, taskNum=None, **kwargs):
        super().__init__(**kwargs)

        self.taskNum = taskNum
        self.start_urls = []
        self.start_urls.append(start_urls)

        self.allowed_domains = []

        self.task_name = task_name

        self.spiderName = 'demoSpider'
        self.spiderType = '临时任务'

    name = 'demoSpider'


    def parse(self, response):
        html = response.text
        with open('baidu.html', 'w', encoding='utf-8') as fp:
            fp.write(html)
            fp.close()
        tree = etree.HTML(html)
        # 筛选出js css标签
        ele = tree.xpath('//script | //noscript | //style')
        # 测试
        # ele1 = tree.xpath('//div/text()')
        # print('ele1=%s'%ele1)
        # js css标签踢掉
        for e in ele:
            e.getparent().remove(e)
        # 取网页中剩余标签的纯文本
        content = tree.xpath('string(.)')
        content = content.replace('\n', ' ')
        content = content.replace('\r', ' ')
        content = content.replace('\t', '')
        content = content.replace('\xa0', '')
        content = content.replace('\u3000', '')
        content = content.replace(' ', '')
