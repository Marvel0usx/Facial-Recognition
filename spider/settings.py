# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spider.middlewares.SpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'spider.middlewares.SpiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'spider.pipelines.SpiderPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

SPIDER_MIDDLEWARES = {
    # Custom proxy middleware
    "spider.middlewares.ProxyUADownloaderMiddleware": 150,
}

# Custom pipelines
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1,
                  'spider.pipelines.MongoDBPipeline': 300,
                  }

# Path for ImagePipeline
IMAGES_STORE = r"E:/data"

# MongoDB local instance
MONGO_URI = "mongodb://127.0.0.1:27017/"
MONGO_DB = "local"

# Proxy
PROXY_HTTPS = ['162.159.242.51:80',
               '162.159.242.181:80',
               '162.159.242.65:80',
               '162.159.242.85:80',
               '162.159.242.9:80',
               '162.159.242.250:80',
               '54.38.155.93:6582',
               '185.114.137.14:103',
               '185.114.137.14:14202',
               '159.8.114.37:8123',
               '159.8.114.37:80',
               '159.8.114.37:25',
               '188.170.233.100:3128',
               '188.170.233.106:3128',
               '169.57.1.85:25',
               '83.76.20.220:64527',
               '144.217.101.245:3129',
               '80.187.140.74:8080',
               '81.201.60.130:80',
               '140.227.237.154:1000',
               '46.218.155.194:3128',
               '81.201.60.130:80',
               '51.75.162.18:9999',
               '162.159.242.136:80',
               '58.96.153.138:8080',
               '81.201.60.130:80',
               '34.105.59.26:80',
               '185.243.56.133:80',
               '8.129.33.40:3128',
               '139.99.105.5:80',
               '182.72.150.242:8080',
               '185.243.56.237:80',
               '54.38.218.211:6582',
               '54.38.218.208:6582'
               ]

# Spider Settings
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    "Authorization": "API-Key Cph30qkLrdJDkjW-THCeyA",
    "Connection": "keep-alive",
    "Cookie": "gp_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU4OTVmODZhM2VmNjU1YjAyOWQ5YzhlZjYxYzFjMGJiMDJhNDQwZjc3ZWI1MmU1YjcxODlmM2Y5MGRiZjk1M2M4BjsARkkiDGNhcnRfaWQGOwBGSSIdNWYzNWZkMDE1OWE5N2YwMDE1NWZlNjdjBjsAVA%3D%3D--acd84dae50bb50665804d7b3563468e02960376b; _ga=GA1.2.569598143.1597373702; _gid=GA1.2.976846795.1597373702; _gat=1",
    "DNT": "1",
    "Host": "api.generated.photos",
    "Origin": "https://generated.photos",
    "Referer": "https://generated.photos/faces/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
}

URL = "https://api.generated.photos/api/frontend/v1/images?order_by=latest&page={}&per_page={}"
TOTAL_PAGE = 200
PER_PAGE = 100