#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from sentence_utils import remove_stop_words_and_lemmatize, is_number, is_time


class SentenceUtilsTestCase(unittest.TestCase):


    def test_lemmatization(self):
        string_to_test = 'The striped bats are hanging on their feet for best'
        lemmatized_string = remove_stop_words_and_lemmatize(string_to_test)
        self.assertEqual(lemmatized_string, 'striped bat hang foot best')


    def test_keep_nouns(self):
        string_to_test = """
            Sacchi took over as Milan coach late last year after Uruguayan coach Oscar Washington Tabarez
            handed in his resignation.  Tabarez had himself taken over at Milan from Fabio Capello, who
            moved to Spain's Real Madrid."""
        jj_and_nouns = remove_stop_words_and_lemmatize(string_to_test,
                                                       lowercase = False,
                                                       lemmatize = False,
                                                       keep_nouns_only=True)
        self.assertEqual(jj_and_nouns, 'Sacchi Milan late last year Uruguayan coach Oscar_Washington_Tabarez' +
                         ' resignation Tabarez Milan Fabio_Capello Spain Real Madrid')


    def test_is_number(self):
        self.assertEqual(False, is_number('Fabio_Capello'))
        self.assertEqual(False, is_number('Spain'))
        self.assertEqual(True, is_number('0'))
        self.assertEqual(True, is_number('2:23'))
        self.assertEqual(True, is_number('02:23'))
        self.assertEqual(True, is_number('1-1/4'))
        self.assertEqual(True, is_number('4-2'))
        self.assertEqual(True, is_number('66.5'))
        self.assertEqual(True, is_number('59,500'))
        self.assertEqual(True, is_number('+301'))
        self.assertEqual(True, is_number('1996'))
        self.assertEqual(False, is_number('Spain66'))


    def test_is_time(self):
        self.assertEqual(False, is_time('Fabio_Capello'))
        self.assertEqual(False, is_time('Spain'))
        self.assertEqual(False, is_time('omar'))
        self.assertEqual(True, is_time('Monday'))
        self.assertEqual(True, is_time('monday'))
        self.assertEqual(True, is_time('February'))
        self.assertEqual(True, is_time('february'))
        self.assertEqual(True, is_time('Mar'))
        self.assertEqual(True, is_time('mar'))
        self.assertEqual(True, is_time('1st'))
        self.assertEqual(True, is_time('2nd'))
        self.assertEqual(True, is_time('3rd'))
        self.assertEqual(True, is_time('31st'))
        self.assertEqual(True, is_time('26-oct'))


if __name__ == '__main__':
    unittest.main()