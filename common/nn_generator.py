#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import keras


class DataGenerator(keras.utils.Sequence):


    def __init__(self, x, y, sent_embedding_dim, batch_size=32):
        self.x = x
        self.y = y
        self.sent_embedding_dim = sent_embedding_dim
        self.batch_size = batch_size


    def __len__(self):
        """
        Is called to to determine the number of batches per epoch.
        """
        return int(len(self.x) / self.batch_size) + 1


    def __getitem__(self, index):
        """
        Is called to get one batch of data.
        
        :param index: the index of the batch to return.
        """
        # Generate indexes of the batch
        start_index = index*self.batch_size
        end_index = (index+1)*self.batch_size
        
        batch = None
        batch_y = None
        if end_index > len(self.x):
            batch = self.x[start_index:]
            if self.y is not None:
                batch_y = self.y[start_index:]
        else:
            batch = self.x[start_index:end_index]
            if self.y is not None:
                batch_y = self.y[start_index:end_index]
        
        # Densify batch
        num_in_batch = len(batch)
        dense_batch = np.zeros(shape=(num_in_batch, self.sent_embedding_dim))
    
        for i in range(num_in_batch):
            sparse_embedding = batch[i] 
            dense_batch[i][:len(sparse_embedding)] = sparse_embedding
            
        if self.y is None:
            return dense_batch
        else:
            return dense_batch, batch_y


