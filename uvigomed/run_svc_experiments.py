#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments, shuffled_train_test_split
from classification import run_support_vector_classifier
from loader import load_preprocessed_data

###
### VARIABLES (update as necessary)
###

# Number of times to repeat the experiment for mean and stdev of accuracy
repeats = 1

###
### CODE
###

def support_vector_classifier(train_x, train_y, test_x):
    predict_y = run_support_vector_classifier(train_x, train_y, test_x, C=0.01)
    return predict_y


print('Running Support Vector Classifier experiments')

# To ensure each experiment uses the same train/test split at each repeat
np.random.seed(42)
seeds = np.random.randint(0, np.iinfo(np.int32).max, size=repeats)

for i in range(repeats):
    
    # Ensure each experiment uses the same train/test split at each repeat
    np.random.seed(seeds[i])
    
    # Load the already lowercased, lemmatised data
    train_x, train_y = load_preprocessed_data('data/uvigomed_train.csv')
    test_x, test_y = load_preprocessed_data('data/uvigomed_test.csv')
    
    # Join the data back together and obtain a train/test split
    x = train_x + test_x
    y = train_y + test_y
    train_x, train_y, test_x, test_y = shuffled_train_test_split(x, y)

    # Run the experiments
    run_experiments(support_vector_classifier, train_x, train_y, test_x, test_y, 'svc_proportional')