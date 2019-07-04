#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

literal_matcher = re.compile(r'^<http://dbpedia.org/resource/(.*)>\s<.*>\s<.*>')

resources = set()
with open ('/Users/danielcook/Development/university/Project/downloads/dbpedia-2016-10/redirects_en.ttl', 'r') as redirect_resources:
    for line in redirect_resources:
        match  = literal_matcher.match(line)
        # Ensure hierarchical URLs are not processed
        if match and '/' not in match.group(1):
            underscores_removed = ' '.join(match.group(1).split('_'))
            resources.add(underscores_removed)

# Write out all resources encountered
with open('../data-wiki/redirect_resources.txt', 'w') as sanitised_resources:
    for resource in resources:
        sanitised_resources.write(resource + '\n')