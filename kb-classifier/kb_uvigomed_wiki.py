#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lookup_cache_wiki import LookupCache
from sparql_dao_wiki import SparqlDao

def lookup_cache_init():
    return LookupCache()

def dao_init():
    return SparqlDao(endpoint_url='http://localhost:3030/DBpedia/')

# Max depth of the topic hierarchy
topic_depth=4

# Indexes of wiki root topics
wiki_topics_to_index = {
    'Anatomy': 0,
    'Health': 1,
    'Diseases_and_disorders': 2,
    'Deaths_by_cause': 3,
    'Mammals': 4,
    'Virology': 5,
    'Genetics': 6,
    'Clinical_medicine': 7,
    'Human_pregnancy': 8
}

# Mapping from wiki tipics to target classes for classification
# In the UVigoMED case this is actually irrelevant
wiki_topics_to_actual_topics = {
    'Anatomy': 0,
    'Health': 1,
    'Diseases_and_disorders': 2,
    'Deaths_by_cause': 3,
    'Mammals': 4,
    'Virology': 5,
    'Genetics': 6,
    'Clinical_medicine': 7,
    'Human_pregnancy': 8
}
