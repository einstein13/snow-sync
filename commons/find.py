def list_dict_find(list_of_dicts, name_to_find=None):
    # returns list:
        # [0] - index of element (integer)
        # [1] - element (dictionary)
        # returned element is: name, then name as integer, then default value is the first element
    if name_to_find is None:
        return [0, list_of_dicts[0]]
    for itr in range(len(list_of_dicts)):
        item = list_of_dicts[itr]
        if 'name' in item and item['name'] == name_to_find:
            return [itr, item]
    try:
        number = int(name_to_find)
        item = list_of_dicts[number]
        return [number, item]
    except:
        pass
    return [0, list_of_dicts[0]]
