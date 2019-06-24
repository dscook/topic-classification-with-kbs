#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lookup_cache_mesh import LookupCache
from sparql_dao_mesh import SparqlDao

def lookup_cache_init():
    return LookupCache()

def dao_init():
    return SparqlDao(endpoint_url='http://localhost:3030/MeSH/')

topic_depth=8

wiki_topics_to_index = {
    'C01': 0,
    'C02': 1,
    'C03': 2,
    'C04': 3,
    'C05': 4,
    'C06': 5,
    'C07': 6,
    'C08': 7,
    'C09': 8,
    'C10': 9,
    'C11': 10,
    'C12': 11,
    'C13': 12,
    'C14': 13,
    'C15': 14,
    'C16': 15,
    'C17': 16,
    'C18': 17,
    'C19': 18,
    'C20': 19,
    'C21': 20,
    'C22': 21,
    'C23': 22,
    'C24': 23,
    'C25': 24,
    'C26': 25
}

wiki_topics_to_actual_topics = {
    'C01': 0,
    'C02': 1,
    'C03': 2,
    'C04': 3,
    'C05': 4,
    'C06': 5,
    'C07': 6,
    'C08': 7,
    'C09': 8,
    'C10': 9,
    'C11': 10,
    'C12': 11,
    'C13': 12,
    'C14': 13,
    'C15': 14,
    'C16': 15,
    'C17': 16,
    'C18': 17,
    'C19': 18,
    'C20': 19,
    'C21': 20,
    'C22': 21,
    'C23': 22,
    'C24': 23,
    'C25': 24,
    'C26': 25
}