#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np
import csv
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

from loader import load_preprocessed_data
from classifier import Classifier
from kb_common import wiki_topics_to_actual_topics

###
### LOAD THE DATA
###

#x, y = load_preprocessed_data('data/rcv1_no_stopwords_no_noun_grouping.csv')
x, y = load_preprocessed_data('data/rcv1_no_stopwords_reduced.csv')
x = np.array(x)
y = np.array(y)

total_examples = len(y)
split_point = int(total_examples * 0.8)
train_x = x[:split_point]
train_y = y[:split_point]
test_x = x[split_point:]
test_y = y[split_point:]

###
### GENERATE THE WORD EMBEDDINGS
###

schema = avro.schema.Parse(open('embeddings/embeddings.avsc', 'r').read())
embeddings_writer = DataFileWriter(open('embeddings/embeddings-depth-1.avro', 'wb'), DatumWriter(), schema)

classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=5)

# The written embeddings so far, to ensure we don't write them to the file twice
written_embeddings = set()

# Maintain the topic IDs present in the file
topic_ids_present = set()

total_processed = 0
last_percent_complete = 0

# Loop through training set generating word embedding for each phrase
for document in train_x:
    
    # Print current progress
    percent_complete = int(100 * total_processed / len(train_x))
    if percent_complete != last_percent_complete:
        print('Percent complete: {}%'.format(percent_complete))
        last_percent_complete = percent_complete
    total_processed += 1
    
    # This stage ensures the reachable topic hierarchy has been materialised
    classifier.identify_topic_probabilities(document)
    
    # This stage returns all phrases from the text that are in the knowledge base
    phrase_to_topic_matches, _ = classifier.identify_leaf_topics(document)
        
    # For each phrase if we haven't already generated the word embedding then generate it
    for phrase in phrase_to_topic_matches.keys():
        if phrase not in written_embeddings:
            
            # Classifiy a document containing only the phrase to work out its probability distribution
            classifier.identify_topic_probabilities(phrase)
            
            # Get the probabilities from depth 1 of the tree, should correspond to approximately a dimension of 300
            probabilities = classifier.get_topic_probabilities(1)

            # Create topic id, probability pairs
            topic_id_prob_pairs = []
            for topic_name, probability in probabilities.items():
                if topic_name.startswith('Phrase:'):
                    # This is a workaround at the moment as phrases are not stored in the topic_name_to_id
                    # dictionary.  We will be losing some information, print out the phrases that were dropped
                    # from the embedding (they could have formed a dimension of the embedding)
                    print(topic_name)
                else:     
                    topic_id_prob_pairs.append({'topic_id': classifier.topic_name_to_id[topic_name], 'prob': probability})
                    topic_ids_present.add(classifier.topic_name_to_id[topic_name])
            
            embeddings_writer.append({ 'phrase': phrase, 'topic_probs': topic_id_prob_pairs })
            
            # Ensure we do not process this phrase again
            written_embeddings.add(phrase)
    
embeddings_writer.close()

# Write out word to ID mapping
with open('embeddings/word-id-mapping-depth-1.csv', 'w', newline='') as csv_mapping_file:
    mappings_writer = csv.writer(csv_mapping_file)
    for topic_name, identifier in classifier.topic_name_to_id.items():
        in_use = '0'
        if identifier in topic_ids_present:
            in_use = '1'
        mappings_writer.writerow([topic_name, identifier, in_use])
        