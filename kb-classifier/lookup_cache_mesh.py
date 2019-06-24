#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv


class LookupCache:

    
    def __init__(self, resource_path='../kb-classifier/data-mesh/resources.csv'):
        
        # The resources in the MeSH database, specifically terms.
        # Dictionary keyed by lowercase version of the term to the case exact version of the term.
        self.resources = {}
        
        with open(resource_path, newline='') as csvfile:
            resource_reader = csv.reader(csvfile)
            for row in resource_reader:
                self.resources[row[0].strip()] = row[1].strip()


    def contains_exact(self, phrase): 
        return phrase in self.resources
    
    
    def contains_redirect(self, phrase):
        return False
    
    
    def contains_anchor(self, phrase):
        return False
    
    
    def translate(self, phrase):
        return self.resources[phrase]