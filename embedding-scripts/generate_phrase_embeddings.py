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
from kb_common import wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init

###
### VARIABLES (update as necessary)
###
train_data_path = '../uvigomed/data/uvigomed_lemmatized_train.csv'
test_data_path = '../uvigomed/data/uvigomed_lemmatized_test.csv'
phrase_embeddings_path = '../uvigomed/embeddings/phrase_embeddings.avro'
topic_id_mapping_path = '../uvigomed/embeddings/phrase_topic_id_mapping.csv'


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

train_x = x
train_y = y


###
### GENERATE THE WORD EMBEDDINGS
###

schema = avro.schema.Parse(open('phrase_embedding.avsc', 'r').read())
embeddings_writer = DataFileWriter(open(phrase_embeddings_path, 'wb'), DatumWriter(), schema)

classifier = Classifier(dao=dao_init(),
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=topic_depth,
                        phrase_cache=lookup_cache_init())

# The written embeddings so far, to ensure we don't write them to the file twice
written_embeddings = set()

# Maintain the topic IDs present in the file
topic_ids_present = set()

total_processed = 0
last_percent_complete = 0

# To write out topic to ID mapping
with open(topic_id_mapping_path, 'w', newline='', buffering=1) as csv_mapping_file:
    
    mappings_writer = csv.writer(csv_mapping_file)

    # Loop through training set generating word embedding for each phrase
    for document in train_x:
        
        print(total_processed)
        
        # Print current progress
        percent_complete = int(100 * total_processed / len(train_x))
        if percent_complete != last_percent_complete:
            print('Percent complete: {}%'.format(percent_complete))
            last_percent_complete = percent_complete
        total_processed += 1
                
        # This stage returns all phrases from the text that are in the knowledge base
        phrase_to_node_matches, _ = classifier.identify_leaf_nodes(document)
            
        # For each phrase if we haven't already generated the word embedding then generate it
        for phrase in phrase_to_node_matches.keys():
            if phrase not in written_embeddings:
                
                # Classifiy a document containing only the phrase to work out its probability distribution
                classifier.identify_topic_probabilities(phrase)
                
                # Get the probabilities from a certain depth of the tree
                probabilities = classifier.get_topic_probabilities(0)
                
                # Cover the case where a phrase goes immediately to a root topic
                if len(probabilities.keys()) == 1 and list(probabilities.keys())[0].startswith('Phrase:'):
                    probabilities = classifier.get_topic_probabilities(0)
                            
                # Create topic id, probability pairs
                topic_id_prob_pairs = []
                for topic_name, probability in probabilities.items():
                    topic_id = classifier.topic_name_to_id[topic_name]
                    
                    topic_id_prob_pairs.append({'topic_id': topic_id, 'prob': probability})
                    
                    if topic_id not in topic_ids_present:
                        topic_ids_present.add(topic_id)
                        mappings_writer.writerow([topic_name, topic_id])
                
                embeddings_writer.append({ 'phrase': phrase, 'topic_probs': topic_id_prob_pairs })
                
                # Ensure we do not process this phrase again
                written_embeddings.add(phrase)
    
embeddings_writer.close()