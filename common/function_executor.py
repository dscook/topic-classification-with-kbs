#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def apply_fn_to_list_items_in_dict(dictionary, fn, **kwargs):
    """
    Given a dictionary with items that are lists, applies the given function to each
    item in each list and return an updated version of the dictionary.
    
    :param dictionary: the dictionary to update.
    :param fn: the function to apply.
    :param **kwargs: variable keyworded arguments to run fn with
    :returns: an updated version of the dictionary.
    """
    updated_dictionary = {}
    
    for key, items in dictionary.items():
        updated_items = []
        
        for item in items:
            updated_item = fn(item, **kwargs)
            updated_items.append(updated_item)
            
        updated_dictionary[key] = updated_items
    
    return updated_dictionary