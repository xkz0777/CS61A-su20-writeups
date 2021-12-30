LAB_SOURCE_FILE = __file__


def reverse_iter(lst):
    """Returns the reverse of the given list.

    >>> reverse_iter([1, 2, 3, 4])
    [4, 3, 2, 1]
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(reverse_iter)))
    >>> print("Do not use lst[::-1], lst.reverse(), or reversed(lst)!") if any([r in cleaned for r in ["[::", ".reverse", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"
    length = len(lst)
    for i in range(length // 2):
        lst[i], lst[length - 1 - i] = lst[length - 1 - i], lst[i]
    return lst


def reverse_recursive(lst):
    """Returns the reverse of the given list.

    >>> reverse_recursive([1, 2, 3, 4])
    [4, 3, 2, 1]
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(reverse_recursive)))
    >>> print("Do not use lst[::-1], lst.reverse(), or reversed(lst)!") if any([r in cleaned for r in ["[::", ".reverse", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"
    length = len(lst)
    if length <= 1:
        return lst
    return [lst[-1]] + reverse_recursive(lst[0:length - 1])
    # avoid using method `extend` here because it only modifies the original list and returns None!


from math import sqrt


def distance(city_a, city_b):
    """
    >>> city_a = make_city('city_a', 0, 1)
    >>> city_b = make_city('city_b', 0, 2)
    >>> distance(city_a, city_b)
    1.0
    >>> city_c = make_city('city_c', 6.5, 12)
    >>> city_d = make_city('city_d', 2.5, 15)
    >>> distance(city_c, city_d)
    5.0
    """
    "*** YOUR CODE HERE ***"
    xa, ya = get_lat(city_a), get_lon(city_a)
    xb, yb = get_lat(city_b), get_lon(city_b)
    return sqrt((xa - xb)**2 + (ya - yb)**2)


def closer_city(lat, lon, city_a, city_b):
    """
    Returns the name of either city_a or city_b, whichever is closest to
    coordinate (lat, lon).

    >>> berkeley = make_city('Berkeley', 37.87, 112.26)
    >>> stanford = make_city('Stanford', 34.05, 118.25)
    >>> closer_city(38.33, 121.44, berkeley, stanford)
    'Stanford'
    >>> bucharest = make_city('Bucharest', 44.43, 26.10)
    >>> vienna = make_city('Vienna', 48.20, 16.37)
    >>> closer_city(41.29, 174.78, bucharest, vienna)
    'Bucharest'
    """
    "*** YOUR CODE HERE ***"
    tmp = make_city('tmp', lat, lon)
    closer = city_a if distance(city_a, tmp) < distance(city_b, tmp) else city_b
    return get_name(closer)


def check_abstraction():
    """
    There's nothing for you to do for this function, it's just here for the extra doctest
    >>> change_abstraction(True)
    >>> city_a = make_city('city_a', 0, 1)
    >>> city_b = make_city('city_b', 0, 2)
    >>> distance(city_a, city_b)
    1.0
    >>> city_c = make_city('city_c', 6.5, 12)
    >>> city_d = make_city('city_d', 2.5, 15)
    >>> distance(city_c, city_d)
    5.0
    >>> berkeley = make_city('Berkeley', 37.87, 112.26)
    >>> stanford = make_city('Stanford', 34.05, 118.25)
    >>> closer_city(38.33, 121.44, berkeley, stanford)
    'Stanford'
    >>> bucharest = make_city('Bucharest', 44.43, 26.10)
    >>> vienna = make_city('Vienna', 48.20, 16.37)
    >>> closer_city(41.29, 174.78, bucharest, vienna)
    'Bucharest'
    >>> change_abstraction(False)
    """


# Treat all the following code as being behind an abstraction layer, you shouldn't need to look at it!


def make_city(name, lat, lon):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    >>> get_lat(city)
    0
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return {"name": name, "lat": lat, "lon": lon}
    else:
        return [name, lat, lon]


def get_name(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    """
    if change_abstraction.changed:
        return city["name"]
    else:
        return city[0]


def get_lat(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lat(city)
    0
    """
    if change_abstraction.changed:
        return city["lat"]
    else:
        return city[1]


def get_lon(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return city["lon"]
    else:
        return city[2]


def change_abstraction(change):
    change_abstraction.changed = change


change_abstraction.changed = False


def add_chars(w1, w2):
    """
    Return a string containing the characters you need to add to w1 to get w2.

    You may assume that w1 is a subsequence of w2.

    >>> add_chars("owl", "howl")
    'h'
    >>> add_chars("want", "wanton")
    'on'
    >>> add_chars("rat", "radiate")
    'diae'
    >>> add_chars("a", "prepare")
    'prepre'
    >>> add_chars("resin", "recursion")
    'curo'
    >>> add_chars("fin", "effusion")
    'efuso'
    >>> add_chars("coy", "cacophony")
    'acphon'
    >>> from construct_check import check
    >>> # ban iteration and sets
    >>> check(LAB_SOURCE_FILE, 'add_chars',
    ...       ['For', 'While', 'Set', 'SetComp']) # Must use recursion
    True
    """
    "*** YOUR CODE HERE ***"
    # Iterative solution: double pointer
    # missing_chars = ''
    # len1 = len(w1)
    # len2 = len(w2)
    # i, j = 0, 0
    # while i < len1:
    #     while w2[j] != w1[i] and j < len2:
    #         missing_chars += w2[j]
    #         j += 1
    #     i, j = i + 1, j + 1
    # if j < len2:
    #     missing_chars += w2[j:]
    # return missing_chars
    # Recursive solution:
    if w1 == '':
        return w2
    elif w1[0] == w2[0]:
        return add_chars(w1[1:], w2[1:])
    return w2[0] + add_chars(w1, w2[1:])
