# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from myspiders.items import HomeItem
import json
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from selenium.webdriver.common.by import By
from selenium import webdriver 
import time



class HomeSpider(CrawlSpider):
    
    name = "home"
    
    allowed_domains = ["esf.fang.com"]
    
    start_urls = [
        "http://esf.fang.com/",
    ]

    rules = (
            Rule(LinkExtractor(restrict_xpaths=['//a[@id="PageControl1_hlk_next"]']), callback='parse_items', follow=True),
#             Rule(LinkExtractor(allow=('/house/i32')), callback='parse_items'),
        )

    
    
    def parse_items(self, response):
        print(response.url)
        if 'search.fang.com/captcha-verify' in response.url:
            self.process_captcha(response.url)
        
        selector = Selector(response=response)
        base_url = get_base_url(response)
        
        list = response.xpath('//dl[contains(@id, "list_D03_")]')  
        
        for info in list:
            house = info.xpath('.//dd[@class="info rel floatr"]')
            detail = house.xpath('.//p[@class="title"]/a/@href').extract()[0]
            url = str(urljoin_rfc(base_url, detail), encoding='utf-8')
            yield scrapy.Request(url=url, callback=self.parse_content)
        
    def parse_content(self, response):
        
        if 'search.fang.com/captcha-verify' in response.url:
            self.process_captcha(response.url)
        
        item = HomeItem()
        
        item['campus'] = response.xpath('//div[@class="trl-item2 clearfix"]/div[@class="rcont"]/a/text()').extract_first()
        item['structure'] = response.xpath('//div[@class="tab-cont-right"]/div[2]/div[1]/div[@class="tt"]/text()').extract_first().strip()
        item['area'] = response.xpath('//div[@class="tab-cont-right"]/div[2]/div[2]/div[@class="tt"]/text()').extract_first()
        item['direction'] = response.xpath('//div[@class="tab-cont-right"]/div[3]/div[1]/div[@class="tt"]/text()').extract_first()
        item['floor'] = response.xpath('//div[@class="tab-cont-right"]/div[3]/div[2]/div[@class="tt"]/text()').extract_first()
        item['build_year'] = response.xpath('//div[@class="text-item clearfix"]/span[@class="rcont"]/text()').extract_first()
        item['position'] = response.xpath('//div[@class="tab-cont-right"]/div[4]/div[2]/div[@class="rcont"]/a[1]/text()').extract_first().strip()
        item['elevator'] = response.xpath('//div[@class="content-item fydes-item"]/div[2]/div[2]/span[@class="rcont"]/text()').extract_first()
        item['kind'] = response.xpath('//div[@class="content-item fydes-item"]/div[2]/div[4]/span[@class="rcont"]/text()').extract_first()
        item['price'] = response.xpath('//div[@class="trl-item price_esf  sty1"]/i/text()').extract_first()
        
        yield item
        
    def process_captcha(self, url):
        driver = webdriver.Firefox(executable_path='C:\\scnguh\\spider\\geckodriver-v0.19.1-win64\\geckodriver.exe')
        driver.get(url)
        
        code = input("Please enter any key to continue...")
        
        driver.close()
        
        
        
        
        
        
        