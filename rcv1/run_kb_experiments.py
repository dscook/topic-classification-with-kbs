#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
from sklearn.ensemble import RandomForestClassifier

from experiments_common import load_reutuers_data, run_proportional_experiments, run_balanced_experiments
from lookup_tables import int_to_topic_code
from conversion import convert_array_to_dictionary

###
### VARIABLES (update as necessary)
###
document_embeddings_path = 'embeddings/document_embeddings_depth_2.avro'


###
### CODE
###

def run_kb_classifier(train_x, train_y, test_x, class_priors, balanced):
    classifier = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    classifier.fit(train_x, train_y)
    predict_y = classifier.predict(test_x)
    return predict_y

print('Running Knowledge Base experiments')
np.random.seed(42)

# We only require the topic codes but calculate the topic prior probability to keep experiments common simple
_, _, _, _, _, topic_code_to_prior_prob = load_reutuers_data('data/rcv1_kb.csv')

# Load the document embeddings, train and test are concatenated so split them back out afterwards
embedding_dimension = 0

# First pass to work out maximum topic ID to create numpy embeddings
reader = DataFileReader(open(document_embeddings_path, 'rb'), DatumReader())
for document_embedding in reader:
    topic_probs = document_embedding['topic_probs']
    
    for topic_prob in topic_probs:
        topic_id = topic_prob['topic_id']
        if topic_id + 1 > embedding_dimension:
            embedding_dimension = topic_id + 1

reader.close()

# Second pass to actually store the embeddings
x = []
y = []

reader = DataFileReader(open(document_embeddings_path, 'rb'), DatumReader())
for document_embedding in reader:
    label = document_embedding['label']
    topic_probs = document_embedding['topic_probs']
    
    embedding = np.zeros(shape=embedding_dimension)
    
    for topic_prob in topic_probs:
        topic_id = topic_prob['topic_id']
        prob = topic_prob['prob']
        embedding[topic_id] = prob
    
    x.append(embedding)
    y.append(label)

reader.close()

# Separate back out into train and test sets
total_examples = len(y)
split_point = int(total_examples * 0.8)
train_x = x[:split_point]
train_y = y[:split_point]
test_x = x[split_point:]
test_y = y[split_point:]

training_data_dict = convert_array_to_dictionary(train_x, train_y, int_to_topic_code)


###
### RUN THE EXPERIMENTS
###

run_proportional_experiments(run_kb_classifier, train_x, train_y, test_x, test_y, topic_code_to_prior_prob)
run_balanced_experiments(run_kb_classifier, training_data_dict, test_x, test_y, topic_code_to_prior_prob)
