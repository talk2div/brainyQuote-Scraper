import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from brainyQuote.spiders.bquote import BquoteSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BquoteSpider)
process.start()