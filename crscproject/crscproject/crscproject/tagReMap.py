import MySQLdb
import countTags as ct

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)
cursor.execute('DROP TABLE IF EXISTS `TagMaps`')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `TagMaps`(
        `id` INTEGER NOT NULL AUTO_INCREMENT,
        `article_id` INTEGER NOT NULL,
        `tag_id` INTEGER NOT NULL,
        `in_title` BOOLEAN NOT NULL,
        `count` INTEGER NOT NULL,
        PRIMARY KEY(`id`)
    )
""")
conn.commit()

cursor.execute("SELECT * FROM `Articles`")
items = cursor.fetchall()
for item in items:
    article_id = item['id']
    title = item['title']
    tags = ct.countTags(item['text'])
    for tag in tags:
        tag_id = tag['id']
        name = tag['name']
        cnt = tag['count']
        in_title = name in title
        values = dict([('article_id', article_id), ('tag_id', tag_id), ('in_title', in_title), ('count', cnt)])
        cursor.execute("INSERT INTO `TagMaps` (`article_id`, `tag_id`, `in_title`, `count`) VALUES(%(article_id)s, %(tag_id)s, %(in_title)s, %(count)s)", values)
        conn.commit()
