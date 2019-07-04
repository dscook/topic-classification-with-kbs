#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def split_data(x, y):
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


def calculate_max_sequence_length(train_x):
    # Find the length of a tweet in words
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


def calculate_max_sentence_length(train_x):
    # Find the length of a tweet in words
    article_lengths = np.array([len(sentences) for sentences in train_x])
    
    print('Minimum length of article in sentences: {}'.format(np.min(article_lengths)))
    print('Maximum length of article in sentences: {}'.format(np.max(article_lengths)))
    print('Mean length of article in sentences: {:.4f}'.format(np.mean(article_lengths)))
    print('St dev of length of article in sentences: {:.4f}'.format(np.std(article_lengths)))
    
    # Set the max sequence length to mean plus 3 standard deviations (99.7% confidence)
    max_sequence_length = int(np.mean(article_lengths) + np.std(article_lengths)*3)
    
    # Confirm not many articles exceed this limit
    articles_exceeding_limit = [sentences for sentences in train_x if len(sentences) > max_sequence_length]
    percentage_articles_exceeding_limit = (len(articles_exceeding_limit)/len(train_x))*100
    print('Percentage of articles exceeding max sequence length limit: {:.4f}%'.format(percentage_articles_exceeding_limit))
    
    return max_sequence_length