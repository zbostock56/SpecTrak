def diff(obj1, obj2):
    """Diffs between two objects.

    Args:
        obj1 (unknown): first object to diff.
        obj2 (unknown): second object to diff.

    Returns:
        obj: A dictionary of the changes or None.
    """
    from dictionify import dictionify
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        return diff_dicts(obj1, obj2)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        return diff_lists(obj1, obj2)
    elif not (obj1 == obj2):
        return {'from': dictionify(obj1), 'to': dictionify(obj2)}
    else:
        return None

def diff_dicts(dict1: dict, dict2: dict):
    """Diffs two dictionaries.

    Args:
        dict1 (dict): first dictionary to diff.
        dict2 (dict): secondary dictionary to diff.

    Returns:
        obj: A dictionary of the changes or None.
    """
    diff_result = {}
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    
    for key in all_keys:
        if key in dict1 and key in dict2:
            nested_diff = diff(dict1[key], dict2[key])
            if nested_diff is not None:
                diff_result[key] = {'changed': nested_diff}
        elif key in dict1:
            diff_result[key] = {'removed': dict1[key]}
        else:
            diff_result[key] = {'added': dict2[key]}
    
    return diff_result

def diff_lists(list1: list, list2: list):
    from dictionify import dictionify
    """Diffs two lists.

    Args:
        list1 (list): first list to diff.
        list2 (list): second list to diff.

    Returns:
        obj: A dictionary of the changes or None.
    """
    diff_result = []
    max_length = max(len(list1), len(list2))
    for i in range(max_length):
        if i < len(list1) and i < len(list2):
            nested_diff = diff(list1[i], list2[i])
            if nested_diff is not None:
                diff_result.append({'index': i, 'changed': nested_diff})
        elif i < len(list1):
            diff_result.append({'index': i, 'removed': dictionify(list1[i])})
        else:
            diff_result.append({'index': i, 'added': dictionify(list2[i])})
    
    return diff_result if diff_result else None