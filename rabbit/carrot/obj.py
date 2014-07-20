#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# LIBRARY made in 2012
# This program contains functions for use with other programs.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import with_statement, absolute_import, print_function, unicode_literals

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

try:
    xrange
except NameError:
    xrange = range

encoding = "UTF"

try:
    raw_input
except NameError:
    old_input = input
else:
    old_input = raw_input

raw_input = lambda *args, **kwargs: old_input(*args, **kwargs).decode(encoding)

try:
    unicode
except NameError:
    old_str = bytes
else:
    old_str = str
    str = unicode

old_print = print
print = lambda *args: old_print(*(map(lambda x: str(x).encode(encoding), args)))

def typestr(obj):
    """Formats The Type Of Something Into A String."""
    return str(type(obj)).split("'")[1]

def namestr(obj):
    """Formats Something Into Its Name."""
    if "function" in typestr(obj):
        return str(obj).split(" ")[1]
    elif "method" in typestr(obj):
        return str(obj).split(" ")[2].split(".")[-1].replace(">","")
    else:
        return str(obj)

def hascall(func):
    """Determines If An Object Has A Call Method."""
    if hasattr(func, "isfunc"):
        return func.isfunc()
    elif hasattr(func, "call"):
        return True
    else:
        return False

def getcall(func):
    """Gets The Callable Part Of A Function."""
    if hascall(func):
        return func.call
    else:
        return func

def istext(inputobject):
    """Determines If An Object Is A String."""
    return isinstance(inputobject, (str, unicode, old_str))

def urepr(inputobject):
    """Returns A Pre-Unicode Representation."""
    out = repr(inputobject)
    if istext(inputobject):
        return out[1:]
    else:
        return out

def hasreal(value):
    """Tests To See If A Value Is A Number."""
    try:
        value = float(value)
    except ValueError:
        return None
    except TypeError:
        return None
    else:
        return value

def isnum(inputobject):
    """Determines If An Object Is A Number."""
    return isinstance(inputobject, (float, int, long, complex))

def curry(func, arg, key=None):
    """Returns A Function With A Curried Argument."""
    def _func(*args, **kwargs):
        if key is None:
            args = (arg,) + args
        else:
            kwargs[str(key)] = arg
        return func(*args, **kwargs)
    return _func

class memoize(object):
    """A Memoized Function."""
    memo = ([], [])
    def __init__(self, func):
        """Creates The Memoized Function."""
        self.func = func
    def call(self, *args, **kwargs):
        """Calls The Memoized Function."""
        key = (args, kwargs)
        index = None
        for x in xrange(0, len(self.memo[0])):
            if self.memo[0][x] == key:
                index = x
                break
        if index is None:
            out = self.func(*args, **kwargs)
            self.memo[0].append(key)
            self.memo[1].append(out)
        else:
            out = self.memo[1][index]
        return out
