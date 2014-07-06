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
from rabbit.all import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

cli = commandline(addcolor("\nRunning Tests.txt...", "pink"))
cli.terminate = True
cli.evalfile("Tests.txt")
print(addcolor("Tests.txt Evaluation Complete.", "cyan"))

comp = compiler()
print(addcolor("\nCompiling...", "pink"))
newvars = comp.disassemble(comp.assemble())[1]
print(addcolor("Compiled.", "cyan"))

print(addcolor("Testing Compilation...", "pink"))
for k,v in comp.e.variables.items():
    nv = haskey(newvars, k)
    if v != nv:
        print(addcolor("<!> For variable "+str(k)+" the old value of "+repr(v)+" is not equal to the new value "+repr(nv), "lightred"))
for k,v in newvars.items():
    ov = haskey(comp.e.variables, k)
    if v != ov:
        print(addcolor("<!> For variable "+str(k)+" the new value of "+repr(v)+" is not equal to the old value "+repr(ov), "lightred"))
if not comp.e.variables == newvars:
    raise ExecutionError("CompileError", "Decompiled variables failed to equal compiled variables.")
print(addcolor("Compilation Testing Complete.", "cyan"))

print(addcolor("\nAll Tests Pass.", "green"))
