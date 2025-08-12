def all_but_first(items):
    """Returns a list without the first item in the list. 
    In the case that there is only one item in the list or the first item of the list is empty, 
    [] is returned.
    """
    if len(items) <= 1 or not items[0]:
        return []
    return items[1:]
