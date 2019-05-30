#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from sklearn.metrics import classification_report

from classifier import Classifier


def run_unsupervised_classifier(test_x, test_y, topic_labels, wiki_topics_to_actual_topics):
    """
    Runs the unsupervised classifier and returns a classification report that can be printed.
    
    :param test_x: the test data as a list of strings.
    :param test_y: the test labels as ints.
    :param topic_labels: the full topic labels to label the classification report.
    :param wiki_topics_to_actual_topics: a map of Wikipedia topics to the actual topics to classify (their indexes).
                                         Note several Wikipedia topics may map to the same topic to classify, in this
                                         case the probabilities will be added together to determine the document class.
    :returns: a classification report that can be printed.
    """
    classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                            root_topic_names=wiki_topics_to_actual_topics.keys(),
                            max_depth=5)
    
    topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
    
    predict = np.zeros(shape=len(test_y))
    
    for i in range(len(test_x)):
        print(i)
        doc = test_x[i]
        topic_to_prob = classifier.identify_topic_probabilities(doc)
    
        # Convert Wikipedia topic probabilities to actual topic probabilities
        topic_index_to_prob = np.zeros(shape=len(topic_indexes))
        for topic in topic_to_prob.keys():
            topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += topic_to_prob[topic]
            
        # Determine the most prominent topic
        prominent_topic = np.argmax(topic_index_to_prob)
        predict[i] = prominent_topic
    
    return classification_report(test_y,
                                 predict, 
                                 digits=6, 
                                 target_names=topic_labels)