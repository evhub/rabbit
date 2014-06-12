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

__all__ = ["web", "proc", "path", "crypto", "cli", "ride", "graph"]

__doc__ = """Overview:
    Rabbit (PythonPlus) is a compilation of functions, classes, and variables that extend basic Python functionality.
    Every single function, method, and class in Rabbit is documented, so have a look around, and feel free to contribute.
    The most extensive feature of Rabbit is its own built-in programming language, documented most thouroughly in the readme.

Key:
    name_of_module (dependency_one, dependency_two) : A description of the module.

File List:
    obj () : Functions for managing objects at a base level.

    base (obj) : Base classes for custom objects.
    sys (obj) : Functions for interfacing with the operating system.
    math (obj) : Advanced mathematical functions.
    web (obj) : Utilities for interfacing with the web.
    proc (obj) : Utilities for managing multiple processes.

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

    cli (cmd) : The Rabbit Command Line Interface.
    ride (cmd) : The Rabbit Integrated Development Environment.
    graph (cmd) : A Graphing Module For Rabbit Functions.

    all (graph, ride, crypto, path, proc, web) : All Rabbit functions in one place."""
