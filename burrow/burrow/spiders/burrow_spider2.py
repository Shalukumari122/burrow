import json

import pymysql
import scrapy
import re
from scrapy.cmdline import execute
from json_repair import repair_json
from burrow.items import BurrowItem2

class BurrowSpider2Spider(scrapy.Spider):
    name = "burrow_spider2"
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
            query="select *from burrow_subcat_product_table_old"
            self.cur.execute(query)
        except Exception as e:
            print(e)
        rows = self.cur.fetchall()
        for row in rows:
            catagery_name = row[0]
            subcatagery_name = row[1]
            subcatagery_link = row[2]
            subcatofcat_name=row[3]
            subcatofcat_link=row[4]

            yield scrapy.Request(url=subcatofcat_link, callback=self.parse,meta={'catagery_name': catagery_name, 'subcatagery_name': subcatagery_name, 'subcatagery_link': subcatagery_link,'subcatofcat_name':subcatofcat_name,'subcatofcat_link':subcatofcat_link})


    def parse(self, response):
        catagery_name=response.meta.get('catagery_name')
        subcatagery_name=response.meta.get('subcatagery_name')
        subcatagery_link=response.meta.get('subcatagery_link')
        subcatofcat_name=response.meta.get('subcatofcat_name')
        product_url=response.meta.get('subcatofcat_link')
        product_title=response.xpath('//div[@class="pdp-details-title"]/h2/text()').extract_first()
        original_price=response.xpath('//section/div/h3/span[@class="strikethrough original-price"]/text()').extract_first()
        price=response.xpath('//section/div/h3/span[@class="price"]/text()').extract_first()
        shiping=response.xpath('//section/div/h3/span[@class="free-shipping-note"]/text()').extract_first()
        imgs=response.xpath('//div[@class="pdp__gallery-thumbs"]//div[@class=" graphcms-image-wrapper"]/img[1]/@src').extract()
        result=[]
        for img in imgs:
            img=img.replace("w:20,h:20","w:1000,h:1000")
            result.append(img)
        result="|".join(result)
        # about product
        deminsion_dict={}
        deminsion={}
        text = response.xpath('//section[@class="pdp-btf-section pdp-dimensions"]/div/h2/text()').extract_first()
        d_mesurment_img = response.xpath('//section[@class="pdp-btf-section pdp-dimensions"]//div[@class=" graphcms-image-wrapper"]/img/@src').extract_first()

        if d_mesurment_img != None:
            abs_d_mesurment_img = d_mesurment_img.replace("w:20,h:20", "w:1000,h:500")
            d_mesurments = response.xpath('//section[@class="pdp-btf-section pdp-dimensions"]//div[@class="pdp-dimensions-measurements"]//p')
            for i in d_mesurments:
                sub_demi={}
                title = i.xpath('./span[contains(@class,"pdp-dimensions-measurements-item-title")]/text()').extract_first()
                copy = i.xpath('./span[contains(@class,"pdp-dimensions-measurements-item-copy")]/text()').extract_first()
                if title:
                    if copy:
                        sub_demi[f'{title}']=copy
                deminsion_dict.update(sub_demi)
            deminsion_dict["dim_img"]=abs_d_mesurment_img
            deminsion[f'{text}']=deminsion_dict

        details_dict = {}
        # about = {}

        details_tag = response.xpath('//section[@class="pdp-btf-section about-this-piece"]/div/h2/text()').extract_first()
        details_data = response.xpath('//section[@class="pdp-btf-section about-this-piece"]/div/h3/text()').extract_first()
        if details_tag:
            if details_data:
                details_dict[f'{details_tag}'] = details_data
        sections=response.xpath('//div[@class="about-this-piece-wrapper-sections"]/div')
        for section in sections:
            section_dict={}
            header =section.xpath('./p[@class="header"]/text()').extract_first()
            description=section.xpath('./p[@class="description"]/text()').extract_first()
            if header:
                if description:
                    section_dict[f'{header}']=description
            details_dict.update(section_dict)
        # about[f'{details_tag}']=details_dict


        features_dict={}
        feature={}
        features=response.xpath('//section[@class="pdp-btf-section key-features"]/div/h2/text()').extract_first()
        item=response.xpath('//section[@class="pdp-btf-section key-features"]//div[@class="key-features-item-wrapper"]/div')
        for i in item:
            item_dict={}
            t=i.xpath('./p[@class="key-features-item-title"]/text()').extract_first()
            c=i.xpath('./p[@class="key-features-item-copy"]/text()').extract_first()
            if t:
                if c:
                 item_dict[f'{t}']=c
            features_dict.update(item_dict)
        feature[f'{features}']=features_dict

        approach_dict = {}
        i=response.xpath('//section[@class="pdp-btf-section our-approach"]')
        for j in i:
            approach=j.xpath('./div[@class="pdp-btf-section-title active"]/h2/text()').extract_first()
            quote=j.xpath('./div[@class="pdp-btf-section-wrapper active"]/h3[@class="our-approach-quote"]/text()').extract_first()
            if approach:
                if quote:
                    approach_dict[f'{approach}']=quote

        review=response.xpath("//script[contains(text(), 'window.__PRELOADED_STATE__ =')]/text()").extract_first()
        if review!=None:
            z=review.split('window.__PRELOADED_STATE__ =')
            Json_string=z[1].strip()
            good_json_string = repair_json(Json_string)


            final=json.loads(good_json_string)
            reviews = final['product']['data']['details']['bottomline']['totalReview']
            average_score = final['product']['data']['details']['bottomline']['averageScore']
            abs_average_score = round(average_score, 2)


            items = BurrowItem2()
            items['catagery_name'] = catagery_name
            items['subcatagery_name'] = subcatagery_name
            items['subcatagery_link'] = subcatagery_link
            items['subcatofcat_name'] = subcatofcat_name
            items['product_url'] = product_url
            items['product_title'] = product_title
            items['original_price'] = original_price
            items['price'] = price
            items['shiping'] = shiping
            items['abs_result'] = result
            items['details_tag'] = json.dumps(details_dict,ensure_ascii=False)
            items['text']=json.dumps(deminsion).replace('\\','')
            items['features']=json.dumps(feature,ensure_ascii=False)
            items['approach']=json.dumps(approach_dict,ensure_ascii=False)
            items['Reviews']=reviews
            items['score']=abs_average_score


            yield items
             # print(items)

if __name__=='__main__':
    execute('scrapy crawl burrow_spider2'.split())
