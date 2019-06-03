#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from sentence_utils_copy import remove_stop_words_and_lemmatize


class SentenceUtilsTestCase(unittest.TestCase):
    
    def test_lemmatization(self):
        string_to_test = 'The striped bats are hanging on their feet for best'
        lemmatized_string = remove_stop_words_and_lemmatize(string_to_test)
        self.assertEqual(lemmatized_string, 'striped bat hang foot best')
    
    def test_keep_nouns(self):
        string_to_test = """
Sacchi took over as Milan coach late last year after Uruguayan coach Oscar Washington Tabarez handed in his resignation. Tabarez had himself taken over at Milan from Fabio Capello, who moved to Spain's Real Madrid."""
        print(remove_stop_words_and_lemmatize(string_to_test, lowercase = False, lemmatize = False, keep_nouns_only=True))

if __name__ == '__main__':
    unittest.main()