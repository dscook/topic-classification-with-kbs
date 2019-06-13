#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible and knowledge base classifier code
import sys
sys.path.append('../common/')
sys.path.append('../kb-classifier/')

import requests
from collections import defaultdict

document_to_debug = """
large crowd Moslems rally United_States Israel haj pilgrimage Saudi_Arabia Saudi ban Iranian state media Tehran radio pilgrims Death Israel Death America Mount_Arafat city Mecca site Islam shrine independent confirmation report reaction Saudi_Arabia Iran news agency IRNA pilgrims Iran countries Kuwait Egypt Algeria Afghanistan Libya Bosnia France Germany Netherlands rally Iranian pilgrimage tent compound Iran pilgrims first disavowal infidels rally Mecca Saudi ban political activities haj word Saudi_Arabia demonstration Iran Iranians haj year Tehran casualties pilgrims fire tent compound people Tense relations Saudi_Arabia Iran turn staging rally annual haj climax Moslems Radical Shi'ite_Iran Moslems political grievances haj rallies Israel United_States enemies Islam Conservative Sunni_Saudi_Arabia pilgrimage religious row Gulf richest oil states haj people Iranians clashes Saudi security forces Iranian-led rally Iran haj years Saudi_Arabia violators ban political activity haj confrontation Saudi security Iranian pilgrims recent years low-key rallies Iran haj compounds Saudi forces Iran relations Saudi_Arabia Gulf_Arab states officials state media run tones kingdom
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

