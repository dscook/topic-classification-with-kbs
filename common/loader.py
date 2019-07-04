#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

def load_preprocessed_data(path):
    """
    Loads already lemmatised/lowercased/stopwords removed data.
    Data is expected to be in CSV format, each line like: "<TOPIC CLASS INDEX>,<ARTICLE>"
    
    :param path: the path to the data to load.
    :returns: (array of articles, array of the article topic class indexes).
    """
    y = []
    x = []

    with open(path, newline='') as csvfile:
        article_reader = csv.reader(csvfile)
        for row in article_reader:
            y.append(int(row[0]))
            x.append(row[1])
    
    return (x, y)