#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from loader import load_preprocessed_data
from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from kb_classifier_copy import KnowledgeBasePredictor
from lookup_tables import topic_code_to_topic_dict


def run_kb_classifier(train_x, train_y, test_x, class_priors, balanced):
    kb_predictor = KnowledgeBasePredictor(topic_code_to_topic_dict.values(), topic_depth=3)
    kb_predictor.train(train_x, train_y, balanced_classes=balanced)
    predict_y = kb_predictor.predict(test_x)
    return predict_y

print('Running Knowledge Base experiments')
np.random.seed(42)

x, y = load_preprocessed_data('data/rcv1_no_stopwords_coreference_lemmatized.csv')
kb_predictor = KnowledgeBasePredictor(topic_code_to_topic_dict.values(), topic_depth=3)
total_examples = len(y)
split_point = int(total_examples * 0.95)
kb_predictor.fit_tfidf(x[:split_point])

training_data_dict, test_x, test_y, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_no_stopwords_coreference_lemmatized.csv')
#run_proportional_experiments(run_kb_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(run_kb_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
