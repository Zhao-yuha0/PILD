import json, os, time
from datetime import datetime
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.enterprise import adbapi
import copy
import scrapy
from itemadapter import ItemAdapter

from demo.items import DemoItem, FileItem
import pymysql
# import fileParse
import pika
from scrapy.exporters import JsonItemExporter
from demo.items import DemoItem, FileItem
import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join
import json

# import pika
from scrapy.utils.serialize import ScrapyJSONEncoder

logger = logging.getLogger(__name__)


class RedisSpiderClose(object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number,
                                                                                self.idle_list[0], self.idle_list[0]))
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')


class SaveFilePipeline(object):

    def open_spider(self, spider):
        print('========pipeline open========')
        # 输出到json文件
        fileName = spider.task_name + '.json'
        self.file = open(fileName, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        print('========pipeline close========')
        # 可选实现，当spider被关闭时，这个方法被调用
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, ):
        path = urlparse(request.url).path
        fileName = basename(path)
        return fileName


class FilesParsePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, FileItem):
            print('file parse pipeline', item)


class StrParsePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, DemoItem):
            print('str parse pipeline', item)
        return item


class DefaultPipeline(object):

    def process_item(self, item, spider):
        print(item)


class RabbitMQItemPublisherPipeline(object):
    page = 0
    file = 0
    body = ''

    def process_item(self, item, spider):

        strRes = ''

        # 文件的匹配逻辑
        if isinstance(item, FileItem):

            if item['file_type'] == 'doc':
                path = 'fileDownload/' + item['files'][0]['path']
                # strRes = fileParse.readDoc(path)

            if item['file_type'] == 'docx':
                path = 'fileDownload/' + item['files'][0]['path']
                # strRes = fileParse.readDocx(path)

            if item['file_type'] == 'xls':
                path = 'fileDownload/' + item['files'][0]['path']
                # strRes = fileParse.readXls(path)

            if item['file_type'] == 'xlsx':
                path = 'fileDownload/' + item['files'][0]['path']
                # strRes = fileParse.readXlsx(path)

            if item['file_type'] == 'rar' or 'zip':
                path = 'fileDownload/' + item['files'][0]['path']
                # strRes = fileParse.readZip(path)

            demoItem = DemoItem()

            demoItem['url'] = item['file_urls'][0]
            demoItem['content'] = strRes
            demoItem['taskName'] = spider.taskName
            demoItem['taskType'] = spider.taskType
            demoItem['time'] = datetime.now().strftime('%H:%M:%S')
            demoItem['taskId'] = spider.taskId

            body = str(demoItem)

            self.file += 1
            db = pymysql.connect(user="root", passwd="123456", db="ConTest")
            cursor = db.cursor()
            sql = "update task_list SET file = %s WHERE id = %s "
            val = (self.file, item['taskId'])
            cursor.execute(sql, val)
            db.commit()
            db.close()

        else:  # 普通item

            self.page += 1
            db = pymysql.connect(user="root", passwd="123456", db="ConTest")
            cursor = db.cursor()
            sql = "update task_list SET page = %s WHERE id = %s "
            val = (self.page, item['taskId'])
            cursor.execute(sql, val)
            db.commit()
            db.close()

            body = str(item)

        username = 'root'
        pwd = 'root'
        ip_addr = '127.0.0.1'
        # ip_addr = '192.168.102.201'
        # ip_addr = '172.20.10.5'

        port_num = 5672
        credentials = pika.PlainCredentials(username, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(ip_addr, port_num, '/', credentials, 10))

        channel = connection.channel()
        channel.queue_declare(queue='hello3', durable=False)
        channel.basic_publish(exchange='', routing_key='hello3', body=body)
        channel.confirm_delivery()
        print("[x] Sent %s" % body)
        connection.close()
