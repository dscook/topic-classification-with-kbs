#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import requests
from sklearn.metrics import classification_report, confusion_matrix
#from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from kb_common import wiki_topics_to_actual_topics, wiki_topics_to_index


class KnowledgeBasePredictor():
    
    
    def __init__(self, topic_labels):
        self.topic_labels = topic_labels


    def train(self, x, y):
        predict_y, wiki_class_probabilities = self.make_unsupervised_predictions(x)
        #predict_y = np.concatenate((predict_y, predict_y**2, predict_y**3, np.exp(predict_y)), axis=1)
        #self.classifier = LogisticRegression(random_state=42, solver='lbfgs', multi_class='multinomial', C=10.0).fit(predict_y, y)
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.classifier.fit(wiki_class_probabilities, y)


    def predict(self, x):
        predict_y, wiki_class_probabilities = self.make_unsupervised_predictions(x)
        #predict_y = np.concatenate((predict_y, predict_y**2, predict_y**3, np.exp(predict_y)), axis=1)
        self.last_predict = self.classifier.predict(wiki_class_probabilities)
        return self.last_predict
    
    
    def get_classification_report(self, y, predict):
        clazzification_report = classification_report(y, predict, digits=6, target_names=self.topic_labels)
        confuzion_matrix = confusion_matrix(y, predict)
        return (clazzification_report, confuzion_matrix)
    
    
    def make_unsupervised_predictions(self, x):
        
        class_probabilities = np.zeros(shape=(len(x), len(self.topic_labels)))
        wiki_class_probabilities = np.zeros(shape=(len(x), len(wiki_topics_to_index.keys())))

        for i in range(len(x)):
            
            # Make a REST request to get Wikipedia topic probabilities from the classifier server
            doc = { 'text': x[i] }
            r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
            topic_to_prob = r.json()
                
            # Convert Wikipedia topic probabilities to actual topic probabilities
            topic_index_to_prob, wiki_topic_index_to_prob = self.convert_topic_probs_wikipedia_to_actual(topic_to_prob)
            class_probabilities[i] = topic_index_to_prob
            wiki_class_probabilities[i] = wiki_topic_index_to_prob
        
        self.last_class_probabilities = class_probabilities
        return class_probabilities, wiki_class_probabilities


    def convert_topic_probs_wikipedia_to_actual(self, topic_to_prob):            
        topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
        
        topic_index_to_prob = np.zeros(shape=len(topic_indexes))
        wiki_topic_index_to_prob = np.zeros(shape=len(wiki_topics_to_index.keys()))
        
        for topic in topic_to_prob.keys():
            topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += topic_to_prob[topic]
            wiki_topic_index_to_prob[wiki_topics_to_index[topic]] = topic_to_prob[topic]
                
        return topic_index_to_prob, wiki_topic_index_to_prob