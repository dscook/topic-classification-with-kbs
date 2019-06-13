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
                                         'Association_football_players_by_nationality'])
    
    
    def test_get_resource_for_phrase(self):
         resource = self.dao.get_resource_for_phrase('United States')
         self.assertEqual(resource, 'United_States')
         resource = self.dao.get_resource_for_phrase('Unitad States')
         self.assertEqual(resource, None)
        

    def test_get_resource_for_phrase_from_redirect(self):
         resource = self.dao.get_resource_for_phrase_from_redirect('U.S.')
         self.assertEqual(resource, 'United_States')
         resource = self.dao.get_resource_for_phrase_from_redirect('USA')
         self.assertEqual(resource, 'United_States')
         resource = self.dao.get_resource_for_phrase_from_redirect('USAA')
         self.assertEqual(resource, None)


if __name__ == '__main__':
    unittest.main()