# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import os
import re
import shelve
import time
import pymysql
from datetime import datetime, date, timedelta
import docx
import xlrd
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver


# useful for handling different item types with a single interface


class TestspiderSpiderMiddleware:
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


class TestspiderDownloaderMiddleware:
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


class OldMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    start_time = 0
    end_time = 0
    count = 0
    page = 0
    res = {}
    taskView = {}
    data = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(s.response_received, signal=signals.response_received)
        crawler.signals.connect(s.request_scheduled, signal=signals.request_scheduled)

        return s

    def spider_opened(self, spider):
        file_name = '../../bufferTempTask/' + spider.task_name + '.json'

        if os.path.exists(file_name):
            os.remove(file_name)

        self.file = open(file_name, 'w')

        dic = {'name': spider.task_name}
        self.taskView.update(dic)

        dic = {'start_time': time.asctime(time.localtime(time.time()))}
        self.res.update(dic)
        self.taskView.update(dic)

        dic = {'start_url': spider.start_urls[0]}
        self.res.update(dic)

        dic = {'allow_domain': spider.allowed_domains[0]}
        self.res.update(dic)

    def item_scraped(self, item, spider, response):
        self.count += 1
        item['url'] = response.url
        item['time'] = time.asctime(time.localtime(time.time()))
        self.data.append(dict(item))

    def response_received(self, spider):
        pass

    def request_scheduled(self, spider):
        self.page += 1

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()

        dic = {'end_time': time.asctime(time.localtime(time.time()))}
        self.res.update(dic)
        self.taskView.update(dic)

        dic = {'count': self.count}
        self.res.update(dic)
        self.taskView.update(dic)

        dic = {'page': stats['downloader/response_status_count/200']}
        self.res.update(dic)
        self.taskView.update(dic)

        dic = {'data': self.data}
        self.res.update(dic)

        json_str = json.dumps(self.res)
        self.file.write(json_str)
        self.file.close()

        with open('../../static/json/taskTemp.json', 'r') as listFile:
            fileDict = json.load(listFile)
        listFile.close()

        fileDict['data'].append(self.taskView)

        with open('../../static/json/taskTemp.json', 'w') as listFile:
            json.dump(fileDict, listFile)
        listFile.close()

    def spider_idle(self, spider):
        pass


class SignalSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    taskID = ''
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
        crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def spider_opened(self, spider):

        self.taskName = spider.task_name
        self.startUrl = spider.start_urls[0]

        if spider.domain == '仅本网页':
            self.domain = spider.start_urls[0]
        else:
            self.domain = spider.allowed_domains[0]

        ruleNameList = list(spider.rules.keys())  # 规则字典
        self.rules = ','.join(ruleNameList)

        self.state = 'running'
        self.spider = spider.spiderName
        self.type = spider.spiderType
        self.startTime = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.endTime = ''
        self.page = 0
        self.count = 0
        self.pid = os.getpid()

        db = pymysql.connect(user="root", passwd="", db="ConTest")
        cursor = db.cursor()

        # 添加正在执行任务记录
        sql = "insert into task_list " \
              "(name, start_url, domain, rules, state, spider, type, start_time, page, count, pid) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
        self.taskName, self.startUrl, self.domain, self.rules, self.state, self.spider, self.type, self.startTime,
        self.page, self.count, self.pid)
        cursor.execute(sql, val)
        self.taskID = cursor.lastrowid
        # 爬虫置忙
        sql = "update spiders SET state = 'busy', current_task_id = %s WHERE name = %s"
        val = (self.taskID, self.spider)
        cursor.execute(sql, val)

        db.commit()
        db.close()

    def item_scraped(self, item, spider, response):

        self.page += 1

        db = pymysql.connect(user="root", passwd="", db="ConTest")
        cursor = db.cursor()
        sql = "update task_list SET page = %s WHERE id = %s "
        val = (self.page, self.taskID)
        cursor.execute(sql, val)
        db.commit()
        db.close()

        strEmpty = ''
        strRes = ''
        # 文件的匹配逻辑
        if item['file_name']:

            if item['file_type'] == 'doc' or item['file_type'] == 'docx':
                path = 'fileDownload/' + item['files'][0]['path']
                file = docx.Document(path)
                res = []
                for para in file.paragraphs:
                    if para.text != '':
                        res.append(para.text)
                strRes = strEmpty.join(res)

            if item['file_type'] == 'xls' or item['file_type'] == 'xlsx':
                path = 'fileDownload/' + item['files'][0]['path']
                book = xlrd.open_workbook(path)
                names = book.sheet_names()
                res = []

                for name in names:
                    sheet = book.sheet_by_name(name)
                    rowCounts = sheet.nrows
                    for i in range(rowCounts):
                        data = sheet.row(i)
                        for cell in data:
                            if cell.value != '':
                                resStr = str(cell.value)
                                res.append(resStr.replace('\n', ''))
                    strRes = strEmpty.join(res)

            # 正则检测
            ruleDict = spider.rules  # 规则字典
            for key in ruleDict:
                resFind = re.findall(ruleDict[key], strRes)
                if len(resFind) != 0:
                    for resItem in resFind:
                        self.count += 1

                        timeN = datetime.now().strftime('%Y-%m-%d %H:%M')

                        db = pymysql.connect(user="root", passwd="", db="ConTest")
                        cursor = db.cursor()
                        sql = "update task_list SET page = %s, count = %s WHERE id = %s "
                        val = (self.page, self.count, self.taskID)
                        cursor.execute(sql, val)

                        sql = "insert into res(task_id, name, task_type, rules, content, time, url) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s) "
                        val = (self.taskID, self.taskName, self.type, self.rules, resItem, timeN, response.url)
                        cursor.execute(sql, val)
                        db.commit()
                        db.close()

        else:
            # 正则检测
            ruleDict = spider.rules  # 规则字典
            for key in ruleDict:
                resFind = re.findall(ruleDict[key], item['content'])
                if len(resFind) != 0:
                    # 匹配到内容
                    for resItem in resFind:
                        self.count += 1

                        timeN = datetime.now().strftime('%Y-%m-%d %H:%M')

                        db = pymysql.connect(user="root", passwd="", db="ConTest")
                        cursor = db.cursor()
                        sql = "update task_list SET page = %s, count = %s WHERE id = %s"
                        val = (self.page, self.count, self.taskID)
                        cursor.execute(sql, val)

                        sql = "insert into res(task_id, name, task_type, rules, content, time, url) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s) "
                        val = (self.taskID, self.taskName, self.type, key, str(resItem), timeN, response.url)
                        cursor.execute(sql, val)
                        db.commit()
                        db.close()

                        # 文件写入
                        filePath = '../../' + 'fileTest' + '/' + self.taskName
                        with shelve.open(filePath) as data:
                            data[response.url] = item['content']

    def spider_closed(self, spider):

        db = pymysql.connect(user="root", passwd="", db="ConTest")
        cursor = db.cursor()
        # 标记任务完成
        timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
        sql = "update task_list SET state='finish' , end_time = %s WHERE id = %s"
        val = (timeN, self.taskID)
        cursor.execute(sql, val)

        # 恢复爬虫空闲
        sql = "update spiders SET state='free',current_task_id = -1 WHERE name = %s"
        val = self.spider
        cursor.execute(sql, val)
        db.commit()
        db.close()



class TestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    taskID = ''
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
        crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def spider_opened(self, spider):
        self.spider = spider.name
        # 爬虫置忙
        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        sql = "update spiders SET state = 'busy' WHERE name = %s"
        val = self.spider
        cursor.execute(sql, val)

        db.commit()
        db.close()

    def item_scraped(self, item, spider, response):
        pass

    def spider_closed(self, spider, reason):
        # 恢复爬虫空闲
        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        sql = "update spiders SET state='free' WHERE name = %s"
        val = self.spider
        cursor.execute(sql, val)
        db.commit()
        db.close()
