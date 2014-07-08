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

from .list import *
import os
import subprocess
import imp
import time

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def compute(inputstring, extras=None, builtins=None):
    """Evaluates Code In A Safe Environment."""
    inputstring = str(inputstring)
    if extras is None:
        extras = {}
    extras["__builtins__"] = builtins
    return eval(inputstring, extras)

def runcode(code, extras=None):
    """Executes Code With Access Only To Global Variables."""
    if extras is None:
        exec str(code) in globals()
    else:
        exec str(code) in globals(), extras

def runcmd(command):
    """Runs A System Command."""
    return subprocess.call(str(command), shell=True)

def dirimport(modname, directory=None):
    """Allows Importing Of A Remote Module."""
    modname = str(modname)
    if directory is not None:
        filename, pathname, description = imp.find_module(modname, [directory])
    else:
        filename, pathname, description = imp.find_module(modname)
    return imp.load_module(modname, filename, pathname, description)

def scan(variables=None, lenfunc=len):
    """Scans Variables To Analyze Memory Allocation."""
    if variables is None:
        variables = globals()
    out = []
    for x in variables:
        try:
            v = lenfunc(variables[x])
        except:
            out.append((-1,str(x)))
        else:
            out.append((v, str(x)))
    out.sort()
    return out

def printret(*args):
    """Prints And Returns Values."""
    print(*args)
    if len(args) == 1:
        return args[0]
    elif len(args) > 1:
        return args

def getos(findos=None):
    """Determines The Current Operating System."""
    if findos is None:
        osname = os.name
        if osname in ["nt", "win"]:
            return "win."+osname
        elif osname in ["posix", "os2", "mac"]:
            return "mac."+osname
        else:
            return osname
    else:
        return getos().startswith(str(findos))

class timer(object):
    """An Interfacing Class For Clock Time."""
    def __init__(self):
        """Starts The Timer."""
        self.reset()
    def reset(self):
        """Resets The Timer."""
        self.start = time.clock()
    def get(self):
        """Gets The Current Time Passed."""
        return time.clock()-self.start
    def lap(self):
        """Gets The Current Time Passed And Resets The Timer."""
        temptime = time.clock()
        laptime = temptime-self.start
        self.start = temptime
        return laptime

def thetime():
    """Finds The Current Time."""
    return time.ctime().split(" ")

colors = {
    "end" : "\033[0m",
    "bold" : "\033[1m",
    "blink" : "\033[5m",
    "black" : "\033[30m",
    "red" : "\033[31m",
    "green" : "\033[32m",
    "yellow" : "\033[33m",
    "blue" : "\033[34m",
    "magenta" : "\033[35m",
    "cyan" : "\033[36m",
    "white" : "\033[37m",
    "blackhighlight" : "\033[40m",
    "redhighlight" : "\033[41m",
    "greenhighlight" : "\033[42m",
    "yellowhighlight" : "\033[43m",
    "bluehighlight" : "\033[44m",
    "magentahighlight" : "\033[45m",
    "cyanhighlight" : "\033[46m",
    "whitehighlight" : "\033[47m",
    "pink" : "\033[95m",
    "purple" : "\033[94m",
    "lightgreen" : "\033[92m",
    "lightyellow" : "\033[93m",
    "lightred" : "\033[91m"
    }

def addcolor(inputstring, color):
    """Adds The Specified Colors To The String."""
    if islist(color):
        out = ""
        for item in color:
            out += colors[str(item)]
    else:
        out = colors[str(color)]
    return out+str(inputstring)+colors["end"]

def delcolor(inputstring):
    """Removes Recognized Colors From A String."""
    inputstring = str(inputstring)
    for x in colors:
        inputstring = inputstring.replace(x, "")
    return inputstring
