#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from classification import run_support_vector_classifier

###
### VARIABLES (update as necessary)
###

# Number of times to repeat the experiment for mean and stdev of accuracy
repeats = 100

###
### CODE
###

def support_vector_classifier(train_x, train_y, test_x, class_priors, balanced):
    predict_y = run_support_vector_classifier(train_x, train_y, test_x, C=0.01)
    return predict_y


print('Running Support Vector Classifier experiments')

# To ensure each experiment uses the same train/test split at each repeat
np.random.seed(42)
seeds = np.random.randint(0, np.iinfo(np.int32).max, size=repeats)

for i in range(repeats):
    
    # Ensure each experiment uses the same train/test split at each repeat
    np.random.seed(seeds[i])
    
    (training_data_dict,
     train_x, train_y,
     test_x, test_y,
     topic_code_to_prior_prob) = load_reutuers_data('data/rcv1_baseline.csv')
    
    run_proportional_experiments(support_vector_classifier,
                                 train_x,
                                 train_y,
                                 test_x,
                                 test_y,
                                 topic_code_to_prior_prob,
                                 'svc_proportional')
    run_balanced_experiments(support_vector_classifier,
                             training_data_dict,
                             test_x,
                             test_y,
                             topic_code_to_prior_prob,
                             'svc_balanced')