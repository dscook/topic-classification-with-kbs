#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LookupCache:
    
    def __init__(self,
                 resource_path='../kb-classifier/data-wiki/resources.txt',
                 redirect_path='../kb-classifier/data-wiki/redirect_resources.txt',
                 anchor_path='../kb-classifier/data-wiki/anchors.txt',
                 use_anchors_only=False):
        # Prime a cache of all valid phrases to prevent costly DB lookups
        self.resource_cache = self.load_phrase_cache(resource_path)
        self.redirect_cache = self.load_phrase_cache(redirect_path)
        self.anchor_cache = self.load_phrase_cache(anchor_path)
        self.use_anchors_only = use_anchors_only
        print('Cache Initialised')
    
        
    def load_phrase_cache(self, phrase_path):
        """
        Given a file of phrases,  returns a set of those phrases so it can be used as a cache.
        """
        valid_phrases = set()
        with open(phrase_path, 'r') as phrases:
            for phrase in phrases:
                if phrase.strip() != '':
                    valid_phrases.add(phrase.strip())
        return valid_phrases
    
    
    def contains_exact(self, phrase):        
        # Resources always have their first letter as a capital
        for_resource_search = phrase
        if len(for_resource_search) > 1:
            for_resource_search = for_resource_search[0].upper() + for_resource_search[1:]
        
        return not self.use_anchors_only and for_resource_search in self.resource_cache
        
    
    
    def contains_redirect(self, phrase):
        # Resources always have their first letter as a capital
        for_resource_search = phrase
        if len(for_resource_search) > 1:
            for_resource_search = for_resource_search[0].upper() + for_resource_search[1:]
        
        return not self.use_anchors_only and for_resource_search in self.redirect_cache
    
    
    def contains_anchor(self, phrase):
        return phrase in self.anchor_cache 


    def translate(self, phrase):
        return phrase
        