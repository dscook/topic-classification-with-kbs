#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import requests
from collections import defaultdict

document_to_debug = """
India acute electricity shortage critical point investments free-market reform programme power failures capital city Delhi winter critical nature power problem country government annual Economic_Survey April-March survey Finance_Minister_P._Chidambaram number negative results power outages India economic reform programme economy world unavailable uncertain erratic supplies public grid economy heavy price form foregone production exports goods services frustrated investment intentions survey high-cost captive power generation loss international competitiveness barriers spread information technology terms production technical progress international specialisation world India investments worth power shortages survey India megawatts power generation capacity first years Eighth Five-Year Plan addition megawatts years government survey several reasons slippages power generation problems paucity funds supply equipment land acquisition territorial disputes disturbed conditions plant sites fuel linkages contract failures rehabilitation people power plant sites survey government strategy power shortage encouragement doses private capital restructuring inefficient state-run power distribution utilities
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

