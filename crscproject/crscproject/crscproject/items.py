import scrapy


class Article(scrapy.Item):
    url = scrapy.Field()
    updated = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()


class Tag(scrapy.Item):
    name = scrapy.Field()

    
class Category(scrapy.Item):
    name = scrapy.Field()

class CategoryMap(scrapy.Item):
    article_id = scrapy.Field()
    category_id = scrapy.Field()
