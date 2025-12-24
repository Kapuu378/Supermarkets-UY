from .custom_exceptions import handle_recursion

from dataclasses import dataclass

@handle_recursion
def flatten(d: dict) -> dict:
    """Recursive function for flattening dictonaries.
    This function return a new dict that only contains the keys which hold values different from
    other dicts and arrays.
    Consider that this function will override duplicate keys and use the latest one.
    """
    items = {}
    for k, v in d.items():
        if (isinstance(v, dict)):
            items.update(flatten(v))
        
        elif (isinstance(v, list)):
            for element in v:
                if isinstance(element, dict):
                    items.update(flatten(element))
        else:
            items[k] = v

    return items

def rename_keys(dic: dict, mapping: dict) -> dict:
    """
    Function that takes a dictionary and renames the keys based on a mapping like -> [old_key]:[new_key]
    
    :param d: Dictionary to be processed.
    :type d: dict
    :param mapping: Mapping dictionary in which each key represents the old key to be replaced and the value is the new key.
    :type mapping: dict
    """
    if not isinstance(dic, dict): raise TypeError
    if not isinstance(mapping, dict): raise TypeError
    items = {mapping.get(k, k):v for k, v in dic.items()}
    return items
