#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible and unsupervised classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from reuters_parser import load_data
from lookup_tables import topic_code_to_topic_dict, topic_code_to_int
from sentence_utils import remove_stop_words_and_lemmatize
from conversion import convert_dictionary_to_array
from kb_classifier_copy import KnowledgeBasePredictor


def sanitise_each_topic(text):      
    return remove_stop_words_and_lemmatize(text, lowercase=False, lemmatize=False, keep_nouns_only=True)


###
### LOAD THE DATA
###

year_data = load_data('19960820', '19970819', '../../../downloads/reuters/rcv1/', topic_code_to_topic_dict)
#year_data = load_data('19960820', '19960830', '../../../downloads/reuters/rcv1/', topic_code_to_topic_dict)

# For accurate comparison with the Naive Bayes classifier, keep the last 20% of documents using the same random seed.
# I.e. we are making predictions on the same test set.
np.random.seed(42)

# Get 20% test
x, y = convert_dictionary_to_array(year_data, topic_code_to_int)
total_examples = len(y)
split_point = int(total_examples * 0.8)
test_x = np.array(list(map(sanitise_each_topic, x[split_point:])))
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

train_x = np.array(list(map(sanitise_each_topic, train_x)))
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
