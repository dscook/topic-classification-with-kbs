#!/usr/bin/env python
"""
Script adapted from:
Documenting the Now, 2019. twarc [computer program].
Available from: https://github.com/DocNow/twarc [Accessed 23/05/2019].

Given a JSON Lines file, remove any retweets and non-english language tweets.
Also maintains details of the text of tweets seen so far so duplicates not indicated
as retweets can be removed.

Example usage:
./no_retweets_english_only.py tweets.jsonl > tweets_noretweets.jsonl
"""
from __future__ import print_function
import json
import fileinput
import uuid

namespace = uuid.uuid4()
seen_so_far = set()

for line in fileinput.input():
    tweet = json.loads(line)
    
    tweet_id = uuid.uuid3(namespace, tweet['full_text'])
    
    if tweet_id not in seen_so_far:
        seen_so_far.add(tweet_id)

        if (not 'retweeted_status' in tweet and 
            tweet['lang'] == 'en' and
            not tweet['full_text'].startswith('RT @')):
            print(json.dumps(tweet))
