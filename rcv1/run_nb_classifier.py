#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

from sklearn.metrics import classification_report, confusion_matrix

from loader import load_preprocessed_data
from classification import run_bernoulli_naive_bayes
from lookup_tables import topic_code_to_topic_dict

###
### Load the train and test data.
###

x, y = load_preprocessed_data('data/rcv1_lemmatized.csv')

# Split data into 80% train, 20% test
total_examples = len(y)
split_point = int(total_examples * 0.8)
train_x = x[:split_point]
train_y = y[:split_point]
test_x = x[split_point:]
test_y = y[split_point:]

###
### Assess Bernoulli Naive Bayes baseline classification performance.
###

predict_y = run_bernoulli_naive_bayes(train_x,
                                      train_y,
                                      test_x,
                                      test_y,
                                      ngram_range = (1, 1))

print(classification_report(test_y, predict_y, digits=6, target_names=topic_code_to_topic_dict.values()))
print(confusion_matrix(test_y, predict_y))