# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    reviewers = scrapy.Field()
    rank = scrapy.Field()


class HomeItem(scrapy.Item):
    
    campus = scrapy.Field()
    structure = scrapy.Field()
    area = scrapy.Field()
    direction = scrapy.Field()
    floor = scrapy.Field()
    build_year = scrapy.Field()
    position = scrapy.Field()
    elevator = scrapy.Field()
    kind = scrapy.Field()