#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from sentence_utils import remove_stop_words_and_lemmatize


class SentenceUtilsTestCase(unittest.TestCase):
    
    def test_lemmatization(self):
        string_to_test = 'The striped bats are hanging on their feet for best'
        lemmatized_string = remove_stop_words_and_lemmatize(string_to_test)
        self.assertEqual(lemmatized_string, 'striped bat hang foot best')
        

if __name__ == '__main__':
    unittest.main()