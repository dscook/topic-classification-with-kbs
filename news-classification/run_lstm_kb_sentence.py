#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

from avro.datafile import DataFileReader
from avro.io import DatumReader
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report

from lstm_common import split_data
from lstm_sentence import LstmPredictor
from lookup_tables import int_to_topic_code, topic_code_to_topic_dict

###
### LOAD THE DATA
###

x = []
y = []

max_num_sent_in_doc = 0
sent_embedding_dim = 0

# Determine sentence embedding length
reader = DataFileReader(open('embeddings/sentences-depth-2.avro', 'rb'), DatumReader())

for doc_sent_embedding in reader:

    # Determine the maximum length of a sentence embedding
    sentence_embeddings = doc_sent_embedding['embeddings']
    for embedding in sentence_embeddings:
        for record in embedding:
            topic_id = record['topic_id']
            if topic_id+1 > sent_embedding_dim:
                sent_embedding_dim = topic_id+1
    
    # Determine the maximum number of sentences in a document
    if len(sentence_embeddings) > max_num_sent_in_doc:
        max_num_sent_in_doc = len(sentence_embeddings)
        
    x.append(sentence_embeddings)
    y.append(doc_sent_embedding['label'])
    

reader.close()

# Print out some useful statistics
print('Maximum number of sentences in a document: {}'.format(max_num_sent_in_doc))
print('Sentence embedding dimension: {}'.format(sent_embedding_dim))

# Split data into 60% train, 20% validation, 20% test
train_x, train_y, val_x, val_y, test_x, test_y = split_data(x, y)
print('Number of training examples: {}'.format(len(train_x)))

# Convert sentence embedding vectors to numpy arrays
def convert_to_np(embedded_docs):
    np_array = np.zeros(shape=(len(embedded_docs), max_num_sent_in_doc, sent_embedding_dim))
    
    for i in range(len(embedded_docs)):
        for j in range(len(embedded_docs[i])):

            embedding = np.zeros(shape=sent_embedding_dim)
            
            for topic_prob_object in embedded_docs[i][j]:
                                
                embedding[topic_prob_object['topic_id']] = topic_prob_object['prob']
            
            sent_index = max_num_sent_in_doc - j - 1
            np_array[i, sent_index] = embedding
    
    return np_array

train_x = convert_to_np(train_x)
val_x = convert_to_np(val_x)
test_x = convert_to_np(test_x)

###
### TRAIN THE LSTM
###
#lstm = LstmPredictor(sent_embedding_dim,
#                     max_num_sent_in_doc,
#                     len(int_to_topic_code.values()))


#class_weights = compute_class_weight('balanced', np.unique(train_y), train_y)
#class_weights_dict = {}
#for i in range(len(class_weights)):
#    class_weights_dict[i] = class_weights[i]
#lstm.train(train_x, train_y, val_x, val_y, class_weights_dict)


###
### MAKE THE PREDICTIONS
###

# Re-initialise the LSTM, will use weights from the previous training run.
lstm = LstmPredictor(sent_embedding_dim,
                     max_num_sent_in_doc,
                     len(int_to_topic_code.values()),
                     use_saved_weights=True)
test_y_predict = lstm.predict(test_x)
print(classification_report(test_y, test_y_predict, digits=6, target_names=topic_code_to_topic_dict.values()))