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

from .sys import *
import md5

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class random(object):
    """A Class For Generating And Applying Pseudorandom Numbers."""
    def __init__(self, key=None):
        """Initializes The Random Number Generator."""
        if key == None:
            self.key = os.urandom(16)
        else:
            self.key = md5.new(key).digest()
        self.basestate = md5.new(self.key)
        self.counter = 0

    def goto(self, position=0):
        """Advances The Random Number Generator To A Position."""
        self.counter = position
        self.state = self.basestate.copy()
        self.state.update(str(self.counter))

    def advance(self, amount=1):
        """Advances The Random Number Generator."""
        self.goto(self.counter+amount)

    def getraw(self):
        """Returns A Random String Of Length 16."""
        self.advance()
        return self.state.digest()

    def gethex(self):
        """Returns A Random Hexadecimal String Of Length 32."""
        self.advance()
        return self.state.hexdigest()

    def get(self):
        """Returns A Random Integer In The Range [0, 340282366920938463463374607431768211455]."""
        return int(self.gethex(), 16)

    def getbits(self, bits=1):
        """Returns Random Bits Of A Certain Amount."""
        bitstring = ""
        for x in xrange(0, (bits+127)/128):
            bitstring += self.gethex()
        bitstring = int(bitstring, 16)
        for x in xrange(0, ((bits+127)/128)*128-bits):
            bitstring = bitstring >> 1
        return bitstring

    def getbool(self):
        """Returns A Random Boolean."""
        return bool(self.getbits(1))

    def getdigits(self, digits=1):
        """Returns Random Digits Of A Certain Amount."""
        digitstring = ""
        while len(digitstring) < digits:
            digitstring += str(self.get())[1:]
        while len(digitstring) > digits:
            digitstring = digitstring[1:]
        return digitstring

    def getfloat(self):
        """Returns A Random Float In The Range [0, 1]."""
        return self.get()/340282366920938463463374607431768211455.0

    def trial(self, p=0.5):
        """Returns True With Probability Equal To p."""
        if self.getfloat() <= p:
            return True
        else:
            return False

    def getkey(self):
        """Returns The Seed Key."""
        return self.key

    def getpos(self):
        """Returns The Current Position."""
        return self.counter

    def choosefloat(self, rangestop):
        """Chooses A Random Float From The Range [0, rangestop]."""
        return self.getfloat()*rangestop

    def chooseint(self, rangestop):
        """Chooses A Random Integer From The Range [0, rangestop)."""
        rangestop = int(rangestop)
        if rangestop == 0:
            return 0
        ranges = []
        stop = 0.0
        for x in xrange(0, rangestop):
            start = stop
            stop += 340282366920938463463374607431768211455.0/rangestop
            ranges.append([start, stop])
        while True:
            value = self.get()
            for x in xrange(0, rangestop):
                if isreal(value, ranges[x][0], ranges[x][1]) != None:
                    return x

    def chooserange(self, rangestart, rangestop):
        """Chooses A Random Integer From The Range [rangestart, rangestop)."""
        return self.chooseint(rangestop-rangestart)+rangestart

    def choosefloatrange(self, rangestart, rangestop):
        """Chooses A Random Float From The Range [rangestart, rangestop]."""
        return self.choosefloat(rangestop-rangestart)+rangestart

    def choose(self, inputlist):
        """Chooses A Random Item From A List."""
        return inputlist[self.chooseint(len(inputlist))]

    def split(self, inputlist, groups=2):
        """Randomly Splits A List Into Groups."""
        outputlist = []
        for x in xrange(0, groups):
            outputlist.append([])
        newlist = inputlist[:]
        while len(newlist) > 0:
            listchoose = self.chooseint(len(outputlist))
            if len(outputlist[listchoose])+1 <= (len(inputlist)+groups-1)/groups:
                appendchoice = self.choose(newlist)
                outputlist[listchoose].append(appendchoice)
                newlist.remove(appendchoice)
        return outputlist

    def shift(self, inputlist):
        """Randomly Shifts A List."""
        start = self.chooseint(len(inputlist))
        outputlist = []
        for x in xrange(0, len(inputlist)):
            outputlist.append(inputlist[(x+start)%len(inputlist)])
        return outputlist

    def take(self, inputlist, amount=1):
        """Randomly Take A Certain Amount Of Elements From A List."""
        newlist = inputlist[:]
        outputlist = []
        for x in xrange(0, amount):
            choice = self.choose(newlist)
            outputlist.append(choice)
            newlist.remove(choice)
        return outputlist

    def scramble(self, inputlist):
        """Randomizes The Order Of A List."""
        return self.take(inputlist, len(inputlist))
