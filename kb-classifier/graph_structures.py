#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy

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
        self.vote = 0
        self.steps_left = 0
        self.filtered_parents = {}
        
        
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
    
    
    def __deepcopy__(self, memodict={}):
        new_instance = TopicNode(self.name, self.depth)
        new_instance.__dict__.update(self.__dict__)
        
        new_instance.name = copy.deepcopy(self.name, memodict)
        new_instance.depth = copy.deepcopy(self.depth, memodict)
        new_instance.parent_topics = self.parent_topics
        new_instance.child_topics = self.child_topics
        new_instance.vote = copy.deepcopy(self.vote, memodict)
        new_instance.steps_left = copy.deepcopy(self.steps_left, memodict)
        
        return new_instance