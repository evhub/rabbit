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
    if findos == None:
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
