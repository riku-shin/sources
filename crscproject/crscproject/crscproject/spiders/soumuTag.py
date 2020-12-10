from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

from crscproject.items import Tag

class TagSpider(CrawlSpider):
    name = 'soumu'
    allowd_domains = ['soumu.go.jp']
    start_urls = ['https://www.soumu.go.jp/main_sosiki/joho_tsusin/security/glossary/01.html']

    rules = (
            Rule(LinkExtractor(allow=r'/main_sosiki/joho_tsusin/security/glossary/\d+.html'), callback='parse', follow=True),
    )

    def parse(self, response):
        item = Tag()
        tags = response.css('dt').xpath('string()').getall()
        for tag in tags:
            name = re.sub(r'（.*）', '', tag)
            item['name'] = name 
            yield item
