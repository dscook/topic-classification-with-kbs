#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

literal_matcher = re.compile(r'^<http://dbpedia.org/resource/(.*)>\s<.*>\s<.*>')

# Because we are processing the categories file and a resource can have many categories,
# maintain a set of all resources encountered.
resources = set()
with open ('/Users/danielcook/Development/university/Project/downloads/dbpedia-2016-10/article_categories_en.ttl', 'r') as resource_categories:
    for line in resource_categories:
        match  = literal_matcher.match(line)
        if match:
            underscores_removed = ' '.join(match.group(1).split('_'))
            resources.add(underscores_removed)

# Write out all resources encountered
with open('../data-wiki/resources.txt', 'w') as sanitised_resources:
    for resource in resources:
        sanitised_resources.write(resource + '\n')