#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

from reuters_parser import load_data
from lookup_tables import topic_code_to_topic_dict, topic_code_to_int, int_to_topic_code
from conversion import convert_dictionary_to_array, convert_array_to_dictionary


def load_reutuers_data(sanitise_each_topic):
    # Load the train and test data
    year_data = load_data('19960820', '19970819', '../../../downloads/reuters/rcv1/', topic_code_to_topic_dict)
    
    # Work out the prior class probabilities
    total_number = 0
    topic_code_to_prior_prob = {}
    
    for topic_code, articles in year_data.items():
        topic_code_to_prior_prob[topic_code] = len(articles)
        total_number += len(articles)
    
    for topic_code, number in topic_code_to_prior_prob.items():
        topic_code_to_prior_prob[topic_code] = number / total_number
    
    print('Prior class probabilities are ...')
    for topic_code, probability in topic_code_to_prior_prob.items():
        print('Topic Code: {}, Probability: {}'.format(topic_code, probability))
    print('')
    
    # Convert to better format for processing
    x,y = convert_dictionary_to_array(year_data, topic_code_to_int)
    
    # Get the test set
    total_examples = len(y)
    split_point = int(total_examples * 0.8)
    test_x = np.array(list(map(sanitise_each_topic, x[split_point:])))
    test_y = y[split_point:]
    print('Size of test set is {}'.format(len(test_y)))
    print('')
    
    # Get all potential training data
    potential_train_x = np.array(list(map(sanitise_each_topic, x[:split_point])))
    potential_train_y = y[:split_point]
    
    # Put training data back into dictionary format
    training_data_dict = convert_array_to_dictionary(potential_train_x, potential_train_y, int_to_topic_code)
    
    return (training_data_dict, test_x, test_y, topic_code_to_prior_prob)


def run_proportional_experiments(classifier_runner, training_data_dict, test_x, test_y, topic_code_to_prior_prob):
    # Test proportional to prior class probability
    for train_size in [120, 1200, 12000, 72000]:
        
        article_dict = {}
        
        for topic_code, probability in topic_code_to_prior_prob.items():
            num_to_take_for_topic = int(train_size * probability)
            article_dict[topic_code] = training_data_dict[topic_code][:num_to_take_for_topic]
        
        train_x, train_y = convert_dictionary_to_array(article_dict, topic_code_to_int)
        
        predict_y = classifier_runner(train_x, train_y, test_x, test_y)
        
        print('--------- PROPORTIONAL TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_code_to_topic_dict.values()))
        print(confusion_matrix(test_y, predict_y))
        print('')


def run_balanced_experiments(classifier_runner, training_data_dict, test_x, test_y, topic_code_to_prior_prob):
    # Test balanced classes
    for train_size in [12, 120, 1200, 7200]:
        
        article_dict = {}
        
        for topic_code in topic_code_to_prior_prob.keys():
            num_to_take_for_topic = train_size // 6
            article_dict[topic_code] = training_data_dict[topic_code][:num_to_take_for_topic]
        
        train_x, train_y = convert_dictionary_to_array(article_dict, topic_code_to_int)
        
        predict_y = classifier_runner(train_x, train_y, test_x, test_y)
        
        print('--------- BALANCED TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_code_to_topic_dict.values()))
        print(confusion_matrix(test_y, predict_y))
        print('')