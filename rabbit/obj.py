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

from __future__ import absolute_import, print_function, unicode_literals
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

try:
    xrange
except NameError:
    xrange = range

try:
    raw_input
except NameError:
    old_input = input
else:
    old_input = raw_input

raw_input = lambda *args, **kwargs: old_input(*args, **kwargs).decode("UTF")

try:
    unicode
except NameError:
    old_str = bytes
else:
    old_str = str
    str = unicode

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
    try:
        func.isfunc
    except AttributeError:
        try:
            func.call
        except AttributeError:
            return False
        else:
            return True
    else:
        return func.isfunc()

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
    if key == None:
        return lambda *args: func(arg, *args)
    else:
        key = str(key)
        return lambda *args: func(*args, **{key:arg})
