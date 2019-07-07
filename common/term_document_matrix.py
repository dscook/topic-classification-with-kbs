#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer


class TermDocumentMatrixCreator():
    """
    Fits a text corpus then can be called to create term document matrices.
    """
    
    def __init__(self, documents, binary = False, ngram_range = (1,1)):
        """
        :param documents: list of text strings to fit, each word will form part of the possible vocabularly.
        :param binary: Set to True to do presence or absence of word rather than count.
        :param ngram_range: (lower_word_ngram_number, upper_word_ngram_number).
        """
        # Assume words already lower case
        self.vectoriser = CountVectorizer(lowercase = False, binary = binary, ngram_range = ngram_range)
        self.vectoriser.fit(documents)
        print('Number of words in vocabulary: {}'.format(len(self.vectoriser.vocabulary_.keys())))


    def create_term_document_matrix(self, documents):
        """
        :param documents: list of text strings to transform.
        :returns: a document term matrix.
        """
        return self.vectoriser.transform(documents)
    
    