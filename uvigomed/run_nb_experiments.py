#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments, shuffle_data
from classification import run_multinomial_naive_bayes
from loader import load_preprocessed_data

###
### VARIABLES (update as necessary)
###

# Number of times to repeat the experiment for mean and stdev of accuracy
repeats = 1

###
### CODE
###

def multinomial_naive_bayes(train_x, train_y, test_x):
    predict_y = run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors=None)
    return predict_y


print('Running multinomial naive Bayes experiments')
np.random.seed(42)

for i in range(repeats):
    # Load the already lowercased, lemmatised data
    train_x, train_y = load_preprocessed_data('data/uvigomed_train.csv')
    test_x, test_y = load_preprocessed_data('data/uvigomed_test.csv')
    train_x, train_y = shuffle_data(train_x, train_y)
    test_x, test_y = shuffle_data(test_x, test_y)
    
    # Run the experiments
    run_experiments(multinomial_naive_bayes, train_x, train_y, test_x, test_y, 'nb_proportional')