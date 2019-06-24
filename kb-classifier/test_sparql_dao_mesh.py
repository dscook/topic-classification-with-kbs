#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from sparql_dao_mesh import SparqlDao

    
class SparqlDaoTestCase(unittest.TestCase):

    
    def setUp(self):
        self.dao = SparqlDao(endpoint_url='http://localhost:3030/MeSH/')
    
    
    def test_get_resource_for_phrase(self):
        resource = self.dao.get_resource_for_phrase('Skin Cancer')
        self.assertEqual(resource, 'D012878')
    
    
if __name__ == '__main__':
    unittest.main()