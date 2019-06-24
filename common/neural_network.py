#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import Adam
import numpy as np

from nn_generator import DataGenerator


class NeuralNetwork():
    
    def __init__(self,
                 document_embedding_dim,
                 num_topics,
                 use_saved_weights=False,
                 weights_path='models/nn.h5'):
        """
        :param sentence_embedding_dim: the length of a sentence embedding vector.
        :param max_sentences_in_document: the maximum number of sentences in a document.
        :param num_topics: the number of topics to predict.
        :param use_saved_weights: if True will load saved weights from a previous training run.
        :param weights_path: where to save best model weights.
        """
        self.document_embedding_dim = document_embedding_dim
        self.model = self.create_nn(document_embedding_dim, num_topics)
        
        # Path where weights from training should be saved
        self.weights_path = weights_path
        if use_saved_weights:
            self.model.load_weights(self.weights_path)
        
        self.model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['acc'])


    def create_nn(self, document_embedding_dim, num_topics): 
        model = Sequential()
        model.add(Dropout(0.2, input_shape=(document_embedding_dim,)))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.2))
        #model.add(Dense(128, activation='relu'))
        #model.add(Dropout(0.2))
        #model.add(Dense(128, activation='relu'))
        #model.add(Dropout(0.2))
        model.add(Dense(num_topics, activation='softmax'))
        
        return model
    
    
    def train(self, x, y, x_val, y_val, class_weight=None):
        """
        Trains the LSTM model.
        
        :param x: the documents to train on.
        :param y: the document topics.  Must be one hot encoded.
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
    

    def train_generator(self, x, y, x_val, y_val, class_weight=None):
        # Convert labels into one hot encoding for use with a neural network
        y_cat = to_categorical(y)
        y_val_cat = to_categorical(y_val)
        
        training_generator = DataGenerator(x,
                                           y_cat,
                                           self.document_embedding_dim,
                                           batch_size=128)
        validation_generator = DataGenerator(x_val,
                                             y_val_cat,
                                             self.document_embedding_dim,
                                             batch_size=128)
        
        callbacks_list = [
                EarlyStopping(monitor='val_loss', patience=10),
                ModelCheckpoint(filepath=self.weights_path, monitor='val_loss', save_best_only=True)]
        self.model.fit_generator(generator=training_generator,
                                 validation_data=validation_generator,
                                 epochs=100,
                                 callbacks=callbacks_list,
                                 class_weight=class_weight)
    
    def predict(self, x):
        """
        Make predictions on the provided test data.
        
        :param x: the documents to make predictions on.  Must be a list of lists of integers.
                  Each integer representing a word in the vocabularly.
        :returns: the predictions.
        """
        return np.argmax(self.model.predict(x), axis=1)


    def predict_generator(self, x):
        test_generator = DataGenerator(x,
                                       None,
                                       self.document_embedding_dim,
                                       batch_size=128)
        return np.argmax(self.model.predict_generator(generator=test_generator), axis=1)
    
    