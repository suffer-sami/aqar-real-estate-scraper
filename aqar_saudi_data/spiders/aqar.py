import scrapy


class AqarSpider(scrapy.Spider):
    name = "aqar"
    allowed_domains = ["aqar.fm"]
    start_urls = ["https://aqar.fm"]

    def parse(self, response):
        pass
