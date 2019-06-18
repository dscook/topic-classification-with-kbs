#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np
import csv

from ohsumed_parser import load_data
from sentence_utils import remove_stop_words_and_lemmatize


def shuffle_data(x, y):
    
    indices = np.arange(len(y))
    np.random.shuffle(indices)
    
    x = np.array(x)
    y = np.array(y)
    
    x = x[indices]
    y = y[indices]
    
    return x, y


def write_data(x, y, file_suffix):
    path = 'data/ohsumed_no_stopwords_{}.csv'.format(file_suffix)
    with open(path, 'w', newline='') as csvfile:
        article_writer = csv.writer(csvfile)
        for i in range(len(y)):
            article_writer.writerow([y[i], x[i]])


train_x, train_y, test_x, test_y = load_data('../../../downloads/UVigoMED/single_label/')

# Remove stopwords and lemmatise
train_x = list(map(remove_stop_words_and_lemmatize, train_x))
test_x = list(map(remove_stop_words_and_lemmatize, test_x))

# To ensure the output is always in the same order
np.random.seed(42)

# Shuffle the train and test data
train_x, train_y = shuffle_data(train_x, train_y)
test_x, test_y = shuffle_data(test_x, test_y)

# Write out the data
write_data(train_x, train_y, 'train')
write_data(test_x, test_y, 'test')