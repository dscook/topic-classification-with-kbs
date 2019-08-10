#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import requests
from collections import defaultdict
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

from kb_common import wiki_topics_to_actual_topics


class KnowledgeBaseClassifier():
    """
    The knowledge base classifier that makes HTTP REST calls to embed documents, trains a Random Forest on these
    embeddings then is capable of making predictions on new documents.
    """
    
    def __init__(self, topic_labels, topic_depth, top_level_prediction_number=None):
        """
        :param topic_labels: the target topic class labels.
        :param topic_depth: the topic depth to use for knowledge base document embedding, set to 'all' for all topics.
        :param top_level_prediction_number: the number of root topics, only required to be set if the number of
                                            root topics in the topic hierarchy is different to the number of 
                                            target topic class labels.
        """
        self.topic_labels = topic_labels
        self.topic_depth = topic_depth
        self.top_level_prediction_number = len(self.topic_labels)
        if top_level_prediction_number is not None:
            self.top_level_prediction_number = top_level_prediction_number

        
    def train(self, x, y, balanced_classes=True):
        """
        Train the knowledge base classifier.  Will obtain document embeddings for the supplied input documents then
        fit a Random Forest.
        
        :param x: the input documents.
        :param y: the target class labels as integers.
        :param balanced_classes: set to False if the target class distribution is uneven.
        """
        document_embeddings = self.obtain_document_embeddings(x, training=True)
        
        # Handle case where there is an imbalance in the class labels
        class_weight = None
        if not balanced_classes:
            class_weight = 'balanced'
            
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42, class_weight=class_weight)
        self.classifier.fit(document_embeddings, y)


    def predict(self, x):
        """
        Given a list of input documents returns the predicted target classes.
        
        :param x: the input documents.
        :returns: the predicted target classes.
        """
        document_embeddings = self.obtain_document_embeddings(x, training=False)
        self.last_predict = self.classifier.predict(document_embeddings)
        return self.last_predict
    
    
    def get_classification_report(self, y, predict):
        """
        Given actual target classes and predicted target classes generates a classification report
        and confusion matrix.
        
        :param y: actual target classes.
        :param predict: predicted target classes.
        :returns (classification report, confusion matrix).
        """
        clazzification_report = classification_report(y,
                                                      predict,
                                                      digits=6,
                                                      target_names=self.topic_labels,
                                                      labels=np.arange(len(self.topic_labels)))
        confuzion_matrix = confusion_matrix(y, predict)
        return (clazzification_report, confuzion_matrix)
    
    
    def obtain_document_embeddings(self, x, training):
        """
        Obtain the document embeddings for the given input documents.
        
        :param x: the input documents.
        :param training: set to True if the input documents are the training set.
        :returns: the document embeddings as a numpy array of shape (num of docs, embedding dimension)
        """
        class_probabilities = np.zeros(shape=(len(x), self.top_level_prediction_number))
        wikipedia_topic_probabilities = defaultdict(lambda: {})

        for i in range(len(x)):
            
            print(i)
            # Make a REST request to get Wikipedia root topic probabilities from the classifier server
            doc = { 'text': x[i] }
            r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
            wiki_topic_to_prob = r.json()
                
            # Convert root Wikipedia topic probabilities to actual topic probabilities
            topic_index_to_prob = self.convert_topic_probs_wikipedia_to_actual(wiki_topic_to_prob)
            class_probabilities[i] = topic_index_to_prob
            
            # Get Wikipedia topic probabilities at specified depth for random forest training/prediction
            r = requests.get(url = 'http://127.0.0.1:5000/probabilities/{}'.format(self.topic_depth))
            wiki_topic_to_prob = r.json()
            
            # Store Wikipedia topic probabilities
            for topic, probability in wiki_topic_to_prob.items():
                wikipedia_topic_probabilities[topic][i] = probability
                
        # Convert Wikipedia topic probabilities from dictionary to matrix
        if training:
            self.number_of_features = len(wikipedia_topic_probabilities.keys())
            self.index_to_topic = {}
            i = 0
            for topic in wikipedia_topic_probabilities.keys():
                self.index_to_topic[i] = topic
                i += 1
        
        wiki_prob_matrix = np.zeros(shape=(len(x), self.number_of_features))
        
        print('Wiki topic probabilities shape: {}'.format(wiki_prob_matrix.shape))    # DEBUGGING
        
        for i in range(self.number_of_features):
            for j in range(len(x)):
                
                # Get topic for index
                topic = self.index_to_topic[i]
                
                # A particular document may not have a value for this topic if its unrelated so set to 0
                if topic in wikipedia_topic_probabilities and j in wikipedia_topic_probabilities[topic]:
                     wiki_prob_matrix[j][i] = wikipedia_topic_probabilities[topic][j]
                else:
                    wiki_prob_matrix[j][i] = 0.0
        
        self.last_class_probabilities = class_probabilities
        return wiki_prob_matrix


    def convert_topic_probs_wikipedia_to_actual(self, wiki_topic_to_prob):    
        """
        Converts root level wikipedia topic probabilities to target class probabilities.
        Note more than one root level wikipedia topic may map to the same target class.
        
        :param wiki_topic_to_prob: dict of wiki topic to probability.
        :returns: numpy array of shape (number of target classes,).
        """        
        topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
        topic_index_to_prob = np.zeros(shape=len(topic_indexes))
        
        if wiki_topic_to_prob:
            for topic in wiki_topic_to_prob.keys():
                topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += wiki_topic_to_prob[topic]
                
        return topic_index_to_prob