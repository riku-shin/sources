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

corpus = []

cursor.execute("SELECT MAX(article_id) FROM `TagMaps`")
maxItem = cursor.fetchone()
number = maxItem['MAX(article_id)']
for i in range(1, 1000):
    query = "SELECT * FROM `TagMaps` WHERE `article_id` = '%s'"
    cursor.execute(query % i)
    tagmaps = cursor.fetchall()
    nouns = []
    for tagmap in tagmaps:
        query2 = "SELECT `name` FROM `Tags` WHERE `id` = '%s'"
        cursor.execute(query2 % tagmap['tag_id'])
        name = (cursor.fetchone())['name']
        nouns.append(name)
    corpus.append(' '.join(nouns))
    print(corpus)

