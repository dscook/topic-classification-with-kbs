#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from loader import load_preprocessed_data
from word_embeddings import DocToIntSequenceConverter
from lstm_common import split_data, calculate_max_word_length
from lstm_word import LstmPredictor
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight


###
### VARIABLES (update as necessary)
###
classification_problem_path = '../uvigomed/'
train_data_path = '../uvigomed/data/uvigomed_train.csv'
test_data_path = '../uvigomed/data/uvigomed_test.csv'


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