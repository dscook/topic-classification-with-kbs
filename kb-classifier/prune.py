#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from topic_hierarchy_pruner import TopicHierarchyPruner


topic_hierarchy = TopicHierarchyPruner(max_depth=5, endpoint_url='http://localhost:3030/DBpedia/')
topic_hierarchy.prune_from_root_topic('Crime')
topic_hierarchy.prune_from_root_topic('Law')
topic_hierarchy.prune_from_root_topic('Business')
topic_hierarchy.prune_from_root_topic('Economics')
topic_hierarchy.prune_from_root_topic('Elections')
topic_hierarchy.prune_from_root_topic('Politics')
topic_hierarchy.prune_from_root_topic('Health')
topic_hierarchy.prune_from_root_topic('Medicine')
topic_hierarchy.prune_from_root_topic('Religion')
topic_hierarchy.prune_from_root_topic('Theology')
topic_hierarchy.prune_from_root_topic('Sports')
