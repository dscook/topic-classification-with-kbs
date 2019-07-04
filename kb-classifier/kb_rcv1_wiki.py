#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lookup_cache_wiki import LookupCache
from sparql_dao_wiki import SparqlDao

def lookup_cache_init():
    return LookupCache(use_anchors_only=True)

def dao_init():
    return SparqlDao(endpoint_url='http://localhost:3030/DBpedia/')

# Max depth of the topic hierarchy
topic_depth=5

# Indexes of wiki root topics
wiki_topics_to_index = {
    'Crime': 0,
    'Law': 1,
    'Business': 2,
    'Economics': 3,
    'Elections': 4,
    'Politics': 5,
    'Health': 6,
    'Medicine': 7,
    'Religion': 8,
    'Theology': 9,
    'Sports': 10   
}

# Mapping from wiki tipics to target classes for classification
wiki_topics_to_actual_topics = {
    'Crime': 0,
    'Law': 0,
    'Business': 1,
    'Economics': 1,
    'Elections': 2,
    'Politics': 2,
    'Health': 3,
    'Medicine': 3,
    'Religion': 4,
    'Theology': 4,
    'Sports': 5
}
