import json
from scrapy import signals
import signal


class SignalTrans:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_idle, signal=signals.spider_idle)

        return s

    def spider_opened(self):
        print('爬虫开始')

    def spider_closed(self):
        print('爬虫结束')

    def spider_idle(self):
        print('爬虫空闲')
