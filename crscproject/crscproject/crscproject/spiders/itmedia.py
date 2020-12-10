from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime as dt
import re

from crscproject.items import Article

class ItmediaSpider(CrawlSpider):
    name ='itmedia'
    allowed_domains = ['itmedia.co.jp']
    start_urls = ['https://itmedia.co.jp/news/subtop/security/']

    rules = (
        Rule(LinkExtractor(allow=r'news/subtop/security/'), callback=None, follow=True),
        Rule(LinkExtractor(allow=r'/news/articles/\d+/\d+/news\d+.html'), callback='parse', follow=True),
    )

    def parse(self, response):
        item = Article()
        item['url'] = response.url
        date = response.css('#update').xpath('string()').get()
        l = re.findall('\d+', date)
        date = '-'.join(l)
        item['updated'] = dt.strptime(date, '%Y-%m-%d-%H-%M')
        item['title'] = response.css('h1').xpath('string()').get().replace('　',' ').strip()
        textlist = response.css('p').xpath('string()').getall()
        del textlist[-3:]
        text = ''.join(textlist)
        text = text.replace('　', ' ').strip()
        item['text'] = text
        yield item
