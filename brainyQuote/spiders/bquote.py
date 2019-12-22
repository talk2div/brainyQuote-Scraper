# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
from urllib.parse import urljoin

class BquoteSpider(scrapy.Spider):
    name = 'bquote'
    allowed_domains = ['www.brainyquote.com']
    ua = UserAgent()

    def start_requests(self):
        yield scrapy.Request(url='https://www.brainyquote.com/authors',headers={
            'User-Agent':self.ua.random
        })    

    def parse(self, response):
        author_lnk = response.xpath('//div[@style="padding-top:5px"]/a/@href')
        for row in author_lnk:
            yield scrapy.Request(url=urljoin(response.url,row.get()),callback=self.each_author,headers={
            'User-Agent':self.ua.random
            })
    
    def each_author(self,response):
        alpha_author = response.xpath('//table[@class="table table-hover table-bordered"]/tbody/tr/td[1]/a/@href')
        for row in alpha_author:
            yield scrapy.Request(url=urljoin(response.url,row.get()),callback=self.author_page,headers={
            'User-Agent':self.ua.random
            })
        
        next_page = response.xpath('(//ul[contains(@class,"pagination")])[2]/li[position()=last()]/a/@href').get()
        url_next = urljoin(response.url,next_page)
        if next_page:
            yield scrapy.Request(url=url_next,callback=self.each_author,headers={
            'User-Agent':self.ua.random
            })
    
    # //div[@class="bqLn"]/a[@class="bq_on_link_cl"]/@href
    # (//div[@class="bqLn"]/a[@class="bq_on_link_cl"])[2]/@href
    
    def author_page(self,response):
        row = response.xpath('//div[@class="clearfix"]')
        for each_row in row:
            yield {
                'name':each_row.xpath('.//div/a[@title="view author"]/text()').get(),
                'quote':each_row.xpath('.//a/text()').get(),
                'URL': response.url
            }
        
        next_page = response.xpath('//ul[@class="pagination "]/li[position()=last()]/a/@href').get()
        url_next = urljoin(response.url,next_page)
        if next_page:
            yield scrapy.Request(url=url_next,callback=self.author_page,headers={
            'User-Agent':self.ua.random
            })