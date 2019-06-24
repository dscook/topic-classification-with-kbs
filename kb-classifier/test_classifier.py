#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Make common scripts visible
import sys
sys.path.append('../common/')

import unittest

from classifier_copy import Classifier
from sentence_utils import remove_stop_words_and_lemmatize
from kb_common import dao_init


doc_to_test = """
London rivals Chelsea and Arsenal meet in an all-English Europa League final on Wednesday, 2,500 miles from home.

There is speculation that, win or lose in Baku's Olympic Stadium, it could be Blues boss Maurizio Sarri's final game in charge.
"""

doc_to_test = """
Philip Morris Tuesday Kansas attorney general decision list states lawsuits tobacco firms Medicaid money tobacco-related illnesses Philip Morris Kansas Attorney General Carla Stovall courts public policy tobacco Philip Morris companies lawsuit zealousness bandwagon attorney general fact state viaable legal basis upon cigarette manufacturers Gregory Little lawyer Philip Morris law correct state Kansas process waste millions taxpayer dollars time costs
"""

shorter_doc_to_test = 'London rivals Chelsea and Arsenal meet in an all-English Europa League final.  Chelsea won.'

class ClassifierTestCase(unittest.TestCase):
    

    def setUp(self):
        self.classifier = Classifier(dao=dao_init(),
                                     root_topic_names=set(['Crime',
                                                           'Law',
                                                           'Business',
                                                           'Economics',
                                                           'Elections', 
                                                           'Politics',
                                                           'Health',
                                                           'Medicine',
                                                           'Religion',
                                                           'Theology',
                                                           'Sports']),
                                    max_depth=5)
        self.doc_to_test = remove_stop_words_and_lemmatize(doc_to_test, lowercase=False, lemmatize=False)
        self.shorter_doc_to_test = remove_stop_words_and_lemmatize(shorter_doc_to_test, lowercase=False, lemmatize=False)


    def test_identify_topics_exists(self):
        phrase = 'Maurizio Sarri'
        topics = self.classifier.identify_topics(phrase)
        self.assertEqual(topics, ['Italian_football_managers', 'Serie_A_managers'])


    def test_identify_topics_does_not_exist(self):
        phrase = 'Maurizio Sarrie'
        topics = self.classifier.identify_topics(phrase)
        self.assertEqual(topics, [])
        

    def test_identify_topics_exists_but_no_topic(self):
        phrase = 'Robert C. Martin'    # Uncle Bob
        topics = self.classifier.identify_topics(phrase)
        self.assertEqual(topics, [])


    def test_identify_leaf_topics(self):
        phrase_to_topic_dict, phrase_to_occurences = self.classifier.identify_leaf_topics(self.shorter_doc_to_test)
        self.assertIn('Football_in_England', phrase_to_topic_dict['London rivals'])
        self.assertIn('Football_clubs_in_England', phrase_to_topic_dict['Chelsea'])
        self.assertIn('Association_football_penalty_shootouts', phrase_to_topic_dict['Europa League final'])
        self.assertEqual(phrase_to_occurences['Arsenal'], 1)
        self.assertEqual(phrase_to_occurences['Chelsea'], 2)
        

    def test_identify_topic_probabilities(self):
        topic_to_prob = self.classifier.identify_topic_probabilities(self.doc_to_test)
        print(topic_to_prob)


if __name__ == '__main__':
    unittest.main()