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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__all__ = ["web", "proc", "path", "stats", "crypto", "test"]

__doc__ = """Overview:
    Carrot (RabbitLib) is a compilation of functions, classes, and variables that extend basic Python functionality.
    Every single function, method, and class in Rabbit is documented, so have a look around, and feel free to contribute.

Key:
    name_of_module (dependency_one, dependency_two) : A description of the module.

File List:
    obj () : Functions for managing objects at a base level.

    base (obj) : Base classes for custom objects.
    math (obj) : Advanced mathematical functions.
    web (obj) : Utilities for interfacing with the web.
    proc (obj) : Utilities for managing multiple processes.

    check (base) : Functions for analyzing objects for basic properties.
    path (sys) : Utilities for implementing pathfinding.
    stats (math) : Advanced statistical functions.

    list (check) : Utilities for managing lists and other containers.

    sys (list) : Functions for interfacing with the operating system.
    format (list) : Utilities for managing and formatting strings.

    rand (sys, math) : Random number generation utilities.
    file (format, sys) : Utilities for managing different types of files.

    gui (file) : Utilities for creating and managing basic windows.
    crypto (format, rand) : Cryptographic utilities.

    app (gui, web) : Utilities for creating graphical applications.

    test (app) : A Python interpreter for testing purposes.

    all (test, crypto, matrix, fraction, stats, path, proc, web) : All Carrot functions in one place."""
