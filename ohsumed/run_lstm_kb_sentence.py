#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

from fastavro import reader
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report

from lstm_common import split_data
from lstm_sentence import LstmPredictor
from lookup_tables import int_to_topic, topic_to_int

###
### LOAD THE DATA
###

def load_data():

    x = []
    y = []
    
    max_num_sent_in_doc = 0
    sent_embedding_dim = 0
    
    embedding_files = ['sentences-train.avro']
    
    for file in embedding_files:
        with open('embeddings/' + file, 'rb') as avro_file:
            avro_reader = reader(avro_file)
            
            for doc_sent_embedding in avro_reader:
                        
                # Determine the maximum length of a sentence embedding
                sentence_embeddings = doc_sent_embedding['embeddings']
                
                formatted_sentence_embeddings = []
                
                for embedding in sentence_embeddings:
                    
                    max_topic_id_in_embedding = 0
                                        
                    for record in embedding:
                        topic_id = record['topic_id']
                        if topic_id+1 > sent_embedding_dim:
                            sent_embedding_dim = topic_id+1
                        if topic_id+1 > max_topic_id_in_embedding:
                            max_topic_id_in_embedding = topic_id+1
                    
                    formatted_embedding = np.zeros(shape=max_topic_id_in_embedding, dtype=np.float32)
                        
                    for record in embedding:
                        topic_id = record['topic_id']
                        prob = record['prob']
                        formatted_embedding[topic_id] = prob
                    
                    formatted_sentence_embeddings.append(formatted_embedding)
                
                # Determine the maximum number of sentences in a document
                if len(sentence_embeddings) > max_num_sent_in_doc:
                    max_num_sent_in_doc = len(sentence_embeddings)
                    
                x.append(formatted_sentence_embeddings)
                y.append(doc_sent_embedding['label'])
        
    # Print out some useful statistics
    print('Maximum number of sentences in a document: {}'.format(max_num_sent_in_doc))
    print('Sentence embedding dimension: {}'.format(sent_embedding_dim))
    
    # Split data into 60% train, 20% validation, 20% test
    train_x, train_y, val_x, val_y, test_x, test_y = split_data(x, y)
    print('Number of training examples: {}'.format(len(train_x)))
    
    return train_x, train_y, val_x, val_y, test_x, test_y, max_num_sent_in_doc, sent_embedding_dim


train_x, train_y, val_x, val_y, test_x, test_y, max_num_sent_in_doc, sent_embedding_dim = load_data()

###
### TRAIN THE LSTM
###
lstm = LstmPredictor(sent_embedding_dim,
                     max_num_sent_in_doc,
                     len(int_to_topic.values()))


class_weights = compute_class_weight('balanced', np.unique(train_y), train_y)
class_weights_dict = {}
for i in range(len(class_weights)):
    class_weights_dict[i] = class_weights[i]
lstm.train_generator(train_x, train_y, val_x, val_y, class_weights_dict)


###
### MAKE THE PREDICTIONS
###

# Re-initialise the LSTM, will use weights from the previous training run.
lstm = LstmPredictor(sent_embedding_dim,
                     max_num_sent_in_doc,
                     len(int_to_topic.values()),
                     use_saved_weights=True)

test_y_predict = lstm.predict_generator(test_x)
print(classification_report(test_y, test_y_predict, digits=6, target_names=topic_to_int.keys()))