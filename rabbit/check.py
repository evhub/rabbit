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

from __future__ import absolute_import, print_function

from .base import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getcheck(inputobject):
    """Returns The Evaluator Check Number For The Object Where (-2=unknown; -1=string; 0=number; 1=number-equivalent; 2=matrix-equivalent)."""
    if isinstance(inputobject, evalobject):
        return int(inputobject.check)
    elif isnum(inputobject):
        return 0
    elif istext(inputobject):
        return -1
    else:
        return -2

def hasnum(inputobject):
    """Tests If An Object Is A Number Class."""
    return getcheck(inputobject) >= 0

def iseval(inputobject):
    """Tests If An Object Is An Evaluator Class."""
    return getcheck(inputobject) > 0

def isfunc(inputobject):
    """Tests If An Object Is A Function."""
    check = getcheck(inputobject)
    return (check > 0 and hascall(inputobject)) or check == -2

def hasmatrix(inputobject):
    """Determines If An Object Could Be A Matrix."""
    return getcheck(inputobject) == 2

def isreal(value, start=float("-inf"), end=float("inf"), mid=0.0):
    """Tests To See If A Value Is A Real."""
    value = hasreal(value)
    if value != None:
        if start < value and value < end and (value <= mid or value >= mid):
            return value
        else:
            return None
    else:
        return None

def getnum(inputobject):
    """Always Returns A Number."""
    if isinstance(inputobject, complex):
        return getnum(inputobject.real)
    else:
        value = isreal(inputobject)
        if value == None:
            return 0.0
        else:
            return value

def getint(inputstring):
    """Formats A String Into An Integer."""
    return int(getnum(inputstring))
