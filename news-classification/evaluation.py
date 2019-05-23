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


def macro_f1_score(int_to_topic_code, predicted, actual):
    """
    Calculates the macro F1 score.
        
    :param int_to_topic_code: the index to topic lookup.
    :param predicted: the predicted class labels.
    :param actual: the actual class labels.
    :returns: the macro F1 score.
    """
    sum_f1_score = 0
    num_f1_scores = 0
    
    for index in int_to_topic_code.keys():
        filtered_predicted = predicted[actual == index]
        
        tp = (filtered_predicted == index).sum()
        tp_and_fp = (predicted == index).sum()
        tp_and_fn = (actual == index).sum()
                
        precision = tp / tp_and_fp
        recall = tp / tp_and_fn
                
        sum_f1_score += (2 * precision * recall) / (precision + recall)
        num_f1_scores += 1
        
    return sum_f1_score / num_f1_scores
    


def micro_f1_score(int_to_topic_code, predicted, actual):
    """
    Calculates the micro F1 score
        
    :param int_to_topic_code: the index to topic lookup.
    :param predicted: the predicted class labels.
    :param actual: the actual class labels.
    :returns: the micro F1 score.
    """
    sum_tp = 0
    sum_tp_and_fp = 0
    sum_tp_and_fn = 0
    
    for index in int_to_topic_code.keys():
        filtered_predicted = predicted[actual == index]
        
        tp = (filtered_predicted == index).sum()
        tp_and_fp = (predicted == index).sum()
        tp_and_fn = (actual == index).sum()
        
        sum_tp += tp
        sum_tp_and_fp += tp_and_fp
        sum_tp_and_fn += tp_and_fn
    
    precision = sum_tp / sum_tp_and_fp
    recall = sum_tp / sum_tp_and_fn
    
    return (2 * precision * recall) / (precision + recall)
