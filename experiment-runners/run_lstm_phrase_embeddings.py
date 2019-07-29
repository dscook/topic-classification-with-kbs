#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

from gensim.models import KeyedVectors
import numpy as np
import gensim.downloader as api
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

from loader import load_preprocessed_data
from word_embeddings import DocToIntSequenceConverter
from lstm_common import split_data, calculate_max_word_length
from lstm_word import LstmPredictor


###
### VARIABLES (update as necessary)
###
classification_problem_path = '../rcv1/'
train_data_path = '../rcv1/data/rcv1_kb.csv'
test_data_path = None

use_word2vec = True    # Set to False to use GloVe embeddings

###
### CLASSIFICATION PROBLEM SPECIFIC IMPORTS
###
sys.path.append(classification_problem_path)

if classification_problem_path == '../rcv1/':
    from lookup_tables import int_to_topic_code
    int_to_topic = int_to_topic_code
else:
    from lookup_tables import int_to_topic
    

###
### GET THE WORD EMBEDDINGS
###
word_embedding_dim = 300
embedding_model = None

if use_word2vec:
    embedding_model = KeyedVectors.load_word2vec_format('embeddings/GoogleNews-vectors-negative300.bin.gz',
                                                        binary=True)
else:
    embedding_model = api.load("glove-wiki-gigaword-300")


###
### LOAD THE DATA
###

train_x, train_y = load_preprocessed_data(train_data_path)

x = None
y = None

if test_data_path:
    test_x, test_y = load_preprocessed_data(test_data_path)
    x = train_x + test_x
    y = train_y + test_y
else:
    x = train_x
    y = train_y

x = np.array(x)
y = np.array(y)

# Randomly shuffle the dataset
np.random.seed(42)
indices = np.arange(len(y))
np.random.shuffle(indices)    
x = x[indices]
y = y[indices]

# Split data into 60% train, 20% validation, 20% test
train_x, train_y, val_x, val_y, test_x, test_y = split_data(x, y)
print('Number of training examples: {}'.format(len(train_x)))


###
### PREPROCESS THE DATA
###

max_sequence_length = calculate_max_word_length(train_x)

# Convert articles to sequence of integers representing the phrases
article_to_int_seq_converter = DocToIntSequenceConverter(x, max_sequence_length)
train_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(train_x)
val_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(val_x)
test_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(test_x)


###
### TRAIN THE LSTM
###
lstm = LstmPredictor(article_to_int_seq_converter.get_word_index(),
                     word_embedding_dim,
                     max_sequence_length,
                     embedding_model,
                     len(int_to_topic.values()),
                     weights_path='models/lstm_kb_embeddings.h5')


class_weights = compute_class_weight('balanced', np.unique(train_y), train_y)
class_weights_dict = {}
for i in range(len(class_weights)):
    class_weights_dict[i] = class_weights[i]
lstm.train(train_x_seq, train_y, val_x_seq, val_y, class_weights_dict)


###
### MAKE THE PREDICTIONS
###

# Re-initialise the LSTM, will use weights from the previous training run.
lstm = LstmPredictor(article_to_int_seq_converter.get_word_index(),
                     word_embedding_dim,
                     max_sequence_length,
                     embedding_model,
                     len(int_to_topic.values()),
                     use_saved_weights=True,
                     weights_path='models/lstm_kb_embeddings.h5')
test_y_predict = lstm.predict(test_x_seq)
print(classification_report(test_y, test_y_predict, digits=6, target_names=int_to_topic.values()))