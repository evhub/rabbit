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
from .check import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class fakelist(cotobject):
    """Implements A Fake List."""
    def __init__(self, inputlist=None, default=None, length=0):
        """Creates A Fake List."""
        self.length = int(length)
        self.default = default
        self.a = {}
        if inputlist != None:
            self.extend(inputlist)

    def __len__(self):
        """Returns The Length."""
        return self.length

    def items(self):
        """Returns A Normal List."""
        out = []
        for x in xrange(0, len(self)):
            out.append(self[x])
        return out

    def move(self, amount):
        """Shifts The Whole List By An Amount."""
        amount = int(amount)
        self.length += amount
        new = {}
        for k,v in self.a.items():
            new[k+amount] = v
        self.a = new

    def __radd__(self, other):
        """Adds To The Beginning."""
        if islist(other):
            self.move(len(other))
            for x in xrange(0, len(other)):
                self.store(x, other[x])
        else:
            raise TypeError("Cannot add non-list to fake list")

    def append(self, item):
        """Appends An Item."""
        self.store(len(self), item)

    def new(self, length=None, inputlist=None):
        """Creates An Empty Fake List With The Same Parameters."""
        if length == None:
            length = len(self)
        return fakelist(inputlist, self.default, length)

    def copy(self):
        """Creates A Copy Of The Fake List."""
        out = self.new()
        for x in self.a:
            out[x] = self[x]
        return out

    def code(self, func):
        """Codes A Function Onto The Fake List."""
        self.default = func(self.default)
        for x in self.a:
            self[x] = func(self[x])

    def extend(self, inputlist):
        """Adds A List To The List."""
        for x in xrange(0, len(inputlist)):
            self.append(inputlist[x])

    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, (list, fakelist)):
            if len(self) == len(other):
                for x in xrange(0, len(self)):
                    if self[x] != other[x]:
                        return False
                return True
            else:
                return False
        else:
            try:
                test = other.items()
            except:
                return False
            else:
                return self == test

    def firstdefault(self):
        """Finds The First Occurence Of The Default Value."""
        for x in xrange(0, len(self)):
            if x not in self.a:
                return x

    def __contains__(self, other):
        """Determins If The Fake List Contains A Value."""
        if other == self.default and self.firstdefault != None:
            return True
        else:
            for x in self.a:
                if self[x] == other:
                    return True
            return False

    def __setitem__(self, x, item):
        """Checks An Index And Sets It To A Value."""
        if -1*len(self) < x and x < len(self):
            self.store(x, item)
        else:
            raise IndexError("Fake list could not set to invalid index "+repr(x))

    def store(self, x, item):
        """Sets An Index To A Value."""
        x = int(x)
        if x < 0:
            x += len(self)
        if x >= len(self):
            self.length = x+1
        if not self.default is item:
            self.a[x] = item

    def __getitem__(self, x):
        """Gets The Value Of An Index."""
        x = int(x)
        if x < 0:
            x += len(self)
        if x in self.a:
            return self.a[x]
        elif x < len(self):
            return self.default
        else:
            raise IndexError("Fake list could not retrieve invalid index "+repr(x))

    def __getslice__(self, start, stop, step=1):
        """Gets A Fake Slice."""
        step = int(step)
        if step == 0:
            return self.new(0)
        elif step < 0:
            self.reverse()
            return self[start:stop:-step]
        else:
            start = int(start)
            if start < 0:
                start += len(self)
            elif start > len(self):
                return self.new(0)
            stop = int(stop)
            if stop < 0:
                stop += len(self)
            elif stop > len(self):
                stop = len(self)
            if start > stop:
                raise IndexError("Fake list could not process invalid indice from "+repr(start)+" to "+repr(stop))
            out = self.new((stop-start)/step)
            for x in self.a:
                if start <= x and x < stop and x%step == 0:
                    out.a[x-start] = self.a[x]
            return out

    def sort(self):
        """Sorts The Fake List."""
        new = self.a.values()
        new.append(self.default)
        new.sort()
        m = new.index(self.default)
        a,b = new[:m], new[m+1:]
        out = {}
        for x in xrange(0, len(a)):
            out[x] = a[x]
        for x in xrange(1, len(b)+1):
            out[len(self)-x] = b[-x]
        self.a = out

    def __delitem__(self, x):
        """Deletes The Item At The Index."""
        x = int(x)
        if x < 0:
            x += len(self)
        if x in self.a:
            del self.a[x]
        elif self[x] != self.default:
            raise IndexError("Fake list could not delete invalid index "+repr(x))
        for y in xrange(x+1, len(self)):
            if y in self.a:
                self.a[y-1] = self.a[y]
                del self.a[y]
        self.length -= 1

    def remove(self, item):
        """Removes The First Occurence Of An Item."""
        del self[self.index(item)]       

    def index(self, item):
        """Finds The First Occurence Of An Item."""
        out = []
        if item == self.default:
            test = self.firstdefault()
            if test != None:
                out.append(test)
        for x in self.a:
            if self[x] == item:
                out.append(x)
                break
        if len(out) == 0:
            raise IndexError("Fake list could not find index for item "+repr(item))
        elif len(out) == 1:
            return out[0]
        else:
            return min(out)

    def pop(self, x=None):
        """Pops The Item At The Index."""
        if x == None:
            x = -1
        else:
            x = int(x)
        if x < 0:
            x += len(self)
        out = self[x]
        del self[x]
        return out

    def count(self, item):
        """Counts The Occurences Of An Item."""
        out = 0
        for x in xrange(0, len(self)):
            if self[x] == item:
                out += 1
        return out

    def reverse(self):
        """Reverses The List."""
        out = {}
        for x in self.a:
            y = len(self)-x-1
            out[y] = self[x]
        self.a = out

    def __repr__(self):
        """Returns A Representation."""
        return str((self.default, self.a, len(self)))

