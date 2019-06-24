#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wiki_lookup_cache import LookupCache

def lookup_cache_init():
    return LookupCache(use_anchors_only=True)

sparql_endpoint_url='http://localhost:3030/DBpedia/'

topic_depth=5

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
