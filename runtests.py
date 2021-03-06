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
from rabbit.all import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print()
cli = commandline(addcolor("Running Tests.txt...", "magenta"), debugcolor="red")
cli.fatalerror = always(None)
cli.evalfile("Tests.rab")
print(addcolor("Tests.txt Evaluation Complete.", "blue"))

print()
comp = compiler()
comp.fatalerror = always(None)
print(addcolor("Compiling...", "magenta"))
oldvars = comp.e.variables.copy()
comp.compfile()
comp.decompfile()
print(addcolor("Compiled.", "blue"))

print(addcolor("Testing Compilation...", "magenta"))
for k,v in oldvars.items():
    nv = haskey(comp.e.variables, k)
    if v != nv:
        comp.printdebug(addcolor("<!> For variable "+str(k)+" the old value of "+repr(v)+" is not equal to the new value "+repr(nv), "red"))
for k,v in comp.e.variables.items():
    ov = haskey(oldvars, k)
    if v != ov:
        comp.printdebug(addcolor("<!> For variable "+str(k)+" the new value of "+repr(v)+" is not equal to the old value "+repr(ov), "red"))
if oldvars != comp.e.variables:
    comp.adderror("CompileError", "Decompiled variables failed to equal compiled variables", True)
print(addcolor("Compilation Testing Complete.", "blue"))

print()
if cli.errorlog or comp.errorlog:
    print(addcolor("Some Tests Fail:", "red"))
    raise ExecutionError(addcolor("TestingError", "red"), addcolor("Errors in cli"*cli.errorlog+", "*(cli.errorlog and comp.errorlog)+"Errors in comp"*comp.errorlog, "red"))
else:
    print(addcolor("All Tests Pass.", "green"))
