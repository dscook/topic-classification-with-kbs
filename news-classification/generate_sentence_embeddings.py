#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from collections import defaultdict
import numpy as np

from loader import load_preprocessed_data
from classifier import Classifier
from kb_common import wiki_topics_to_actual_topics

###
### LOAD THE DATA
###

x, y = load_preprocessed_data('data/rcv1_no_stopwords_eos_reduced_1.csv')

###
### GENERATE THE SENTENCE EMBEDDINGS
###

schema = avro.schema.Parse(open('embeddings/sentence.avsc', 'r').read())
embeddings_writer = DataFileWriter(open('embeddings/sentences.avro', 'wb'), DatumWriter(), schema)

classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=5)

# Maintain dictionary of document IDs to topic probabilities for each sentence in the document
doc_id_to_topic_probs = defaultdict(list)
doc_id_to_label = {}

# Maintain topic name to index dictionary for word embedding array
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
    for sentence in document.split('<EOS>'):
        if sentence != '':
            topic_to_prob_dict = classifier.identify_topic_probabilities(sentence)
            
            if topic_to_prob_dict:
                topic_to_prob_dict = classifier.get_topic_probabilities(1)
                
                doc_id_to_topic_probs[i].append(topic_to_prob_dict)
            
                # Add any new topic names 
                for topic_name in topic_to_prob_dict.keys():
                    if topic_name not in topic_name_to_index:
                        topic_name_to_index[topic_name] = current_index
                        current_index += 1
    
    # Store the document label
    doc_id_to_label[i] = y[i]


# Convert document sentence probabilities to embeddings
embedding_length = current_index
print('Length of each sentence embedding is {}'.format(embedding_length))
    
for doc_id, sentence_probs in doc_id_to_topic_probs.items():
    
    embeddings = []
    for sentence_prob in sentence_probs:
        embedding = np.zeros(shape=embedding_length)
        
        for topic, probability in sentence_prob.items():
            embedding[topic_name_to_index[topic]] = probability
        
        embeddings.append(embedding.tolist())
    
    embeddings_writer.append({ 'doc_id': doc_id, 'label': doc_id_to_label[doc_id], 'embeddings': embeddings })


# Close the avro file
embeddings_writer.close()