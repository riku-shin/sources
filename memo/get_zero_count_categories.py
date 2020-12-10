from scrapy.exceptions import DropItem
import MySQLdb

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

with open('zero_count_categories.txt', mode='w') as f:
    cursor.execute('SELECT * FROM `Categories`')
    categories = cursor.fetchall()
    query = "SELECT COUNT(*) FROM `CategoryMaps` WHERE `category_id` = '%s'"
    for category in categories:
        category_id = category['id']
        cursor.execute(query % category_id)
        item = cursor.fetchone()
        prid = 'id:' + str(category['id'])
        prname = 'name:' + category['name']
        prcnt = 'count:' + str(item['COUNT(*)'])
        if item['COUNT(*)'] == 0:
            print(prid, prname, prcnt)

