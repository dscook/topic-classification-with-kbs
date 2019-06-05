#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from kb_classifier import KnowledgeBasePredictor
from lookup_tables import topic_code_to_topic_dict


def run_kb_classifier(train_x, train_y, test_x, test_y):
    kb_predictor = KnowledgeBasePredictor(topic_code_to_topic_dict.values(), topic_depth=1)
    kb_predictor.train(train_x, train_y)
    predict_y = kb_predictor.predict(test_x)
    return predict_y

print('Running Knowledge Base experiments')
np.random.seed(42)

training_data_dict, test_x, test_y, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_no_stopwords.csv')
run_proportional_experiments(run_kb_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(run_kb_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
