# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from ..items import ChoutiproItem
class ChoutiDemoSpider(RedisCrawlSpider):
    name = 'chouti_demo'
    # allowed_domains = ['www.1.1']
    # start_urls = ['http://www.1.1/']
    redis_key = 'chouti'

    rules = (
        Rule(LinkExtractor(allow=r'/all/hot/recent/\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        div_list = response.xpath('//div[@id="content-list"]/div')
        for div in div_list:
            item = ChoutiproItem()
            detail_url = div.xpath('./div/div/a/@href')
            title = div.xpath('./div/div/a/text()').extract_first()
            author = div.xpath('.//div[@class="part2"]/a[4]/b/text()').extract_first()
            if detail_url:
                detail_url = detail_url[0].extract()
                item['title'] = title
                item['author'] = author
                yield item
