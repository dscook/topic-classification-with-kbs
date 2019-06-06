#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

from classifier import Classifier
from tfidf import TfIdf
from kb_common import wiki_topics_to_actual_topics

app = Flask(__name__)
classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=5)
tfidf_calculator = TfIdf(classifier)


@app.route('/tfidf', methods=['POST'])
def tfidf():
    body = request.get_json()
    tfidf_calculator.fit(body['documents'])
    classifier.tfidf = tfidf_calculator


@app.route('/classify', methods=['POST'])
def classify():
    body = request.get_json()
    topic_to_prob = classifier.identify_topic_probabilities(body['text'])
    return jsonify(topic_to_prob)


@app.route('/probabilities/<depth>', methods=['GET'])
def probabilities(depth):
    """
    Get the topic probabilities for the last classified example at the specified depth
    of the topic tree.  0 = root topics, 1 = next level and so on.
    """
    probabilities = classifier.get_topic_probabilities(int(depth))
    return jsonify(probabilities)


if __name__ == '__main__':
    app.run(debug=True)