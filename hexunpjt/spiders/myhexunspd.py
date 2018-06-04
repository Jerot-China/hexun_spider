# -*- coding: utf-8 -*-
import scrapy
import requests
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request
import re


class MyhexunspdSpider(scrapy.Spider):
    name = 'hexunspd'
    allowed_domains = ['hexun.com']
    start_urls = ['http://hexun.com/']
    uid = 'fjrs168'

    # 通过构造start_requests方法只作为第一次的请求
    def start_requests(self):
        global headers
        url = "http://" + str(self.uid) + ".blog.hexun.com/p1/default.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': '*/*',

        }
        # 首次模拟浏览器爬取
        yield Request(url, headers=headers)

    def parse(self, response):
        item = HexunpjtItem()
        item['name'] = response.xpath(".//span[@class='ArticleTitleText']/a/text()").extract()
        item['url'] = response.xpath(".//span[@class='ArticleTitleText']/a/@href").extract()
        # 获取class='ArticleInfo'的所有子节点
        clicks =  response.xpath(".//div[@class='ArticleInfo']")
        # 设置空的点击数和评论数列表
        hit = []
        comment = []
        for click in clicks:
            # 获取文章的点击Id
            click_id = click.xpath("./span/@id").extract()
            # 用replace去掉不需要click字符，直接获取id
            click_id = click_id[0].strip('click')
            hcurl = "http://click.tool.hexun.com/linkclick.aspx?blogid=19020056&articleids=" + click_id
            # print(hcurl)
            r = requests.get(hcurl,headers=headers).text
            # print(r)
            # par2是点击数的正则  par3是评论数的正则
            par2 = r"click\d*?','(\d*?)'"
            par3 = r"comment\d*?','(\d*?)'"
            hit.append(re.compile(par2).findall(str(r)))
            comment.append(re.compile(par3).findall(str(r)))
        item['hit'] = hit
        item['comment'] = comment
        # page为该个人微博的总页数
        page = response.xpath("//div[@class='PageSkip_1']/a[5]/text()").extract()
        for i in range(2,int(page[0])+1):
            next_url = "http://fjrs168.blog.hexun.com/p"+str(i)+"/default.html"
            print(next_url)
            yield Request(next_url, callback=self.parse, headers=headers)
        yield item

