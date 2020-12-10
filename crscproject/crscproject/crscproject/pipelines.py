from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from . import countTags as ct
from . import judgeCategories as jd
import MySQLdb
import datetime as tm


class ArticlePipeline:
    """
    ItemをMySQLに保存するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        #self.c.execute('DROP TABLE IF EXISTS `Articles`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `Articles`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `url` VARCHAR(200) NOT NULL,
                `updated` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `text` TEXT NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        #self.c.execute('DROP TABLE IF EXISTS `TagMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `TagMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `tag_id` INTEGER NOT NULL,
                `in_title` BOOLEAN NOT NULL,
                `count` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `Articles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
        self.c.execute('SELECT LAST_INSERT_ID()')
        lastrowid = self.c.fetchone()
        article_id = lastrowid['LAST_INSERT_ID()']
        title = item['title']
        tags = ct.countTags(item['text'])
        for tag in tags:
            tag_id = tag['id']
            name = tag['name']
            cnt = tag['count']
            in_title = name in title
            tag_values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
            self.c.execute("INSERT INTO `TagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", tag_values) 
        category_id = jd.judge(article_id)
        category_values = dict([('article_id', article_id), ('category_id', category_id)])
        self.c.execute("INSERT INTO `CategoryMaps` (`article_id`, `category_id`) VALUES(%(article_id)s, %(category_id)s)", category_values)
        self.conn.commit()
        return item

class DummyArticlePipeline:
    """
    ItemをMySQLに保存するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute('DROP TABLE IF EXISTS `DummyArticles`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyArticles`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `url` VARCHAR(200) NOT NULL,
                `updated` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `text` TEXT NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.c.execute('DROP TABLE IF EXISTS `DummyTagMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyTagMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `tag_id` INTEGER NOT NULL,
                `in_title` BOOLEAN NOT NULL,
                `count` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.c.execute('DROP TABLE IF EXISTS `DummyCategoryMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyCategoryMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `category_id` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `DummyArticles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
        self.c.execute('SELECT LAST_INSERT_ID()')
        lastrowid = self.c.fetchone()
        article_id = lastrowid['LAST_INSERT_ID()']
        title = item['title']
        tags = ct.countTags(item['text'])
        for tag in tags:
            tag_id = tag['id']
            name = tag['name']
            cnt = tag['count']
            in_title = name in title
            values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
            self.c.execute("INSERT INTO `DummyTagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
        category_id = jd.judge(article_id)
        category_values = dict([('article_id', article_id), ('category_id', category_id)])
        self.c.execute("INSERT INTO `DummyCategoryMaps` (`article_id`, `category_id`) VALUES(%(article_id)s, %(category_id)s)", category_values)
        self.conn.commit()
        return item


class SecurityNextPipeline:
    """
    ItemをMySQLに保存するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        #self.c.execute('DROP TABLE IF EXISTS `Articles`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `Articles`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `url` VARCHAR(200) NOT NULL,
                `updated` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `text` TEXT NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        #self.c.execute('DROP TABLE IF EXISTS `TagMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `TagMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `tag_id` INTEGER NOT NULL,
                `in_title` BOOLEAN NOT NULL,
                `count` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        query = "SELECT * FROM `Articles` WHERE `title` = '%s'"
        if self.c.execute(query % item['title']):
            self.c.execute(query % item['title'])
            preItem = self.c.fetchone()
            preArticle_id = preItem['id']
            newText = preItem['text'] + item['text']
            url = preItem['url']
            item['text'] = newText
            item['url'] = url
            self.c.execute("DELETE FROM `Articles` WHERE `id` = '%s'" % preArticle_id)
            self.c.execute("DELETE FROM `TagMaps` WHERE `article_id` = '%s'" % preArticle_id)
            self.c.execute("INSERT INTO `Articles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
            self.c.execute('SELECT LAST_INSERT_ID()')
            lastrowid = self.c.fetchone()
            article_id = lastrowid['LAST_INSERT_ID()']
            title = item['title']
            tags = ct.countTags(item['text'])
            for tag in tags:
                tag_id = tag['id']
                name = tag['name']
                cnt = tag['count']
                in_title = name in title
                values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
                self.c.execute("INSERT INTO `TagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
            self.conn.commit()
            return item

        else:
            self.c.execute("INSERT INTO `Articles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
            self.c.execute('SELECT LAST_INSERT_ID()')
            lastrowid = self.c.fetchone()
            article_id = lastrowid['LAST_INSERT_ID()']
            title = item['title']
            tags = ct.countTags(item['text'])
            for tag in tags:
                tag_id = tag['id']
                name = tag['name']
                cnt = tag['count']
                in_title = name in title
                values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
                self.c.execute("INSERT INTO `TagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
            self.conn.commit()
            return item

class DummySecurityNextPipeline:
    """
    ItemをMySQLに保存するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute('DROP TABLE IF EXISTS `DummyArticles`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyArticles`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `url` VARCHAR(200) NOT NULL,
                `updated` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `text` TEXT NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.c.execute('DROP TABLE IF EXISTS `DummyTagMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyTagMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `tag_id` INTEGER NOT NULL,
                `in_title` BOOLEAN NOT NULL,
                `count` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        query = "SELECT * FROM `DummyArticles` WHERE `title` = '%s'"
        if self.c.execute(query % item['title']):
            self.c.execute(query % item['title'])
            preItem = self.c.fetchone()
            preArticle_id = preItem['id']
            newText = preItem['text'] + item['text']
            url = preItem['url']
            item['text'] = newText
            item['url'] = url
            self.c.execute("DELETE FROM `DummyArticles` WHERE `id` = '%s'" % preArticle_id)
            self.c.execute("DELETE FROM `DummyTagMaps` WHERE `article_id` = '%s'" % preArticle_id)
            self.c.execute("INSERT INTO `DummyArticles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
            self.c.execute('SELECT LAST_INSERT_ID()')
            lastrowid = self.c.fetchone()
            article_id = lastrowid['LAST_INSERT_ID()']
            title = item['title']
            tags = ct.countTags(item['text'])
            for tag in tags:
                tag_id = tag['id']
                name = tag['name']
                cnt = tag['count']
                in_title = name in title
                values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
                self.c.execute("INSERT INTO `DummyTagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
            self.conn.commit()
            return item

        else:
            self.c.execute("INSERT INTO `DummyArticles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
            self.c.execute('SELECT LAST_INSERT_ID()')
            lastrowid = self.c.fetchone()
            article_id = lastrowid['LAST_INSERT_ID()']
            title = item['title']
            tags = ct.countTags(item['text'])
            for tag in tags:
                tag_id = tag['id']
                name = tag['name']
                cnt = tag['count']
                in_title = name in title
                values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
                self.c.execute("INSERT INTO `DummyTagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
            self.conn.commit()
            return item

class TagsPipeline:
    """
    タグ用のテーブルに最初に一定数のタグを入れるためのパイプライン
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        #self.c.execute('DROP TABLE IF EXISTS `Tags`')
        '''
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `Tags`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(200) NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()
        '''

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `Tags` (`name`) VALUES(%(name)s)", dict(item))
        self.conn.commit()
        return item

class CategoriesPipeline:
    """
    カテゴリー用のテーブルに最初に一定数のタグを入れるためのパイプライン
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute('DROP TABLE IF EXISTS `Categories`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `Categories`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(200) NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `Categories` (`name`) VALUES(%(name)s)", dict(item))
        self.conn.commit()
        return item

class CategoryMappingPipeline:
    """
    カテゴリー用のテーブルに最初に一定数のタグを入れるためのパイプライン
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute('DROP TABLE IF EXISTS `CategoryMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `CategoryMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `category_id` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `CategoryMaps` (`article_id`,`category_id`) VALUES(%(article_id)s, %(category_id)s)", dict(item))
        self.conn.commit()
        return item

class DummyCategoryMappingPipeline:
    """
    カテゴリー用のテーブルに最初に一定数のタグを入れるためのパイプライン
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute('DROP TABLE IF EXISTS `DummyCategoryMaps`')
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `DummyCategoryMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `category_id` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `DummyCategoryMaps` (`article_id`,`category_id`) VALUES(%(article_id)s, %(category_id)s)", dict(item))
        self.conn.commit()
        return item


class ItemValidationPipeline:
    """
    Itemを検証するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if not item['url'] or not item['title'] or not item['text']:
            raise DropItem('url or title or text')

        query = "SELECT * FROM `Articles` WHERE `title` = '%s'"
        if self.c.execute(query % item['title']):
            raise DropItem('Duplicate title.')

        return item

class DummyItemValidationPipeline:
    """
    Itemを検証するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if not item['url'] or not item['title'] or not item['text']:
            raise DropItem('url or title or text')

        query = "SELECT * FROM `DummyArticles` WHERE `title` = '%s'"
        if self.c.execute(query % item['title']):
            raise DropItem('Duplicate title.')

        if not item['updated'] == tm.datetime.now().date():
            raise DropItem('Old updated')

        return item


class TagValidationPipeline:
    """
    Tagを検証するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        query = "SELECT * FROM `Tags` WHERE `name` = '%s'"
        if self.c.execute(query % item['name']):
            raise DropItem('Duplicate Name.')

        return item

class CategoryValidationPipeline:
    """
    Categoryを検証するPipeline
    """
    def process_item(self, item, spider):
        if item['name'] == 'TOP記事':
            raise DropItem('Duplicate Name.')

        return item

class EvaluationDataPipeline:
    """
    ItemをMySQLに保存するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `EvaluationArticles`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `url` VARCHAR(200) NOT NULL,
                `updated` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `text` TEXT NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `EvaluationTagMaps`(
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `article_id` INTEGER NOT NULL,
                `tag_id` INTEGER NOT NULL,
                `in_title` BOOLEAN NOT NULL,
                `count` INTEGER NOT NULL,
                PRIMARY KEY(`id`)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute("INSERT INTO `EvaluationArticles` (`url`, `updated`, `title`, `text`) VALUES(%(url)s, %(updated)s, %(title)s, %(text)s)", dict(item))
        self.c.execute('SELECT LAST_INSERT_ID()')
        lastrowid = self.c.fetchone()
        article_id = lastrowid['LAST_INSERT_ID()']
        title = item['title']
        tags = ct.countTags(item['text'])
        for tag in tags:
            tag_id = tag['id']
            name = tag['name']
            cnt = tag['count']
            in_title = name in title
            tag_values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
            self.c.execute("INSERT INTO `EvaluationTagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", tag_values) 
        self.conn.commit()
        return item

class EvaluationItemValidationPipeline:
    """
    Itemを検証するPipeline
    """
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'csasdb'),
            'user': settings.get('MYSQL_USER', 'csasmaster'),
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if not item['url'] or not item['title'] or not item['text']:
            raise DropItem('url or title or text')

        query = "SELECT * FROM `EvaluationArticles` WHERE `title` = '%s'"
        if self.c.execute(query % item['title']):
            raise DropItem('Duplicate title.')

        if not item['updated'] == tm.datetime.now().date():
            raise DropItem('Old updated')

        return item
