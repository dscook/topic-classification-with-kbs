#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

wiki_topics_to_index = {
    'Crime': 0,
    'Law': 1,
    'Business': 2,
    'Economics': 3,
    'Elections': 4,
    'Politics': 5,
    'Health': 6,
    'Medicine': 7,
    'Religion': 8,
    'Theology': 9,
    'Sports': 10   
}

wiki_topics_to_actual_topics = {
    'Crime': 0,
    'Law': 0,
    'Business': 1,
    'Economics': 1,
    'Elections': 2,
    'Politics': 2,
    'Health': 3,
    'Medicine': 3,
    'Religion': 4,
    'Theology': 4,
    'Sports': 5
}

int_to_topic = {
    0: 'CRIME, LAW ENFORCEMENT',
    1: 'ECONOMIC PERFORMANCE',
    2: 'ELECTIONS',
    3: 'HEALTH',
    4: 'RELIGION',
    5: 'SPORTS'
}


def wikipedia_topic_probs_as_array(topic_to_prob):
    probs = np.zeros(shape=len(wiki_topics_to_index.keys()))
    
    for topic, prob in topic_to_prob.items():
        probs[wiki_topics_to_index[topic]] = prob
    
    return probs
    

def convert_topic_probs_wikipedia_to_actual(topic_to_prob):
    """
    Convert Wikipedia topic probabilities to actual topic probabilities.
    """
        
    topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
    
    topic_index_to_prob = np.zeros(shape=len(topic_indexes))
    for topic in topic_to_prob.keys():
        topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += topic_to_prob[topic]
        
    topic_index_to_prob /= np.array([0.5,2,1.75,1,1,1])
    topic_index_to_prob /= np.sum(topic_index_to_prob)
    
    return topic_index_to_prob


def print_topic_probs(topic_to_prob):
    for i in range(len(topic_to_prob)):
        print('Topic: {} Probability: {}'.format(int_to_topic[i], topic_to_prob[i]))