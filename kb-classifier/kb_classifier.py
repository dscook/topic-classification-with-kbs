#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import requests
from sklearn.metrics import classification_report, confusion_matrix, f1_score

from kb_common import wiki_topics_to_actual_topics


class KnowledgeBasePredictor():
    
    
    def __init__(self, topic_labels):
        self.topic_labels = topic_labels
        self.weights = np.array([1,1,1,1,1,1])


    def train(self, x, y):
        predict_y = self.make_unsupervised_predictions(x, return_probs=True)
        
        # Figure out how to reweight the probabilities to give us the best possible micro F1 score
        best_micro_f1 = 0
        
        for i in range(100000):
            weights = np.random.uniform(0.25, 4, 6)
            
            new_predict_y = predict_y.copy()
            new_predict_y /= weights
            new_predict_y /= np.sum(new_predict_y, axis=1)[:, None]
            new_predict_y = np.argmax(new_predict_y, axis=1)
            
            micro_f1 = f1_score(y, new_predict_y, average='micro')
            
            if micro_f1 > best_micro_f1:
                best_micro_f1 = micro_f1
                self.weights = weights
        
        print('Best weights found {}'.format(self.weights))
        
    
    def predict(self, x):
        predict_y = self.make_unsupervised_predictions(x)
        return predict_y
    
    
    def get_classification_report(self, y, predict):
        clazzification_report = classification_report(y, predict, digits=6, target_names=self.topic_labels)
        confuzion_matrix = confusion_matrix(y, predict)
        return (clazzification_report, confuzion_matrix)
    
    
    def make_unsupervised_predictions(self, x, return_probs=False):
        
        predict = np.zeros(shape=len(x))
        apply_weighting = True
        
        if return_probs:
            predict = np.zeros(shape=(len(x), len(self.topic_labels)))
            apply_weighting = False
        
        for i in range(len(x)):
            print(i)
            
            # Make a REST request to get Wikipedia topic probabilities from the classifier server
            doc = { 'text': x[i] }
            r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
            topic_to_prob = r.json()
                
            # Convert Wikipedia topic probabilities to actual topic probabilities
            topic_index_to_prob = self.convert_topic_probs_wikipedia_to_actual(topic_to_prob, apply_weighting)
            
            # Store prediction
            if not return_probs:
                predict[i] = np.argmax(topic_index_to_prob)
            else:
                predict[i] = topic_index_to_prob

        return predict


    def convert_topic_probs_wikipedia_to_actual(self, topic_to_prob, apply_weighting):            
        topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
        
        topic_index_to_prob = np.zeros(shape=len(topic_indexes))
        for topic in topic_to_prob.keys():
            topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += topic_to_prob[topic]
        
        if apply_weighting:
            #topic_index_to_prob /= np.array([0.5,2,1.75,1,1,1])
            topic_index_to_prob /= self.weights
            topic_index_to_prob /= np.sum(topic_index_to_prob)
        
        return topic_index_to_prob