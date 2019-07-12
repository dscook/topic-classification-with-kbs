#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
from collections import defaultdict
import numpy as np

###
### VARIABLES (update as necessary)
###

data_to_analyse_path = '../rcv1/results/2019-07-12/rcv1/'


###
### CODE
###

# To store means and standard deviations keyed by classifier type then keyed by training set size then micro/macro
mean_dict = {}
stdev_dict = {}

def calculate_mean_stdev(train_size_to_results, f1_type):
    for train_size, results in train_size_to_results.items():
        mean_dict[classifier_balance][train_size][f1_type] = np.mean(results)
        stdev_dict[classifier_balance][train_size][f1_type] = np.std(results, ddof=1)


result_files = os.listdir(data_to_analyse_path)

for result_file in result_files:
        
    classifier_balance = result_file.split('.')[0]
    classifier_balance_split = classifier_balance.split('_')
    
    # Initialise the mean and stdev dictionaries for this classifier
    mean_dict[classifier_balance] = defaultdict(lambda: {})
    stdev_dict[classifier_balance] = defaultdict(lambda: {})
    
    # First part of the name before underscore is the classifier name, 'nb', 'svc' or 'kb.'
    classifier = classifier_balance_split[0]
    
    # Second part of the filename is proportional or balanced
    dataset_balance = classifier_balance_split[1]
    
    # Dictionary containing list of results for each training set size
    train_size_to_micro_results = defaultdict(list)
    train_size_to_macro_results = defaultdict(list)
    
    # Get the results
    with open(data_to_analyse_path + result_file, newline='') as csvfile:
        result_reader = csv.reader(csvfile)
        for row in result_reader:
            train_size = int(row[0])
            micro_f1 = float(row[1])
            macro_f1 = float(row[2])
            train_size_to_micro_results[train_size].append(micro_f1)
            train_size_to_macro_results[train_size].append(macro_f1)
    
    # Calculate means and standard deviations at each training set size        
    calculate_mean_stdev(train_size_to_micro_results, 'micro')
    calculate_mean_stdev(train_size_to_macro_results, 'macro')


# Print out results in a format that can be pasted into a Jupyer notebook and a Latex report
def print_results():  
    for classifier, results in mean_dict.items():
        train_sizes = '['
        micro_results = '['
        macro_results = '['
        micro_results_std = '['
        macro_results_std = '['
        
        comma = False
        for train_size, f1_results in results.items():
            if comma:
                train_sizes += ', '
                micro_results += ', '
                macro_results += ', '
                micro_results_std += ', '
                macro_results_std += ', '
                
            train_sizes += '{}'.format(train_size)
            micro_results += '{:.6f}'.format(f1_results['micro'])
            macro_results += '{:.6f}'.format(f1_results['macro'])
            micro_results_std += '{:.6f}'.format(stdev_dict[classifier][train_size]['micro'])
            macro_results_std += '{:.6f}'.format(stdev_dict[classifier][train_size]['macro'])
            
            comma = True
            
        train_sizes += ']'
        micro_results += ']'
        macro_results += ']'
        micro_results_std += ']'
        macro_results_std += ']'
        
        print('---------------------------')
        print('Results for {}'.format(classifier))
        print('')
        print('train_sizes = {}'.format(train_sizes))
        print('{}_micro = {}'.format(classifier, micro_results))
        print('{}_macro = {}'.format(classifier, macro_results))
        print('{}_micro_std = {}'.format(classifier, micro_results_std))
        print('{}_macro_std = {}'.format(classifier, macro_results_std))
        print('')


print_results()