def haskey(inputlist, key):
    """Checks To See If A Key Exists In A List."""
    try:
        temp = inputlist[key]
    except KeyError:
        return None
    except IndexError:
        return None
    else:
        return temp

def containsany(searchlist, itemlist):
    """Determines If A List Contains Any Of A Set Of Items."""
    for x in itemlist:
        if x in searchlist:
            return x
    return False

def clean(haystack, needle="", func=False):
    """Recursively Removes An Item From A List."""
    cleaned = []
    for x in haystack:
        if islist(x):
            cleaned.append(clean(x, needle))
        elif (not func and x != needle) or (func and not needle(x)):
            cleaned.append(x)
    return cleaned

def delist(inputlist):
    """Finds The First Item."""
    while islist(inputlist):
        if len(inputlist) == 0:
            break
        else:
            inputlist = inputlist[0]
    return inputlist

def mapto(keylist, termlist, nothing=None):
    """Maps A List Of Keys To A List of Terms."""
    outdict = {}
    for x in xrange(0, len(keylist)):
        outdict[keylist[x]] = haskey(termlist, x) or nothing
    extra = []
    if len(termlist) > len(keylist):
        for x in xrange(len(keylist), len(termlist)):
            extra.append(termlist[x])
    return outdict, extra

def useparams(params, maps, nothing=None):
    """Maps A Set Of Maps To A Set Of Parameters."""
    if isinstance(params, tuple):
        return mapto(maps, list(params), nothing)
    elif islist(params):
        return mapto(maps, params, nothing)
    else:
        newparams = {}
        for x in maps:
            newparams[x] = haskey(params, x) or nothing
        return newparams, []

def flip(inputdict):
    """Swaps The Keys And Terms In A Dictionary."""
    outputdict = {}
    for x,y in inputdict.items():
        outputdict[y] = x
    return outputdict

def islist(inputobject):
    """Determines If An Object Is A List."""
    return isinstance(inputobject, (list, fakelist))

def callfuncs(funclist, *args):
    """Calls A List Of Functions."""
    out = args
    for f in reversed(funclist):
        if hascall(f):
            if islist(out):
                out = f.call(out)
            elif isinstance(out, tuple):
                out = f.call(list(out))
            else:
                out = f.call([out])
        elif islist(out) or isinstance(out, tuple):
                out = f(*out)
        else:
            out = f(out)
    return out
