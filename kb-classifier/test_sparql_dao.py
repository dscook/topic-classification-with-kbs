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


    def test_get_resource_for_phrase_from_anchor(self):
        resources = self.dao.get_resources_for_phrase_from_anchor('David Cameron')
        self.assertEqual(resources, ['David_Cameron',
                                     'Dave_Cameron_(footballer)',
                                     'Premiership_of_David_Cameron',
                                     'Shadow_Cabinet_of_David_Cameron',
                                     'Family_of_David_Cameron',
                                     'David_Cameron_(soccer)',
                                     'David_Cameron_(darts_player)',
                                     'Second_Cameron_ministry'])
        resources = self.dao.get_resources_for_phrase_from_anchor('No Match')
        self.assertEqual(resources, [])
        

    def test_filter_undesired_types(self):
        resource = self.dao.filter_undesired_types('David_Cameron')
        self.assertEqual(resource, 'David_Cameron')
        resource = self.dao.filter_undesired_types('United_States')
        self.assertEqual(resource, None)


if __name__ == '__main__':
    unittest.main()