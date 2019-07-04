#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments
from classification import run_random_forest_classifier
from loader import load_preprocessed_data


def random_forest_classifier(train_x, train_y, test_x, test_y):
    predict_y = run_random_forest_classifier(train_x, train_y, test_x, ngram_range = (1, 1))
    return predict_y


print('Running Random Forest experiments')
np.random.seed(42)

# Load the already lowercased, lemmatised data
train_x, train_y = load_preprocessed_data('data/ohsumed_no_stopwords_train.csv')
test_x, test_y = load_preprocessed_data('data/ohsumed_no_stopwords_test.csv')

# Run the experiments
print('--------- RUNNING RANDOM FOREST CLASSIFIER ---------')
run_experiments(random_forest_classifier, train_x, train_y, test_x, test_y)