#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from term_document_matrix import TermDocumentMatrixCreator
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

def run_bernoulli_naive_bayes(train_x, train_y, test_x, test_y, ngram_range):
    """
    Runs Bernoulli Naive Bayes and returns the predictions.
    
    :param train_x: the training data as a list of strings.
    :param train_y: the training labels as ints.
    :param test_x: the test data as a list of strings.
    :param test_y: the test labels as ints.
    :param ngram_range: the ngram range to use as a tuple (lower, upper).
    :returns: predictions
    """
    tdm_creator = TermDocumentMatrixCreator(train_x, ngram_range=ngram_range)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)

    naive_bayes = BernoulliNB()
    naive_bayes.fit(train_tdm, train_y)
    predict_y = naive_bayes.predict(test_tdm)
    
    return predict_y


def run_multinomial_naive_bayes(train_x, train_y, test_x, class_priors, ngram_range):
    tdm_creator = TermDocumentMatrixCreator(train_x, binary = False, ngram_range=ngram_range)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)

    naive_bayes = MultinomialNB(class_prior=class_priors)
    naive_bayes.fit(train_tdm, train_y)
    predict_y = naive_bayes.predict(test_tdm)
    
    return predict_y


def run_multinomial_naive_bayes_tfidf(train_x, train_y, test_x, ngram_range):
    tdm_creator = TermDocumentMatrixCreator(train_x, binary = False, ngram_range=ngram_range)
    train_tdm = tdm_creator.create_term_document_matrix(train_x)
    test_tdm = tdm_creator.create_term_document_matrix(test_x)
    
    tfidf_transformer = TfidfTransformer()
    train_tfidf = tfidf_transformer.fit_transform(train_tdm)
    test_tfidf = tfidf_transformer.transform(test_tdm)

    naive_bayes = MultinomialNB()
    naive_bayes.fit(train_tfidf, train_y)
    predict_y = naive_bayes.predict(test_tfidf)
    
    return predict_y