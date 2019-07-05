#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

from sklearn.metrics import classification_report

from lookup_tables import topic_to_int


def run_experiments(classifier_runner, train_x, train_y, test_x, test_y):
    for train_size in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, len(train_x)]:
                
        predict_y = classifier_runner(train_x[:train_size], train_y[:train_size], test_x)
        
        print('--------- TRAINING SET SIZE {} ---------'.format(train_size))
        print(classification_report(test_y, predict_y, digits=6, target_names=topic_to_int.keys()))
        print('')