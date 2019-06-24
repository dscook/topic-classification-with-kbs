#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from sparql_dao_mesh import SparqlDao

    
class SparqlDaoTestCase(unittest.TestCase):

    
    def setUp(self):
        self.dao = SparqlDao(endpoint_url='http://localhost:3030/MeSH/')
    
    
    def test_get_resource_for_phrase(self):
        resource = self.dao.get_resource_for_phrase('Skin Cancer')
        self.assertEqual(resource, 'M0333435')


    def test_get_topics_for_resource(self):
        topics = self.dao.get_topics_for_resource('M0333435')
        self.assertEqual(topics, ['C04.588.805', 'C17.800.882'])

 
    def test_get_parent_topics(self):
        parent_topics = self.dao.get_parent_topics('C04.588.805')
        self.assertEqual(parent_topics, ['C04.588'])


    def test_get_child_topics(self):
        child_topics = self.dao.get_child_topics('C04.588')
        self.assertEqual(child_topics, ['C04.588.033',
                                        'C04.588.083',
                                        'C04.588.149',
                                        'C04.588.180',
                                        'C04.588.274',
                                        'C04.588.322',
                                        'C04.588.364',
                                        'C04.588.443',
                                        'C04.588.448',
                                        'C04.588.531',
                                        'C04.588.614',
                                        'C04.588.699',
                                        'C04.588.805',
                                        'C04.588.839',
                                        'C04.588.842',
                                        'C04.588.894',
                                        'C04.588.945'])
    
    
if __name__ == '__main__':
    unittest.main()