#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from loader import load_preprocessed_data
from word_embeddings import DocToIntSequenceConverter
from lstm_common import split_data, calculate_max_sequence_length
from lstm_word import LstmPredictor
from embeddings import EmbeddingModel
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

###
### VARIABLES (update as necessary)
###
classification_problem_path = '../ohsumed/'
train_data_path = '../ohsumed/data/ohsumed_lemmatized_train.csv'
test_data_path = '../ohsumed/data/ohsumed_lemmatized_test.csv'
phrase_embedding_path = '../ohsumed/embeddings/phrase_embeddings.avro'
phrase_topic_id_mapping_path = '../ohsumed/embeddings/phrase_topic_id_mapping.csv'


###
### CLASSIFICATION PROBLEM SPECIFIC IMPORTS
###
sys.path.append(classification_problem_path)
from lookup_tables import int_to_topic

###
### LOAD THE DATA
###

train_x, train_y = load_preprocessed_data(train_data_path)

x = None
y = None

if test_data_path:
    test_x, test_y = load_preprocessed_data(test_data_path)
    x = train_x + test_x
    y = train_y + test_y
else:
    x = train_x
    y = train_y

x = np.array(x)
y = np.array(y)

# Split data into 60% train, 20% validation, 20% test
train_x, train_y, val_x, val_y, test_x, test_y = split_data(x, y)
print('Number of training examples: {}'.format(len(train_x)))

max_sequence_length = calculate_max_sequence_length(train_x)

# Convert articles to sequence of integers representing the words
article_to_int_seq_converter = DocToIntSequenceConverter(x, max_sequence_length)
train_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(train_x)
val_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(val_x)
test_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(test_x)

###
### GET THE CUSTOM KNOWLEDGE BASE WORD EMBEDDINGS
###
embedding_model = EmbeddingModel(phrase_embedding_path, phrase_topic_id_mapping_path)
word_embedding_dim = embedding_model.get_embedding_dim()
print('Word embedding dimension is {}'.format(word_embedding_dim))


###
### TRAIN THE LSTM
###
lstm = LstmPredictor(article_to_int_seq_converter.get_word_index(),
                     word_embedding_dim,
                     max_sequence_length,
                     embedding_model,
                     len(int_to_topic.values()),
                     weights_path='models/lstm_kb_embeddings.h5')


class_weights = compute_class_weight('balanced', np.unique(train_y), train_y)
class_weights_dict = {}
for i in range(len(class_weights)):
    class_weights_dict[i] = class_weights[i]
lstm.train(train_x_seq, train_y, val_x_seq, val_y, class_weights_dict)


###
### MAKE THE PREDICTIONS
###

# Re-initialise the LSTM, will use weights from the previous training run.
lstm = LstmPredictor(article_to_int_seq_converter.get_word_index(),
                     word_embedding_dim,
                     max_sequence_length,
                     embedding_model,
                     len(int_to_topic.values()),
                     use_saved_weights=True,
                     weights_path='models/lstm_kb_embeddings.h5')
test_y_predict = lstm.predict(test_x_seq)
print(classification_report(test_y, test_y_predict, digits=6, target_names=int_to_topic.values()))