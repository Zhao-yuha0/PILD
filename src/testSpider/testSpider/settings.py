# -*- coding: utf-8 -*-
# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'demo'

SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'

FILES_STORE = 'fileDownload'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 64
CONCURRENT_REQUESTS_PER_IP = 64

RETRY_ENABLED = False
RETRY_TIMES = 2  # 重试次数
DOWNLOAD_TIMEOUT = 3  # 超时
# RETRY_HTTP_CODES = [429, 404, 403]  # 重试
# HTTPERROR_ALLOWED_CODES = [429]

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# 消息队列设置
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_VIRTUAL_HOST = "/"
RABBITMQ_EXCHANGE = "scrapy"
RABBITMQ_ROUTING_KEY = "item"
RABBITMQ_QUEUE = "item"

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'demo.middlewares.DemoSpiderMiddleware': 543,
    # 'demo.middlewares.SignalSpiderMiddleware': 543,
    # 'demo.middlewares.MyFirstSpiderMiddleware': 543,
    # 'demo.middlewares.SeleniumDownloadMiddleware': 543,
    # 'demo.middlewares.SignalSpiderMiddleware': 200,

}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
    # 'demo.middlewares.DemoDownloaderMiddleware': 543,
    # 'demo.middlewares.SeleniumDownloadMiddleware': 543,
    # 'demo.middlewares.SignalSpiderMiddleware': 200,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.files.FilesPipeline': 1,
    # 'demo.pipelines.JsonWriterPipeline': 300,
    # 'demo.pipelines.MyFilesPipeline': 2,
    # 'demo.middlewares.SaveFilePipeline': 543,
    # 'demo.pipelines.DefaultPipeline': 300,
    # 'demo.pipelines.RedisSpiderClose': 300,
    # "demo.pipelines.RabbitMQItemPublisherPipeline": 300,
    # 'demo.pipelines.FilesParsePipeline': 300,
    # 'demo.pipelines.StrParsePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# TWISTED_REACTOR = 'scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')'


# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 调度器持久化
SCHEDULER_PERSIST = True
# 自动清理
SCHEDULER_FLUSH_ON_START = False
# 指定redis地址
# REDIS_URL = "redis://127.0.0.1:6379>"


MYEXT_ENABLED = True  # 开启扩展
IDLE_NUMBER = 24  # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# # 在 EXTENSIONS 配置，激活扩展
# EXTENSIONS = {
#                  'demo.extensions.RedisSpiderSmartIdleClosedExensions': 300,
#              },
