#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.layers import Embedding, LSTM, Dense
from keras.models import Sequential
import numpy as np


def create_embedding_matrix(word_index,
                            word_embedding_dim,
                            word_embedding_model):
    """
    Creates a word embedding matrix, containing a word embedding for each word in the vocabularly.
    
    Method adapted from:
        Chastney, J., Cook, D., Ma, J., Melamed, T., 2019. Lab 1: Group Project.
        CM50265: Machine Learning 2. University of Bath. Unpublished.

    But was originally implemented in:
        Chollet, F., 2017. Deep learning with python. 1st ed. Greenwich, CT, USA: Manning Publications Co.
    
    :param word_index: a mapping of words in the vocabularly to integer IDs.
    :param word_embedding_dim: the length of a word embedding vector.
    :param word_embedding_model: a Gensim KeyedVectors word embedding model.
    :returns: a word embedding matrix.
    """
    num_words_in_vocab = len(word_index)
    embedding_matrix = np.zeros((num_words_in_vocab, word_embedding_dim))

    for word, i in word_index.items():
        embedding_vector = None
        try:
            embedding_vector = word_embedding_model.get_vector(word)
        except:
            # Do nothing
            pass
        # Words not found in word embedding model will be set to all zeros
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    
    return embedding_matrix


def create_lstm(word_index, word_embedding_dim, max_words_in_document, word_embedding_model, num_topics):
    """
    Creates the LSTM Keras model.
    
    :param word_index: a mapping of words in the vocabularly to integer IDs.
    :param word_embedding_dim: the length of a word embedding vector.
    :param max_words_in_document: the maximum number of words in a document.
    :param word_embedding_model: a Gensim KeyedVectors word embedding model.
    :param num_topics: the number of topics to predict.
    :returns: the compiled LSTM model.
    """
    num_words_in_vocab = len(word_index)
    
    model = Sequential()
    model.add(Embedding(num_words_in_vocab, word_embedding_dim, input_length=max_words_in_document))
    model.add(LSTM(64))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_topics, activation='softmax'))
        
    # Initialise the word embedding layer with pre-trained word vectors
    # and ensure training does not change the weights
    embedding_matrix = create_embedding_matrix(word_index, word_embedding_dim, word_embedding_model)
    model.layers[0].set_weights([embedding_matrix])
    model.layers[0].trainable = False
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    
    return model
    