#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

from loader import load_preprocessed_data
from embedding_algorithm import EmbeddingAlgorithm
from kb_common import wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init

###
### VARIABLES (update as necessary)
###

# Path to the knowledge base preprocessed data (RCV1 or UVigoMED)
data_path = '../uvigomed/data/uvigomed_train.csv'

# Additional data path.  Only required for UVigoMED (point to the test set), set to None for RCV1
additional_data_path = '../uvigomed/data/uvigomed_test.csv'

# Path where the embeddings should be written to
document_embeddings_path = '../uvigomed/embeddings/document_embeddings_depth_all.avro'

# The depth of the topic tree to get probabilities for, set to 'all' to retrieve all topic probabilities
# The topic probabilities form the embedding
topic_depth_to_retrieve = 'all'

###
### LOAD THE DATA
###

train_x, train_y = load_preprocessed_data(data_path)

x = None
y = None

if additional_data_path is not None:
    test_x, test_y = load_preprocessed_data(additional_data_path)
    x = train_x + test_x
    y = train_y + test_y
else:
    x = train_x
    y = train_y

###
### GENERATE THE SENTENCE EMBEDDINGS
###

schema = avro.schema.Parse(open('document_embedding.avsc', 'r').read())
embeddings_writer = DataFileWriter(open(document_embeddings_path, 'wb'), DatumWriter(), schema)

embedder = EmbeddingAlgorithm(dao=dao_init(),
                              root_topic_names=wiki_topics_to_actual_topics.keys(),
                              max_depth=topic_depth,
                              phrase_cache=lookup_cache_init())

# Maintain topic name to index dictionary for document embeddings
topic_name_to_index = {}
current_index = 0

# For progress indicator
total_processed = 0
last_percent_complete = 0

for i in range(len(x)):
    
    print(total_processed)
        
    # Print current progress
    percent_complete = int(100 * total_processed / len(x))
    if percent_complete != last_percent_complete:
        print('Percent complete: {}%'.format(percent_complete))
        last_percent_complete = percent_complete
    total_processed += 1
    
    # Get the topic probabilities for each sentence of the document
    document = x[i]
    topic_to_prob_dict = embedder.identify_topic_probabilities(document)
    
    if topic_depth_to_retrieve == 'all':
        topic_to_prob_dict = embedder.get_all_topic_probabilities()
    else:
        topic_to_prob_dict = embedder.get_topic_probabilities(topic_depth_to_retrieve)
         
    # Add any new topic names 
    for topic_name in topic_to_prob_dict.keys():
        if topic_name not in topic_name_to_index:
            topic_name_to_index[topic_name] = current_index
            current_index += 1

    # For topic id, probability pairs
    topic_id_prob_pairs = []
        
    # Add to the set of topic id, probability pairs
    for topic_name, probability in topic_to_prob_dict.items():
        topic_id_prob_pairs.append({'topic_id': topic_name_to_index[topic_name], 'prob': probability})
            
    # Write the document embedding 
    embeddings_writer.append({ 'doc_id': i, 
                               'label': y[i], 
                               'topic_probs': topic_id_prob_pairs })

# Close the avro file
embeddings_writer.close()

# Output some debug
embedding_length = current_index
print('Length of each document embedding is {}'.format(embedding_length))