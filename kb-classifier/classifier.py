#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

from sparql_dao import SparqlDao
from graph_structures import TopicNode


class Classifier:


    def __init__(self, sparql_endpoint_url, root_topic_names, max_depth):
        """
       :param endpoint_url: the SPARQL endpoint URL.
       :param root_topic_names: set of the names of the topics we are classifying.
       :param max_depth: the maximum depth we are permitted to traverse upwards from the leaf nodes.
        """
        self.dao = SparqlDao(sparql_endpoint_url)
        self.root_topic_names = root_topic_names
        self.max_depth = max_depth
        self.topic_name_to_node = {}    # Cache of topics so we can avoid costly DB lookups
            
        
    def identify_topic_probabilities(self, text):
        """
        Given a text identifies the topic probabilities.
        It is assumed the text has had stopwords removed and can be tokenised by splitting on
        whitespace.
        
        :param text: the text to identify the topic probabilities for.
        :returns: a dict containing topic name to topic probability.
        """
        topic_to_prob_dict = {}
        
        phrase_to_topic_dict = self.identify_leaf_topics(text)
        
        # Materialise the reachable topic hierarchy        
        for phrase, topics in phrase_to_topic_dict.items():
            for topic_name in topics:
                self.populate_topic_name_to_node(self.topic_name_to_node, topic_name)
        
        # Determine the vote for each leaf node
        
        return topic_to_prob_dict
        
        
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
    
    
    def populate_topic_name_to_node(self, topic_name_to_node, topic_name):
        """        
        Populates topic_name_to_node dict with all reachable topics from the given topic name.
        
        :param topic_name_to_node: the dictionary of topic names to their graph nodes.
        :param topic_name: the topic name to lookup.
        """        
        # If we have already seen the topic no action is required
        if topic_name not in topic_name_to_node:
            
            # Haven't seen the topic yet, create it
            topic_node = TopicNode(topic_name, 0)
            topic_name_to_node[topic_name] = topic_node
            
            # We need to explore upwards from this topic
            to_process = deque([])
            to_process.append(topic_node)
            
            while to_process:
                
                # Get all parents of the topic at the front of the queue
                topic = to_process.pop()
                
                # Ensure we do not progress any further up the topic hierachy than the root topics
                if topic.name not in self.root_topic_names:
                
                    # No need to make database call if we already know the parent topics
                    parent_topic_names = None
                    
                    if topic.parent_topics:
                        parent_topic_names = [parent.name for parent in topic.parent_topics]
                    else:
                        parent_topic_names = self.dao.get_parent_topics(topic.name)
                    
                    # Process each parent topic
                    for parent_topic_name in parent_topic_names:

                        parent_topic = None
                        parent_topic_depth = topic.depth+1
                    
                        # Check if parent topic has already been discovered
                        if parent_topic_name not in topic_name_to_node:
                            parent_topic = TopicNode(parent_topic_name, parent_topic_depth)
                            topic_name_to_node[parent_topic_name] = parent_topic
                            
                            # Only get topic's parent if we haven't exceeded the max depth
                            if parent_topic_depth < self.max_depth:
                                to_process.append(parent_topic)
                        else:
                            parent_topic = topic_name_to_node[parent_topic_name]
                            
                            # We may need to process the parent topic if we've encountered it at a lower level
                            if parent_topic_depth < self.max_depth and parent_topic_depth < parent_topic.depth:
                                parent_topic.depth = parent_topic_depth
                                to_process.append(parent_topic)
                            
                        # Let the topic know it has another parent
                        topic.add_parent_topic(parent_topic)
