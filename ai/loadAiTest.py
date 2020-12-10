import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys

if len(sys.argv) > 1:
    number = sys.argv[1]
else:
    number = '100'

if len(sys.argv) > 2:
    n_epochs = sys.argv[2]
else:
    n_epochs = '300'


dirname = 'saved_model/' + number + '-' + n_epochs + '/'
checkpoint_path = dirname + 'model/cp-{epoch:04d}.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)
path = dirname + 'model.h5'
loadpath = dirname + 'model/cp-' + sys.argv[2] + '.ckpt'

latest = tf.train.latest_checkpoint(checkpoint_dir)

new_model = tf.keras.models.load_model(loadpath)

new_model.summary()

new_model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=0.01),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

testdirname = dirname + 'test/'
x_test_path = testdirname + 'x_test.txt'
t_test_path = testdirname + 't_test.txt'

x_test = np.loadtxt(x_test_path)
t_test = np.loadtxt(t_test_path)

print(x_test.shape)
print(t_test.shape)

loss, acc = new_model.evaluate(x_test, t_test, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))
