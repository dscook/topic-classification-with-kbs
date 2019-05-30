#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from term_document_matrix import TermDocumentMatrixCreator
from sklearn.metrics import classification_report
from sklearn.naive_bayes import BernoulliNB

def run_bernoulli_naive_bayes(train_x, train_y, test_x, test_y, topic_labels, ngram_range):
    """
    Runs Bernoulli Naive Bayes and returns a classification report that can be printed.
    
    :param train_x: the training data as a list of strings.
    :param train_y: the training labels as ints.
    :param test_x: the test data as a list of strings.
    :param test_y: the test labels as ints.
    :param topic_labels: the full topic labels to label the classification report.
    :param ngram_range: the ngram range to use as a tuple (lower, upper).
    :returns: a classification report that can be printed.
    """
    tdm_creator = TermDocumentMatrixCreator(train_x, ngram_range=ngram_range)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)

    naive_bayes = BernoulliNB()
    naive_bayes.fit(train_tdm, train_y)
    predict = naive_bayes.predict(test_tdm)
    
    return classification_report(test_y,
                                 predict, 
                                 digits=6, 
                                 target_names=topic_labels)