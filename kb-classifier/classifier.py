#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cachetools import cached, LFUCache
from collections import deque, defaultdict
import copy
import numpy as np

from graph_structures import TopicNode


phrase_to_resource_cache = LFUCache(maxsize=100000)
phrase_to_resource_from_redirect_cache = LFUCache(maxsize=100000)
phrase_to_resources_from_anchor_cache = LFUCache(maxsize=1000000)
resource_to_topics_cache = LFUCache(maxsize=1000000)

class Classifier:


    def __init__(self, dao, root_topic_names, max_depth, phrase_cache):
        """
       :param root_topic_names: set of the names of the topics we are classifying.
       :param max_depth: the maximum depth we are permitted to traverse upwards from the leaf nodes.
        """
        self.dao = dao
        self.root_topic_names = root_topic_names
        self.max_depth = max_depth
        self.phrase_cache = phrase_cache
        self.topic_name_to_node = {}    # Cache of topics so we can avoid costly DB lookups
        # Below is so we can maintain an integer identifier to topic name mapping for generating word embeddings
        self.topic_id = 0
        self.topic_name_to_id = {}
        # Will be initialised if TFIDF is used
        self.tfidf = None
        print('Classifier Initialised')
    
    
    def identify_topic_probabilities(self, text):
        """
        Given a text identifies the topic probabilities.
        It is assumed the text has had stopwords removed and can be tokenised by splitting on
        whitespace.
        
        :param text: the text to identify the topic probabilities for.
        :returns: a dict containing topic name to topic probability.
        """
        # Get the resources associated with the phrases
        phrase_to_resources, phrase_to_occurences = self.identify_leaf_nodes(text)
        
        # Calculate document length based on the number of matching phrases
        document_length = 0
        for count in phrase_to_occurences.values():
            document_length += count
        
        # Get the topics associated with the resources
        resource_to_topics = {}
        for resources in phrase_to_resources.values():
            for resource in resources:
                resource_to_topics[resource] = self.identify_topics(resource)
                                
        # Materialise the reachable topic hierarchy        
        for topics in resource_to_topics.values():
            for topic_name in topics:
                self.populate_topic_name_to_node(self.topic_name_to_node, topic_name)
        
        # Reset the vote to 0 for each topic node
        for topic in self.topic_name_to_node.values():
            topic.vote = 0
            topic.transferring_vote = 0
            
        # Maintain graph that was traversed so we can later obtain the probability tree
        self.traversed_nodes = {}
        
        # Initialise the votes
        for phrase, resources in phrase_to_resources.items():
            
            phrase_leaf = self.get_or_add_topic_to_cache('Phrase:' + phrase, self.traversed_nodes, depth=0)
            phrase_leaf.upwards_vote = phrase_to_occurences[phrase]
            
            # Note the phrase has a higher starting vote if it occurs multiple times in the document
            # Split the vote amongst the phrases resources
            split_vote = phrase_to_occurences[phrase] / len(resources)
            
            if self.tfidf:
                # We have the TF-IDF module so we can use TFIDF instead as the starting vote
                split_vote = (self.tfidf.calculate_tfidf(phrase, 
                                                         phrase_to_occurences[phrase], 
                                                         document_length) / len(resources))
            
            # Now allocate each resources vote amongst its topics
            for resource in resources:
                topics = resource_to_topics[resource]
                split_vote_among_topics = split_vote / len(topics)
                
                for topic in topics:
                    self.topic_name_to_node[topic].vote += split_vote_among_topics
                    
                    traversed_topic = self.get_or_add_topic_to_cache(topic, self.traversed_nodes, depth=1)
                    traversed_topic.upwards_vote += split_vote_among_topics
                    traversed_topic.add_child_topic(phrase_leaf)
        
        # Transfer each node's vote evenly across its parents
        for i in range(self.max_depth):
                        
            for topic in self.topic_name_to_node.values():
                # Check we haven't reached a terminal node and if there is vote to transfer
                if topic.vote > 0 and len(topic.parent_topics) > 0:
                    
                    filtered_parents = []
                    if i in topic.filtered_parents:
                        filtered_parents = topic.filtered_parents[i]
                    else:
                        # Determine what parent topics are valid.
                        # A parent topic is not valid if there is no route from that topic to a root node
                        # within the remaining advances up the topic tree.
                        filtered_parents = self.remove_parents_where_no_path_to_root(
                                topic.parent_topics, steps_left=self.max_depth-i)
                        topic.filtered_parents[i] = filtered_parents
                    
                    if len(filtered_parents) == 0:
                        raise Exception('Implementation error: there should be a valid path to a root topic.')
                    
                    vote = topic.vote
                    topic.vote = 0
                    split_vote = vote / len(filtered_parents)
                    for parent_topic in filtered_parents:
                        parent_topic.transferring_vote += split_vote
                        traversed_topic = self.get_or_add_topic_to_cache(parent_topic.name, self.traversed_nodes, depth=2+i)
                        traversed_topic.upwards_vote += split_vote
                        traversed_topic.add_child_topic(self.traversed_nodes[1+i][topic.name])
            
            for topic in self.topic_name_to_node.values():
                topic.vote += topic.transferring_vote
                topic.transferring_vote = 0
                        
        
        # Return the root topic probabilities
        total_votes = 0
        topic_to_prob_dict = {}
        
        for root_topic in self.root_topic_names:
            if root_topic in self.topic_name_to_node:
                vote = self.topic_name_to_node[root_topic].vote
                topic_to_prob_dict[root_topic] = vote
                total_votes += vote
            else:
                topic_to_prob_dict[root_topic] = 0
            
        # Normalise the votes to turn into probabilities
        if total_votes == 0:
            return None
            
        for root_topic in self.root_topic_names:
            topic_to_prob_dict[root_topic] /= total_votes
            
        # Store the probabilities in case the user wants a breakdown of how each child topic / phrase contributed
        self.last_topic_to_prob_dict = topic_to_prob_dict
        
        return topic_to_prob_dict
        
    
    def identify_leaf_nodes(self, text):
        """
        Given a text returns a dictionary keyed by phrase with the value of the corresponding
        resource matches in DBpedia.
        It is assumed the text has had stopwords removed and can be tokenised by splitting on
        whitespace.
        The method attempts to match a 3 word phrase, if this fails then 2 word phrase down to 1.
        Once a match is achieved the words are consumed.
        
        The algorithm will first attempt to match the phrase directly with a DBpedia resource,
        if this succeeds this node only will be returned.
        If this fails then all matching resources that use the same anchor text as the phrase will be matched.
        
        :param text: the text to find leaf nodes for.
        :returns: tuple (dictionary of phrase to leaf node (resource) matches, 
                         dictionary of phrase to number of occurences in document)
        """
        phrase_to_node_matches = {}
        phrase_to_occurences = defaultdict(int)
        
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
            while phrase_length > 0:
                # Check to see if we can obtain topics for the phrase
                updated_tokens= []
                for token in tokens[index:index+phrase_length]:
                    updated_tokens.extend(token.split('_'))
                
                phrase = ' '.join(updated_tokens)
                
                nodes = None
                                
                # Look for exact phrase match
                if self.phrase_cache.contains_exact(phrase):
                    print('Getting exact match for: {}'.format(phrase))
                    node = self.get_resource(phrase)
                    if node:
                        nodes = [node]
                        print('Found')
                
                # Look for redirect exact match
                if nodes is None and self.phrase_cache.contains_redirect(phrase):
                    print('Getting redirect for: {}'.format(phrase))
                    node = self.get_resource_from_redirect(phrase)
                    if node:
                        nodes = [node]
                        print('Found')
                
                # Oherwise look for anchor text matches
                if nodes is None and self.phrase_cache.contains_anchor(phrase):
                    nodes = self.get_resources_from_anchor(phrase)
                
                # Found nodes, no need to look for smaller word n-gram matches
                if nodes:
                    phrase_to_node_matches[phrase] = nodes
                    phrase_to_occurences[phrase] += 1
                    break
            
                phrase_length -= 1
            
            # Cover the case where we couldn't find a topics match
            if phrase_length == 0:
                phrase_length = 1
                
            # We have a match, consume the phrase
            index += phrase_length
            
            # Reset phrase length for processing next index
            phrase_length = 3
        
        return phrase_to_node_matches, phrase_to_occurences
    

    @cached(resource_to_topics_cache)
    def identify_topics(self, resource):
        """
        Given a resource, looks up the resource in the ontology to determine its immediate topics.
        
        :param resource: the resource to lookup
        """
        # Get the the list of topic names for the resource
        return self.dao.get_topics_for_resource(resource)
    
    
    @cached(phrase_to_resource_cache)
    def get_resource(self, phrase):
        """
        Given a phrase, looks up the corresponding resource node for the phrase.
        
        :param phrase: the phrase to lookup
        :returns: the name of the resource for the phrase.
        """
        resource = self.dao.get_resource_for_phrase(phrase)
        return self.dao.filter_undesired_types(resource)


    @cached(phrase_to_resource_from_redirect_cache)
    def get_resource_from_redirect(self, phrase):
        """
        Given a phrase, looks up the corresponding resource node for the phrase from a redirect link.
        
        :param phrase: the phrase to lookup
        :returns: the name of the resource for the phrase.
        """
        resource = self.dao.get_resource_for_phrase_from_redirect(phrase)
        return self.dao.filter_undesired_types(resource)


    @cached(phrase_to_resources_from_anchor_cache)
    def get_resources_from_anchor(self, phrase):
        """
        Given a phrase, looks up the corresponding resource nodes that hyperlinks have linked
        to using the phrase as the link text.
        
        :param phrase: the phrase to lookup
        :returns: the name of the resources for the phrase.
        """
        return self.dao.get_resources_for_phrase_from_anchor(phrase)


    def get_topic_probabilities(self, depth):
        depths = sorted(self.traversed_nodes.keys(), reverse=True)
        depth_to_return = None
        if depth == -1:
            depth_to_return = depths[-1]
        else:
            depth_to_return = depths[0] - depth
            if depth_to_return < 0:
                depth_to_return = 0
        
        total_vote = 0
        for topic in self.traversed_nodes[depth_to_return].values():
            total_vote += topic.upwards_vote
        
        topic_probabilities = {}
        for topic_name, topic in self.traversed_nodes[depth_to_return].items():
            topic_probabilities[topic_name] = topic.upwards_vote / total_vote
        
        return topic_probabilities
    
    
    def get_all_topic_probabilities(self):
        topic_probabilities = defaultdict(list)
        
        tree_depth = np.max(list(self.traversed_nodes.keys())) + 1
        
        # Do not return the phrase probabilities by default
        for i in range(1, tree_depth):
                        
            total_vote = 0
            for topic in self.traversed_nodes[i].values():
                total_vote += topic.upwards_vote

            for topic_name, topic in self.traversed_nodes[i].items():
                topic_probabilities[topic_name].append(topic.upwards_vote / total_vote)
        
        max_topic_probabilities = {}
        
        for topic_name, probabilities in topic_probabilities.items():
            max_topic_probabilities[topic_name] = np.max(probabilities)
        
        return max_topic_probabilities
    
    
    def populate_topic_name_to_node(self, topic_name_to_node, topic_name):
        """        
        Populates topic_name_to_node dict with all reachable topics from the given topic name.
        
        :param topic_name_to_node: the dictionary of topic names to their graph nodes.
        :param topic_name: the topic name to lookup.
        """        
        # If we have already seen the topic no action is required unless it didn't occur
        # as a leaf node
        if topic_name not in topic_name_to_node or topic_name_to_node[topic_name].depth != 0:
            
            topic_node = None
            
            if topic_name in topic_name_to_node:
                topic_node = topic_name_to_node[topic_name]
                topic_node.depth = 0
            else:
                # Haven't seen the topic yet, create it
                topic_node = TopicNode(topic_name, 0)
                topic_name_to_node[topic_name] = topic_node
                
                # Update the topic name ID lookup table
                self.topic_name_to_id[topic_name] = self.topic_id
                self.topic_id += 1
            
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
                            
                            # Update the topic name ID lookup table
                            self.topic_name_to_id[parent_topic_name] = self.topic_id
                            self.topic_id += 1
                            
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


    def remove_parents_where_no_path_to_root(self, parent_topics, steps_left):
        
        filtered_parents = []
        
        for parent_topic in parent_topics:
            
            # We need to explore upwards from this topic
            copied_parent_topic = copy.deepcopy(parent_topic)
            copied_parent_topic.steps_left = steps_left
            to_process = deque([])
            to_process.append(copied_parent_topic)
            
            while to_process:
                
                # Get all parents of the topic at the front of the queue
                topic = to_process.pop()
                
                # if we have found a root topic then the parent_topic is on a valid path
                if topic.name in self.root_topic_names:
                    filtered_parents.append(parent_topic)
                    break
                            
                # Process each parent topic
                for ptopic in topic.parent_topics:
                    
                    # If we still have steps left, keep going
                    copied_ptopic = copy.deepcopy(ptopic)
                    copied_ptopic.steps_left = topic.steps_left - 1
                    
                    if copied_ptopic.steps_left > 0:
                        to_process.append(copied_ptopic)
            
        return filtered_parents
    
    
    def get_or_add_topic_to_cache(self, topic_name, cache, depth):
        
        if depth not in cache:
            cache[depth] = {}
        
        topic = None
        if topic_name in cache[depth]:
            topic = cache[depth][topic_name]
        else:
            topic = TopicNode(topic_name, depth=None)
            
            topic.upwards_vote = 0
            # For root nodes that appear at many levels of the topic tree transfer their vote
            if topic.name in self.root_topic_names and depth > 0:
                for i in range(depth-1,-1,-1):
                    if topic.name in cache[i]:
                        topic.upwards_vote = cache[i][topic_name].upwards_vote
                        break
            
            cache[depth][topic_name] = topic
        
        return topic
            
