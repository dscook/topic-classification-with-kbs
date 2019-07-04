#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

literal_matcher = re.compile(r'.*"(.*)".*')

with open('/Users/danielcook/Development/university/Project/downloads/dbpedia-2016-10/anchors.txt', 'w') as sanitised_anchors:
    with open ('../data/anchor_text_en.ttl', 'r') as anchors:
        for line in anchors:
            
            match  = literal_matcher.match(line)
            if match:
                sanitised_anchors.write(match.group(1) + '\n')
        