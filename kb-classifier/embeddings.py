#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from avro.datafile import DataFileReader
from avro.io import DatumReader
from collections import defaultdict
import csv
import numpy as np

class EmbeddingModel:
    """
    Implements the same interface as a Gensim KeyedVectors word embedding model.
    This enables the knowledge base embeddings to be used with the LSTM in a consistent way.
    """
    
    def __init__(self,
                 embedding_file_path,
                 topic_id_mapping_path,
                 underscored_phrase=False,
                 filter_low_occur_features=False):
        """
        :param embedding_file_path: the path to the word embeddings in avro format.
        :param topic_id_mapping_path: the path to the CSV that contains all valid topic IDs.
        :param underscored_phrase: set to True if phrase should be stored with an underscore rather than a space.
        :param filter_low_occur_features: removes any features that occur in less than 0.1% of the phrases.
        """
        
        # To store mapping from topic ID to index into embedding vector
        self.topic_id_to_index = {}
                
        # Determine topics involved in the embeddings
        self.topic_id_to_name = {}
        self.topic_name_to_id = {}
        self.embedding_dim = 0
        with open(topic_id_mapping_path, newline='') as csvfile:
            mapping_reader = csv.reader(csvfile)
            for row in mapping_reader:
                topic_name = row[0]
                identifier = int(row[1])
                self.topic_id_to_index[identifier] = self.embedding_dim
                self.embedding_dim += 1
                self.topic_id_to_name[identifier] = topic_name
                self.topic_name_to_id[topic_name] = identifier
        
        # Maintain index to topic mapping
        self.index_to_topic = {}
        for topic_id, index in self.topic_id_to_index.items():
            self.index_to_topic[index] = self.topic_id_to_name[topic_id]
        
        # To store phrase to embedding vector
        self.phrase_to_embedding = {}
        
        # Maint count of number of times there is an entry in each dimension of the embedding
        self.embedding_dim_to_count = defaultdict(int)
        
        # Create the phrase embedding vectors
        reader = DataFileReader(open(embedding_file_path, 'rb'), DatumReader())
        for phrase_topic_mappings in reader:
            phrase = phrase_topic_mappings['phrase']
            
            if underscored_phrase:
                phrase = '_'.join(phrase.split())
            
            topic_probs = phrase_topic_mappings['topic_probs']
            
            embedding = np.zeros(shape=self.embedding_dim)
            
            # Loop through topic mappings adding to the embedding
            for topic_prob in topic_probs:
                topic_id = topic_prob['topic_id']
                prob = topic_prob['prob']
                embedding[self.topic_id_to_index[topic_id]] = prob
                self.embedding_dim_to_count[self.topic_id_to_index[topic_id]] += 1
                            
            self.phrase_to_embedding[phrase] = embedding
            
        reader.close()
        
        # If we are filtering features that don't occur very often then calculate what features we should keep
        self.filter_low_occur_features = filter_low_occur_features
        if filter_low_occur_features:
            
            self.features_to_keep = []
            
            num_phrases = len(self.phrase_to_embedding.keys())
            
            for feature, count in self.embedding_dim_to_count.items():
                if count/num_phrases >= 0.001:
                    self.features_to_keep.append(feature)


    def get_vector(self, word):
        """
        Get the word embedding for the given word.
        
        :param word: the word to lookup the embedding for.
        :returns: a vector containing the word embedding.
        """
        if self.filter_low_occur_features:
            return self.phrase_to_embedding[word][self.features_to_keep]
        else:
            return self.phrase_to_embedding[word]


    def get_embedding_dim(self):
        """
        :returns: the length of the knowledge base word embeddings.
        """
        if self.filter_low_occur_features:
            return len(self.features_to_keep)
        else:
            return self.embedding_dim


    def get_topic_for_index(self, index):
        """
        Gets the topic name for a supplied embedding position index.  Gives a human understandable term that the
        particular feature represents.
        
        :param index: the embedding position to obtain a topic name for.
        :returns: the name of the topic that corresponds to the given embedding position.
        """
        return self.index_to_topic[index]


    def get_index_for_topic(self, topic):
        """
        Gets the embedding index for a human readable topic name.
        
        :param topic: the name of the topic to obtain the embedding position for.
        :returns: the embedding position that corresponds to the given topic.
        """
        topic_id = self.topic_name_to_id[topic]
        return self.topic_id_to_index[topic_id]