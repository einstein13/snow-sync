#!/usr/bin/env python
# -*- coding: utf-8 -*-

def list_dict_find_by_name(list_of_dicts, name_to_find):
    if name_to_find is None:
        return None

    for itr in range(len(list_of_dicts)):
        item = list_of_dicts[itr]
        if 'name' in item and item['name'] == name_to_find:
            return [itr, item]

    return None

def list_dict_find(list_of_dicts, name_to_find=None):
    # returns list:
        # [0] - index of element (integer)
        # [1] - element (dictionary)
        # returned element is: name, then name as integer, then default value is the first element

    if name_to_find is None:
        return [0, list_of_dicts[0]]

    result = list_dict_find_by_name(list_of_dicts, name_to_find)
    if result is not None:
        return result

    try:
        number = int(name_to_find)
        item = list_of_dicts[number]
        return [number, item]
    except:
        pass

    return [0, list_of_dicts[0]]

def remove_from_list(list, name):
    if name in list:
        list.remove(name)
        return 1
    return 0

