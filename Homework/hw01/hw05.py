def hailstone(x):
    """Print the hailstone sequence starting at x and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    step = 0
    while x != 1:
        step += 1
        print(x)
        if x % 2:
            x = x * 3 + 1
        else:
            x = x // 2
    print(1)
    return step + 1
