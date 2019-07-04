#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def convert_dictionary_to_array(dataset, topic_code_to_int):
    """
    Given a dataset dictionary keyed by topic code with items a list of the articles for that topic; 
    returns a tuple (x_data, y_data) where x_data is an array of all articles and y_data is the corresponding
    topic indexes from topic_code_to_int.  The data is also shuffled.
    
    :param dataset: dictionary keyed by topic code with items a list of the articles for that topic.
    :param topic_code_to_int: dictionary of topic codes to their integer indexes.
    :returns: (array of all articles, array of topic indexes)
    """
    x_data = []
    y_data = []
    
    for topic_code, articles in dataset.items():
        x_data.extend(articles)
        y_data.extend([topic_code_to_int[topic_code]] * len(articles))
    
    # Randomly shuffle the dataset
    indices = np.arange(len(y_data))
    np.random.shuffle(indices)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    
    x_data = x_data[indices]
    y_data = y_data[indices]
    
    return (x_data, y_data)


def convert_array_to_dictionary(x, y, int_to_topic_code):
    """
    Convert data in array format to a dictionary keyed by topic code.
    
    :param x: the array of articles.
    :param y: the integer indexes of the topic classes.
    :param int_to_topic_code: dictionary of integer indexes to topic codes.
    :returns: a dictionary keyed by topic code with items a list of the articles for that topic.
    """
    dictionary = {}
    
    for index in int_to_topic_code.keys():
        dictionary[int_to_topic_code[index]] = x[y == index]
    
    return dictionary