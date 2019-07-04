#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv


class LookupCache:
    """
    Prime a cache of all valid knowledge base phrases to prevent costly DB lookups for phrases that do not exist.
    """

    def __init__(self, resource_path='../kb-classifier/data-mesh/resources.csv'):
        """
        :param resource_path: the path to the CSV file containing 
                              "<case insensitive resource name>, <resource name>" pairs.
        """
        
        # The resources in the MeSH database, specifically terms.
        # Dictionary keyed by lowercase version of the term to the case exact version of the term.
        self.resources = {}
        
        with open(resource_path, newline='') as csvfile:
            resource_reader = csv.reader(csvfile)
            for row in resource_reader:
                self.resources[row[0].strip()] = row[1].strip()


    def contains_exact(self, phrase): 
        """
        Does an exact resource match for the phrase exist.
        
        :param phrase: the phrase to match.
        :returns: True if a resource exists for the phrase.
        """
        return phrase in self.resources
    
    
    def contains_redirect(self, phrase):
        """
        Redirects do not exist in MeSH.
        """
        return False
    
    
    def contains_anchor(self, phrase):
        """
        Anchors do not exist in MeSH.
        """
        return False
    
    
    def translate(self, phrase):
        """
        Convert the lowercased version of the phrase to its exact case version.
        
        :param phrase: lowercase version of the phrase.
        :returns: case exact version of the phrase.
        """
        return self.resources[phrase]