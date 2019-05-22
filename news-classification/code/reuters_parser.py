#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def load_data(start_date, end_date, directory, code_to_topic_dict):
    """
    Loads the Reuters RCV1 data between the given date ranges inclusive.
        
    :param start_date: the state date YYYYMMDD.
    :param end_date: the end date YYYYMMDD.
    :param directory: the directory where the news articles are located.
    :param code_to_topic_dict: dictionary of topic codes to names to filter by.
    :returns: a dictionary of news articles keyed by topic.
    """
    articles_keyed_by_topic = defaultdict(list)
    
    start_date_obj = datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.strptime(end_date, '%Y%m%d')
    
    current_date = start_date_obj
        
    while current_date <= end_date_obj:
        date_string = current_date.strftime('%Y%m%d')
        
        # Obtain the news articles for the current date
        date_path = directory + date_string
        articles = os.listdir(date_path)
        
        # Parse each news article
        for article in articles:
            #article = '4933newsML.xml'
            article_path = date_path + '/' + article
            news_element = ET.parse(article_path).getroot()
            
            # Get the article text
            text = ''
            text_element = news_element.find('text')
            for line_element in text_element.iter('p'):
                text += line_element.text
                text += ' '
            
            # Get the article topic
            topic_matches = 0
            topic_match = None
            
            for codes_element in news_element.iter('codes'):
                if codes_element.attrib['class'] == 'bip:topics:1.0':
                    for code_element in codes_element.findall('code'):
                        if code_element.attrib['code'] in code_to_topic_dict.keys():
                            topic_matches += 1
                            topic_match = code_element.attrib['code']
            
            # For now only keep news articles if it matches one topic exactly
            if topic_matches == 1:
                articles_keyed_by_topic[topic_match].append(text)
            
        current_date += timedelta(days=1)
    
    return articles_keyed_by_topic
    