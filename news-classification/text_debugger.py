#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import requests
from collections import defaultdict
from loader import load_preprocessed_data


# Prime TFIDF scores
x, y = load_preprocessed_data('data/rcv1_no_stopwords_coreference_lemmatized.csv')
doc = { 'documents': x }
requests.post(url = 'http://127.0.0.1:5001/tfidf', json = doc) 


document_to_debug = """
estimated Singaporeans time music mass outdoor aerobic workout nation fit red white clothing colour national flag participant Prime_Minister_Goh_Chok_Tong several member cabinet part km two-mile walk Officials Great_Singapore_Workout participant previous year State television total attendance similar event World_Guiness record aerobics gymnastics display participant Goh reporter workout large number young people part youth lead habit open fresh air sun director Ministry Health Healthy_Lifestyle_Unit K._Vijaya workout event fitness Singaporeans Reuters number Singaporeans sort regular exercise level obesity child annual workout
"""

print('')
print('------------ Text Analysed ------------')
print('')
print(document_to_debug)
print('')


# Make a REST request to get Wikipedia topic probabilities from the classifier server
doc = { 'text': document_to_debug }
r = requests.post(url = 'http://127.0.0.1:5001/classify', json = doc) 
wiki_topic_to_prob = r.json()


print('')
print('------------ Wikipedia Topic Probabilities ------------')
print('')
print(wiki_topic_to_prob)
print('')


r = requests.get(url = 'http://127.0.0.1:5001/probabilities/{}'.format(-1))
phrase_to_prob = r.json()

topics_to_phrases = defaultdict(set)

for phrase in phrase_to_prob.keys():
    doc = { 'text': phrase[7:] }
    r = requests.post(url = 'http://127.0.0.1:5001/classify', json = doc) 
    wiki_topic_to_prob = r.json()
    max_prob = 0
    max_topic = 0
    for topic, prob in wiki_topic_to_prob.items():
        if prob > max_prob:
            max_prob = prob
            max_topic = topic
    topics_to_phrases[max_topic].add(phrase[7:])

print('')
print('------------ Phrases Matched per Topic ------------')
print('')
for topic, phrases in topics_to_phrases.items():
    print('Topic: {}, Total Matches: {}'.format(topic, len(phrases)))
print('')
print('')
for topic, phrases in topics_to_phrases.items():
    print('Topic: {}, Matches: {}'.format(topic, phrases))

