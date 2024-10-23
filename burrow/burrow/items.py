# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BurrowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    catagery_name=scrapy.Field()
    subcatagery_name=scrapy.Field()
    subcatagery_link=scrapy.Field()

class BurrowItem1(scrapy.Item):
    catagery_name = scrapy.Field()
    subcatagery_name = scrapy.Field()
    subcatagery_link = scrapy.Field()
    subcatofcat_name=scrapy.Field()
    subcatofcat_link = scrapy.Field()

class BurrowItem2(scrapy.Item):
    catagery_name=scrapy.Field()
    subcatagery_name=scrapy.Field()
    subcatagery_link=scrapy.Field()
    subcatofcat_name=scrapy.Field()
    product_url=scrapy.Field()
    product_title=scrapy.Field()
    original_price=scrapy.Field()
    price=scrapy.Field()
    shiping=scrapy.Field()
    abs_result=scrapy.Field()
    details_tag=scrapy.Field()
    text=scrapy.Field()
    features=scrapy.Field()
    approach=scrapy.Field()
    Reviews=scrapy.Field()
    score=scrapy.Field()





