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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__all__ = ["web", "path", "crypto", "ride"]

__doc__ = """Overview:
    Rabbit (PythonPlus) is a compilation of functions, classes, and variables that extend basic Python functionality.
    Every single function, method, and class in Rabbit is documented, so have a look around.
    The most extensive feature of Rabbit is its own built-in programming language, found in rabbit.eval.

File List:
    obj () : Functions for managing objects at a base level.

    base (obj) : Base classes for custom objects.
    sys (obj) : Functions for interfacing with the operating system.
    math (obj) : Advanced mathematical functions.
    web (obj) : Utilities for interfacing with the web.

    check (base) : Functions for analyzing objects for basic properties.
    path (sys) : Utilities for implementing pathfinding.
    stats (math) : Advanced statistical functions.
    rand (math, sys) : Random number generation utilities.

    list (check) : Utilities for managing lists and other containers.

    format (list) : Utilities for managing and formatting strings.

    file (format, sys) : Utilities for managing different types of files.
    fraction (format, math) : Utilities for managing fraction objects.
    matrix (format, rand) : Utilities for using mathematical matrices.
    crypto (format, rand) : Cryptographic utilities.

    gui (file) : Utilities for creating and managing basic windows.
    func (matrix) : Utilities for managing functions as mathematical objects.

    app (gui) : Utilities for creating graphical applications.
    data (func, stats) : Utilities for managing statistical data.

    test (app) : A Python interpreter for testing purposes.
    eval (data, fraction) : Utilities for implementing the Rabbit language.

    cmd (eval, app) : The standard Rabbit language interpreter.

    ride (cmd) : The Rabbit Integrated Development Environment.

    all (ride, crypto, path, web) : All Rabbit functions in one place."""
