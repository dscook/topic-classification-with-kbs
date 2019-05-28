#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

from sparql_dao import SparqlDao
from graph_structures import TopicNode

class TopicHierarchyPruner:
    """
    Initialises and provides methods to access the topic hierarchy.
    """
    
    def __init__(self, max_depth, endpoint_url):
        """
        :param max_depth: the maximum depth of the topic tree to keep from the root node.
        :param endpoint_url: the SPARQL endpoint URL.
        """
        self.max_depth = max_depth
        self.dao = SparqlDao(endpoint_url)
        
    
    def prune_from_root_topic(self, root_topic_name):
        """
        Mark only child topics as accessible from the given root topic.
        
        :param root_topic_name: the root topic name.
        """
        # Keep a topic name to topic node mapping table for easy access of topics
        topic_dict = {}
    
        # Starting from the root topic perform a breadth first search to get the entire topic hierarchy
        root_topic = TopicNode(root_topic_name, 0)
        topic_dict[root_topic_name] = root_topic
        
        to_process = deque([])
        to_process.append(root_topic)
        
        while to_process:
                        
            # Get all child topics of this topic
            parent_topic = to_process.pop()
            child_topic_names = self.dao.get_child_topics(parent_topic.name)
            
            # Process each child topic
            for child_topic_name in child_topic_names:
                
                child_topic = None
                
                # Check if child topic has already been discovered
                if child_topic_name not in topic_dict:
                    child_topic_depth = parent_topic.depth+1
                    child_topic = TopicNode(child_topic_name, child_topic_depth, set([parent_topic]))
                    topic_dict[child_topic_name] = child_topic
                    
                    # Only get child topic's children if we haven't exceeded the max depth
                    if child_topic_depth < self.max_depth:
                        to_process.append(child_topic)
                    
                else:
                    # Child topic has already been discovered but we still need to add a parent
                    child_topic = topic_dict[child_topic_name]
                    child_topic.add_parent_topic(parent_topic)
                
                # Let the parent know it has another child
                parent_topic.add_child_topic(child_topic)
            
            print('Visited {}'.format(parent_topic.name))
        
        # Iterate through reached topics marking as accessible
        for _, topic in topic_dict.items():
            self.dao.mark_as_accessible(topic.name)
            print('Marked {}'.format(parent_topic.name))
    
    
        