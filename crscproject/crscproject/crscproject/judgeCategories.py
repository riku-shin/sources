import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
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

def get_nouns(article_id):
    query = "SELECT * FROM `TagMaps` WHERE `article_id` = '%s'"
    cursor.execute(query % article_id)
    tagmaps = cursor.fetchall()
    nouns = []
    for tagmap in tagmaps:
        query2 = "SELECT `name` FROM `Tags` WHERE `id` = '%s'"
        cursor.execute(query2 % tagmap['tag_id'])
        name = (cursor.fetchone())['name']
        nouns.append(name)
    return nouns
    print('get_corpus END')

def judge(article_id):
    #path = '/vagrant/ai/saved_model/10000-500/model/cp-500.ckpt'
    path = '/vagrant/ai/saved_model/11741-0.004-4000-2048-128/model/cp-4000.ckpt'
    model = tf.keras.models.load_model(path)
    model.compile(
        optimizer=tf.keras.optimizers.SGD(lr=0.004),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    word_collect= []
    word_collect_path = '/vagrant/ai/saved_model/word_collect.txt'
    with open(word_collect_path, mode='r') as f:
        for line in f.readlines():
            word_collect.append(line.replace('\n', ''))

    nouns = get_nouns(int(article_id))
    tags = ' '.join(nouns)

    word_collect.append(tags)

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(word_collect)
    x = x.toarray()
    x = x.astype('float32')
    x_expand = x[-1][np.newaxis, ...]

    predictions_single = model.predict(x_expand)
    print('PREDICTION =', predictions_single[0].argmax())
    return predictions_single[0].argmax()
    #if predictions_single[0]:
    #    print('PREDICTION =', predictions_single[0].argmax())
    #    return predictions_single[0].argmax()
    #else:
    #    print('PREDICTION = UNCATEGORYABLE')
    #    return 30


if __name__ == '__main__':
    if len(sys.argv) == 2:  
        judge(sys.argv[1])
    else:
        print('Number of Arguments is 2.')
