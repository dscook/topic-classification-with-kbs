#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

# Change the below to the dataset-knowledge base combination in use
#dataset = 'rcv1_wiki'                    # RCV1 using a DBpedia knowledge base
#dataset = 'uvigomed_wiki'                # UVigoMED using a DBpedia knowledge base
dataset = 'uvigomed_mesh'                # UVigoMED using a MeSH knowledge base

if dataset == 'rcv1_wiki':
    from kb_rcv1_wiki import wiki_topics_to_index, wiki_topics_to_actual_topic, topic_depth, dao_init, lookup_cache_init
elif dataset == 'uvigomed_wiki':
    from kb_uvigomed_wiki import wiki_topics_to_index, wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init
elif dataset == 'uvigomed_mesh':
    from kb_mesh import wiki_topics_to_index, wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init


def wikipedia_topic_probs_as_array(topic_to_prob):
    """
    Converts root wikipedia topic probabilities represented as a dict of topic to probability to an array
    representation.
    
    :param topic_to_prob: dict of root topic to probability.
    :returns: numpy array representation of root topic probabilities.
    """
    probs = np.zeros(shape=len(wiki_topics_to_index.keys()))
    
    for topic, prob in topic_to_prob.items():
        probs[wiki_topics_to_index[topic]] = prob
    
    return probs