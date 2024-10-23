import scrapy
from scrapy.cmdline import execute

from burrow.items import BurrowItem
class BurrowSpiderSpider(scrapy.Spider):
    name = "burrow_spider"
    allowed_domains = ["burrow.com"]
    start_urls = ["https://burrow.com"]

    def parse(self, response):
        catagery=response.xpath('//div[@class="navigation p3Pz08ieUrv0QY2UMrUrvw=="]/div[contains(@class, "navigation-position hidden-mobile")]')[0:7]
        for name in catagery:
            catagery_name=name.xpath('.//button//span/text()').extract_first()
            subcatagery=name.xpath('.//div[@class="navigation-position-drawer__children navigation-position-drawer__children--column _3dkoWKLeMyR-wiQhDKeZ4Q== q2GCFF38d4xhnVsWPchSQQ=="]')
            for i in subcatagery:
                subcatagery_links=i.xpath('.//a')
                for j in subcatagery_links:
                    subcatagery_link=j.xpath('./@href').extract_first()
                    subcatagery_link=response.urljoin(subcatagery_link)
                    subcatagery_name=j.xpath('./text()').extract_first()

                    item=BurrowItem()
                    item['catagery_name']=catagery_name
                    item['subcatagery_name']=subcatagery_name
                    item['subcatagery_link']=subcatagery_link
                    yield item
                    # print(item)

if __name__=='__main__':
    execute('scrapy crawl burrow_spider -o items.csv'.split())