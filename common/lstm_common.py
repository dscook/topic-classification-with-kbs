#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def split_data(x, y):
    """
    Splits a dataset into 60% training, 20% validation and 20% test.
    
    :param x: the training features.
    :param y: the target class labels.
    :returns: (train features, train labels, validation features, validation labels, test features, test labels).
    """
    total_examples = len(y)
    split_point_1 = int(total_examples * 0.6)
    split_point_2 = int(total_examples * 0.8)
    train_x = x[:split_point_1]
    train_y = y[:split_point_1]
    val_x = x[split_point_1:split_point_2]
    val_y = y[split_point_1:split_point_2]
    test_x = x[split_point_2:]
    test_y = y[split_point_2:]
    
    return (train_x, train_y, val_x, val_y, test_x, test_y)


def calculate_max_word_length(train_x):
    """
    Caculates the maximum length of a training document in words to use in the LSTM.
    This length is calculated as the mean length plus 3 standard deviations.
    
    :param train_x: the documents as an array of strings.
    :returns the max sequence length (in words) to use in the LSTM.
    """
    # Find the length of an article in words
    article_lengths = np.array([len(article.split()) for article in train_x])
    
    print('Minimum length of article in words: {}'.format(np.min(article_lengths)))
    print('Maximum length of article in words: {}'.format(np.max(article_lengths)))
    print('Mean length of article in words: {:.4f}'.format(np.mean(article_lengths)))
    print('St dev of length of article in words: {:.4f}'.format(np.std(article_lengths)))
    
    # Set the max sequence length to mean plus 3 standard deviations (99.7% confidence)
    max_sequence_length = int(np.mean(article_lengths) + np.std(article_lengths)*3)
    
    # Confirm not many articles exceed this limit
    articles_exceeding_limit = [article for article in train_x if len(article.split()) > max_sequence_length]
    percentage_articles_exceeding_limit = (len(articles_exceeding_limit)/len(train_x))*100
    print('Percentage of articles exceeding max sequence length limit: {:.4f}%'.format(percentage_articles_exceeding_limit))
    
    return max_sequence_length
