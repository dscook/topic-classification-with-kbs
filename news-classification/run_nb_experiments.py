#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from classification import run_multinomial_naive_bayes 


def run_naive_bayes(train_x, train_y, test_x, test_y, class_priors):
    predict_y = run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors, ngram_range = (1, 1))
    return predict_y

print('Running Naive Bayes experiments')
np.random.seed(42)

training_data_dict, test_x, test_y, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_lemmatized.csv')
run_proportional_experiments(run_naive_bayes, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(run_naive_bayes, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
