#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import os
import json

def load_data(tweet_limit, directory):
    """
    Load the tweet data, limiting to the given number of tweets per topic.
    Accepts only English language tweets and rejects duplicates such as retweets.
    
    :param tweet_limit: the maximum number of tweets per topic.
    :param directory: the directory where the tweets are located.
    :returns: a dictionary of tweets keyed by topic.
    """
    tweets_keyed_by_topic = defaultdict(list)
    
    # Obtain the list of topics
    tweet_topics = os.listdir(directory)

    # Load the tweets for each topic
    for topic in tweet_topics:
        tweets = []
        
        topic_name = topic[:-6]
        topic_path = directory + topic
                
        # Process tweets until limit reached
        count = 0
        with open(topic_path) as file:
            for line in file:
                tweet = json.loads(line)
                
                tweets.append(tweet['full_text'])
                count += 1
                if count == tweet_limit:
                    break
        
        # Add tweets to dictionary
        tweets_keyed_by_topic[topic_name] = tweets
    
    
    return tweets_keyed_by_topic


tweets_keyed_by_topic = load_data(100, 'data/')

for topic, tweets in tweets_keyed_by_topic.items():
    print('Topic: {}'.format(topic))
    print('')
    for tweet in tweets:
        print('{}'.format(tweet))
        print('-----------------------')
    print('-----------------------')