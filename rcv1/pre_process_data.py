#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make common scripts visible
import sys
sys.path.append('../common/')

from collections import defaultdict
import uuid
import csv
import numpy as np

from reuters_parser import load_data
from sentence_utils import remove_stop_words_and_lemmatize
from lookup_tables import topic_code_to_topic_dict, topic_code_to_int
from conversion import convert_dictionary_to_array


# Used for eliminating duplicate news articles
namespace = uuid.uuid4()


def print_number_of_articles_per_topic(dataset, dataset_name):
    # Print out the number of documents in each category
    print('')
    print('------------------ {} ------------------'.format(dataset_name))
    print('')
    total_number = 0
    for topic_code, articles in dataset.items():
        print('Number of articles for topic {}: {}'.format(topic_code_to_topic_dict[topic_code], len(articles)))
        total_number += len(articles)
    print('')
    print('Total number of articles: {}'.format(total_number))
    

def sanitise_each_topic(dataset):
    data_sanitised = defaultdict(list)
    
    for topic_code, articles in dataset.items():
        
        seen_so_far = set()
        number_of_duplicates = 0
        
        for article in articles:
            
            article_id = uuid.uuid3(namespace, article)
                        
            if article_id not in seen_so_far:
                #article_sanitised = remove_stop_words_and_lemmatize(article)    # For Naive Bayes
                article_sanitised = remove_stop_words_and_lemmatize(article, 
                                                                    lowercase=False, 
                                                                    lemmatize=True, 
                                                                    keep_nouns_only=True,
                                                                    eos_indicators=True)    # For Knowledge Base Classifier
                seen_so_far.add(article_id)
                data_sanitised[topic_code].append(article_sanitised)
            else:
                number_of_duplicates += 1
        
        print('{} duplicates removed for topic code {}'.format(number_of_duplicates, topic_code))
    
    return data_sanitised


year_data = load_data('19960820', '19970819', '../../../downloads/reuters/rcv1/', topic_code_to_topic_dict)
#year_data = load_data('19960820', '19960830', '../../../downloads/reuters/rcv1/', topic_code_to_topic_dict)

print_number_of_articles_per_topic(year_data, 'Data for a Year August 96 to August 97')

year_data_sanitised = sanitise_each_topic(year_data)

# To ensure the output is always in the same order
np.random.seed(42)

x, y = convert_dictionary_to_array(year_data_sanitised, topic_code_to_int)

#path = 'data/rcv1_lemmatized.csv'    # Naive Bayes
path = 'data/rcv1_no_stopwords_eos.csv'   # Knowledge Base Classifier
with open(path, 'w', newline='') as csvfile:
    article_writer = csv.writer(csvfile)
    for i in range(len(y)):
        article_writer.writerow([y[i], x[i]])

