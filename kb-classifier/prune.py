#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from topic_hierarchy_pruner import TopicHierarchyPruner
from kb_common import dao_init, topic_depth, wiki_topics_to_index


def prune(topic, topic_hierarchy_pruner):
    """
    Ensures only hyponym topics to a specified depth are reachable from the given root topic.
    
    :param topic: the root topic to prune from.
    :param topic_hierarchy_pruner: the object that does the pruning.
    """
    num_nodes_accessible = topic_hierarchy_pruner.prune_from_root_topic(topic)
    print('{} pruned with {} topics accessible'.format(topic, num_nodes_accessible))


###
### For every root topic ensure only hyponym topics to a specified depth are reachable
###
topic_hierarchy_pruner = TopicHierarchyPruner(max_depth=topic_depth, dao=dao_init())

for topic in wiki_topics_to_index.keys():
    prune(topic, topic_hierarchy_pruner)
