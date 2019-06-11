#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import requests
from collections import defaultdict

document_to_debug = """
Republican presidential candidate Bob_Dole final weeks campaign votes California West Mid-Atlantic states Northeast CNN CNN Dole campaign aides Republican challenger strategy major final push western states Oregon Washington Dole key states Ohio Michigan Indiana Nebraska home state Kansas Dole New_Hampshire weekend victory aides CNN states Pennsylvania New_Jersey rest Mid-Atlantic Northeast interview cable on-line network MSNBC Dole President_Clinton lead percentage points California lot time opportunity Dole win Kansas hometown Russell Kansas Nov. Dole Clinton lead percentage points Reuters daily poll Clinton percent poll Dole percent Reform_Party candidate Ross_Perot percent percent poll John_Zogby_Group_International likely voters three-day period result percentage point margin error numbers direction Dole MSNBC
"""

print('')
print('------------ Text Analysed ------------')
print('')
print(document_to_debug)
print('')


# Make a REST request to get Wikipedia topic probabilities from the classifier server
doc = { 'text': document_to_debug }
r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
wiki_topic_to_prob = r.json()


print('')
print('------------ Wikipedia Topic Probabilities ------------')
print('')
print(wiki_topic_to_prob)
print('')


r = requests.get(url = 'http://127.0.0.1:5000/probabilities/{}'.format(-1))
phrase_to_prob = r.json()

topics_to_phrases = defaultdict(set)

for phrase in phrase_to_prob.keys():
    doc = { 'text': phrase[7:] }
    r = requests.post(url = 'http://127.0.0.1:5000/classify', json = doc) 
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

