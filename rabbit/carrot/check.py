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
    if check == -2:
        return True
    elif check <= 0:
        return False
    elif not hasattr(inputobject, "isfunc"):
        return hascall(inputobject)
    elif isinstance(inputobject.isfunc, bool):
        return inputobject.isfunc
    else:
        return inputobject.isfunc()

def hasmatrix(inputobject):
    """Determines If An Object Could Be A Matrix."""
    check = getcheck(inputobject)
    if check <= 0:
        return False
    elif not hasattr(inputobject, "ismatrix"):
        return check == 2
    elif isinstance(inputobject.ismatrix, bool):
        return inputobject.ismatrix
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
            raise ValueError("Cannot convert to number "+repr(inputobject))
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

def makeint(inputobject):
    """Makes An Object An Integer."""
    if isnum(inputobject):
        return int(inputobject)
    else:
        return getint(inputobject)

def getcopy(inputobject):
    """Copies The Object If It Has A copy Method."""
    if hasattr(inputobject, "copy"):
        return inputobject.copy()
    elif isinstance(inputobject, list):
        return map(getcopy, inputobject[:])
    elif isinstance(inputobject, dict):
        out = {}
        for k,v in inputobject.items():
            out[getcopy(k)] = getcopy(v)
        return out
    else:
        return inputobject

def catch(function, *args, **kwargs):
    """Gets The Errors From A Function."""
    result = None
    try:
        result = function(*args, **kwargs)
    except ZeroDivisionError as detail:
        err = ("ZeroDivisionError", detail, True)
    except ValueError as detail:
        err = ("ValueError", detail, True)
    except OverflowError as detail:
        err = ("OverflowError", detail, True)
    except TypeError as detail:
        err = ("TypeError", detail, True)
    except KeyError as detail:
        err = ("KeyError", detail, True)
    except AttributeError as detail:
        err = ("AttributeError", detail, True)
    except IndexError as detail:
        err = ("IndexError", detail, True)
    except NotImplementedError as detail:
        err = ("NotImplementedError", detail, False)
    except RuntimeError as detail:
        err = ("RuntimeError", detail, False)
    except AssertionError as detail:
        err = ("AssertionError", detail, False)
    except IOError as detail:
        err = ("IOError", detail, True)
    except SyntaxError as detail:
        err = ("PythonSyntaxError", detail, True)
    except NameError as detail:
        err = ("PythonNameError", detail, True)
    except EOFError as detail:
        err = ("EOFInterrupt", detail or "Action has been terminated", True)
    except KeyboardInterrupt as detail:
        err = ("KeyboardInterrupt", detail or "Action has been terminated", False)
    except ExecutionError as detail:
        err = (detail.name, detail.message, detail.fatal, detail.variables)
    except Exception as detail:
        err = ("Error", detail or "An error occured", True)
    except BaseException as detail:
        err = ("PythonError", detail or "An error occured", True)
    else:
        err = None
    return result, err
