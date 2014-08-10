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

__all__ = ["carrot.all", "ride", "graph", "comp"]

__doc__ = """Overview:
    Rabbit (RabbitLang) is a modern, functional programming language, documented most thouroughly in the README.

Key:
    name_of_module (dependency_one, dependency_two) : A description of the module.

File List:
    fraction (carrot.format, carrot.math) : Utilities for managing fraction objects.
    matrix (carrot.format, carrot.rand) : Utilities for using mathematical matrices.

    func (matrix) : Utilities for managing functions as mathematical objects.

    data (func, carrot.stats) : Utilities for managing statistical data.

    eval (data, fraction, carrot.file) : Utilities for implementing the Rabbit language.

    cmd (eval, carrot.app) : The standard Rabbit language interpreter.

    cli (cmd) : The Rabbit Command Line Interface.
    ride (cmd) : The Rabbit Integrated Development Environment.
    graph (cmd) : A Graphing Module For Rabbit Functions.

    comp (cli) : The Rabbit Semi-Compiler.

    all (comp, graph, ride, carrot.all) : All Rabbit functions in one place."""
