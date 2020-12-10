from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime as dt
import re

from crscproject.items import Article

class NextSpider(CrawlSpider):
    name ='crspsecnex'
    allowed_domains = ['www.security-next.com']
    start_urls = ['https://www.security-next.com/monthlyarchive']

    rules = (
        Rule(LinkExtractor(allow=r'/date/\d+/\d+')),
        Rule(LinkExtractor(allow=r'/\d+/\d'), callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/\d+'), callback='parse', follow=True),
    )

    def parse(self, response):
        item = Article()
        item['url'] = response.url
        text_get = response.css('p').xpath('string()').getall()
        date_get = re.findall(r'\d+', text_get[-2])
        date = '-'.join(date_get)
        item['updated'] = dt.strptime(date, '%Y-%m-%d')
        item['title'] = response.css('h1').xpath('string()').get().replace('　',' ').strip()
        del text_get[-2:]
        text = ''.join(text_get)
        text = text.replace('　', ' ').strip()
        item['text'] = text
        yield item
