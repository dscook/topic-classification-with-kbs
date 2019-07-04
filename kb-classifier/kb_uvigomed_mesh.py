#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lookup_cache_mesh import LookupCache
from sparql_dao_mesh import SparqlDao

def lookup_cache_init():
    return LookupCache()

def dao_init():
    return SparqlDao(endpoint_url='http://localhost:3030/MeSH/')

# Max depth of the topic hierarchy
topic_depth=12


def generate_root_topics():
    """
    Helper method to generate root topics so the entire MeSH topic hierarchy is covered.
    
    :returns: dict of all root topics in MeSH associated with a unique index.
    """
    wiki_topics_to_index = {}
    
    last_index = 0
    
    category_to_num_in_cat = { 'A': 21,
                               'B': 5,
                               'C': 26,
                               'D': 27,
                               'E': 7,
                               'F': 4,
                               'G': 17,
                               'H': 2,
                               'I': 3,
                               'J': 3,
                               'K': 1,
                               'L': 1,
                               'M': 1,
                               'N': 6,
                               'V': 4,
                               'Z': 1 }
    
    for category, number in category_to_num_in_cat.items():
        
        for i in range(1, number+1):
            wiki_topics_to_index['{}{:02d}'.format(category, i)] = last_index
            last_index += 1
        
    return wiki_topics_to_index

# Indexes of wiki root topics
wiki_topics_to_index = generate_root_topics()

# Mapping from wiki tipics to target classes for classification
# In the UVigoMED case this is actually irrelevant
wiki_topics_to_actual_topics = generate_root_topics()
