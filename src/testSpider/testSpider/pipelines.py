# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from os.path import basename
from urllib.parse import urlparse
from testSpider.items import StrItem,FileItem

import scrapy.pipelines
import re
import time

from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.files import FilesPipeline


class FileParsePipeline(object):

    def process_item(self, item, spider):
        if item['file_name']:
            print('==============file item==============')
            print(item)
            # item = StrItem()
        return item


class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None,):
        path = urlparse(request.url).path
        fileName = str(response.meta['link_text'])
        return fileName
