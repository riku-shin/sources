from scrapy.exceptions import DropItem
import MySQLdb
import sys

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

def get_tags():
    #cursor.execute('SELECT * FROM `Tags` LIMIT 10000')
    cursor.execute('SELECT * FROM `Tags`')
    for row in cursor:
        yield row

def get_cnts(text):
    tags = get_tags()
    for tag in tags:
        name = tag['name']
        cnt = text.count(name)
        if cnt:
            yield {'id' : tag['id'], 'name' : name, 'count' : cnt}

def countTags(text):
    cnts = get_cnts(text)
    for cnt in cnts:
        yield cnt

if __name__=='__main__':
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    countTags(text)
