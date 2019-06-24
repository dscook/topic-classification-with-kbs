#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from lookup_cache_mesh import LookupCache

class LookupCacheTestCase(unittest.TestCase):


    def setUp(self):
        self.cache = LookupCache()
        
    
    def test_contains_exact(self):
        present = self.cache.contains_exact('Not Present')
        self.assertFalse(present)
        present = self.cache.contains_exact('hepatitis b')
        self.assertTrue(present)
    
    
    def test_get_normal_form(self):
        normal_form = self.cache.get_normal_form('hepatitis b')
        self.assertEqual(normal_form, 'Hepatitis B')


if __name__ == '__main__':
    unittest.main()