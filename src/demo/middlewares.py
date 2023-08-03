# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from datetime import datetime
from demo.items import DemoItem, FileItem
import json
import time
import re
import threading
from threading import Thread
import pymysql
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

# useful for handling different item types with a single interface
# import fileParse
from demo.items import DemoItem


class DemoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumDownloadMiddleware(object):
    def process_request(self, request, spider):
        content = self.selenium_request(request.url)
        if content.strip() != '':
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        return None
        # return None
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    def selenium_request(self, url):
        # js控制浏览器滚动到底部js
        js = """
        function scrollToBottom() {
            var Height = document.body.clientHeight,  //文本高度
                screenHeight = window.innerHeight,  //屏幕高度
                INTERVAL = 100,  // 滚动动作之间的间隔时间
                delta = 500,  //每次滚动距离
                curScrollTop = 0;    //当前window.scrollTop 值
            console.info(Height)
            var scroll = function () {
                //curScrollTop = document.body.scrollTop;
                curScrollTop = curScrollTop + delta;
                window.scrollTo(0,curScrollTop);
                console.info("偏移量:"+delta)
                console.info("当前位置:"+curScrollTop)
            };
            var timer = setInterval(function () {
                var curHeight = curScrollTop + screenHeight;
                if (curHeight >= Height){   //滚动到页面底部时，结束滚动
                    clearInterval(timer);
                }
                scroll();
            }, INTERVAL)
        };
        scrollToBottom()
        """

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        # 窗口最大化
        driver.maximize_window()
        # 执行js滚动浏览器窗口到底部
        driver.execute_script(js)
        content = driver.page_source.encode('utf-8')
        # driver.quit()
        driver.close()
        # return None
        return content


class SignalSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    taskId = 0
    taskName = ''
    startUrl = ''
    domain = ''
    rules = ''
    state = ''
    spider = ''
    type = ''
    startTime = ''
    endTime = ''
    page = 0
    count = 0
    pid = 0

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def spider_opened(self, spider):
        print('spider busy')

        self.taskName = spider.taskName
        self.startUrl = spider.url

        if spider.domain == '仅本网页':
            self.domain = spider.url
        else:
            self.domain = spider.allowed_domains[0]

        self.state = 'running'
        self.taskId = spider.taskId
        self.spider = spider.name
        self.type = spider.spiderType
        self.startTime = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.endTime = ''
        self.page = 0
        self.count = 0
        self.pid = os.getpid()

        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()

        # 添加正在执行任务记录
        sql = "insert into task_list " \
              "(id, name, start_url, domain, rules, state, spider, type, start_time, page, count, pid) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
            self.taskId, self.taskName, self.startUrl, self.domain, self.rules, self.state, self.spider, self.type,
            self.startTime,
            self.page, self.count, self.pid)
        cursor.execute(sql, val)

        # 爬虫置忙
        sql = "update spiders SET state = 'busy', current_task_id = %s WHERE name = %s"
        val = (self.taskId, self.spider)
        cursor.execute(sql, val)

        db.commit()
        db.close()

    # def item_scraped(self, item, spider, response):
    #
    #     self.page += 1
    #
    #     db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    #     cursor = db.cursor()
    #     sql = "update task_list SET page = %s WHERE id = %s "
    #     val = (self.page, self.taskId)
    #     cursor.execute(sql, val)
    #     db.commit()
    #     db.close()
    #
    #     strEmpty = ''
    #     strRes = ''
    #     # 文件的匹配逻辑
    #     if isinstance(item, FileItem):
    #
    #         if item['file_type'] == 'doc':
    #             path = 'fileDownload/' + item['files'][0]['path']
    #             strRes = fileParse.readDoc(path)
    #
    #         if item['file_type'] == 'docx':
    #             path = 'fileDownload/' + item['files'][0]['path']
    #             strRes = fileParse.readDocx(path)
    #
    #         if item['file_type'] == 'xls':
    #             path = 'fileDownload/' + item['files'][0]['path']
    #             strRes = fileParse.readXls(path)
    #
    #         if item['file_type'] == 'xlsx':
    #             path = 'fileDownload/' + item['files'][0]['path']
    #             strRes = fileParse.readXlsx(path)
    #
    #         if item['file_type'] == 'rar' or 'zip':
    #             path = 'fileDownload/' + item['files'][0]['path']
    #             strRes = fileParse.readZip(path)
    #
    #         demoItem = DemoItem()
    #
    #         demoItem['url'] = response.url
    #         demoItem['content'] = strRes
    #         demoItem['taskName'] = spider.taskName
    #         demoItem['taskType'] = spider.taskType
    #         demoItem['time'] = datetime.now().strftime('%H:%M:%S')
    #         demoItem['taskId'] = spider.taskId
    #
    #         yield demoItem

    def spider_closed(self, spider):
        print('spider closed')

        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        # 标记任务完成
        timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
        sql = "update task_list SET state='finish' , end_time = %s WHERE id = %s"
        val = (timeN, self.taskId)
        cursor.execute(sql, val)

        # 恢复爬虫空闲
        sql = "update spiders SET state='free',current_task_id = -1 WHERE name = %s"
        val = self.spider
        cursor.execute(sql, val)
        db.commit()
        db.close()
