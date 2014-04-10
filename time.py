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

import time

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
