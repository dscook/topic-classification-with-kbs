#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import numpy as np

from lookup_tables import int_to_topic
from uvigomed_parser import load_data


class UvigomedParserTestCase(unittest.TestCase):

    
    def test_load_data(self):
        train_x, train_y, test_x, test_y = load_data('../../../downloads/UVigoMED/single_label/')
        
        # Output how many articles are in each category
        counts = np.unique(train_y, return_counts=True)
        counts = list(zip(counts[0], counts[1]))
        train_counts = np.zeros(shape=np.max(counts[0])+1)
        for index, count in counts:
            train_counts[index] = count
        
        counts = np.unique(test_y, return_counts=True)
        counts = list(zip(counts[0], counts[1]))
        test_counts = np.zeros(shape=np.max(counts[0])+1)
        for index, count in counts:
            test_counts[index] = count
        
        number_train = len(train_y)
        print('Total number of training examples: {}'.format(number_train))
        for index, topic in int_to_topic.items():
            print('{}, Count: {}, Percentage: {}'.format(topic, train_counts[index], 100*(train_counts[index]/number_train)))
        print('')
        
        number_test = len(test_y)
        print('Total number of test examples: {}'.format(number_test))
        for index, topic in int_to_topic.items():
            print('{}, Count: {}, Percentage: {}'.format(topic, test_counts[index], 100*(test_counts[index]/number_test)))
            

if __name__ == '__main__':
    unittest.main()