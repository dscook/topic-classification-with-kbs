#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import os
import csv
import numpy as np
from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix, f1_score

from loader import load_preprocessed_data
from lookup_tables import topic_code_to_topic_dict, topic_code_to_int, int_to_topic_code
from conversion import convert_dictionary_to_array, convert_array_to_dictionary

# Directory to store results
today = datetime.today().strftime('%Y-%m-%d')
results_dir = './results/{}/'.format(today)


def create_results_directory():
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)


def write_result(file_prefix, train_size, micro, macro):
    file_path = results_dir + file_prefix + '.csv'
    with open(file_path, 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile)
        result_writer.writerow([train_size, micro, macro])


def load_reutuers_data(preprocessed_article_path):
    # Load the train and test data
    x, y = load_preprocessed_data(preprocessed_article_path)
    x = np.array(x)
    y = np.array(y)
    
    # Randomly shuffle the dataset
    indices = np.arange(len(y))
    np.random.shuffle(indices)    
    x = x[indices]
    y = y[indices]
    
    # Work out the prior class probabilities
    unique, counts = np.unique(y, return_counts=True)
    topic_index_to_count = dict(zip(unique, counts))
        
    total_number = 0
    topic_code_to_prior_prob = {}
    
    for topic_index, count in topic_index_to_count.items():
        topic_code_to_prior_prob[int_to_topic_code[topic_index]] = count
        total_number += count
    
    for topic_code, number in topic_code_to_prior_prob.items():
        topic_code_to_prior_prob[topic_code] = number / total_number
    
    print('Prior class probabilities are ...')
    for topic_code, probability in topic_code_to_prior_prob.items():
        print('Topic Code: {}, Probability: {}'.format(topic_code, probability))
    print('')
        
    # Get the test set
    total_examples = len(y)
    split_point = int(total_examples * 0.8)
    test_x = x[split_point:]
    test_y = y[split_point:]
    print('Size of test set is {}'.format(len(test_y)))
    print('')
    
    # Get all potential training data
    potential_train_x = x[:split_point]
    potential_train_y = y[:split_point]
    
    # Put training data back into dictionary format
    training_data_dict = convert_array_to_dictionary(potential_train_x, potential_train_y, int_to_topic_code)
    
    return (training_data_dict, potential_train_x, potential_train_y, test_x, test_y, topic_code_to_prior_prob)


def run_proportional_experiments(classifier_runner, train_x, train_y, test_x, test_y, topic_code_to_prior_prob, name):
    create_results_directory()
    for train_size in [12, 60, 120, 600, 1200, 6000, 12000, 60000, len(train_x)]:                
        class_priors = np.zeros(shape=len(topic_code_to_prior_prob.keys()))
        for topic_code, probability in topic_code_to_prior_prob.items():
            class_priors[topic_code_to_int[topic_code]] = probability
                
        predict_y = classifier_runner(train_x[:train_size], train_y[:train_size], test_x, class_priors, balanced=False)
        
        print('--------- PROPORTIONAL TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_code_to_topic_dict.values()))
        print(confusion_matrix(test_y, predict_y))
        print('')
        
        # Write result into log file.  CSV format with name {name}.csv, entries {train_size},{micro F1},{macro F1}
        micro = f1_score(test_y, predict_y, average='micro')
        macro = f1_score(test_y, predict_y, average='macro')
        write_result(name, train_size, micro, macro)
        

def run_balanced_experiments(classifier_runner, training_data_dict, test_x, test_y, topic_code_to_prior_prob, name):
    create_results_directory()
    for train_size in [12, 60, 120, 600, 1200, 6000]:
        
        article_dict = {}
        
        class_priors = np.zeros(shape=len(topic_code_to_prior_prob.keys()))
        for topic_code, probability in topic_code_to_prior_prob.items():
            num_to_take_for_topic = train_size // 6
            article_dict[topic_code] = training_data_dict[topic_code][:num_to_take_for_topic]
            class_priors[topic_code_to_int[topic_code]] = probability
        
        train_x, train_y = convert_dictionary_to_array(article_dict, topic_code_to_int)
        
        predict_y = classifier_runner(train_x, train_y, test_x, class_priors, balanced=True)
        
        print('--------- BALANCED TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_code_to_topic_dict.values()))
        print(confusion_matrix(test_y, predict_y))
        print('')
        
        # Write result into log file.  CSV format with name {name}.csv, entries {train_size},{micro F1},{macro F1}
        micro = f1_score(test_y, predict_y, average='micro')
        macro = f1_score(test_y, predict_y, average='macro')
        write_result(name, train_size, micro, macro)
