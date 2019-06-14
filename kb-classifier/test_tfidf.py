#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible
import sys
sys.path.append('../common/')

import unittest

from loader import load_preprocessed_data
from classifier import Classifier
from kb_common import wiki_topics_to_actual_topics
from tfidf import TfIdf


class TfidfTestCase(unittest.TestCase):

    
    def setUp(self):
        classifier = Classifier(sparql_endpoint_url='http://localhost:3030/DBpedia/',
                                root_topic_names=wiki_topics_to_actual_topics.keys(),
                                max_depth=5)
        self.tfidf = TfIdf(classifier)


    def test_tfidf(self):
        #x, y = load_preprocessed_data('data/rcv1_no_stopwords_coreference.csv')
        x, y = load_preprocessed_data('data/rcv1_no_stopwords_reduced.csv')
        
        self.tfidf.fit(x)
        
        # Sort the TFIDFs
        term_idfs = []
        for term, idf in self.tfidf.idf_dict.items():
            term_idfs.append((term, idf))
        sorted_term_idfs = sorted(term_idfs, key=lambda tup: tup[1])
            
        # Write out inverse document frequencies to file for inspection
        with open('idfs.txt', 'w') as idf_file:
            for term_idf in sorted_term_idfs:
                idf_file.write(term_idf + '\n')

if __name__ == '__main__':
    unittest.main()