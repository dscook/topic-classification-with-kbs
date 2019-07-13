#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')
sys.path.append('../embedding-scripts/')

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from lookup_tables import int_to_topic_code
from conversion import convert_array_to_dictionary
from load_embeddings import load_document_embeddings

###
### VARIABLES (update as necessary)
###
embedding_depth = 2
document_embeddings_path = 'embeddings/document_embeddings_depth_{}.avro'.format(embedding_depth)

# Number of times to repeat the experiment for mean and stdev of accuracy
repeats = 100

###
### CODE
###

def run_kb_classifier(train_x, train_y, test_x, class_priors, balanced):
    classifier = RandomForestClassifier(n_estimators=200, class_weight='balanced')
    
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

# To ensure each experiment uses the same train/test split at each repeat
np.random.seed(42)
seeds = np.random.randint(np.iinfo(np.int32).min, np.iinfo(np.int32).max, size=repeats)

# We only require the topic codes but calculate the topic prior probability to keep experiments common simple
_, _, _, _, _, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_kb.csv')

# Load the document embeddings, train and test are concatenated so split them back out afterwards
x, y = load_document_embeddings(document_embeddings_path)
x = np.array(x, dtype=np.float32)
y = np.array(y)

for i in range(repeats):
    
    # Ensure each experiment uses the same train/test split at each repeat
    np.random.seed(seeds[i])
    
    # Randomly shuffle the dataset
    indices = np.arange(len(y))
    np.random.shuffle(indices)    
    shuffled_x = x[indices]
    shuffled_y = y[indices]

    # Separate back out into train and test sets
    total_examples = len(y)
    split_point = int(total_examples * 0.8)
    train_x = shuffled_x[:split_point]
    train_y = shuffled_y[:split_point]
    test_x = shuffled_x[split_point:]
    test_y = shuffled_y[split_point:]
    
    training_data_dict = convert_array_to_dictionary(train_x, train_y, int_to_topic_code)
    
    
    ###
    ### RUN THE EXPERIMENTS
    ###
    
    run_proportional_experiments(run_kb_classifier,
                                 train_x,
                                 train_y,
                                 test_x,
                                 test_y,
                                 topic_code_to_prior_prob,
                                 'kb{}_proportional'.format(embedding_depth))
    run_balanced_experiments(run_kb_classifier,
                             training_data_dict,
                             test_x,
                             test_y,
                             topic_code_to_prior_prob,
                             'kb{}_balanced'.format(embedding_depth))
