#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

from classifier import Classifier
from kb_common import wiki_topics_to_actual_topics

app = Flask(__name__)
classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                        root_topic_names=wiki_topics_to_actual_topics.keys(),
                        max_depth=5)


@app.route('/classify', methods=['POST'])
def classify():
    body = request.get_json()
    topic_to_prob = classifier.identify_topic_probabilities(body['text'])
    return jsonify(topic_to_prob)


if __name__ == '__main__':
    app.run(debug=True)