# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()
    file_type = scrapy.Field()


class StrItem(scrapy.Item):
    file_name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()


class DemoItem(scrapy.Item):
    file_name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()