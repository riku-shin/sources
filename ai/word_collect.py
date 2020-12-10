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
array = []
checks = [0] * 70

def get_corpus():
    corpus = []
    categorymap_query = "SELECT * FROM `CategoryMaps` WHERE `category_id` = '%s' LIMIT 250"
    tagmap_query = "SELECT * FROM `TagMaps` WHERE `article_id` = '%s'"
    tag_query = "SELECT `name` FROM `Tags` WHERE `id` = '%s'"
    for i in range(1, 70 + 1):
        cursor.execute(categorymap_query % i)
        category_maps = cursor.fetchall()
        for category_map in category_maps:
            cursor.execute(tagmap_query % category_map['article_id'])
            tag_maps = cursor.fetchall()
            nouns = []
            for tag_map in tag_maps:
                cursor.execute(tag_query % tag_map['tag_id'])
                name = (cursor.fetchone())['name']
                nouns.append(name)
            array.append(i - 1)
            checks[i - 1] += 1
            yield nouns

    for i, check in enumerate(checks):
        print(i + 1, check)
    print(len(array))
    print('get_corpus END')

def get_word_collect():
    word_collect = []
    corpus = get_corpus()
    
    for nouns in corpus:
        word_collect.append(' '.join(nouns))

    with open('./saved_model/word_collect.txt', mode='w') as f:
        for words in word_collect:
            print(words, file=f)

    print('get_word_collect END')


if __name__=='__main__':
    get_word_collect()
