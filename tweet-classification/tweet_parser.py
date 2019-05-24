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
                
                # Extract the tweet
                tweet_text = tweet['full_text']
                
                print(tweet_text)
                print('----')
                
                # Replace mentions with names of people/organisations
                prev_upper_index = 0
                expanded_tweet_text = ''
                
                for user_mention in tweet['entities']['user_mentions']:
                    lower_index = user_mention['indices'][0] + 1
                    expanded_tweet_text += tweet_text[prev_upper_index:lower_index]
                    expanded_tweet_text += user_mention['name']
                    prev_upper_index = user_mention['indices'][1] + 1
                
                expanded_tweet_text += tweet_text[prev_upper_index:]
                
                tweets.append(expanded_tweet_text)
                count += 1
                if count == tweet_limit:
                    break
        
        # Add tweets to dictionary
        tweets_keyed_by_topic[topic_name] = tweets
    
    
    return tweets_keyed_by_topic


tweets_keyed_by_topic = load_data(10, 'data/')

for topic, tweets in tweets_keyed_by_topic.items():
    print('Topic: {}'.format(topic))
    print('')
    for tweet in tweets:
        print('{}'.format(tweet))
        print('-----------------------')
    print('-----------------------')