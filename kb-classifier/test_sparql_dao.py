#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from sparql_dao import SparqlDao

class SparqlDaoTestCase(unittest.TestCase):
    

    def setUp(self):
        self.dao = SparqlDao(endpoint_url='http://localhost:3030/DBpedia/')


    def test_get_parent_topics(self):
        parent_topics = self.dao.get_parent_topics('English_footballers')
        self.assertEqual(parent_topics, ['English_sportspeople',
                                         'British_footballers',
                                         'Association_football_players_by_nationality',
                                         'Footballers_in_England'])
        

if __name__ == '__main__':
    unittest.main()