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
limit = 0

def get_corpus():
    corpus = []
    categorymap_query = "SELECT * FROM `CategoryMaps` WHERE `category_id` = '%s' LIMIT 200"
    tagmap_query = "SELECT * FROM `TagMaps` WHERE `article_id` = '%s'"
    tag_query = "SELECT `name` FROM `Tags` WHERE `id` = '%s'"
    limit_max = 0
    for i in range(1, 70 + 1):
        cursor.execute(categorymap_query % i)
        category_maps = cursor.fetchall()
        get_max = len(category_maps)
        if limit_max < get_max:
            limit_max = get_max
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
    global limit 
    limit = limit_max

    for i, check in enumerate(checks):
        print(i + 1, check)
    print(len(array))
    print('get_corpus END')

def reset_seed(seed=0):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

def weighting():
    word_collect = []
    corpus = get_corpus()
    
    for nouns in corpus:
        word_collect.append(' '.join(nouns))

    print('get_word_collect END')

    n_labels = 70 
    labels = np.eye(n_labels)[array]

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(word_collect)
    x = x.toarray()

    x = x.astype('float32')
    t = np.array(labels)

    x_train, x_test, t_train, t_test = train_test_split(x, t, train_size=0.7, random_state=0)

    _, n_input = x_train.shape
    n_output = len(np.unique(array))
    n_output = 70

    reset_seed(0)

    model = tf.keras.models.Sequential([
        layers.Dense(128, input_shape=(n_input, ), activation='relu'),
        layers.Dense(n_output, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        n_epochs = int(arg)
    else:
        n_epochs = 300

    number = len(labels)

    dirname = 'saved_model/' + str(number) + '-' + str(limit) + '-' + str(n_epochs) + '/'

    checkpoint_path = dirname + 'model/cp-{epoch}.ckpt'
    checkpoint_dir = os.path.dirname(checkpoint_path)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=False,
        verbose=2,
        period=5
    )

    history = model.fit(
        x_train,
        t_train,
        batch_size=2048,
        epochs=n_epochs,
        verbose=1,
        validation_data=(x_test, t_test),
        callbacks=[cp_callback]
    )

    model.evaluate(x_test, t_test, verbose=1)
    modelname = dirname + 'model.h5'
    model.save(modelname)

    textdirname = dirname + 'texts/'
    if not os.path.exists(textdirname):
        os.mkdir(textdirname)
    x_test_path = textdirname + 'x_test.txt'
    t_test_path = textdirname + 't_test.txt'

    np.savetxt(x_test_path, x_test)
    np.savetxt(t_test_path, t_test)

    imgdirname = dirname + 'imgs/'
    pngname = imgdirname + 'model.png'
    if not os.path.exists(imgdirname):
        os.mkdir(imgdirname)
    tf.keras.utils.plot_model(model, to_file=pngname, show_shapes=True)
    results = pd.DataFrame(history.history)
    results[['loss', 'val_loss']].plot(title='loss')
    plt.xlabel('epochs')
    plt.grid()
    lossname = imgdirname + 'loss.png'
    plt.savefig(lossname)
    results[['accuracy', 'val_accuracy']].plot(title='metric')
    plt.xlabel('epochs')
    plt.grid()
    metricname = imgdirname + 'metric.png'
    plt.savefig(metricname)

    with open(textdirname + 'results.txt', mode='w') as f:
        print(results.head(n_epochs), file=f)
    with open(textdirname + 'checks.txt', mode='w') as f:
        for i, check in enumerate(checks, 1):
            print('{:>2}'.format(str(i)) + ' : {:>4}'.format(check), file=f)


weighting()
