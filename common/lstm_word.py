#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Embedding, LSTM, Dense
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import Adadelta
import numpy as np


class LstmPredictor():
    """
    Wraps the building of a Keras LSTM as well as methods for training and prediction on word embeddings.
    """
    
    def __init__(self,
                 word_index,
                 word_embedding_dim,
                 max_words_in_document,
                 word_embedding_model,
                 num_topics,
                 use_saved_weights=False,
                 weights_path='models/lstm.h5'):
        """
        :param word_index: a mapping of words in the vocabularly to integer IDs.
        :param word_embedding_dim: the length of a word embedding vector.
        :param max_words_in_document: the maximum number of words in a document.
        :param word_embedding_model: a Gensim KeyedVectors word embedding model.
        :param num_topics: the number of topics to predict.
        :param use_saved_weights: if True will load saved weights from a previous training run.
        :param weights_path: where to save best model weights.
        """
        self.model = self.create_lstm(word_index,
                                      word_embedding_dim,
                                      max_words_in_document,
                                      word_embedding_model,
                                      num_topics)
        
        # Path where weights from training should be saved
        self.weights_path = weights_path
        if use_saved_weights:
            self.model.load_weights(self.weights_path)
        
        self.model.compile(optimizer=Adadelta(), loss='categorical_crossentropy', metrics=['acc'])


    def create_embedding_matrix(self,
                                word_index,
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
        # Addition of 1 to account for special 'word not found' indicator
        num_words_in_vocab = len(word_index) + 1
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


    def create_lstm(self,
                    word_index,
                    word_embedding_dim,
                    max_words_in_document,
                    word_embedding_model,
                    num_topics):
        """
        Creates the LSTM Keras model.
        
        :param word_index: a mapping of words in the vocabularly to integer IDs.
        :param word_embedding_dim: the length of a word embedding vector.
        :param max_words_in_document: the maximum number of words in a document.
        :param word_embedding_model: a Gensim KeyedVectors word embedding model.
        :param num_topics: the number of topics to predict.
        :returns: the compiled LSTM model.
        """
        # Addition of 1 to account for special 'word not found' indicator
        num_words_in_vocab = len(word_index) + 1
        
        model = Sequential()
        model.add(Embedding(num_words_in_vocab, word_embedding_dim, input_length=max_words_in_document))
        model.add(LSTM(128))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(num_topics, activation='softmax'))
            
        # Initialise the word embedding layer with pre-trained word vectors
        # and ensure training does not change the weights
        embedding_matrix = self.create_embedding_matrix(word_index, word_embedding_dim, word_embedding_model)
        model.layers[0].set_weights([embedding_matrix])
        model.layers[0].trainable = False
        
        return model
    
    
    def train(self, x, y, x_val, y_val, class_weight=None):
        """
        Trains the LSTM model.
        
        :param x: the documents to train on.  Must be a list of lists of integers.
                  Each integer representing a word in the vocabularly.
        :param y: the document topic labels as integers.
        :param x_val: the validation documents, same format as x param.
        :param y_val: the validation document topics, same format as y param.
        :param class_weight: the class weights to use to pay more attention to under represented classes.
        """
        # Convert labels into one hot encoding for use with a neural network
        y_cat = to_categorical(y)
        y_val_cat = to_categorical(y_val)
        
        callbacks_list = [
                EarlyStopping(monitor='val_loss', patience=20),
                ModelCheckpoint(filepath=self.weights_path, monitor='val_loss', save_best_only=True)]
        self.model.fit(x, y_cat, epochs=100, callbacks=callbacks_list, 
                       batch_size=32, validation_data=(x_val, y_val_cat), class_weight=class_weight)
   
    
    def predict(self, x):
        """
        Make predictions on the provided test data.
        
        :param x: the documents to make predictions on.  Must be a list of lists of integers.
                  Each integer representing a word in the vocabularly.
        :returns: the predictions.
        """
        return np.argmax(self.model.predict(x), axis=1)
    
    