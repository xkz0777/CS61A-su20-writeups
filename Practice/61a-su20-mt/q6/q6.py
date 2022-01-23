email = 'example_key'

def copycat(lst1, lst2):
    """
    Write a function `copycat` that takes in two lists.
        `lst1` is a list of strings
        `lst2` is a list of integers

    It returns a new list where every element from `lst1` is copied the
    number of times as the corresponding element in `lst2`. If the number
    of times to be copied is negative (-k), then it removes the previous
    k elements added.

    Note 1: `lst1` and `lst2` do not have to be the same length, simply ignore
    any extra elements in the longer list.

    Note 2: you can assume that you will never be asked to delete more
    elements than exist


    >>> copycat(['a', 'b', 'c'], [1, 2, 3])
    ['a', 'b', 'b', 'c', 'c', 'c']
    >>> copycat(['a', 'b', 'c'], [3])
    ['a', 'a', 'a']
    >>> copycat(['a', 'b', 'c'], [0, 2, 0])
    ['b', 'b']
    >>> copycat([], [1, 2, 3])
    []
    >>> copycat(['a', 'b', 'c'], [1, -1, 3])
    ['c', 'c', 'c']
    """
    def copycat_helper(lst1, lst2, new_lst):
        if not lst1 or not lst2:
            return new_lst
        if lst2[0] >= 0:
            new_lst = new_lst + [lst1[0]] * lst2[0]
        else:
            new_lst = new_lst[:lst2[0]]  # lst[:-n] can be used to remove the last k elements
        return copycat_helper(lst1[1:], lst2[1:], new_lst)
    return copycat_helper(lst1, lst2, [])

# ORIGINAL SKELETON FOLLOWS

# def copycat(lst1, lst2):
#     """
#     Write a function `copycat` that takes in two lists.
#         `lst1` is a list of strings
#         `lst2` is a list of integers

#     It returns a new list where every element from `lst1` is copied the
#     number of times as the corresponding element in `lst2`. If the number
#     of times to be copied is negative (-k), then it removes the previous
#     k elements added.

#     Note 1: `lst1` and `lst2` do not have to be the same length, simply ignore
#     any extra elements in the longer list.

#     Note 2: you can assume that you will never be asked to delete more
#     elements than exist


#     >>> copycat(['a', 'b', 'c'], [1, 2, 3])
#     ['a', 'b', 'b', 'c', 'c', 'c']
#     >>> copycat(['a', 'b', 'c'], [3])
#     ['a', 'a', 'a']
#     >>> copycat(['a', 'b', 'c'], [0, 2, 0])
#     ['b', 'b']
#     >>> copycat([], [1,2,3])
#     []
#     >>> copycat(['a', 'b', 'c'], [1, -1, 3])
#     ['c', 'c', 'c']
#     """
#     def copycat_helper(______, ______, ______):
#         if ______:
#             return ______
#         if ______:
#             ______ = ______
#         else:
#             ______ = ______[:______]
#         return ______
#     return ______
