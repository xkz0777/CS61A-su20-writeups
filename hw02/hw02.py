from operator import add, mul, sub


def square(x): return x * x


def identity(x): return x


def triple(x): return 3 * x


def increment(x): return x + 1


HW_SOURCE_FILE = __file__


def product(n, term):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    term -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    "*** YOUR CODE HERE ***"
    product, k = 1, 1
    while k <= n:
        product, k = product * term(k), k + 1
    return product


def accumulate(combiner, base, n, term):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are term(1), term(2), ..., term(n).  combiner is a
    two-argument commutative function.

    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19

    """
    "*** YOUR CODE HERE ***"
    total, k = base, 1
    while k <= n:
        total, k = combiner(total, term(k)), k + 1
    return total


def summation_using_accumulate(n, term):
    """Returns the sum of term(1) + ... + term(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    return accumulate(add, 0, n, term)


def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    return accumulate(mul, 1, n, term)


def compose1(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f


def make_repeater(func, n):
    """Return the function that computes the nth application of func.
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    """
    return accumulate(compose1, lambda x: x, n, lambda x: func)


def one(f):
    """Church numeral 1: same as successor(zero)"""
    return lambda x: f(x)


def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    return lambda x: f(f(x))


def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


one = successor(zero)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer."""
    return n(lambda x: x + 1)(0)


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n."""
    return lambda f: lambda x: m(f)(n(f)(x))


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n."""
    return lambda f: n(m(f))


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n."""
    return n(m)  # how does it work?
    # equal to lambda f: lambda x: (n(m))(f)(x)
    # for example, if n == 4, then 4(m) is to say m(m(m(m(f)))),
    # which is f^{m^4}, so represents m^4
    # so m^n is simply n(m)
