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

from .rand import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class encoder(object):
    """A Formatting Class For Encoding Strings."""
    def __init__(self, key=None, level=16):
        """Initializes The Encoder."""
        self.charlist = []
        for x in string.printable:
            self.charlist.append(x)
        if key == None:
            self.key = random().getraw()
        else:
            self.key = key
        self.level = level

    def basic(self, inputstring):
        """Turns A String Into A List Of Data."""
        final = []
        for x in inputstring:
            final.append(self.charlist.index(x))
        return final

    def expand(self, inputstring):
        """Turns A String Into A String Integer While Preserving All Data."""
        output = ""
        for x in self.basic(inputstring):
            if x < 10:
                output += "0"+str(x)
            else:
                output += str(x)
        return output

    def compress(self, inputstring):
        """Turns A String Integer Back Into A String."""
        outstring = ""
        y = 0
        for x in inputstring:
            if y == 0:
                z = x
                y = 1
            elif y == 1:
                z += x
                outstring += self.charlist[int(z)]
                y = 0
        return outstring

    def encode(self, inputstring, entropy=""):
        """Encodes A Message Into A String."""
        inputint = self.intencode(inputstring, entropy)
        gen = random(entropy+str(self.level)+self.key+str(len(inputint)))
        slicer = gen.get()%len(inputint)
        return self.compress(inputint[:slicer]+str(gen.getdigits(1))+inputint[slicer:])

    def decode(self, inputcode, entropy=""):
        """Decodes A Message From A String."""
        inputint = self.expand(inputcode)
        gen = random(entropy+str(self.level)+self.key+str(len(inputint)-1))
        slicer = gen.get()%(len(inputint)-1)
        return self.intdecode(inputint[:slicer]+inputint[slicer+1:], entropy)

    def intencode(self, inputstring, entropy=""):
        """Encodes A Message Into An Integer."""
        inputint = str(int("1"+self.binencode(inputstring, entropy),2))
        gen = random(entropy+str(len(inputint))+str(self.level)+self.key)
        xdigits = gen.getdigits(len(inputint))
        newint = ""
        for x in xrange(0,len(inputint)):
            newint += str((int(inputint[x])+int(xdigits[x]))%10)
        return newint

    def intdecode(self, inputint, entropy=""):
        """Decodes A Message From An Integer."""
        gen = random(entropy+str(len(inputint))+str(self.level)+self.key)
        xdigits = gen.getdigits(len(inputint))
        newint = ""
        for x in xrange(0,len(inputint)):
            newint += str((int(inputint[x])-int(xdigits[x]))%10)
        return self.bindecode(bin(int(newint))[3:], entropy)

    def binencode(self, inputstring, entropy=""):
        """Encodes A Message Into Binary."""
        inputint = int("1"+self.expand(inputstring))
        binstring = bin(self.stream(inputint, entropy))[2:]
        while len(binstring) < inputint.bit_length():
            binstring = "0"+binstring
        return binstring

    def bindecode(self, inputbin, entropy=""):
        """Decodes A Message From Binary."""
        return self.compress(str(self.stream(int(inputbin,2), entropy, len(inputbin)))[1:])

    def stream(self, inputint, entropy="", length=None):
        """Encodes An Integer Into Another Integer."""
        if length == None:
            length = inputint.bit_length()
        gen = random(entropy+str(self.level)+str(length)+self.key)
        for x in xrange(0, self.level):
            inputint = inputint^gen.getbits(length)
        return inputint

    def getlevel(self):
        """Returns The Current Encryption Level."""
        return self.level

    def setlevel(self, level):
        """Sets The Encryption Level."""
        self.level = int(level)

    def getkey(self):
        """Returns The Current Key."""
        return self.key

    def setkey(self, key):
        """Sets The Key."""
        self.key = str(key)

    def randomkey(self):
        """Sets The Key To A Random Value."""
        self.key = random().getraw()

def keyexchange(send,receive,privatekey=None,
                prime=2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919,
                generator=2):
    """Performs A Diffie-Hellman Key Exchange."""
    if privatekey == None:
        privatekey = random().get()
    send(str(pow(generator, privatekey, prime)))
    return pow(int(receive()), privatekey, prime)
