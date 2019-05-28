#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from topic_hierarchy_pruner import TopicHierarchyPruner


topic_hierarchy = TopicHierarchyPruner(max_depth=5, endpoint_url='http://localhost:3030/DBpedia/')
topic_hierarchy.prune_from_root_topic('Sports')