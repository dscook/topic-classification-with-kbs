#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

from kb_common import wiki_topics_to_actual_topics, wikipedia_topic_probs_as_array


class KnowledgeBasePredictor():
    
    
    def __init__(self, topic_labels):
        self.topic_labels = topic_labels
        self.regression = LogisticRegression(solver='lbfgs', multi_class='multinomial')
        
    
    def train(self, x, y):
        unsupervised_y = self.make_unsupervised_predictions(x)
        self.regression.fit(unsupervised_y, y)
    
    
    def predict(self, x):
        unsupervised_y = self.make_unsupervised_predictions(x)
        return self.regression.predict(unsupervised_y)
    
    
    def get_classification_report(self, y, predict):
        clazzification_report = classification_report(y, predict, digits=6, target_names=self.topic_labels)
        confuzion_matrix = confusion_matrix(y, predict)
        return (clazzification_report, confuzion_matrix)
    
    
    def make_unsupervised_predictions(self, x):
        predict = np.zeros(shape=(len(x), len(wiki_topics_to_actual_topics.keys())))
        
        for i in range(len(x)):
            print(i)
            
            # Make a REST request to get Wikipedia topic probabilities from the classifier server
            doc = { 'text': x[i] }
            r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
            topic_to_prob = r.json()
                
            # Convert Wikipedia topic probabilities to array structure
            prob_array = wikipedia_topic_probs_as_array(topic_to_prob)
            
            # Store prediction
            predict[i] = prob_array

        return predict