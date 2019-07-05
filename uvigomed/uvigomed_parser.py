#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import uuid

from lookup_tables import topic_to_int


# Used for eliminating duplicate news articles
namespace = uuid.uuid4()
seen_so_far = set()


def load_articles(directory, titles_only=False):
    """
    Loads the UVigoMED articles from the given directory.
    
    :param directory: the directory where the UVigoMED articles are located.
    :param titles_only: use the document titles as the documents rather than the abstracts.
    :returns: (x - list of abstracts, y - topic codes)
    """
    x = []
    y = []
    
    articles = os.listdir(directory)

    # Parse each article
    for article in articles:
        
        with open(directory + article, 'r') as file:
            # Some files are empty, ignore them
            try:
                article_dict = json.load(file)
            except:
                continue    # Do not process the file
            
            document = None
            if titles_only:
                document = article_dict['title']
            else:
                document = article_dict['abstract']
            
            article_id = uuid.uuid3(namespace, document)
            
            if article_id not in seen_so_far:
                x.append(document)
                y.append(topic_to_int[article_dict['categories']])
            else:
                seen_so_far.add(article_id)
    
    return (x, y)


def load_data(directory, titles_only=False):
    """
    Loads the UVigoMED dataset.
    
    :param directory: the directory where the UVigoMED articles are located.
    :param titles_only: use the document titles as the documents rather than the abstracts.
    :returns: (train x - list of abstracts, train y - topic codes, test x, test y)
    """
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    
    # Get the training articles
    train_path = directory + 'train/'
    train_x, train_y = load_articles(train_path, titles_only)
    
    # Get the test articles
    test_path = directory + 'test/'
    test_x, test_y = load_articles(test_path, titles_only)
    
    return (train_x, train_y, test_x, test_y)
