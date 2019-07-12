#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments
from classification import run_multinomial_naive_bayes
from loader import load_preprocessed_data


def multinomial_naive_bayes(train_x, train_y, test_x):
    predict_y = run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors=None)
    return predict_y


print('Running multinomial naive Bayes experiments')
np.random.seed(42)

# Load the already lowercased, lemmatised data
train_x, train_y = load_preprocessed_data('data/uvigomed_train.csv')
test_x, test_y = load_preprocessed_data('data/uvigomed_test.csv')

# Run the experiments
run_experiments(multinomial_naive_bayes, train_x, train_y, test_x, test_y, 'nb_proportional')