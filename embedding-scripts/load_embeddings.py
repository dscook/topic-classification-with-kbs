#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader


def load_document_embeddings(path):
    """
    Loads the document embeddings from the given path.
    
    :param path: where to load the embeddings from.
    :returns: (document embeddings, target class labels)
    """
    embedding_dimension = 0
    
    # First pass to work out maximum topic ID to create numpy embeddings
    reader = DataFileReader(open(path, 'rb'), DatumReader())
    for document_embedding in reader:
        topic_probs = document_embedding['topic_probs']
        
        for topic_prob in topic_probs:
            topic_id = topic_prob['topic_id']
            if topic_id + 1 > embedding_dimension:
                embedding_dimension = topic_id + 1
    
    reader.close()
    
    # Second pass to actually store the embeddings
    x = []
    y = []
    
    reader = DataFileReader(open(path, 'rb'), DatumReader())
    for document_embedding in reader:
        label = document_embedding['label']
        topic_probs = document_embedding['topic_probs']
        
        embedding = np.zeros(shape=embedding_dimension)
        
        for topic_prob in topic_probs:
            topic_id = topic_prob['topic_id']
            prob = topic_prob['prob']
            embedding[topic_id] = prob
        
        x.append(embedding)
        y.append(label)
    
    reader.close()
    
    return x, y