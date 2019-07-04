#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from term_document_matrix import TermDocumentMatrixCreator
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


def run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors=None):
    """
    Runs Multinomial Naive Bayes and returns the predictions.
    
    :param train_x: list of documents as text strings forming the training data.
    :param train_y: training data target classes as integers.
    :param test_x: list of documents as text strings forming the test data.
    :param class_priors: prior probabilities of target classes of shape (num target classes,).
                         set to None to determine from the training data.
    :returns: the predicted target classes for the test data.
    """
    tdm_creator = TermDocumentMatrixCreator(train_x)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)

    naive_bayes = MultinomialNB(class_prior=class_priors)
    naive_bayes.fit(train_tdm, train_y)
    predict_y = naive_bayes.predict(test_tdm)
    
    return predict_y


def run_support_vector_classifier(train_x, train_y, test_x, C=0.01):
    """
    Runs Support Vector Classifier and returns the predictions.
    
    :param train_x: list of documents as text strings forming the training data.
    :param train_y: training data target classes as integers.
    :param test_x: list of documents as text strings forming the test data.
    :param C: the C hyperparameter controlling the width of the street.
    :returns: the predicted target classes for the test data.
    """
    tdm_creator = TermDocumentMatrixCreator(train_x)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)
    
    svc = LinearSVC(loss='hinge', class_weight='balanced', max_iter=10000, C=C)
    svc.fit(train_tdm, train_y)
    predict_y = svc.predict(test_tdm)
    
    return predict_y
    