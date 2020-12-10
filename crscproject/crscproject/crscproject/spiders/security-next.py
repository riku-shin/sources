from scrapy.spiders import SitemapSpider
from datetime import datetime as dt
import re

from crscproject.items import Article

class NextSpider(SitemapSpider):
    name ='secnex'
    allowed_domains = ['www.security-next.com']
    sitemap_urls = ['https://www.security-next.com/robots.txt']

    sitemap_follow = [
        r'/sitemap-pt-post-\d+-\d+',
    ]
    sitemap_rules = [
        (r'/\d+', 'parse'),
        (r'/\d+/\d+', 'parse'),
    ]

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
