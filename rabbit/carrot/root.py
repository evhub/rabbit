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

try:
    from future_builtins import map, filter
except ImportError:
    pass

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

try:
    xrange
except NameError:
    xrange = range
else:
    range = xrange

try:
    long
except NameError:
    long = int

try:
    ascii
except NameError:
    ascii = repr

try:
    unichr
except NameError:
    unichr = chr

encoding = "UTF"

old_print = print
def_str = str
try:
    unicode
except NameError:
    old_str = bytes
    unicode = str
else:
    old_str = str
    str = unicode
    print = lambda *args: old_print(*(map(lambda x: str(x).encode(encoding), args)))
