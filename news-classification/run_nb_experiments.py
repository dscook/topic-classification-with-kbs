#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from sentence_utils import remove_stop_words_and_lemmatize
from classification import run_bernoulli_naive_bayes 


def sanitise_each_topic(text):      
    return remove_stop_words_and_lemmatize(text)

def run_naive_bayes(train_x, train_y, test_x, test_y):
    predict_y = run_bernoulli_naive_bayes(train_x, train_y, test_x, test_y, ngram_range = (1, 1))
    return predict_y

print('Running Naive Bayes experiments')
np.random.seed(42)

training_data_dict, test_x, test_y, topic_code_to_prior_prob = load_reutuers_data(sanitise_each_topic)
run_proportional_experiments(run_naive_bayes, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(run_naive_bayes, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
