#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cachetools import cached, LFUCache
from flask import Flask, request, jsonify
import uuid

from embedding_algorithm import EmbeddingAlgorithm
from kb_common import wiki_topics_to_actual_topics, topic_depth, dao_init, lookup_cache_init


# Used for generating document IDs
namespace = uuid.uuid4()
last_doc_id = None
doc_id_to_text = {}
doc_id_to_topic_prob_cache = LFUCache(maxsize=100000)
doc_id_to_depth_prob_cache = LFUCache(maxsize=100000)
doc_id_to_all_prob_cache = LFUCache(maxsize=100000)

app = Flask(__name__)
embedder = EmbeddingAlgorithm(dao=dao_init(),
                              root_topic_names=wiki_topics_to_actual_topics.keys(),
                              max_depth=topic_depth,
                              phrase_cache=lookup_cache_init())


@app.route('/classify', methods=['POST'])
def classify():
    """
    Get the root topic probabilities for the POSTed document.
    """
    body = request.get_json()
    document = body['text']
    
    global last_doc_id
    last_doc_id = uuid.uuid3(namespace, document)
    
    global doc_id_to_text
    if last_doc_id not in doc_id_to_text:
        doc_id_to_text[last_doc_id] = document
    
    return identify_topic_probabilities(last_doc_id)


@app.route('/probabilities/<depth>', methods=['GET'])
def probabilities(depth):
    """
    Get the topic probabilities for the last classified example at the specified depth
    of the topic tree.  0 = root topics, 1 = next level and so on.
    """
    if depth == 'all':
        return get_all_topic_probabilities(last_doc_id)
    else:
        return get_topic_probabilities(last_doc_id, int(depth))


@cached(doc_id_to_topic_prob_cache)
def identify_topic_probabilities(doc_id):
    topic_to_prob = embedder.identify_topic_probabilities(doc_id_to_text[doc_id])
    return jsonify(topic_to_prob)


@cached(doc_id_to_depth_prob_cache)
def get_topic_probabilities(doc_id, depth):
    probabilities = embedder.get_topic_probabilities(depth)
    return jsonify(probabilities)


@cached(doc_id_to_all_prob_cache)
def get_all_topic_probabilities(doc_id):
    probabilities = embedder.get_all_topic_probabilities()
    return jsonify(probabilities)
    

if __name__ == '__main__':
    app.run(debug=False)