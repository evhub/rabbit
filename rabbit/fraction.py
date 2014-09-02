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

from .carrot.format import *
from .carrot.math import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class negative(numobject):
    """Implements Curried Subtraction."""
    evaltype = "-"

    def __init__(self, item):
        """Creates The Negative Object."""
        self.n = item

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("negative", itemstate(self.n))

    def copy(self):
        """Copies The Negative Object."""
        return negative(getcopy(self.n))

    def calc(self):
        """Calculates The Negative Object."""
        return -self.n

    def __iadd__(self, other):
        """Does The Curried Subtraction."""
        return other - self.n

class reciprocal(numobject):
    """Implements Curried Division."""
    evaltype = "/"
    n = 1.0

    def __init__(self, base):
        """Creates The Reciprocal Object."""
        self.d = base

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("reciprocal", itemstate(self.d))

    def copy(self):
        """Copies The Reciprocal Object."""
        return reciprocal(getcopy(self.d))

    def calc(self):
        """Calculates The Reciprocal."""
        return self.n/self.d

    def __imul__(self, other):
        """Does The Curried Division."""
        return self.n*other/self.d

class fraction(numobject):
    """Implements A Fraction."""
    evaltype = "fraction"

    def __init__(self, n=0, d=1):
        """Constructs The Fraction."""
        self.n = n
        self.d = d

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("fraction", itemstate(self.n), itemstate(self.d))

    def copy(self):
        """Copies The Fraction Object."""
        return fraction(self.n, self.d)

    def simplify(self):
        """Simplifies The Fraction."""
        ns = primefactor(self.n)
        ds = primefactor(self.d)
        for x in ns:
            if x in ds:
                self.n /= x
                self.d /= x
                ds.remove(x)
        if self.d < 0 and self.n > 0:
            self.n *= -1
            self.d *= -1

    def simptens(self):
        """Simplifies All Multiples Of 10."""
        ns = repr(self.n).replace("L","").split(".", 1)
        ds = repr(self.d).replace("L","").split(".", 1)
        ni = ns[0]
        di = ds[0]
        if len(ns) > 1:
            nf = ns[1]
        else:
            nf = ""
        if len(ds) > 1:
            df = ds[1]
        else:
            df = ""
        if "e" in nf:
            nf, ne = nf.split("e")
            ni += "0"*int(ne)
        if "e" in df:
            df, de = df.split("e")
            di += "0"*int(de)
        while ni.endswith("0") and di.endswith("0") and len(ni) > 1 and len(di) > 1:
            ni = ni[:-1]
            di = di[:-1]
        if nf == "":
            self.n = int(ni)
        else:
            self.n = float(ni+"."+nf)
        if df == "":
            self.d = int(di)
        else:
            self.d = float(di+"."+df)

    def collapse(self):
        """Performs The Division."""
        return self.n/self.d

    def getfloat(self):
        """Retrieves A Float."""
        return float(self.n)/float(self.d)

    def __int__(self):
        """Retrieves An Integer."""
        return int(self.n//self.d)

    def __repr__(self):
        """Retrieves A String."""
        return "("+str(self.n)+")/("+str(self.d)+")"

    def __idiv__(self, other):
        """Performs Division In-Place."""
        if isinstance(other, fraction):
            self.n *= other.d
            self.d *= other.n
        else:
            self.d *= other
        return self

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        if isinstance(other, fraction):
            self.n *= other.n
            self.d *= other.d
        else:
            self.n *= other
        return self

    def __div__(self, other):
        """Performs Division."""
        out = fraction(self.n, self.d)
        if isinstance(other, fraction):
            out.n *= other.d
            out.d *= other.n
        else:
            out.d *= other
        return out

    def __mul__(self, other):
        """Performs Multiplication."""
        out = fraction(self.n, self.d)
        if isinstance(other, fraction):
            out.n *= other.n
            out.d *= other.d
        else:
            out.n *= other
        return out

    def __ipow__(self, other):
        """Performs Exponentitation In-Place."""
        if isinstance(other, fraction):
            self **= other.n
            self /= self**other.d
        else:
            self.n **= other
            self.d **= other
        return self

    def __pow__(self, other):
        """Performs Exponentiation."""
        out = fraction(self.n, self.d)
        if isinstance(other, fraction):
            out **= other.n
            out /= out**other.d
        else:
            out.n **= other
            out.d **= other
        return out

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        return other**self.n/other**self.d

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        return other*fraction(self.d, self.n)

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        if isinstance(other, fraction):
            self.n *= other.d
            self.n += other.n*self.d
            self.d *= other.d
        else:
            self.n += other*self.d
        return self

    def __add__(self, other):
        """Performs Addition."""
        out = fraction(self.n, self.d)
        if isinstance(other, fraction):
            out.n *= other.d
            out.n += other.n*self.d
            out.d *= other.d
        else:
            out.n += other*self.d
        return out

    def same(self, other):
        """Tests Identity."""
        if isinstance(other, fraction):
            if self.n == other.n and self.d == other.d:
                return True
            else:
                return False
        else:
            if self.d == 1 and self.n == other:
                return True
            else:
                return False

def fractionstr(inputstr, converter=float):
    """Converts A Fraction String Back Into A Fraction."""
    n,d=basicformat(inputstr).split("/")
    return fraction(converter(basicformat(n)), converter(basicformat(d)))

def fractionfloat(inputfloat, replen=16):
    """Converts A Float Into A Fraction."""
    inputfloat = float(inputfloat)
    if isinstance(inputfloat, old_float):
        replen = int(replen)
        intpart, floatpart = repr(inputfloat).split(".", 1)
        if intpart.startswith("-"):
            intpart = intpart[1:]
            sign = -1
        else:
            sign = 1
        if "e" in floatpart:
            floatpart, exppart = floatpart.split("e", 1)
            exppart = exppart
        else:
            exppart = 0
        out = fraction(int(intpart))
        if len(floatpart) >= replen-len(intpart):
            floatstart, floatrep = repeating(floatpart[:-1])
            if floatstart != "":
                out += fraction(int(floatstart), 10**len(floatstart))
            if floatrep != "":
                out += fraction(int(floatrep), 10**len(floatstart)*(10**len(floatrep)-1))
        else:
            out += fraction(int(floatpart), 10**len(floatpart))
        out *= sign*10**int(exppart)
        return out
    else:
        return fraction(inputfloat)
