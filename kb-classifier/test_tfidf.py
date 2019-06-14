#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible
import sys
sys.path.append('../common/')

import unittest
import numpy as np

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
        x, y = load_preprocessed_data('../news-classification/data/rcv1_no_stopwords_coreference.csv')
        #x, y = load_preprocessed_data('../news-classification/data/rcv1_no_stopwords_reduced.csv')
        
        self.tfidf.fit(x)
        
        # Sort the TFIDFs
        term_idfs = []
        for term, idf in self.tfidf.idf_dict.items():
            term_idfs.append((term, idf))
        sorted_term_idfs = sorted(term_idfs, key=lambda tup: tup[1])
        
        # Calculate min, max and mean TFIDF
        idfs = []
        for term, idf in self.tfidf.idf_dict.items():
            idfs.append(idf)
        print('Min TFIDF {}'.format(np.min(idfs)))
        print('Median TFIDF {}'.format(np.median(idfs)))
        print('Mean TFIDF {}'.format(np.mean(idfs)))
        print('Max TFIDF {}'.format(np.max(idfs)))
            
        # Write out inverse document frequencies to file for inspection
        with open('idfs.txt', 'w') as idf_file:
            for term_idf in sorted_term_idfs:
                idf_file.write('{},{}'.format(term_idf[0], term_idf[1]) + '\n')

if __name__ == '__main__':
    unittest.main()