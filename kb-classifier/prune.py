#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from topic_hierarchy_pruner import TopicHierarchyPruner
from kb_common import dao_init, topic_depth, wiki_topics_to_index


def prune(topic, topic_hierarchy_pruner):
    num_nodes_accessible = topic_hierarchy_pruner.prune_from_root_topic(topic)
    print('{} pruned with {} topics accessible'.format(topic, num_nodes_accessible))


topic_hierarchy_pruner = TopicHierarchyPruner(max_depth=topic_depth, dao=dao_init())

for topic in wiki_topics_to_index.keys():
    prune(topic, topic_hierarchy_pruner)
