# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HexunpjtPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='hexun',charset='utf8')

    def process_item(self, item, spider):
        for j in range(0,len(item["name"])):
            name = item['name'][j]
            url = item['url'][j]
            hits = item['hit'][j]
            comment = item['comment'][j]
            sql = "insert into myhexun(name,url,hits,comment) values('"+str(name)+"','"+str(url)+"','"+hits[0]+"','"+comment[0]+"')"
            self.conn.query(sql)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
