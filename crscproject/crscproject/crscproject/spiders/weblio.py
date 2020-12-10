from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

from crscproject.items import Tag

class TagSpider(CrawlSpider):
    name = 'weblio'
    allowd_domains = ['weblio.jp']
    start_urls = ['https://www.weblio.jp/cat/computer']

    rules = (
        Rule(LinkExtractor(allow=r'/cat/computer/binit')),
        Rule(LinkExtractor(allow=r'/category/computer/binit/.+'), callback='parse_binit', follow=True),
        Rule(LinkExtractor(allow=r'/category/computer/binit/.+/\d+'), callback='parse_binit', follow=True),
        #Rule(LinkExtractor(allow=r'/cat/computer/msdnf')),
        #Rule(LinkExtractor(allow=r'/category/computer/msdnf/.+'), callback='parse_msdnf', follow=True),
        #Rule(LinkExtractor(allow=r'/cat/computer/opsyg')),
        #Rule(LinkExtractor(allow=r'/category/computer/opsyg/.+'), callback='parse_opsyg', follow=True),
        #Rule(LinkExtractor(allow=r'/cat/computer/jhscy')),
        #Rule(LinkExtractor(allow=r'/category/computer/jhscy#AA_OO'), callback='parse_jhscy', follow=True),
        #Rule(LinkExtractor(allow=r'/cat/computer/ntwky')),
        #Rule(LinkExtractor(allow=r'/category/computer/ntwky/.+'), callback='parse_ntwky', follow=True),
    )

    def parse_binit(self, response):
        item = Tag()
        r = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlR > li').xpath('string()').getall()
        l = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlL > li').xpath('string()').getall()
        names = r + l
        for name in names:
            item['name'] = name
            yield item

    def parse_msdnf(self, response):
        item = Tag()
        r = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlR > li').xpath('string()').getall()
        l = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlL > li').xpath('string()').getall()
        names = r + l
        for name in names:
            item['name'] = name
            yield item

    def parse_opsyg(self, response):
        item = Tag()
        r = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlR > li').xpath('string()').getall()
        l = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlL > li').xpath('string()').getall()
        names = r + l
        for name in names:
            item['name'] = name
            yield item

    def parse_jhscy(self, response):
        item = Tag()
        names = response.css('#main > div.mainBoxB > div.CtgryLink > ul > li').xpath('string()').getall()
        for name in names:
            item['name'] = name
            yield item

    def parse_ntwky(self, response):
        item = Tag()
        r = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlR > li').xpath('string()').getall()
        l = response.css('#main > div.mainBoxB > div.CtgryLink > ul.CtgryUlL > li').xpath('string()').getall()
        names = r + l
        for name in names:
            item['name'] = name
            yield item
