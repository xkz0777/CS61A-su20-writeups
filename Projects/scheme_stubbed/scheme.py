"""A Scheme interpreter and its read-eval-print loop."""
from __future__ import print_function
from cmath import exp
from multiprocessing.managers import SyncManager  # Python 2 compatibility

import sys
import os
from traceback import format_list
from unittest import result

from markupsafe import re, string
from numpy import isin

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace


##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # atom
    if self_evaluating(expr):
        return expr
    elif scheme_symbolp(expr):
        return env.lookup(expr)

    # combination
    if not scheme_listp(expr):
        raise SchemeError('{0} is not an expression'.format(expr))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](expr, env)
    else:                                                    # call
        operator = scheme_eval(first, env)
        if isinstance(operator, MacroProcedure):
            return scheme_eval(operator.apply_macro(rest, env), env)
        else:
            args = rest.map(lambda x: scheme_eval(x, env))
            return scheme_apply(operator, args, env)


def self_evaluating(expr):
    return expr is nil or expr is None or isinstance(expr, (bool, int, float))


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        return procedure.apply(args, env)
    elif isinstance(procedure, LambdaProcedure):
        # formals 与 args 的值相对应, 再创建新环境
        formals = procedure.formals.to_list()
        args = args.to_list()
        if len(formals) != len(args):
            raise SchemeError('Incorrect number of arguments to function call')

        curr_envi = Frame(env) if isinstance(
            procedure, MuProcedure) else Frame(procedure.env)
        for formal, arg in zip(formals, args):
            curr_envi.define(formal, arg)

        expr = procedure.body
        while expr.rest is not nil:
            scheme_eval(expr.first, curr_envi)
            expr = expr.rest
        return scheme_eval(expr.first, curr_envi, True)


################
# Environments #
################

class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        "Your Code Here"
        self.value = dict()
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        self.value[symbol] = value

    # BEGIN PROBLEM 2/3
    "*** YOUR CODE HERE ***"

    def lookup(self, symbol):
        def lookup_in_frame(frame):
            if frame.value.get(symbol) is not None:
                return frame.value.get(symbol)
            elif frame.parent:
                return lookup_in_frame(frame.parent)
            else:
                raise SchemeError('symbol {0} not found'.format(symbol))
        return lookup_in_frame(self)
    # END PROBLEM 2/3

##############
# Procedures #
##############


class Procedure(object):
    """The supertype of all Scheme procedures."""


def scheme_procedurep(x):
    return isinstance(x, Procedure)


class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        try:
            if self.use_env:
                return self.fn(*(args.to_list() + [env]))
            else:
                return self.fn(*(args.to_list()))
        except(TypeError):
            raise SchemeError('Wrong numbers of arguments')
        # END PROBLEM 2


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env=None):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        validate_formals(formals)
        self.formals = formals
        self.body = body
        if body is nil:
            raise SchemeError('Invalid lambda expression')
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))


class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def apply_macro(self, operands, env):
        """Apply this macro to the operand expressions."""
        return complete_apply(self, operands, env)


def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################


"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

# Special forms


def do_and_form(expr, env):
    ret_val = True
    while expr.rest is not nil:
        expr = expr.rest
        if expr.rest is nil:
            return scheme_eval(expr.first, env, True)
        ret_val = scheme_eval(expr.first, env)
        if is_false_primitive(ret_val):
            break
    return ret_val


def do_or_form(expr, env):
    ret_val = False
    while expr.rest is not nil:
        expr = expr.rest
        if expr.rest is nil:
            return scheme_eval(expr.first, env, True)
        ret_val = scheme_eval(expr.first, env)
        if is_true_primitive(ret_val):
            break
    return ret_val


def do_if_form(expr, env):
    validate_form(expr, 3)
    cond = scheme_eval(expr.rest.first, env)
    if is_true_primitive(cond):
        return scheme_eval(expr.rest.rest.first, env, True)
    else:
        if expr.rest.rest.rest is nil:
            return None
        return scheme_eval(expr.rest.rest.rest.first, env, True)


def do_cond_form(expr, env):
    validate_form(expr, 2)
    while expr.rest is not nil:
        expr = expr.rest
        clause = expr.first
        cond = True if clause.first == 'else' else clause.first
        test = scheme_eval(cond, env)
        if is_true_primitive(test):
            clause_val = do_begin_form(clause, env)
            return test if clause_val is None else clause_val
    return None


