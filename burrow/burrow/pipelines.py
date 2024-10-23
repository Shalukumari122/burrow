# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from burrow.items import BurrowItem
from burrow.items import BurrowItem1
from burrow.items import BurrowItem2

class BurrowPipeline:

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

    def process_item(self, item, spider):

        if isinstance(item,BurrowItem):
            try:
                query="create table if not exists burrow_subcat_table(catagery_name varchar(255),subcatagery_name varchar(255),subcatagery_link varchar(255) unique)"
                self.cur.execute(query)
            except Exception as e:
                print(e)
            try:
                query1="insert ignore into burrow_subcat_table(catagery_name,subcatagery_name,subcatagery_link) values(%s,%s,%s)"
                values=tuple(item.values())
                self.cur.execute(query1,values)
                self.con.commit()
            except Exception as e1:
                print(e1)

        if isinstance(item,BurrowItem1):
            try:
                query="create table if not exists burrow_subcat_product_table(catagery_name varchar(255),subcatagery_name varchar(255),subcatagery_link varchar(255),subcatofcat_name varchar(255),subcatofcat_link varchar(255) unique)"
                self.cur.execute(query)
            except Exception as e:
                print(e)
            try:
                query1="insert ignore into burrow_subcat_product_table(catagery_name,subcatagery_name,subcatagery_link,subcatofcat_name,subcatofcat_link) values(%s,%s,%s,%s,%s)"
                values=tuple(item.values())
                self.cur.execute(query1,values)
                self.con.commit()
                # self.cur.execute("update burrow_subcat_product_table set status='Done' where subcatagery_link = subcatagery_link ")
                # self.con.commit()
            except Exception as e1:
                print(e1)

        if isinstance(item,BurrowItem2):
            try:
                query="create table if not exists burrow_final_product_table(catagery_name varchar(255),subcatagery_name varchar(255),subcatagery_link varchar(255),subcatofcat_name varchar(255),product_url varchar(255) unique,product_title varchar(255),original_price varchar(255),price varchar(255),shiping varchar(255),abs_result varchar(255),details_tag Longtext,text Longtext,features Longtext,approach Longtext, score varchar(5),Reviews varchar(5))"
                self.cur.execute(query)
            except Exception as e:
                print(e)

            try:
                query1="insert ignore into burrow_final_product_table (catagery_name,subcatagery_name,subcatagery_link,subcatofcat_name,product_url,product_title,original_price,price,shiping,abs_result,details_tag,text,features,approach,score,Reviews) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values=tuple(item.values())
                self.cur.execute(query1,values)
                self.con.commit()
            except Exception as e1:
                print(e1)

        return item
