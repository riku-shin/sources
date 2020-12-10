from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

from crscproject.items import Tag

class TagSpider(CrawlSpider):
    name = 'qiita'
    allowd_domains = ['qiita.com']
    start_urls = ['https://qiita.com/tags']

    rules = (
        Rule(LinkExtractor(allow=r'/tags'), callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/tags?page=\d+'), callback='parse', follow=True),
    )

    def parse(self, response):
        item = Tag()
        names = response.css('.TagList__item').xpath('string()').getall()
        for name in names:
            item['name'] = name
            yield item
