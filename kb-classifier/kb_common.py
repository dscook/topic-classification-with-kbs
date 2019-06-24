#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

# Change the below to the dataset in use
#dataset = 'reuters'
dataset = 'mesh'

if dataset == 'reuters':
    from kb_reuters import wiki_topics_to_index, wiki_topics_to_actual_topic, topic_depth, dao_init, lookup_cache_init
elif dataset == 'ohsumed':
    from kb_ohsumed import wiki_topics_to_index, wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init
elif dataset == 'mesh':
    from kb_mesh import wiki_topics_to_index, wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init


def wikipedia_topic_probs_as_array(topic_to_prob):
    probs = np.zeros(shape=len(wiki_topics_to_index.keys()))
    
    for topic, prob in topic_to_prob.items():
        probs[wiki_topics_to_index[topic]] = prob
    
    return probs