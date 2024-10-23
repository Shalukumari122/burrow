import pymysql
import scrapy
from scrapy.cmdline import execute

from  burrow.items import BurrowItem1
class BurrowSpider1Spider(scrapy.Spider):
    name = "burrow_spider1"
    allowed_domains = ["burrow.com"]
    # start_urls = ["https://burrow.com"]
    def __init__(self):
        try:
            self.con = pymysql.Connect(
                host='localhost',
                user='root',
                password='actowiz',
                database='burrow_db'
            )
            self.cur = self.con.cursor()

        except Exception as e:
            print(e)
    def start_requests(self):
        try:
            query="select *from burrow_subcat_table"
            self.cur.execute(query)
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)

        for row in rows:
            catagery_name = row[0]
            subcatagery_name = row[1]
            subcatagery_link = row[2]

            yield scrapy.Request(url=subcatagery_link,meta={'catagery_name': catagery_name, 'subcatagery_name': subcatagery_name, 'subcatagery_link': subcatagery_link}, callback=self.parse)

    def parse(self, response):
        subcats=response.xpath('//div/section[contains(@class, "product-component-collection plp ProductCollection")]')
        for i in subcats:
            collection=i.xpath('./div[contains(@class, "collection")]')
            for j in collection:
                subcatofcat_name = j.xpath('.//div/h3/text()').extract_first()
                subcatofcat_links=j.xpath('./div[contains(@class,"collection-grid-wrapper")]/div[contains(@class, "collection-grid-container")]/div[contains(@class,"product-card")]')
                for subcatofcat_link in subcatofcat_links:
                    link=subcatofcat_link.xpath('./div[contains(@class, "product-card__image-wrapper")]/a/@href').extract_first()
                    link=response.urljoin(link)
                    subcatagery_link=response.meta.get('subcatagery_link')
                    catagery_name = response.meta.get('catagery_name')
                    subcatagery_name = response.meta.get('subcatagery_name')

                    item=BurrowItem1()
                    item['catagery_name']=catagery_name
                    item['subcatagery_name']=subcatagery_name
                    item['subcatagery_link']=subcatagery_link
                    item['subcatofcat_name']=subcatofcat_name
                    item['subcatofcat_link']=link
                    yield item
                    # print(item)








if __name__=='__main__':
    execute('scrapy crawl burrow_spider1 -o items1.csv'.split())


