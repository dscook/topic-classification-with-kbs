#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

from sparql_dao import SparqlDao
from graph_structures import TopicNode

class TopicHierarchy:
    """
    Initialises and provides methods to access the topic hierarchy.
    """
    
    def __init__(self):
        self.dao = SparqlDao('http://localhost:3030/DBpedia/query')
        
        # Keep a topic name to topic node mapping table for easy access of topics
        self.topic_dict = {}
    
        # Starting from the root topic perform a breadth first search to get the entire topic hierarchy
        root_topic_name = 'Sports'
        root_topic = TopicNode(root_topic_name, 0)
        self.topic_dict[root_topic_name] = root_topic
        
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
                if child_topic_name not in self.topic_dict:
                    child_topic_depth = parent_topic.depth+1
                    child_topic = TopicNode(child_topic_name, child_topic_depth, set([parent_topic]))
                    self.topic_dict[child_topic_name] = child_topic
                    
                    # Only get child topic's children if we haven't exceeded the max depth
                    if child_topic_depth < 5:
                        to_process.append(child_topic)
                    
                else:
                    # Child topic has already been discovered but we still need to add a parent
                    child_topic = self.topic_dict[child_topic_name]
                    child_topic.add_parent_topic(parent_topic)
                
                # Let the parent know it has another child
                parent_topic.add_child_topic(child_topic)
            
            print('Processed {}'.format(parent_topic.name))
    
    
        