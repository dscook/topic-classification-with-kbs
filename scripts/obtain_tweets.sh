#!/bin/bash

##
## This script rehydrates tweets from https://www.docnow.io/.
## Twarc must be installed, see https://github.com/DocNow/twarc.
##

echo "Obtaining Brexit tweets"
twarc hydrate brexit/million_ids.txt > brexit/tweets.jsonl

echo "Obtaining Climate Change tweets"
twarc hydrate climate_change/million_ids.txt > climate_change/tweets.jsonl

echo "Obtaining Fake News tweets"
twarc hydrate fake_news/million_ids.txt > fake_news/tweets.jsonl

echo "Obtaining Gaza tweets"
twarc hydrate gaza/million_ids.txt > gaza/tweets.jsonl

echo "Obtaining Hurricane Harvey tweets"
twarc hydrate hurricane_harvey/million_ids.txt > hurricane_harvey/tweets.jsonl

echo "Obtaining Winter Olympics tweets"
twarc hydrate winter_olympics/million_ids.txt > winter_olympics/tweets.jsonl
