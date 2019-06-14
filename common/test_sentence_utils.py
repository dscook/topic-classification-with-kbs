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
        
    
    def test_coreference_resolution(self):
        string_with_coreferences = """Bob Dole jumped to about five percentage points behind President Bill Clinton in the latest Reuters tracking poll on Tuesday, as Republican voters continued coming home& to their party's candidate.
            The poll, conducted for Reuters by John Zogby Group International, produced the best results for Dole in a Reuters survey since its polling began in August.
            It showed Clinton at 43.8 percent, Dole at 38.5 percent for a gap of just 5.3 percentage points. Reform Party candidate Ross Perot was at 4.5 percent, 1.9 percent supported other candidates and 11.3 percent were undecided.
            """
        coreference_resolved = remove_stop_words_and_lemmatize(string_with_coreferences,
                                                               lowercase = False,
                                                               lemmatize = False,
                                                               keep_nouns_only=True)
        print(coreference_resolved)


if __name__ == '__main__':
    unittest.main()