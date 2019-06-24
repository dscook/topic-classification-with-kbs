#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import csv

literal_matcher = re.compile(r'^<.*>\s<http://id\.nlm\.nih\.gov/mesh/vocab#(prefLabel|altLabel)>\s"(.*)"@en \.$')

resources = set()
with open ('/Users/danielcook/Development/university/Project/downloads/MeSH/mesh2019.nt', 'r') as medline_triples:
    for line in medline_triples:
        match  = literal_matcher.match(line)
        if match:
            resources.add(match.group(2))

# Write out all resources encountered
with open('../data-mesh/resources.csv', 'w') as resources_csv:
    resource_writer = csv.writer(resources_csv)
    for resource in resources:
        resource_writer.writerow([resource.lower(), resource])
