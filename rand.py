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

from __future__ import absolute_import

from .sys import *
from .math import *
import md5

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class random(object):
    """A Class For Generating And Applying Pseudorandom Numbers."""
    maxget = 340282366920938463463374607431768211455

    def __init__(self, key=None, debug=False):
        """Initializes The Random Number Generator."""
        self.debug = bool(debug)
        if key == None:
            self.key = os.urandom(16)
        else:
            self.key = md5.new(key).digest()
        self.basestate = md5.new(self.key)
        self.counter = 0
        self.bitstore = ""
        self.digitstore = ""

    def goto(self, position=0):
        """Advances The Random Number Generator To A Position."""
        position = int(position)
        if self.counter != position:
            self.counter = position
            self.state = self.basestate.copy()
            self.state.update(str(self.counter))

    def advance(self, amount=1):
        """Advances The Random Number Generator."""
        amount = int(amount)
        if amount != 0:
            self.goto(self.counter+amount)
            self.bitstore = ""
            self.digitstore = ""

    def getraw(self, times=1):
        """Returns A Random Unicode String Of Length 16."""
        rawstring = ""
        for x in xrange(0, int(times)):
            self.advance()
            rawstring += self.state.digest()
        if self.debug and times > 0:
            print("Generated Raw: "+repr(rawstring))
        return rawstring

    def gethex(self, times=1):
        """Returns A Random Hexadecimal String Of Length 32."""
        hexstring = ""
        for x in xrange(0, int(times)):
            self.advance()
            hexstring += self.state.hexdigest()
        if self.debug and times > 0:
            print("Generated Int: "+hexstring+" | "+str(int(hexstring, 16))+" | "+bin(int(hexstring, 16))[2:])
        return hexstring

    def get(self, times=1):
        """Returns A Random Integer In The Range [0, maxget]."""
        return int(self.gethex(times) or "0", 16)

    def getbits(self, bits=1):
        """Returns Random Bits Of A Certain Amount."""
        newbits = bits
        bitstring = ""
        while newbits > 0 and len(self.bitstore) > 0:
            bitstring += self.bitstore[0]
            self.bitstore = self.bitstore[1:]
            newbits -= 1
        bit_length = self.maxget.bit_length()
        tests = (newbits+bit_length-1)/bit_length
        for x in xrange(0, tests):
            test = bin(self.get(tests))[2:]
            while len(test) < bit_length:
                test = "0"+test
            bitstring += test
        self.bitstore += bitstring[bits:]
        return int(bitstring[:bits], 2)

    def getbool(self):
        """Returns A Random Boolean."""
        return bool(self.getbits(1))

    def getdigits(self, digits=1):
        """Returns Random Digits Of A Certain Amount."""
        newdigits = digits
        digitstring = ""
        while newdigits > 0 and len(self.digitstore) > 0:
            digitstring += self.digitstore[0]
            self.digitstore = self.digitstore[1:]
            newdigits -= 1
        while len(digitstring) < digits:
            test = float("inf")
            while test > int(str(self.maxget)[0])*10.0**len(str(self.maxget)):
                test = self.get()
            test = str(test)
            if len(test) >= len(str(self.maxget)):
                test = test[1:]
            while len(test) < len(str(self.maxget))-1:
                test = "0"+test
            digitstring += test
        self.digitstore += digitstring[digits:]
        return int(digitstring[:digits])

    def getfloat(self):
        """Returns A Random Float In The Range [0, 1]."""
        return self.get()/float(self.maxget)

    def trial(self, p=0.5):
        """Returns True With Probability Equal To p."""
        if self.getfloat() < p:
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
        tests = int(math.ceil(rangestop/float(self.maxget)))
        endpoint = float(rangestop)*self.maxget/rangestop
        test = float("inf")
        while test > endpoint:
            test = self.get(tests)
        return test % rangestop

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
