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
    try:
        inputobject.ismatrix
    except AttributeError:
        return getcheck(inputobject) == 2
    else:
        return inputobject.ismatrix()

def isreal(value, start=float("-inf"), end=float("inf"), mid=0.0):
    """Tests To See If A Value Is A Real."""
    value = hasreal(value)
    if value is not None:
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
        if value is None:
            return 0.0
        else:
            return value

def getimag(inputobject):
    """Gets The Imaginary Part Of An Object."""
    if isinstance(inputobject, complex):
        return getnum(inputobject.imag)
    else:
        return 0.0

def getint(inputobject):
    """Turns An Object Into An Integer."""
    return int(getnum(inputobject))

def makenum(inputobject):
    """Makes An Object A Number."""
    if isnum(inputobject):
        return inputobject
    else:
        return getnum(inputobject)

def catch(function, *args):
    """Gets The Errors From A Function."""
    result = None
    try:
        result = function(*args)
    except ZeroDivisionError as detail:
        err = ("ZeroDivisionError", detail)
    except ValueError as detail:
        err = ("ValueError", detail)
    except OverflowError as detail:
        err = ("OverflowError", detail)
    except TypeError as detail:
        err = ("TypeError", detail)
    except KeyError as detail:
        err = ("KeyError", detail)
    except AttributeError as detail:
        err = ("AttributeError", detail)
    except IndexError as detail:
        err = ("IndexError", detail)
    except RuntimeError as detail:
        err = ("RuntimeError", detail)
    except AssertionError as detail:
        err = ("AssertionError", detail)
    except ExecutionError as detail:
        err = (detail.name, detail.message, detail.variables)
    else:
        err = None
    return result, err
