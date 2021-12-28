def count_change(total):
    """Return the number of ways to make change for total.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_change', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    mp = {}

    def cal_exponent(n):  # return the max exponent
        if n <= 1:
            return 0
        else:
            return cal_exponent(n >> 1) + 1

    def helper(total, m):  # sum up to total using numbers up to m
        if total == 1 or total == 0 or m == 1:
            return 1
        elif total < 0:
            return 0
        elif (total, m) in mp:
            return mp[(total, m)]
        else:
            mp[(total, m)] = helper(total - m, m) + helper(total, m // 2)
            return mp[(total, m)]

    return helper(total, pow(2, cal_exponent(total)))

print(count_change(10))