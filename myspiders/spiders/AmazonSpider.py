import scrapy
from scrapy.selector import Selector
from myspiders.items import MyspidersItem
import requests


class AmazonSpider(scrapy.Spider):
    
    name = "amazon"
    
    allowed_domains = ['www.amazon.com']
    
    start_urls = ['https://www.amazon.com/gp/bestsellers/books/283155/ref=s9_acsd_ri_bw_clnk_r?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-8&pf_rd_r=13D14JRYTPP562A3ZTK8&pf_rd_r=13D14JRYTPP562A3ZTK8&pf_rd_t=101&pf_rd_p=b8c0a303-a08e-4b0b-bd49-040811fd7080&pf_rd_p=b8c0a303-a08e-4b0b-bd49-040811fd7080&pf_rd_i=283155']
    
    def parse(self, response):
        se = Selector(response=response)
        books = se.xpath('//div[@class="zg_itemImmersion"]').extract()
        for book in books:
            item = MyspidersItem()
            se2 = Selector(text=book)
            
            author = se2.xpath('//span[contains(@class, "a-size-small a-color-")]/text()').extract()[0]
            rank = se2.xpath('//span[@class="zg_rankNumber"]/text()').extract()[0]
            name = se2.xpath('//img/@alt').extract()[0]
            
            price = se2.xpath('//span[@class="p13n-sc-price"]/text()')
            if len(price) == 0:
                price = se2.xpath('//span[@class="a-size-base a-color-price"]/text()').extract()[0]
            else:
                price = price.extract()[0]
            
            stars = se2.xpath('//div[@class="a-icon-row a-spacing-none"]/a/@title').extract()
            if len(stars) == 0:
                stars = 0
            else:
                stars = stars[0]
                
            reviewers = se2.xpath('//div[@class="a-icon-row a-spacing-none"]/a[@class="a-size-small a-link-normal"]/text()').extract()
            if len(reviewers) == 0:
                reviewers = 0
            else:
                reviewers = reviewers[0]
            
            item['name'] = name
            item['author'] = author
            item['rank'] = rank.strip().replace('.', '')
            item['price'] = price
            item['stars']=  stars
            item['reviewers'] = reviewers
            
            yield item
        
        current_page = se.xpath('//li[@class="zg_page zg_selected"]/following-sibling::*[1]/a/@href').extract()
        if len(current_page) != 0:
            url = current_page[0]
            response = requests.get(url)
            if response.status_code == 404:
                return
              
            yield scrapy.Request(url=url, callback=self.parse)
            
            
            
            
            
            
            
            
        