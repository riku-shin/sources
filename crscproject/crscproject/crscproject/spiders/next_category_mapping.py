from scrapy.spiders import SitemapSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from crscproject.items import Category
from scrapy.exceptions import DropItem
import MySQLdb

from crscproject.items import CategoryMap

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

class NextCategoryMappingSpider(CrawlSpider):
    name ='catmap'
    allowed_domains = ['www.security-next.com']
    start_urls = [
        'https://www.security-next.com/category/cat2https:/www.security-next.com/category/cat3/cat46/cat80',
        'https://www.security-next.com/category/cat3/iot',
        'https://www.security-next.com/category/cat3/cat38/cat73',
        'https://www.security-next.com/category/cat3/cat38/cat81',
        'https://www.security-next.com/category/cat191/cat170',
        'https://www.security-next.com/category/cat/3/cat38/cat190',
        'https://www.security-next.com/category/cat3/cat42/cat48',
        #'https://www.security-next.com/category/cat192',
        'https://www.security-next.com/category/cat3/cat103/cat51',
        'https://www.security-next.com/category/cat179/cat33',
        'https://www.security-next.com/category/cat191/cat25/cat174',
        'https://www.security-next.com/category/cat3/cat103',
        'https://www.security-next.com/category/cat3/cat103/cat102',
        'https://www.security-next.com/category/cat179/guidelines-docs',
        'https://www.security-next.com/category/cat8',
        'https://www.security-next.com/category/cat3/cat42/cat43',
        'https://www.security-next.com/category/cat3/cat71/cat60',
        'https://www.security-next.com/category/cat3/catsmartphone',
        'https://www.security-next.com/category/cat179/cat34',
        'https://www.security-next.com/category/cat3/cat117',
        'https://www.security-next.com/category/cat3/cat38/cat50',
        'https://www.security-next.com/category/cat3/cat46/cat79',
        'https://www.security-next.com/category/cat3/cat42/cat49',
        'https://www.security-next.com/category/cat3/cat42/cat44',
        'https://www.security-next.com/category/cat191',
        'https://www.security-next.com/category/cat3/cat103/cat56',
        'https://www.security-next.com/category/cat3/cat46/cat53',
        'https://www.security-next.com/category/cat3/cat107',
        'https://www.security-next.com/category/cat3/cat71/cat58',
        'https://www.security-next.com/category/cat191/cat189',
        'https://www.security-next.com/category/cat3/cat71/cat55',
        'https://www.security-next.com/category/cat3/feed_products',
        'https://www.security-next.com/category/cat3/cat38/cat39',
        'https://www.security-next.com/category/mynumber-trend',
        'https://www.security-next.com/category/cat3/cat38/catmynumber-products',
        'https://www.security-next.com/category/cat3/cat38',
        'https://www.security-next.com/category/cat191/cat28',
        'https://www.security-next.com/category/cat3/cat42/cat52',
        'https://www.security-next.com/category/cat3/cat42/cat82',
        'https://www.security-next.com/category/cat3/cat46/cat97',
        'https://www.security-next.com/category/cat191/cat178',
        'https://www.security-next.com/category/cat191/cat27',
        'https://www.security-next.com/category/cat3/cat71',
        'https://www.security-next.com/category/cat179/cat166',
        'https://www.security-next.com/category/cat3/cat38/cat163',
        'https://www.security-next.com/category/cat3/cat103/cat101',
        'https://www.security-next.com/category/cat3/cat42/cat54',
        'https://www.security-next.com/category/cat191/cat25',
        'https://www.security-next.com/category/cat3/cat116',
        'https://www.security-next.com/category/cat191/cat25/cat173',
        'https://www.security-next.com/category/cat3/cat42/cat47',
        'https://www.security-next.com/category/cat3/cat42',
        'https://www.security-next.com/category/cat191/cat25/cat175',
        'https://www.security-next.com/category/cat179',
        'https://www.security-next.com/category/cat179/cat24',
        'https://www.security-next.com/category/cat3/cat38/cat61',
        'https://www.security-next.com/category/cat3/cat38/cat76',
        'https://www.security-next.com/category/%e6%9c%aa%e5%88%86%e9%a1%9e'
        'https://www.security-next.com/category/cat191/cat176',
        'https://www.security-next.com/category/cat3/cat42/cat59',
        'https://www.security-next.com/category/special',
        'https://www.security-next.com/category/cat191/cat25/cat172',
        'https://www.security-next.com/category/cat191/cat25/cat171',
        'https://www.security-next.com/category/cat191/cat177',
        'https://www.security-next.com/category/cat3/cat71/cat77',
        'https://www.security-next.com/category/cat3/cat38/cat57',
        'https://www.security-next.com/category/cat191/cat180',
        'https://www.security-next.com/category/cat3',
        'https://www.security-next.com/category/cat3/cat46/cat95',
        'https://www.security-next.com/category/cat3/cat46',
        'https://www.security-next.com/category/cat3/cat42/cat45',
        'https://www.security-next.com/category/cat3/cat46/cat78',
    ]

    rules = (
            Rule(LinkExtractor(allow=r'/category/(cat\w+/)*page/\d+', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/(cat\w+/)*', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/catsmartphone(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/feed_products(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/mynumber-trend(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/catmynumber-products(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/%e6%9c%aa%e5%88%86%e9%a1%9e(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'/category/special(/page\d+)?', deny='https://www.security-next.com/category/cat192(/page\d+)?'),  callback='parse', follow=True),
    )

    def parse(self, response):
        item = CategoryMap()
        category = response.css('title').xpath('string()').get()
        category = re.sub(r'関連記事.*', '', category)
        query = "SELECT * FROM `Categories` WHERE `name` = '%s'"
        cursor.execute(query % category)
        categoryItem = cursor.fetchone()
        
        titles = response.css('#wrapper > div.main > div.content > dl > dd').xpath('string()').getall()
        for title in titles:
            query2 = "SELECT * FROM `Articles` WHERE `title` = '%s'"
            cursor.execute(query2 % title)
            articleItem = cursor.fetchone()
            item['article_id'] = articleItem['id'] 
            item['category_id'] = categoryItem['id'] 
            yield item


'''
class NextCategoryMappingSpider(SitemapSpider):
    name ='catmap'
    allowed_domains = ['www.security-next.com']
    sitemap_urls = ['https://www.security-next.com/robots.txt']

    sitemap_follow = [
        r'/sitemap-tax-category.xml',
    ]
    sitemap_rules = [
        (r'/category/(cat\w+/)*page/\d+', 'parse'),
        (r'/category/(cat\w+/)*', 'parse'),
    ]

    def parse(self, response):
        item = CategoryMap()
        category = response.css('title').xpath('string()').get()
        category = re.sub(r'関連記事.*', '', category)
        query = "SELECT * FROM `Categories` WHERE `name` = '%s'"
        cursor.execute(query % category)
        categoryItem = cursor.fetchone()
        
        titles = response.css('#wrapper > div.main > div.content > dl > dd').xpath('string()').getall()
        for title in titles:
            query2 = "SELECT * FROM `Articles` WHERE `title` = '%s'"
            cursor.execute(query2 % title)
            articleItem = cursor.fetchone()
            item['article_id'] = articleItem['id'] 
            item['category_id'] = categoryItem['id'] 
            yield item
'''
