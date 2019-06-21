#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

import numpy as np
import csv
import uuid
from langdetect import detect

from ohsumed_parser import load_data
from sentence_utils import remove_stop_words_and_lemmatize


# Used for eliminating duplicate articles
namespace = uuid.uuid4()


def shuffle_data(x, y):
    
    indices = np.arange(len(y))
    np.random.shuffle(indices)
    
    x = np.array(x)
    y = np.array(y)
    
    x = x[indices]
    y = y[indices]
    
    return x, y


def remove_non_english_and_empty(x, y):
    
    filtered_x = []
    filtered_y = []
    
    number_non_english_articles = 0
    number_empty = 0
    
    for i in range(len(x)):
        if x[i]:
            lang = detect(x[i])
            if lang != 'en':
                number_non_english_articles += 1
            else:
                filtered_x.append(x[i])
                filtered_y.append(y[i])
        else:
            number_empty += 1
    
    print('{} non English articles removed.'.format(number_non_english_articles))
    print('{} empty articles removed.'.format(number_empty))
    
    return filtered_x, filtered_y


# Intentionally here so duplicates that span the train and test set are removed
seen_so_far = set()

def remove_duplicates(x, y):
    
    number_of_duplicates = 0
    
    filtered_x = []
    filtered_y = []
    
    for i in range(len(x)):
        if x[i]:
            
            article_id = uuid.uuid3(namespace, x[i])
                        
            if article_id not in seen_so_far:
                filtered_x.append(x[i])
                filtered_y.append(y[i])
                seen_so_far.add(article_id)
            else:
                number_of_duplicates += 1
        
    print('{} duplicates removed'.format(number_of_duplicates))
    
    return filtered_x, filtered_y


def write_data(x, y, file_suffix):
    path = 'data/ohsumed_eng_only_{}.csv'.format(file_suffix)
    with open(path, 'w', newline='') as csvfile:
        article_writer = csv.writer(csvfile)
        for i in range(len(y)):
            article_writer.writerow([y[i], x[i]])


train_x, train_y, test_x, test_y = load_data('../../../downloads/UVigoMED/single_label/')

# Remove non english articles
train_x, train_y = remove_non_english_and_empty(train_x, train_y)
test_x, test_y = remove_non_english_and_empty(test_x, test_y)

# Remove stopwords and lemmatise - for non-KB classifiers
train_x = list(map(remove_stop_words_and_lemmatize, train_x))
test_x = list(map(remove_stop_words_and_lemmatize, test_x))

# Remove stopwords for knowledge base classifier
def format_for_kb_classifier(article):
    return remove_stop_words_and_lemmatize(article, lowercase=False, lemmatize=True, keep_nouns_only=True)

#train_x = list(map(format_for_kb_classifier, train_x))
#test_x = list(map(format_for_kb_classifier, test_x))

# Remove any examples that are duplicates
train_x, train_y = remove_duplicates(train_x, train_y)
test_x, test_y = remove_duplicates(test_x, test_y)

# To ensure the output is always in the same order
np.random.seed(42)

# Shuffle the train and test data
train_x, train_y = shuffle_data(train_x, train_y)
test_x, test_y = shuffle_data(test_x, test_y)

# Write out the data
write_data(train_x, train_y, 'train')
write_data(test_x, test_y, 'test')