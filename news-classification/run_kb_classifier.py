#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible and unsupervised classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from loader import load_preprocessed_data
from lookup_tables import topic_code_to_topic_dict, topic_code_to_int
from kb_classifier import KnowledgeBasePredictor

###
### LOAD THE DATA
###

# Get 20% test
x, y = load_preprocessed_data('data/rcv1_no_stopwords.csv')
x = np.array(x)
y = np.array(y)

total_examples = len(y)
split_point = int(total_examples * 0.8)
test_x = x[split_point:]
test_y = y[split_point:]


# Take 20 documents of each type from the training set for classifier tuning
train_x = []
train_y = np.zeros(shape=7200)

counts = np.zeros(shape=len(topic_code_to_int.keys()))
current_index = 0
print(split_point)
for i in range(split_point):
    topic_int = y[i]
    
    if counts[topic_int] < 1200:
        train_x.append(x[i])
        train_y[current_index] = topic_int
        counts[topic_int] += 1
        current_index += 1

print(counts)

###
### TRAIN THE CLASSIFIER
###

np.random.seed(42)
kb_predictor = KnowledgeBasePredictor(topic_code_to_topic_dict.values())
kb_predictor.train(train_x, train_y)

predict_y = kb_predictor.predict(train_x)
classification_report, confusion_matrix = kb_predictor.get_classification_report(train_y, predict_y)

print(classification_report)
print(confusion_matrix)

###
### ASSESS PERFORMANCE
###

print('Making predictions for {} documents'.format(len(test_y)))
predict_y = kb_predictor.predict(test_x)
classification_report, confusion_matrix = kb_predictor.get_classification_report(test_y, predict_y)

print(classification_report)
print(confusion_matrix)
