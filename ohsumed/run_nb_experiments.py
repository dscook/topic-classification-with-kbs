#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np

from experiments_common import run_experiments
from classification import run_bernoulli_naive_bayes, run_multinomial_naive_bayes, run_multinomial_naive_bayes_tfidf
from loader import load_preprocessed_data


def bernoulli_naive_bayes(train_x, train_y, test_x, test_y):
    predict_y = run_bernoulli_naive_bayes(train_x, train_y, test_x, test_y, ngram_range = (1, 1))
    return predict_y


def multinomial_naive_bayes(train_x, train_y, test_x, test_y):
    predict_y = run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors=None, ngram_range = (1, 1))
    return predict_y


def multinomial_naive_bayes_tfidf(train_x, train_y, test_x, test_y):
    predict_y = run_multinomial_naive_bayes_tfidf(train_x, train_y, test_x, ngram_range = (1, 1))
    return predict_y


print('Running Naive Bayes experiments')
np.random.seed(42)

# Load the already lowercased, lemmatised data
train_x, train_y = load_preprocessed_data('data/ohsumed_no_stopwords_train.csv')
test_x, test_y = load_preprocessed_data('data/ohsumed_no_stopwords_test.csv')

# Run the experiments
print('--------- RUNNING BERNOULLI NAIVE BAYES ---------')
run_experiments(bernoulli_naive_bayes, train_x, train_y, test_x, test_y)
print('--------- RUNNING MULTINOMIAL NAIVE BAYES ---------')
run_experiments(multinomial_naive_bayes, train_x, train_y, test_x, test_y)
print('--------- RUNNING MULTINOMIAL NAIVE BAYES (TFIDF) ---------')
run_experiments(multinomial_naive_bayes_tfidf, train_x, train_y, test_x, test_y)