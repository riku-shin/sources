import MySQLdb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import models, layers
import os
import random

import MeCab

mecab = MeCab.Tagger('-Ochasen')

params = {
    'host': 'localhost',
    'db': 'csasdb',
    'user': 'csasmaster',
    'passwd': 'password',
    'charset': 'utf8mb4',
}
conn = MySQLdb.connect(**params)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

def get_nouns(text):
    nouns = []
    print(text)
    print(type(text))
    print(mecab.parse(text))
    print(type(mecab.parse(text)))
    #res = mecab.parse(text)
    
    words = mecab.parse(text).split('\n')[:-2]
    for word in words:
        part = word.split('\t')
        if '名詞' in part[3]:
            nouns.append(part[0])
    return nouns

def reset_seed(seed=0):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

def get_articles():
    cursor.execute('SELECT * FROM `Articles` LIMIT 10000')
    for row in cursor:
        yield row

def weighting():
    texts, labels = [], []
    articles = get_articles()
    for (i, article) in enumerate(articles):
        text = article['text']
        texts.append(text)
        labels.append(i)

    word_collect = []
    for text in texts:
        nouns = get_nouns(text)
        word_collect.append(' '.join(nouns))

    print(type(word_collect))
    print(type(word_collect[1]))

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(word_collect)
    x = x.toarray()

    x = x.astype('float32')
    t = np.array(labels, 'int32')

    x_train, x_test, t_train, t_test = train_test_split(x, t, train_size=0.7, random_state=0)

    _, n_input = x_train.shape
    n_output = len(np.unique(t_test))

    reset_seed(0)

    model = models.Sequential([
        layers.Dense(200, input_shape=(n_input, ), activation='relu'),
        layers.Dense(n_output, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.SGD(lr=0.01)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    history = model.fit(x_train, t_train, batch_size=100, epochs=20, verbose=1, validation_data=(x_test, t_test))


weighting()
