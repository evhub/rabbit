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

from .obj import *
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
    if extras == None:
        extras = {}
    extras["__builtins__"] = builtins
    eval(inputstring, extras)

def runcode(code, extras=None):
    """Executes Code With Access Only To Global Variables."""
    if extras == None:
        exec str(code) in globals()
    else:
        exec str(code) in globals(), extras

def runcmd(command):
    """Runs A System Command."""
    return subprocess.call(str(command), shell=True)

def dirimport(modname, directory=None):
    """Allows Importing Of A Remote Module."""
    modname = str(modname)
    if directory != None:
        filename, pathname, description = imp.find_module(modname, [directory])
    else:
        filename, pathname, description = imp.find_module(modname)
    return imp.load_module(modname, filename, pathname, description)

def scan(variables=None, lenfunc=len):
    """Scans Variables To Analyze Memory Allocation."""
    if variables == None:
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

def getos(findos=None):
    """Determines The Current Operating System."""
    maclist = ["posix", "os2", "mac"]
    otherlist = ["ce", "riscos", "java"]
    osname = os.name
    if findos == None:
        if osname == "nt":
            return "win"
        elif osname in maclist:
            return "mac"
        elif osname in otherlist:
            return "other"
        else:
            return "unknown"
    else:
        if "win" in findos:
            if osname == "nt":
                return osname
            else:
                return False
        elif "mac" in findos:
            if osname in maclist:
                return osname
            else:
                return False
        elif "other" in findos:
            if osname in otherlist:
                return osname
            else:
                return False
        elif "unknown" in findos:
            if osname == "nt":
                return False
            elif osname in maclist:
                return False
            elif osname in otherlist:
                return False
            else:
                return osname
        elif osname in findos:
            return osname
        else:
            return False

class timer(object):
    """An Interfacing Class For Clock Time."""
    def __init__(self):
        """Starts The Timer."""
        self.reset()
    def reset(self):
        """Resets The Timer."""
        self.start = time.clock()
    def get(self):
        """Return The Current Time Passed."""
        return time.clock()-self.start
    def lap(self):
        """Returns The Current Time Passed And Resets The Timer."""
        temptime = time.clock()
        laptime = temptime-self.start
        self.start = temptime
        return laptime

def thetime():
    """Determines The Current Time."""
    return time.ctime().split(" ")
