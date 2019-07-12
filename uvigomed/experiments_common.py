#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import os
import csv
from datetime import datetime
import numpy as np
from sklearn.metrics import classification_report, f1_score

from lookup_tables import topic_to_int


# Directory to store results
today = datetime.today().strftime('%Y-%m-%d')
results_dir = './results/{}/uvigomed/'.format(today)


def create_results_directory():
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)


def write_result(file_prefix, train_size, micro, macro):
    file_path = results_dir + file_prefix + '.csv'
    with open(file_path, 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile)
        result_writer.writerow([train_size, micro, macro])
        
        
def shuffle_data(x, y):
    # Randomly shuffle the dataset
    indices = np.arange(len(y))
    np.random.shuffle(indices)    
    x = x[indices]
    y = y[indices]
    return x, y


def run_experiments(classifier_runner, train_x, train_y, test_x, test_y, name):
    create_results_directory()
    for train_size in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, len(train_x)]:
                
        predict_y = classifier_runner(train_x[:train_size], train_y[:train_size], test_x)
        
        print('--------- TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_to_int.keys()))
        print('')
        
        # Write result into log file.  CSV format with name {name}.csv, entries {train_size},{micro F1},{macro F1}
        micro = f1_score(test_y, predict_y, average='micro')
        macro = f1_score(test_y, predict_y, average='macro')
        write_result(name, train_size, micro, macro)