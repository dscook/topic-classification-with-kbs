#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

def load_preprocessed_data(path):
    y = []
    x = []

    with open(path, newline='') as csvfile:
        article_reader = csv.reader(csvfile)
        for row in article_reader:
            y.append(int(row[0]))
            x.append(row[1])
    
    return (x, y)