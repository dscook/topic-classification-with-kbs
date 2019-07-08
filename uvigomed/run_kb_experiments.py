#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common/')
sys.path.append('../embedding-scripts/')

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from experiments_common import run_experiments
from load_embeddings import load_document_embeddings

###
### VARIABLES (update as necessary)
###
document_embeddings_path = 'embeddings/document_embeddings_depth_all.avro'


###
### CODE
###

def run_kb_classifier(train_x, train_y, test_x):
    classifier = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    
    # Obtain non zero dimensions for this training set size, i.e. some topics will not be present
    # given this size of training set.  Remove them so the random subspace method of the Random Forest is
    # operating on dimensions with data
    non_zero_topics = ~np.all(train_x.T == 0.0, axis=1)
    train_x_non_zero = train_x.T[non_zero_topics].T
    test_x_non_zero = test_x.T[non_zero_topics].T
    
    print('Dimensions of training set before zero feature filtering: {}'.format(train_x.shape))
    print('Dimensions of training set after zero feature filtering: {}'.format(train_x_non_zero.shape))
    
    classifier.fit(train_x_non_zero, train_y)
    predict_y = classifier.predict(test_x_non_zero)
    return predict_y


print('Running Knowledge Base experiments')
np.random.seed(42)

# Load the document embeddings, train and test are concatenated so split them back out afterwards
x, y = load_document_embeddings(document_embeddings_path)

# Separate back out into train and test sets
split_point = 43972
train_x = np.array(x[:split_point], dtype=np.float32)
train_y = np.array(y[:split_point])
test_x = np.array(x[split_point:], dtype=np.float32)
test_y = np.array(y[split_point:])

# Run the experiments
run_experiments(run_kb_classifier, train_x, train_y, test_x, test_y)