#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np


class TfIdf:
    
    
    def __init__(self, classifier):
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
            
            # Determine what phrases in the document are valid from the knowledge base
            valid_phrases = self.identify_valid_phrases(document)
            
            # Update term counts for corpus
            for phrase in valid_phrases:
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
    
    
    def identify_valid_phrases(self, document):
        valid_phrases = set()
                
        tokens = document.split()
        
        # Maintain the start of the phrase we are processing
        index = 0
        
        # Initially consider a phrase of word length 3
        phrase_length = 3
        
        while index < len(tokens):
            
            # Check the phrase length doesn't exceed the end of the string
            while index + phrase_length > len(tokens):
                phrase_length -= 1
            
            # Try and find a match for 3 word phrase, then 2 then 1
            while phrase_length > 0:
                # Check to see if phrase exists in the knowledge base
                updated_tokens= []
                for token in tokens[index:index+phrase_length]:
                    updated_tokens.extend(token.split('_'))
                
                phrase = ' '.join(updated_tokens)
                
                # Look for phrase in anchor text matches
                if phrase in self.classifier.anchor_cache:
                    valid_phrases.add(phrase)
                            
                phrase_length -= 1
                            
            # Advance a token
            index += 1
            
            # Reset phrase length for processing next index
            phrase_length = 3
        
        return valid_phrases
        