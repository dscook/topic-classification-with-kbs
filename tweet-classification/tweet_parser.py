#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import os
import json
import re


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
                                
                # Replace mentions with names of people/organisations
                prev_upper_index = 0
                expanded_tweet_text = ''
                
                for user_mention in tweet['entities']['user_mentions']:
                    lower_index = user_mention['indices'][0]
                    expanded_tweet_text += tweet_text[prev_upper_index:lower_index]
                    expanded_tweet_text += user_mention['name']
                    prev_upper_index = user_mention['indices'][1]
                
                expanded_tweet_text += tweet_text[prev_upper_index:]
                
                tweets.append(expanded_tweet_text)
                count += 1
                if count == tweet_limit:
                    break
        
        # Add tweets to dictionary
        tweets_keyed_by_topic[topic_name] = tweets
    
    
    return tweets_keyed_by_topic


def create_topic_hashtags_dict(directory):
    """
    Create a dictionary of topic names to the list of hashtags that were used to find tweets from that topic.
    
    :param: directory: the path of a directory containing a file per topic, with each file containing
                       a hashtag per line.
    :returns: a dictionary of hashtag lists keyed by topic.
    """
    topic_hashtags_dict = {}
    
    hashtag_lists = os.listdir(directory)
    
    for hashtag_list in hashtag_lists:
        hashtag_list_path = directory + hashtag_list
        with open(hashtag_list_path) as file:
            hashtags = []
            for line in file:
                hashtags.append(line.strip())
        topic_hashtags_dict[hashtag_list] = hashtags
    
    return topic_hashtags_dict
            


def cleanup_tweets(tweets_keyed_by_topic, topic_hashtags_dict):
    """
    Given a dictionary of lists of tweets keyed by topic, cleans up the tweet text as follows:
        * Removed hashtags that were used to find the tweets as these are topic tags.
        * Remove any URLs present in the tweet as these add no value unless they are resolved and summarised.
        * Remove any sequence of hashtags at the end of the tweet as these are effectively topic tags.
        * For remaining hashtags, remove hash and split into words when camel case or separated by underscores.
        
    :param: tweets_keyed_by_topic: dictionary of topics to their list of tweets.
    :param: topic_hashtags_dict: a dictionary of hashtag lists keyed by topic.
    :returns: cleaned up version of tweets_keyed_by_topic.
    """
    cleaned_tweets_keyed_by_topic = {}
    
    # To match URLs in tweets
    url_matcher = re.compile(r'(www|http:|https:)[^\s]+')
    
    # To match camel case words
    camel_matcher = re.compile(r'(?<![A-Z])([A-Z][a-z]+)')
    
    for topic, tweets in tweets_keyed_by_topic.items():
        
        # Process each tweet separately
        processed_tweets = []
        for tweet in tweets:
            
            # Remove hashtags used to find tweets, these are topic indicators
            hashtags_to_remove = topic_hashtags_dict[topic]
            for hashtag in hashtags_to_remove:
                tweet = tweet.replace(hashtag, '')
            
            # Remove URLs present in the tweet
            tweet = url_matcher.sub('', tweet)
            
            # Remove hashtags at end of the tweet as these are effectively topic tags
            tweet_split = tweet.split()
            keep_until = len(tweet_split)
            for i in range(len(tweet_split)-1, -1, -1):
                if not tweet_split[i].startswith('#'):
                    break
                keep_until = i
                
            tweet_split = tweet_split[:keep_until]
            
            # For remaining hashtags, remove hash and split into words when camel case
            # or separated by underscores.
            for i in range(len(tweet_split)):
                if tweet_split[i].startswith('#'):
                    tweet_split[i] = tweet_split[i][1:]
                    
                    # Check for snake case
                    if len(tweet_split[i].split('_')) > 1:
                        tweet_split = tweet_split[:i] + tweet_split[i].split('_') + tweet_split[i+1:]
                    else:    # Check for camel case
                        tweet_split = (tweet_split[:i] + 
                                       camel_matcher.sub(r' \1', tweet_split[i]).split() + 
                                       tweet_split[i+1:])
            
            # Reform tweet string now processing is complete
            tweet = ' '.join(tweet_split)
            processed_tweets.append(tweet)
        
        cleaned_tweets_keyed_by_topic[topic] = processed_tweets
    
    return cleaned_tweets_keyed_by_topic
