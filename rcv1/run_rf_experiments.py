#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from classification import run_random_forest_classifier


def random_forest_classifier(train_x, train_y, test_x, test_y, class_priors, balanced):
    predict_y = run_random_forest_classifier(train_x, train_y, test_x, ngram_range = (1, 1))
    return predict_y


print('Running Random Forest experiments')
np.random.seed(42)

training_data_dict, test_x, test_y, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_lemmatized.csv')
run_proportional_experiments(random_forest_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
#run_balanced_experiments(random_forest_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)