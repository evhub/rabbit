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
import multiprocessing
import multiprocessing.managers

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class manager(object):
    """Manages Objects."""
    class top(multiprocessing.managers.BaseManager):
        """Holds Registered Objects."""
        pass
    def register(self, name, item):
        """Registers An Object."""
        self.top.register(str(name), item)
    def get(self):
        """Returns An Instance Of The Registry."""
        out = top()
        out.start()
        return out
    def wrap(self, name, item):
        """Wraps An Object In The Registry."""
        name = str(name)
        self.register(name, item)
        return getattr(self.get(), name)

class queue(object):
    def __init__(self):
        """Creates The Queue."""
        self.procs = []
    def add(self, func, *args, **kwargs):
        """Adds A Function To The Queue."""
        proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        self.procs.append(proc)
    def start(self):
        """Starts All The Functions In The Queue."""
        for proc in self.procs:
            proc.start()
    def join(self):
        """Joins All The Functions In The Queue."""
        for proc in self.procs:
            proc.join()

class pool(queue):
    def __init__(self):
        """Creates The Pool."""
        self.queue = multiprocessing.Queue()
        self.procs = []
    def add(self, func, *args, **kwargs):
        """Adds A Function To The Pool."""
        func = lambda *args, **kwargs: self.queue.put(func(*args, **kwargs))
        proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        self.procs.append(proc)
    def get(self):
        """Gets The Results Of The Functions In The Pool."""
        out = []
        for x in xrange(0, len(self.procs)):
            out.append(self.queue.get())
        return out
