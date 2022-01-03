def make_generators_generator(g):
    """Generates all the "sub"-generators of the generator returned by
    the generator function g.

    >>> def every_m_ints_to(n, m):
    ...     i = 0
    ...     while (i <= n):
    ...         yield i
    ...         i += m
    ...
    >>> def every_3_ints_to_10():
    ...     for item in every_m_ints_to(10, 3):
    ...         yield item
    ...
    >>> for gen in make_generators_generator(every_3_ints_to_10):
    ...     print("Next Generator:")
    ...     for item in gen:
    ...         print(item)
    ...
    Next Generator:
    0
    Next Generator:
    0
    3
    Next Generator:
    0
    3
    6
    Next Generator:
    0
    3
    6
    9
    """
    "*** YOUR CODE HERE ***"

    # a easy to understand version

    # def generator_helper(n):
    #     for ele, _ in zip(g(), range(n)):
    #         yield ele

    # for index, _ in enumerate(g()):
    #     yield generator_helper(index + 1)

    def generator_helper(n):
        yield from map(lambda ele: ele[0], zip(g(), range(n)))

    yield from map(lambda ele: generator_helper(ele[0] + 1), enumerate(g()))
