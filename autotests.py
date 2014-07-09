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
from rabbit.all import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print()
cli = commandline(addcolor("Running Tests.txt...", "magenta"), debugcolor="red")
cli.evalfile("Tests.txt")
print(addcolor("Tests.txt Evaluation Complete.", "blue"))

print()
comp = compiler()
print(addcolor("Compiling...", "magenta"))
newvars = comp.disassemble(comp.assemble())[1]
print(addcolor("Compiled.", "blue"))

print(addcolor("Testing Compilation...", "magenta"))
for k,v in comp.e.variables.items():
    nv = haskey(newvars, k)
    if v != nv:
        comp.printdebug(addcolor("<!> For variable "+str(k)+" the old value of "+repr(v)+" is not equal to the new value "+repr(nv), "red"))
for k,v in newvars.items():
    ov = haskey(comp.e.variables, k)
    if v != ov:
        comp.printdebug(addcolor("<!> For variable "+str(k)+" the new value of "+repr(v)+" is not equal to the old value "+repr(ov), "red"))
if not comp.e.variables == newvars:
    comp.adderror("CompileError", "Decompiled variables failed to equal compiled variables")
print(addcolor("Compilation Testing Complete.", "blue"))

print()
if cli.errorlog or comp.errorlog:
    print(addcolor("Some Tests Fail:", "red"))
    raise ExecutionError(addcolor("TestingError", "red"), addcolor("Errors in cli"*cli.errorlog+", "*(cli.errorlog and comp.errorlog)+"Errors in comp"*comp.errorlog, "red"))
else:
    print(addcolor("All Tests Pass.", "green"))
