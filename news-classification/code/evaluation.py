#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def calculate_classification_accuracy(int_to_topic_code, predicted, actual):
    """
    Calculates the classification accuracy on a per class basis.
        
    :param int_to_topic_code: the index to topic lookup.
    :param predicted: the predicted class labels.
    :param actual: the actual class labels.
    :returns: a dictionary of topic code to classification accuracy values.
    """
    per_class_accuracy = {}
    
    for index in int_to_topic_code.keys():
        filtered_predicted = predicted[actual == index]
        filtered_actual = actual[actual == index]
        
        correct = (filtered_predicted == index).sum()
        total = len(filtered_actual)
        
        per_class_accuracy[int_to_topic_code[index]] = correct / total
    
    return per_class_accuracy



#per_class_accuracy = calculate_classification_accuracy({0: 'A', 1: 'B', 2: 'C'}, 
#                                                       np.array([0, 1, 0, 1, 1]), 
#                                                       np.array([0, 0, 0, 1, 2]))
#print(per_class_accuracy)