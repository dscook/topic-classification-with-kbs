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
from classifier import Classifier
from kb_common import wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init

###
### LOAD THE DATA
###

train_x, train_y = load_preprocessed_data('data/ohsumed_eos_train.csv')
test_x, test_y = load_preprocessed_data('data/ohsumed_eos_test.csv')

x = train_x + test_x
y = train_y + test_y

###
### GENERATE THE SENTENCE EMBEDDINGS
###

schema = avro.schema.Parse(open('embeddings/sentence.avsc', 'r').read())
embeddings_writer = DataFileWriter(open('embeddings/sentences.avro', 'wb'), DatumWriter(), schema)

classifier = Classifier(dao=dao_init(),
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=topic_depth,
                        phrase_cache=lookup_cache_init())

# Maintain topic name to index dictionary for word embeddings
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
    
    # To store sentence embeddings
    embeddings = []
    
    for sentence in document.split('<eos>'):
        if sentence != '':
            topic_to_prob_dict = classifier.identify_topic_probabilities(sentence)
            
            if topic_to_prob_dict:
                topic_to_prob_dict = classifier.get_all_topic_probabilities()

                # Add any new topic names 
                for topic_name in topic_to_prob_dict.keys():
                    if topic_name not in topic_name_to_index:
                        topic_name_to_index[topic_name] = current_index
                        current_index += 1
                
                # Add the topic probabilities to the embeddings array
                sentence_embedding = []
                for topic_name, probability in topic_to_prob_dict.items():
                    sentence_embedding.append({'topic_id': topic_name_to_index[topic_name], 'prob': probability})
                embeddings.append(sentence_embedding)
    
    # Write the embeddings  
    if embeddings:
        embeddings_writer.append({ 'doc_id': i, 
                                   'label': y[i], 
                                   'embeddings': embeddings })

# Close the avro file
embeddings_writer.close()

# Output some debug
embedding_length = current_index
print('Length of each sentence embedding is {}'.format(embedding_length))