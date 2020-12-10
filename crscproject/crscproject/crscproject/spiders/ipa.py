from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime as dt
from crscproject.items import Article
import re

class IpaSpider(CrawlSpider):
    name = 'ipa'
    allowed_domains = ['ipa.go.jp']
    start_urls = ['https://www.ipa.go.jp/security/announce/announce.html']
    
    rules = (
        Rule(LinkExtractor(allow=r'/security/(\w+/)*\w+\.html'), callback='parse'),
    )

    def parse(self, response):
        item = Article()
        item['url'] = response.url
        date = response.css('.ipar_text_right').xpath('string()').get()
        date = re.findall(r'\d+', date)
        date = '-'.join(date)
        item['updated'] = dt.strptime(date, '%Y-%m-%d')
        item['title'] = response.css('title').xpath('string()').get().replace('　', ' ').strip()
        item['text'] = response.css('body').xpath('string()').get().strip()
        yield item