def do_define_form(expr, env):
    validate_form(expr, 3)
    symbol = expr.rest.first
    validate_formals(symbol)
    if isinstance(symbol, Pair):
        formals = symbol.rest
        proc_name = symbol.first
        value = LambdaProcedure(formals, expr.rest.rest, env)
        env.define(proc_name, value)
        return proc_name
    else:
        value = scheme_eval(expr.rest.rest.first, env)
        env.define(symbol, value)
        return symbol


def do_begin_form(expr, env):
    if expr.rest is nil:
        return None
    while expr.rest is not nil:
        expr = expr.rest
        if expr.rest is nil:
            return scheme_eval(expr.first, env, True)
        scheme_eval(expr.first, env)


def do_let_form(expr, env):
    validate_form(expr, 3)
    bidings = expr.rest.first
    formals_args_list = []
    while bidings is not nil:
        validate_form(bidings.first, 2, 2)
        formals_args_list += [(bidings.first.first, bidings.first.rest.first)]
        bidings = bidings.rest
    formals_args_list.reverse()
    formals, args = nil, nil
    for formal, arg in formals_args_list:
        formals, args = Pair(formal, formals), Pair(arg, args)
    proc = LambdaProcedure(formals, expr.rest.rest, env)
    args = args.map(lambda x: scheme_eval(x, env))
    return scheme_apply(proc, args, env)


def do_lambda_form(expr, env):
    validate_form(expr, 3)
    return LambdaProcedure(expr.rest.first, expr.rest.rest, env)


def do_mu_form(expr, env):
    validate_form(expr, 3)
    return MuProcedure(expr.rest.first, expr.rest.rest)


def do_quote_form(expr, env):
    return expr.rest.first


def do_unquote(expr, env):
    raise SchemeError('unquote not within quasiquote')


def do_quasiquote_form(expr, env):
    def helper(node):
        '''for node.first.first == unquote，eval，替换 node.first'''
        if not isinstance(node, Pair):  # base case
            return node
        if isinstance(node.first, Pair) and node.first.first == 'unquote':
            return Pair(scheme_eval(node.first.rest.first, env), helper(node.rest))
        else:
            return Pair(helper(node.first), helper(node.rest))
    return helper(expr).rest.first


def do_define_macro(expr, env):
    """Evaluate a define-macro form."""
    # BEGIN Problem 21
    "*** YOUR CODE HERE ***"
    validate_form(expr, 3)
    target = expr.rest.first
    if not scheme_listp(target):
        raise SchemeError('Wrong define macro form')
    name, parameters, body = target.first, target.rest, expr.rest.rest
    if not scheme_symbolp(name):
        raise SchemeError('Wrong define macro form')
    macro_procedure = MacroProcedure(parameters, body, env)
    env.define(name, macro_procedure)
    return name


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'mu': do_mu_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
}

# Utility methods for checking the structure of Scheme programs


def validate_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')


def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()

    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest

    # here for compatibility with DOTS_ARE_CONS
    if formals != nil:
        validate_and_add(formals, True)


def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))


#################
# Dynamic Scope #
#################


class MuProcedure(LambdaProcedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))


##################
# Tail Recursion #
##################
# Make classes/functions for creating tail recursive programs here?


class Thunk():
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env


def optimize_tail_calls(prior_eval_function):
    def optimized_eval(expr, env, tail=False):
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Thunk(expr, env)

        result = Thunk(expr, env)
        while isinstance(result, Thunk):
            result = prior_eval_function(result.expr, result.env)
        return result
    return optimized_eval


scheme_eval = optimize_tail_calls(scheme_eval)


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    val = scheme_apply(procedure, args, env)
    # Add stuff here?
    if isinstance(val, Thunk):
        return scheme_eval(val.expr, val.env)
    return val


####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))


def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head


def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

################
# Input/Output #
################


def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                    'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return


def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)

    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)


def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))


def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    # note what does use_env mean
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env


@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('--pillow-turtle', action='store_true',
                        help='run with pillow-based turtle. This is much faster for rendering but there is no GUI')
    parser.add_argument('--turtle-save-path', default=None,
                        help='save the image to this location when done')
    parser.add_argument('-load', '-i', action='store_true',
                        help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    import scheme
    scheme.TK_TURTLE = not args.pillow_turtle
    scheme.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, '')
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(scheme.__file__))))

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()

            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()
