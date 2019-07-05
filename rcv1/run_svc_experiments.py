#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from classification import run_support_vector_classifier


def support_vector_classifier(train_x, train_y, test_x, class_priors, balanced):
    predict_y = run_support_vector_classifier(train_x, train_y, test_x, C=0.01)
    return predict_y


print('Running Support Vector Classifier experiments')
np.random.seed(42)

(training_data_dict,
 train_x, train_y,
 test_x, test_y,
 topic_code_to_prior_prob) = load_reutuers_data('data/rcv1_baseline.csv')

run_proportional_experiments(support_vector_classifier, train_x, train_y, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(support_vector_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)