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

from .base import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class pathfinder(cotobject):
    """Implements Pathfinding."""

    def __init__(self, paths=None, debug=False):
        """Initializes The Paths."""
        self.debug = bool(debug)
        if paths == None:
            self.paths = []
        else:
            self.paths = paths
        self.gotsort = False

    def copy(self):
        """Creates A Copy."""
        out = pathfinder(self.paths, self.debug)
        out.gotsort = self.gotsort
        return out

    def add(self, connections, length=1.0):
        """Adds A Path."""
        self.paths.append((length, connections))
        self.gotsort = False

    def sort(self):
        """Sorts The Paths."""
        if not self.gotsort:
            self.paths.sort()
            self.gotsort = True

    def items(self):
        """Returns A List Of Nodes."""
        out = []
        for d,cs in self.paths:
            for x in cs:
                if x not in out:
                    out.append(x)
        return out

    def connections(self, node):
        """Returns A List Of All Connections To A Node."""
        out = []
        for d,cs in self.paths:
            if node in cs:
                ncs = cs[:]
                ncs.remove(node)
                out.append((d,ncs))
        return out

    def single(self, start, end):
        """Finds The Length Of A Single Path Between Two Nodes."""
        roads = self.connections(start)
        roads.sort()
        for d,cs in roads:
            if end in cs:
                return d
        return float("inf")

    def solve(self, start, end):
        """Finds The Shortest Possible Path Between Two Nodes."""
        self.sort()
        items = self.items()
        if start in items and end in items:
            unvisited = []
            for x in items:
                if x != start:
                    unvisited.append((self.single(start, x), [start], x))
            if self.debug:
                print(unvisited)
            while len(unvisited) > 0:
                unvisited.sort()
                if unvisited[0][2] == end:
                    unvisited[0][1].append(end)
                    return (unvisited[0][0], unvisited[0][1])
                elif unvisited[0][0] == float("inf"):
                    break
                else:
                    unvisited = self.update(unvisited)
                if self.debug:
                    print(unvisited)
        return (float("inf"), [start, end])

    def update(self, unvisited):
        """Updates A List Of Unvisited."""
        item = unvisited.pop(0)
        for x in xrange(0, len(unvisited)):
            v = item[0]+self.single(item[2], unvisited[x][2])
            if v < unvisited[x][0]:
                unvisited[x] = (v, item[1]+[item[2]], unvisited[x][2])
        return unvisited

    def __eq__(self, other):
        """Performs ==."""
        self.sort()
        if isinstance(other, pathfinder):
            other.sort()
            test = other.paths
        else:
            try:
                test = other.items()
            except AttributeError:
                test = other
        if self.paths == test:
            return True
        else:
            return False

    def __repr__(self):
        """Gets A Representation."""
        return str(self.paths)

    def __getitem__(self, key):
        """Retreives Paths For A Node."""
        return self.connections(key)
