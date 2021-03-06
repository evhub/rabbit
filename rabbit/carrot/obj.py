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

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division

from .root import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

old_int = int
def int(x, *args, **kwargs):
    """Does Proper Integer Conversion."""
    if istext(x) and "." in x:
        while x.endswith("0"):
            x = x[:-1]
        if x.endswith("."):
            x = x[:-1]
    return old_int(x, *args, **kwargs)

old_float = float
def float(x, *args, **kwargs):
    """Converts To The Proper Number Object."""
    if isinstance(x, (old_int, long)):
        return int(x, *args, **kwargs)
    elif isinstance(x, old_float):
        try:
            test_int = int(x, *args, **kwargs)
        except:
            return old_float(x, *args, **kwargs)
        else:
            if test_int == x:
                return test_int
            else:
                return old_float(x, *args, **kwargs)
    elif hasattr(x, "getfloat"):
        return x.getfloat(*args, **kwargs)
    else:
        test_float = old_float(x, *args, **kwargs)
        try:
            test_float_int = int(test_float, *args, **kwargs)
        except:
            return test_float
        else:
            if test_float_int == test_float:
                try:
                    test_int = int(x, *args, **kwargs)
                except:
                    return test_float
                else:
                    return test_int
            else:
                return test_float

def getbytes(obj):
    """Gets A Bytes Object."""
    if isinstance(obj, old_str):
        return obj
    else:
        return str(obj).encode(encoding)

def getstr(obj):
    """Gets A Unicode Object."""
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, old_str):
        return str(obj, encoding)
    else:
        return str(obj)

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
    return hasattr(func, "call") or hasattr(func, "getcall")

def getcall(func, *args, **kwargs):
    """Gets The Callable Part Of A Function."""
    if not hascall(func):
        return func
    elif hasattr(func, "call"):
        return func.call
    elif hasattr(func, "getcall"):
        return func.getcall(*args, **kwargs)
    else:
        raise AttributeError("Function has no call method")

def istext(inputobject):
    """Determines If An Object Is A String."""
    return isinstance(inputobject, (str, old_str))

def urepr(inputobject):
    """Returns A Pre-Unicode Representation."""
    out = repr(inputobject)
    if istext(inputobject):
        while out and out[0] not in "\"'":
            out = out[1:]
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

def isint(inputobject):
    """Determines If An Object Is An Integer."""
    return isinstance(inputobject, (old_int, long))

def isnum(inputobject):
    """Determines If An Object Is A Number."""
    return isinstance(inputobject, (old_float, old_int, long, complex, bool))

def ismethod(inputobject):
    """Determines Whether An Object Is A Method."""
    return typestr(inputobject) in ["instancemethod", "method"]

def iseq(a, b):
    """Determines Whether Two Objects Are Really Equal."""
    return a is b or (type(a) is type(b) and a == b)

def curry(func, arg, key=None):
    """Returns A Function With A Curried Argument."""
    def _func(*args, **kwargs):
        if key is None:
            args = (arg,) + args
        else:
            kwargs[str(key)] = arg
        return func(*args, **kwargs)
    return _func

def always(out):
    """Creates A Function That Always Returns out."""
    return lambda *args, **kwargs: out

def itemstate(item):
    """Gets The State Of An Item."""
    if hasattr(item, "getstate"):
        return item.getstate()
    else:
        return item

def liststate(inputlist):
    """Compiles A List."""
    out = []
    for item in inputlist:
        out.append(itemstate(item))
    return out

def getstates(variables):
    """Compiles Variables."""
    out = {}
    for k,v in variables.items():
        out[itemstate(k)] = itemstate(v)
    return out

def getcopy(inputobject):
    """Copies The Object If It Has A copy Method."""
    if isinstance(inputobject, list):
        return list(map(getcopy, inputobject[:]))
    elif hasattr(inputobject, "copy"):
        return inputobject.copy()
    else:
        return inputobject

class memoizer(object):
    """A Memoized Function."""
    def __init__(self, func):
        """Creates The Memoized Function."""
        self.memo = [[], []]
        self.func = func
    def __call__(self, *args, **kwargs):
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
