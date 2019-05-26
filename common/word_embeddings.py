#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class DocToIntSequenceConverter():
    """
    Provides functionality for converting documents to integer sequences.
    """
    
    def __init__(self, corpus, max_sequence_length, max_words=None):
        """
        :param corpus: the training data documents as a list of strings.
        :param max_sequence_length: Sequences must be of the same length for learning. Truncate or pad if necessary.
        :param max_words: Consider only the top words in the dataset when converting to integer sequences.
                          None means consider all words.
        """
        self.max_sequence_length = max_sequence_length
        # To store the tokenizer used to convert text to lists of integers representing the words
        # A pre-requisite step before converting to word embeddings.
        self.tokenizer = Tokenizer(num_words=max_words, lower=False)
        self.tokenizer.fit_on_texts(corpus)


    def convert_to_integer_sequences(self, corpus, padding='pre'):
        """
        Convert each document in the corpus to a sequence of integers, padding with 0s to achieve max_sequence_length.
        
        :param corpus: the documents to convert as a list of strings.
        :param padding: where padding should be applied, before (pre) or at the end (post) of the sequence.
        :returns: the corpus with each document as a sequence of integers, a list of lists.
        """
            
        # Convert text to list of integers
        sequences = self.tokenizer.texts_to_sequences(corpus)
        padded_data = pad_sequences(sequences, maxlen=self.max_sequence_length, padding=padding)
        return padded_data