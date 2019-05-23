#!/bin/bash

head -10000 ../../../downloads/tweets/brexit/tweets.jsonl > data/brexit.jsonl
head -10000 ../../../downloads/tweets/climate_change/tweets.jsonl > data/climate_change.jsonl
head -10000 ../../../downloads/tweets/fake_news/tweets.jsonl > data/fake_news.jsonl
head -10000 ../../../downloads/tweets/gaza/tweets.jsonl > data/gaza.jsonl
head -10000 ../../../downloads/tweets/hurricane_harvey/tweets.jsonl > data/hurricane_harvey.jsonl
head -10000 ../../../downloads/tweets/winter_olympics/tweets.jsonl > data/winter_olympics.jsonl
