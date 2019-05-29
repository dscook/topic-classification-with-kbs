#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TopicNode:
    """
    Stores details about a topic including its name, parent topic and child topics.
    """
    
    def __init__(self, name, depth):
        """
        :param name: name of the topic node, must be a unique identifier.
        :param depth: the depth of this node in the tree
        :param parent_topics: a list of the parent topic nodes.
        :param child_topics: a list of the child topic nodes.
        """
        self.name = name
        self.depth = depth
        self.parent_topics = set()
        self.child_topics = set()
        
        
    def add_parent_topic(self, topic):
        """
        Adds a parent topic.
        
        :param topic: the parent topic to add.
        """
        self.parent_topics.add(topic)
       

    def add_child_topic(self, topic):
        """
        Adds a child topic.
        
        :param topic: the child topic to add.
        """
        self.child_topics.add(topic)
