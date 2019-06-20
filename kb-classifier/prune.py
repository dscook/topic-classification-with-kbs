#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from topic_hierarchy_pruner import TopicHierarchyPruner


def prune(topic, topic_hierarchy):
    num_nodes_accessible = topic_hierarchy.prune_from_root_topic(topic)
    print('{} pruned with {} topics accessible'.format(topic, num_nodes_accessible))


# Reuters RCV1 dataset
#topic_hierarchy = TopicHierarchyPruner(max_depth=5, endpoint_url='http://localhost:3030/DBpedia/')
#prune('Crime', topic_hierarchy)
#prune('Law', topic_hierarchy)
#prune('Business', topic_hierarchy)
#prune('Economics', topic_hierarchy)
#prune('Elections', topic_hierarchy)
#prune('Politics', topic_hierarchy)
#prune('Health', topic_hierarchy)
#prune('Medicine', topic_hierarchy)
#prune('Religion', topic_hierarchy)
#prune('Theology', topic_hierarchy)
#prune('Sports', topic_hierarchy)


# OHSUMED dataset
topic_hierarchy = TopicHierarchyPruner(max_depth=4, endpoint_url='http://localhost:3030/DBpedia/')
prune('Anatomy', topic_hierarchy)
prune('Health', topic_hierarchy)
prune('Diseases_and_disorders', topic_hierarchy)
prune('Deaths_by_cause', topic_hierarchy)
prune('Mammals', topic_hierarchy)

