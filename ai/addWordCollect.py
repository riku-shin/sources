import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import MySQLdb
import csv

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

from scrapy.exceptions import DropItem

def get_tags():
    cursor.execute('SELECT * FROM `Tags`')
    for row in cursor:
        yield row

def get_nouns(text):
    tags = get_tags()
    for tag in tags:
        name = tag['name']
        cnt = text.count(name)
        if cnt:
            yield name 

#def evaluation(learn_rate, mini_batch):
learn_rate = '0.004'
mini_batch = '2048'
model_name = '11741-' + learn_rate + '-4000-' + mini_batch + '-128'
path = '/vagrant/ai/saved_model/' + model_name + '/model/cp-4000.ckpt'
model = tf.keras.models.load_model(path)
model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=float(learn_rate)),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

word_collect_org= []
word_collect_path = '/vagrant/ai/saved_model/word_collect.txt'
with open(word_collect_path, mode='r') as f:
    for line in f.readlines():
        word_collect_org.append(line.replace('\n', ''))

labels = []

vectorizer = CountVectorizer()

with open('dteval.txt', mode='r') as f:
    reader = csv.reader(f, delimiter='　')
    word_collect = word_collect_org
    for i, row in enumerate(reader):
        nouns = get_nouns(row[5])
        tags = ' '.join(nouns)
        word_collect.append(tags)
        x = vectorizer.fit_transform(word_collect)
        x = x.toarray()
        x.astype('float32')
        x_expand = x[-1][np.newaxis, ...]
        predictions_single = model.predict(x_expand)
        print(i, row[0], predictions_single[0].argmax())

        #labels.append(row[0])

#vectorizer = CountVectorizer()
#x = vectorizer.fit_transform(word_collect)
#x = x.toarray()
#x = x.astype('float32')

#for i in range(180):
#    print(-180 + i)
#    x_expand = x[-180 + i][np.newaxis, ...]
#    predictions_single = model.predict(x_expand)
#    print(i, labels[i], predictions_single[0].argmax())
#    yield predictions_single[0].argmax()
