#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments
from classification import run_support_vector_classifier
from loader import load_preprocessed_data


def support_vector_classifier(train_x, train_y, test_x):
    predict_y = run_support_vector_classifier(train_x, train_y, test_x, C=0.01)
    return predict_y


print('Running Support Vector Classifier experiments')
np.random.seed(42)

# Load the already lowercased, lemmatised data
train_x, train_y = load_preprocessed_data('data/uvigomed_train.csv')
test_x, test_y = load_preprocessed_data('data/uvigomed_test.csv')

# Run the experiments
run_experiments(support_vector_classifier, train_x, train_y, test_x, test_y)