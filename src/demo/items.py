# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TestItem(scrapy.Item):
    order = scrapy.Field()
    time = scrapy.Field()
    pid = scrapy.Field()


class StrItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()


class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()
    file_type = scrapy.Field()
    taskId = scrapy.Field()


class DemoItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    taskName = scrapy.Field()
    taskType = scrapy.Field()
    time = scrapy.Field()
    taskId = scrapy.Field()
