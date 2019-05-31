#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import requests
from sklearn.metrics import classification_report, confusion_matrix

from kb_common import convert_topic_probs_wikipedia_to_actual


def run_unsupervised_classifier(test_x, test_y, topic_labels):
    """
    Runs the unsupervised classifier and returns a classification report that can be printed.
    
    :param test_x: the test data as a list of strings.
    :param test_y: the test labels as ints.
    :param topic_labels: the full topic labels to label the classification report.
    :returns: tuple of (classification report, confusion matrix) that can be printed.
    """        
    predict = np.zeros(shape=len(test_y))
    
    for i in range(len(test_x)):
        print(i)
        
        # Make a REST request to get Wikipedia topic probabilities from the classifier server
        doc = { 'text': test_x[i] }
        r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
        topic_to_prob = r.json()
            
        # Convert Wikipedia topic probabilities to actual topic probabilities
        topic_index_to_prob = convert_topic_probs_wikipedia_to_actual(topic_to_prob)
            
        # Determine the most prominent topic
        prominent_topic = np.argmax(topic_index_to_prob)
        predict[i] = prominent_topic
    
    clazzification_report = classification_report(test_y, predict, digits=6, target_names=topic_labels)
    confuzion_matrix = confusion_matrix(test_y, predict)
    
    return (clazzification_report, confuzion_matrix)