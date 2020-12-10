from scrapy.spiders import SitemapSpider
from datetime import datetime as dt
import re

from crscproject.items import Category 

class NextCategorySpider(SitemapSpider):
    name ='nextcategory'
    allowed_domains = ['www.security-next.com']
    sitemap_urls = ['https://www.security-next.com/robots.txt']

    sitemap_follow = [
        r'/sitemap-tax-category.xml',
    ]
    sitemap_rules = [
        (r'/category/(cat\d+/)*', 'parse'),
    ]

    def parse(self, response):
        item = Category()
        category = response.css('title').xpath('string()').get()
        category = re.sub(r'関連記事.*', '', category)
        item['name'] = category
        yield item
