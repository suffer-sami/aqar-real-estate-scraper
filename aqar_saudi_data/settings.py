# Scrapy settings for aqar_saudi_data project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from dotenv import load_dotenv
from aqar_saudi_data.items import AqarItem

load_dotenv()

ZYTE_API_KEY = os.getenv("ZYTE_API_KEY")
if not ZYTE_API_KEY:
    raise ValueError("ZYTE_API_KEY is not set in the environment variables")

BASE_URL = 'https://sa.aqar.fm'

BOT_NAME = "aqar_saudi_data"

SPIDER_MODULES = ["aqar_saudi_data.spiders"]
NEWSPIDER_MODULE = "aqar_saudi_data.spiders"

ADDONS = {
    "scrapy_zyte_api.Addon": 500,
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'app-version': '0.20.44',
        'content-type': 'application/json',
        'dpr': '1.25',
        'origin': BASE_URL,
        'priority': 'u=1, i',
        'referer': BASE_URL,
        'req-app': 'web',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "aqar_saudi_data.middlewares.AqarSaudiDataSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "aqar_saudi_data.middlewares.AqarSaudiDataDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "aqar_saudi_data.pipelines.AqarSaudiDataPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# CSV Export Settings
FEEDS = {
    'saudi_real_estate.csv': {
        'format': 'csv',
        'encoding': 'utf-8-sig',
        'store_empty': False,
        'fields': AqarItem.fields_order,
        'overwrite': False,  # This ensures appending to existing file
    }
}

FEED_EXPORTERS = {
    'csv': 'scrapy.exporters.CsvItemExporter',
}
FEED_EXPORT_FIELDS = AqarItem.fields_order
FEED_EXPORT_FIELDS_OUTPUT_ORDER = AqarItem.fields_order
