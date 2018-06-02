import sys
import sqlite3
import csv
import nltk
import gc
import numpy as np
sys.path.append('../lib')
import pandas
import tensorflow as tf

MAX_DOCUMENT_LENGTH = 10
EMBEDDING_SIZE = 220
n_words = 0
MAX_LABEL = 15
WORDS_FEATURE = 'words'


def estimator_spec_for_softmax_classification(
    logits, labels, mode):
  """Returns EstimatorSpec instance for softmax classification."""
  predicted_classes = tf.argmax(logits, 1)
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions={
            'class': predicted_classes,
            'prob': tf.nn.softmax(logits)
        })


def rnn_model(features, labels, mode):
  """RNN model to predict from sequence of words to a class."""
  # Convert indexes of words into embeddings.
  # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
  # maps word indexes of the sequence into [batch_size, sequence_length,
  # EMBEDDING_SIZE].
  word_vectors = tf.contrib.layers.embed_sequence(
      features[WORDS_FEATURE], vocab_size=n_words, embed_dim=EMBEDDING_SIZE)

  # Split into list of embedding per word, while removing doc length dim.
  # word_list results to be a list of tensors [batch_size, EMBEDDING_SIZE].
  word_list = tf.unstack(word_vectors, axis=1)

  # Create a Gated Recurrent Unit cell with hidden size of EMBEDDING_SIZE.
  cell = tf.nn.rnn_cell.GRUCell(EMBEDDING_SIZE)

  # Create an unrolled Recurrent Neural Networks to length of
  # MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit.
  _, encoding = tf.nn.static_rnn(cell, word_list, dtype=tf.float32)

  # Given encoding of RNN, take encoding of last step (e.g hidden size of the
  # neural network of last step) and pass it as features for softmax
  # classification over output classes.
  logits = tf.layers.dense(encoding, MAX_LABEL, activation=None)
  return estimator_spec_for_softmax_classification(
      logits=logits, labels=labels, mode=mode)

test_file = open('forumpedia_csv\\test.csv', 'r',  encoding='utf-8')
train_file = open('forumpedia_csv\\train.csv', 'r',  encoding='utf-8')
test_reader = csv.reader(test_file, delimiter=',', quotechar='|')
train_reader = csv.reader(train_file, delimiter=',', quotechar='|')
x_train = []
x_test = []
y_train = []
y_test = []
for idx, row in enumerate(test_reader):
    y_train.append(row[0])
    x_train_row = list(map(int, row[1].split(" ")))
    for x in range(0, 220-len(x_train_row)):
        x_train_row.append(0)
    x_train.append(np.array(x_train_row))
for idx, row in enumerate(train_reader):
    y_test.append(row[0])
    x_test_row = list(map(int, row[1].split(" ")))
    for x in range(0, 220-len(x_test_row)):
        x_test_row.append(0)
    x_test.append(np.array(x_test_row))

y_train = pandas.Series(y_train)
y_test = pandas.Series(y_test)
x_train = np.array(x_train)
x_test = np.array(x_test)

model_fn = rnn_model
classifier = tf.estimator.Estimator(model_fn=model_fn)
# Train.
train_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={WORDS_FEATURE: x_train},
    y=y_train,
    batch_size=len(x_train),
    num_epochs=None,
    shuffle=True)
#classifier.train(input_fn=train_input_fn, steps=100)
# Predict.
test_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={WORDS_FEATURE: x_test},
    y=y_test,
    num_epochs=1,
    shuffle=False)
predictions = classifier.predict(input_fn=test_input_fn)
y_predicted = np.array(list(p['class'] for p in predictions))
y_predicted = y_predicted.reshape(np.array(y_test).shape)

# Score with tensorflow.
scores = classifier.evaluate(input_fn=test_input_fn)
print('Accuracy (tensorflow): {0:f}'.format(scores['accuracy']))
