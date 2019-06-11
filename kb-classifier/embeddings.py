#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from avro.datafile import DataFileReader
from avro.io import DatumReader
import csv
import numpy as np

class EmbeddingModel:
    
    def __init__(self, embedding_file_path, topic_id_mapping_path):
        
        # To store mapping from topic ID to index into embedding vector
        self.topic_id_to_index = {}
        
        # Determine topics involved in the embeddings
        self.embedding_dim = 0
        with open(topic_id_mapping_path, newline='') as csvfile:
            mapping_reader = csv.reader(csvfile)
            for row in mapping_reader:
                identifier = int(row[1])
                self.topic_id_to_index[identifier] = self.embedding_dim
                self.embedding_dim += 1
        
        # To store phrase to embedding vector
        self.phrase_to_embedding = {}
        
        # Create the phrase embedding vectors
        reader = DataFileReader(open(embedding_file_path, 'rb'), DatumReader())
        for phrase_topic_mappings in reader:
            phrase = phrase_topic_mappings['phrase']
            topic_probs = phrase_topic_mappings['topic_probs']
            
            embedding = np.zeros(shape=self.embedding_dim)
            
            # Loop through topic mappings adding to the embedding
            for topic_prob in topic_probs:
                topic_id = topic_prob['topic_id']
                prob = topic_prob['prob']
                embedding[self.topic_id_to_index[topic_id]] = prob
                            
            self.phrase_to_embedding[phrase] = embedding
            
        reader.close()
        
    def get_vector(self, word):
        return self.phrase_to_embedding[word]
    
    def get_embedding_dim(self):
        return self.embedding_dim