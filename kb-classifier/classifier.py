#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sparql_dao import SparqlDao


class Classifier:


    def __init__(self, sparql_endpoint_url):
        """
       :param endpoint_url: the SPARQL endpoint URL.
        """
        self.dao = SparqlDao(sparql_endpoint_url)
            
        
    def identify_leaf_topics(self, text):
        """
        Given a text returns a dictionary keyed by phrase with value of the corresponding topic
        matches at the bottom of the topic hierarchy.
        It is assumed the text has had stopwords removed and can be tokenised by splitting on
        whitespace.
        The method attempts to match a 3 word phrase, if this fails then 2 word phrase down to 1.
        Once a match is achieved the words are consumed.
        
        :param text: the text to find leaf topics for.
        :returns: the dictionary of leaf topic matches.
        """
        phrase_to_topic_matches = {}
        
        tokens = text.split()
        
        # Maintain the start of the phrase we are processing
        index = 0
        
        # Initially consider a phrase of word length 3
        phrase_length = 3
        
        while index < len(tokens):
            
            # Check the phrase length doesn't exceed the end of the string
            while index + phrase_length > len(tokens):
                phrase_length -= 1
            
            # Try and find a match for 3 word phrase, then 2 then 1
            topics = []
            while phrase_length > 0:
                # Check to see if we can obtain topics for the phrase
                phrase = ' '.join(tokens[index:index+phrase_length])
                topics = self.identify_topics(phrase)
                
                # Found topics, no need to look for smaller word n-gram matches
                if topics:
                    phrase_to_topic_matches[phrase] = topics
                    break
            
                phrase_length -= 1
            
            # Cover the case where we couldn't find a topics match
            if phrase_length == 0:
                phrase_length = 1
                
            # We have a match, consume the phrase
            index += phrase_length
            
            # Reset phrase length for processing next index
            phrase_length = 3
        
        return phrase_to_topic_matches
                
            
    def identify_topics(self, phrase):
        """
        Given a phrase, looks up the phrase in the ontology to determine its immediate topics.
        
        :param phrase: the phrase to lookup
        """
        # Get the the list of topic names for the phrase
        return self.dao.get_topics_for_phrase(phrase)