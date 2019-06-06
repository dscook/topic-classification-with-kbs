#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np


class TfIdf:
    
    
    def __init__(self, classifier):
        # Reuse classifier so we can determine if phrases are in the knowledge base
        self.classifier = classifier
        
        
    def fit(self, documents):
        """
        Given a set of documents, calculates the IDF value for each term.
        
        :param documents: iterable list of documents.
        """
        self.idf_dict = {}
        
        # Get the number of documents in the corpus
        N = len(documents)
        
        # Loop through the documents incrementing a count for each term encountered
        # Note the term must exist in the knowledge base for it to be valid
        self.term_document_counts = defaultdict(int)
        for document in documents:
            
            # Reuse classifier functionality to determine what phrases are valid
            phrase_to_topic_dict, _ = self.classifier.identify_leaf_topics(document)
            
            # Update term counts for corpus
            for phrase in phrase_to_topic_dict.keys():
                self.term_document_counts[phrase] += 1
        
        # Calculate IDF values
        # Store the maximum IDF value, we will use it when we encounter terms in the test set we haven't seen before
        self.max_idf_value = 0
        for term, document_count in self.term_document_counts.items():
            idf_value = np.log(N / document_count)
            self.idf_dict[term] = idf_value
            if idf_value > self.max_idf_value:
                self.max_idf_value = idf_value


    def calculate_tfidf(self, term, term_count, document_length):
        """
        Calculates the TF-IDF value for the provided term.
        
        :param term: the term to calculate the TF-IDF value for.
        :param term_count: the number of times the term appears in the document.
        :param document_length: the number of words in the document.
        :returns: the calculated TF-IDF value.
        """
        if term not in self.idf_dict:
            return term_count/document_length * self.max_idf_value
        else:
            return term_count/document_length * self.idf_dict[term]
        
        
        
            