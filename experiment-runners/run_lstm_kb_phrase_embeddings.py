#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import numpy as np

from loader import load_preprocessed_data
from word_embeddings import DocToIntSequenceConverter
from lstm_common import split_data, calculate_max_word_length
from lstm_word import LstmPredictor
from embeddings import EmbeddingModel
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

###
### VARIABLES (update as necessary)
###
classification_problem_path = '../uvigomed/'
train_data_path = '../uvigomed/data/uvigomed_train.csv'
test_data_path = '../uvigomed/data/uvigomed_test.csv'
phrase_embedding_path = '../uvigomed/embeddings/phrase_embeddings.avro'
phrase_topic_id_mapping_path = '../uvigomed/embeddings/phrase_topic_id_mapping.csv'

# Set below to True to remove phrase embedding features that occur in less than 0.1% of the phrases.
reduce_phrase_embedding_dimensions = True


###
### CLASSIFICATION PROBLEM SPECIFIC IMPORTS
###
sys.path.append(classification_problem_path)

if classification_problem_path == '../rcv1/':
    from lookup_tables import int_to_topic_code
    int_to_topic = int_to_topic_code
else:
    from lookup_tables import int_to_topic


###
### GET THE CUSTOM KNOWLEDGE BASE WORD EMBEDDINGS
###
embedding_model = EmbeddingModel(phrase_embedding_path,
                                 phrase_topic_id_mapping_path,
                                 underscored_phrase=True,
                                 filter_low_occur_features=reduce_phrase_embedding_dimensions)
word_embedding_dim = embedding_model.get_embedding_dim()
print('Word embedding dimension is {}'.format(word_embedding_dim))


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


###
### OBTAIN THE PHRASES
###

def convert_to_valid_phrases(x):
    """
    Group separate words into phrases where appropriate by examining the list of valid phrase embeddings.
    
    :param x: list of documents as strings.
    :returns: the list of documents with valid phrases joined by an underscore and non valid phrases removed.
    """
    updated_x = []
    
    for doc in x:
        tokens = doc.split()
        phrase_tokens = []
        
        # Maintain the start of the phrase we are processing
        index = 0
        
        # Initially consider a phrase of word length 3
        phrase_length = 3
        
        while index < len(tokens):
            
            # Check the phrase length doesn't exceed the end of the string
            while index + phrase_length > len(tokens):
                phrase_length -= 1
            
            # Try and find a match for 3 word phrase, then 2 then 1
            while phrase_length > 0:
                # Check to see if we have a valid phrase match
                updated_tokens = []
                for token in tokens[index:index+phrase_length]:
                    updated_tokens.extend(token.split('_'))
                
                phrase = '_'.join(updated_tokens)
                
                try:
                    embedding_model.get_vector(phrase)
                    phrase_tokens.append(phrase)
                    break
                except:
                    phrase_length -= 1
            
            # Cover the case where we couldn't find a valid phrase
            if phrase_length == 0:
                phrase_length = 1
                
            # We have a match, consume the phrase
            index += phrase_length
            
            # Reset phrase length for processing next index
            phrase_length = 3
        
        updated_x.append(' '.join(phrase_tokens))
    
    return updated_x


train_x = convert_to_valid_phrases(train_x)
val_x = convert_to_valid_phrases(val_x)
test_x = convert_to_valid_phrases(test_x)

max_sequence_length = calculate_max_word_length(train_x)

# Convert articles to sequence of integers representing the phrases
article_to_int_seq_converter = DocToIntSequenceConverter(x, max_sequence_length)
train_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(train_x)
val_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(val_x)
test_x_seq = article_to_int_seq_converter.convert_to_integer_sequences(test_x)


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