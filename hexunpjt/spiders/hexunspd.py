# -*- coding: utf-8 -*-
import scrapy
import requests
from hexunpjt.items import HexunpjtItem


class MyhexunspdSpider(scrapy.Spider):
    name = 'myhexunspd'
    allowed_domains = ['hexun.com']
    start_urls = ['http://hexun.com/']
    uid = 'fjrs168'

    # 通过构造start_requests方法只作为第一次的请求
    def start_requests(self):
        url = "http://" + str(uid) + ".blog.hexun.com/p1/default.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': '*/*',

        }
        # 首次模拟浏览器爬取
        yield Request(url, headers=headers)

    def parse(self, response):
        item = HexunpjtItem()
        articles = response.xpath("/div[@class='Article']")
        for article in articles:
            item['name'] = articles.xpath("./span[@class='ArticleTitleText']/a/text()")
            print(item['name'])
        yield item

