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

from .format import *
from .rand import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class matrix(mctobject):
    """Implements A Mathematical Matrix."""

    def __init__(self, y, x=None, empty=0.0, converter=float, fake=False):
        """Constructs The Matrix."""
        self.y = int(y)
        if x == None:
            self.x = self.y
        else:
            self.x = int(x)
        self.converter = converter
        empty = self.prepare(empty)
        self.a = []
        if fake:
            temp = fakelist(default=empty, length=self.x)
        else:
            temp = [empty]*self.x
        for z in xrange(0, self.y):
            self.a.append(temp[:])

    def new(self, y=None, x=None, fake=None):
        """Creates A New Matrix With The Same Basic Attributes."""
        if fake == None:
            fake = self.onlydiag()
        return matrix(y or self.y, x or self.x, converter=self.converter, fake=fake)

    def copy(self):
        """Creates A Copy Of The Matrix."""
        out = self.new()
        for y,x in self.coords():
            out.store(y,x, self.retreive(y,x))
        return out

    def code(self, func):
        """Codes A Function Over The Matrix."""
        for y,x in self.coords():
            self.store(y,x, func(self.retreive(y,x)))

    def prepare(self, v):
        """Prepares A Value."""
        if isinstance(v, matrix):
            v.converter = self.converter
            return v
        elif iseval(v):
            return v
        else:
            return self.converter(v)

    def convert(self, converter=None):
        """Converts All The Values Using The Converter."""
        if converter != None:
            self.converter = converter
        self.code(self.prepare)

    def store(self, y, x, v):
        """Stores A Value."""
        self.a[int(y)][int(x)] = self.prepare(v)

    def retreive(self, y=0, x=None):
        """Retreives A Value."""
        if x == None:
            x = y
        return self.a[int(y)][int(x)]

    def items(self):
        """Returns A List Of All Items In A Matrix."""
        out = []
        for y,x in self.coords():
            out.append(self.retreive(y, x))
        return out

    def trans(self):
        """Finds The Transpose."""
        out = self.copy()
        out.flip()
        return out

    def flip(self):
        """Flips The Matrix."""
        a = []
        for x in xrange(0, self.x):
            a.append([])
            for y in xrange(0, self.y):
                a[x].append(self.a[y][x])
        self.a = a
        y = self.y
        x = self.x
        self.y = x
        self.x = y

    def __len__(self):
        """Performs len."""
        return self.y*self.x

    def __repr__(self):
        """Gets A Representation."""
        return str(self.a)

    def __str__(self):
        """Performs str."""
        return strlist(self.a, "\n")

    def __getitem__(self, y):
        """Retreives A Row."""
        return self.a[y][:]

    def __mul__(self, other):
        """Performs Multiplication."""
        if isinstance(other, matrix):
            if self.x == other.y:
                out = self.new(self.y, other.x)
                for y,x in out.coords():
                    v = 0
                    for z in xrange(0, self.x):
                        v += self.retreive(y, z)*other.retreive(z, x)
                    out.store(y, x, v)
            elif self.onlyrow() and other.onlyrow() and self.x == other.x:
                out = self*other.trans()
                out = out.retreive(0, 0)
            else:
                raise IndexError
        else:
            out = self.new()
            for y,x in self.coords():
                out.store(y, x, self.retreive(y, x)*other)
        return out

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        if isinstance(other, matrix):
            self = self*other
        else:
            for y,x in self.coords():
                self.store(y, x, self.retreive(y, x)*other)
        return self

    def __add__(self, other):
        """Performs Addition."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                out = self.new()
                for y,x in self.coords():
                    out.store(y, x, self.retreive(y, x)+other.retreive(y, x))
            else:
                raise IndexError
        elif other == 0:
            out = self.copy()
        elif self.onlydiag():
            length = self.lendiag()
            out = self.new(length, length)
            for x in xrange(0, length):
                out.store(x, x, self.retreive(x)+other)
        else:
            out = self.new()
            for y in xrange(0, self.y):
                for x in xrange(0, self.x):
                    out.store(y, x, self.retreive(y, x)+other)
        return out

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                for y,x in self.coords():
                    self.store(y, x, self.retreive(y, x)+other.retreive(y, x))
            else:
                raise IndexError
        elif other != 0 and self.onlydiag():
            for x in xrange(0, self.lendiag()):
                self.store(x, x, self.retreive(x)+other)
        elif other != 0:
            for y,x in self.coords():
                self.store(y, x, self.retreive(y, x)+other)
        return self

    def __pow__(self, other):
        """Performs Exponentiation."""
        if hasnum(other):
            other = int(other)
            if other > 0:
                out = self.copy()
                for x in xrange(1, other):
                    out *= self
                return out
            elif other == 0:
                return diagmatrix(self.x, converter=self.converter)
            elif self.det() != 0.0:
                return self.inv(False)**(-1.0*other)
            else:
                raise IndexError
        else:
            raise TypeError

    def __ipow__(self, other):
        """Performs Exponentiation In-Place."""
        if hasnum(other):
            other = int(other)
            if other > 0:
                for x in xrange(1, other):
                    self *= self
            elif other == 0:
                self = diagmatrix(self.x, converter=self.converter)
            else:
                self = self.inv()
                self **= -1.0*other
            return self
        else:
            raise TypeError

    def __div__(self, other):
        """Performs Division."""
        if hasnum(other):
            out = self.new()
            for y,x in self.coords():
                out.store(y, x, self.retreive(y, x)/other)
            return out
        else:
            raise TypeError

    def __idiv__(self, other):
        """Performs Division In-Place."""
        if hasnum(other):
            for y,x in self.coords():
                self.store(y, x, self.retreive(y, x)/other)
            return self
        else:
            raise TypeError

    def __imod__(self, other):
        """Performs Modulus In-Place."""
        if isinstance(other, matrix):
            self = self.cross(other)
        else:
            self.code(lambda x: x%other)
        return self

    def __mod__(self, other):
        """Performs Modulus."""
        if isinstance(other, matrix):
            out = self.cross(other)
        else:
            out = self.new()
            for y,x in self.coords():
                out.store(y, x, self.retreive(y, x)%other)
        return out

    def __abs__(self):
        """Performs abs."""
        out = self**2.0
        return sum(out.items())**0.5

    def entries(self):
        """Returns A List Of Items With Coordinates."""
        out = []
        for y,x in self.coords():
            out.append((y,x,self.retreive(y,x)))
        return out

    def coords(self):
        """Returns A List Of Coordinates."""
        out = []
        for y in xrange(0, self.y):
            for x in xrange(0, self.x):
                out.append((y,x))
        return out

    def scaledrow(self, y, scaler=1.0):
        """Retreives A Scaled Row."""
        out = self[y]
        for x in xrange(0, len(out)):
            out[x] = out[x]*scaler
        return out

    def scalerow(self, y, scaler=1.0):
        """Scales A Row."""
        for x in xrange(0, self.x):
            self.store(y,x, self.retreive(y,x)*scaler)

    def addrow(self, y, addlist):
        """Adds A Row With A List."""
        for x in xrange(0, self.x):
            self.store(y,x, self.retreive(y,x)+addlist[x])

    def addedrow(self, y, addlist):
        """Retreives A Row Added With A List."""
        out = self[y]
        for x in xrange(0, len(out)):
            out[x] = out[x]+addlist[x]
        return out

    def fill(self, func=lambda: random().getdigits(1)):
        """Fills The Matrix With The Results From A Function."""
        for y,x in self.coords():
            self.store(y,x, func())

    def newrow(self, rowlist):
        """Appends A New Row."""
        if islist(rowlist[0]):
            for row in rowlist:
                self.newrow(row)
        elif len(rowlist) == self.x:
            for x in xrange(0, len(rowlist)):
                rowlist[x] = self.prepare(rowlist[x])
            self.a.append(rowlist)
            self.y += 1
        else:
            raise IndexError

    def delrow(self, y):
        """Deletes A Row."""
        self.a.pop(y)
        self.y -= 1

    def delcol(self, x):
        """Deletes A Column."""
        self.flip()
        self.delrow(x)
        self.flip()

    def minor(self, y, x):
        """Returns The Minor Matrix Without The Given Row And Column."""
        out = self.copy()
        out.delrow(y)
        out.delcol(x)
        return out

    def cross(self, other):
        """Finds The Cross Product With Another Matrix."""
        if self.x == other.x:
            cross = self.copy()
            for row in other.a:
                cross.newrow(row)
            cross.newrow([self.prepare(1.0)]*cross.x)
            out = cross.new(1)
            for x in xrange(0, out.x):
                out.store(0,x, cross.minor(cross.y-1, x).det())
            return out
        else:
            raise IndexError

    def C(self, y, x):
        """Finds The Cofactor For The Given Row And Column."""
        return self.minor(y,x).det()*(-1.0)**(y+x+2.0)

    def det(self):
        """Finds The Determinant Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return None
        elif self.x == 1 or self.y == 1:
            return self.retreive(0,0)
        else:
            out = 0.0
            for x in xrange(0, self.x):
                out += self.retreive(1,x)*self.C(1,x)
            return out

    def inv(self, check=True, maxtries=float("inf"), debug=False):
        """Finds The Inverse Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return matrix(0)
        elif self.x == 1 or self.y == 1:
            return self*self.retreive(0,0)**-1.0
        elif not (check and self.det() == 0.0):
            size = self.y
            out = self.copy()
            out.augment(diagmatrix(size))
            out.keepsolvingfull(False, maxtries, debug)
            return matrixlist(out.getaugment(size), self.converter).trans()

    def augment(self, aug):
        """Augments The Matrix."""
        self.flip()
        if islist(aug) and len(aug) == self.y:
            self.newrow(aug)
        elif isinstance(aug, matrix) and aug.y == self.y:
            for row in aug.trans().a:
                self.newrow(row)
        self.flip()

    def getaugment(self, auglen=None):
        """Gets The Augment."""
        if auglen == None:
            auglen = self.x-self.y
        else:
            auglen = int(auglen)
        return self.trans().a[-auglen:]

    def solve(self, debug=False):
        """Solves The Matrix As An Augmented Matrix."""
        for y,x in self.coords():
            if x == y:
                if debug:
                    print("Scale Row "+str(y)+" By 1/"+str(self.retreive(y,x)))
                self.scalerow(y, 1.0/self.retreive(y,x))
                if debug > 1:
                    print(self)
            elif x < y:
                if debug:
                    print("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retreive(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retreive(y,x)))
                if debug > 1:
                    print(self)

    def solvetop(self, debug=False):
        """Solves The Top Of The Matrix As An Augmented Matrix."""
        for y,x in reversed(self.coords()):
            if x == y:
                if debug:
                    print("Scale Row "+str(y)+" By 1/"+str(self.retreive(y,x)))
                self.scalerow(y, 1.0/self.retreive(y,x))
                if debug > 1:
                    print(self)
            elif x < self.y and x > y:
                if debug:
                    print("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retreive(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retreive(y,x)))
                if debug > 1:
                    print(self)

    def solvefull(self, debug=False):
        """Fully Solves The Matrix As An Augmented Matrix."""
        self.solvetop(debug)
        self.solve(debug)

    def mixrows(self, func=lambda a: random().scramble(a)):
        """Scrambles The Rows Using A Function."""
        self.a = func(self.a)

    def keepsolving(self, check=True, maxtries=float("inf"), debug=False):
        """Recursively Solves The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError
        elif maxtries > 0:
            try:
                self.solve(debug)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    print("Mix Rows")
                    print(self)
                self.keepsolving(False, maxtries-1.0, debug)

    def keepsolvingtop(self, check=True, maxtries=float("inf"), debug=False):
        """Recursively Solves The Top Of The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError
        elif maxtries > 0:
            try:
                self.solvetop(debug)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    print("Mix Rows")
                    print(self)
                self.keepsolvingtop(False, maxtries-1.0, debug)

    def keepsolvingfull(self, check=True, maxtries=float("inf"), debug=False):
        """Recursively Fully Solves The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError
        elif maxtries > 0:
            try:
                self.solvefull(debug)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    print("Mix Rows")
                    print(self)
                self.keepsolvingfull(False, maxtries-1.0, debug)

    def solutions(self):
        """Retreives The Solutions For A Solved Augmented Matrix."""
        answers = []
        for y in reversed(xrange(0, self.y)):
            answer = self.retreive(y,self.y)
            i = 0
            for x in reversed(xrange(y+1, self.y)):
                answer -= self.retreive(y,x)*answers[i]
                i += 1
            answers.append(answer)
        answers.reverse()
        return answers

    def topsolutions(self):
        """Retreives The Solutions For A Top Solved Augmented Matrix."""
        answers = []
        for y in xrange(0, self.y):
            answer = self.retreive(y,self.y)
            i = 0
            for x in xrange(0,y):
                answer -= self.retreive(y,x)*answers[i]
                i += 1
            answers.append(answer)
        return answers

    def swaprows(self, ya, yb):
        """Swaps Two Rows."""
        self.a[ya], self.a[yb] = self[yb], self[ya]

    def lendiag(self):
        """Returns The Length Of The Main Diagonal."""
        if self.y <= self.x:
            return self.y
        else:
            return self.x

    def getdiag(self):
        """Returns The Main Diagonal."""
        out = []
        for x in xrange(0, self.lendiag()):
            out.append(self.retreive(x))
        return out

    def onlydiag(self):
        """Determines If The Matrix Is A Diagonal List."""
        for x in self.a:
            if not isinstance(x, fakelist):
                return False
        for y,x in self.coords():
            if y != x and self.a[y][x] != self.prepare(0.0):
                return False
        return True

    def onlyrow(self):
        """Determines If The Matrix Is A Row List."""
        return self.y <= 1

    def getitems(self):
        """Gets Items Or The Diagonal."""
        if self.onlydiag():
            return self.getdiag()
        else:
            return self.items()

    def getlen(self):
        """Gets The Length Of Items Or The Diagonal."""
        if self.onlydiag():
            return self.lendiag()
        else:
            return len(self)

    def __round__(self, n=0):
        """Performs round."""
        out = self.copy()
        for y,x in out.coords():
            out.store(y,x, round(out.retreive(y,x), n))
        return out

    def __float__(self):
        """Retreives A Float Of The First Item."""
        if len(self) == 0:
            return 0.0
        else:
            return float(self.retreive())

    def __int__(self):
        """Retreives An Integer Of The First Item."""
        if len(self) == 0:
            return 0
        else:
            return int(self.retreive())

    def df(self):
        """Finds The Degrees Of Freedom."""
        return (self.x-1.0)*(self.y-1.0)

    def ymarg(self, y):
        """Calculates A Marginal For The Given Row."""
        return sum(self.a[y])

    def xmarg(self, x):
        """Calculates A Marginal For The Given Column."""
        self.flip()
        out = self.ymarg(x)
        self.flip()
        return out

    def sum(self):
        """Calculates The Sum Of All The Items."""
        return sum(self.items())

    def indep(self):
        """Returns Expected Values For A Chi Squared Independence Test."""
        out = self.new()
        for y,x in self.coords():
            out.store(y,x, float(self.xmarg(x)*self.ymarg(y))/float(self.sum()))
        return out

    def chisq(self, expected=None):
        """Calculates Chi Squared For Independence."""
        if expected == None:
            expected = self.indep()
        if self.y == expected.y and self.x == expected.x:
            tot = 0.0
            for y,x in self.coords():
                tot += float(self.retreive(y,x)-expected.retreive(y,x))**2.0/float(expected.retreive(y,x))
            return tot
        else:
            raise IndexError

def diagmatrix(size=2, full=1.0, empty=0.0, converter=float, fake=True):
    """Constructs Matrix I."""
    size = int(size)
    I = matrix(size, size, empty, converter, fake)
    for x in xrange(0, size):
        I.store(x, x, full)
    return I

def matrixitems(inputitems, y, x=None):
    """Constructs A Matrix From Items."""
    if x == None:
        x = len(inputitems)/y
    out = matrix(y, x)
    z = 0
    for y,x in out.coords():
        out.store(y,x, inputitems[z])
        z += 1
    return out

def domatrixlist(inputlist, converter=float):
    """Turns A List Into A Matrix."""
    try:
        out = matrixlist(inputlist, converter)
    except:
        out = diagmatrixlist(inputlist, converter, domatrixlist)
    return out

def diagmatrixlist(inputlist, converter=float, func=None, fake=True):
    """Constructs A Diagonal Matrix From A List."""
    if func == None:
        func = diagmatrixlist
    out = matrix(len(inputlist), converter=converter, fake=fake)
    for x in xrange(0, len(inputlist)):
        if islist(inputlist[x]):
            inputlist[x] = func(inputlist[x])
        out.store(x,x, inputlist[x])
    return out

def rowmatrixlist(inputlist, converter=float, func=None, fake=False):
    """Constructs A Row Matrix From A List."""
    if func == None:
        func = rowmatrixlist
    out = matrix(1, len(inputlist), converter=converter, fake=fake)
    for x in xrange(0, len(inputlist)):
        if islist(inputlist[x]):
            inputlist[x] = func(inputlist[x])
        out.store(0,x, inputlist[x])
    return out

def matrixstr(inputstr, converter=float):
    """Converts A Matrix String Back Into A Matrix."""
    ys = basicformat(inputstr).split("\n")
    for x in xrange(0,len(ys)):
        ys[x] = basicformat(ys[x])[1:-1].split(",")
        for z in xrange(0, len(ys[x])):
            ys[x][z] = converter(ys[x][z])
    return matrixlist(ys, converter)

def matrixlist(inputlist, converter=float, fake=False):
    """Converts A List Of Lists Into A Matrix."""
    if converter == None:
        converter = type(inputlist[0][0])
    xlen = len(inputlist[0])
    for x in xrange(1,len(inputlist)):
        if len(inputlist[x]) != xlen:
            raise IndexError
    out = matrix(len(inputlist), xlen, converter=converter, fake=bool(fake))
    out.a = inputlist[:]
    out.convert()
    return out

def rangematrix(start, stop, step=1.0, fake=True):
    """Constructs A Matrix On A Range."""
    start = float(start)
    stop = float(stop)
    step = float(step)
    if stop < start:
        amount = int((start-stop)/step)
        out = matrix(amount, fake=fake)
        for x in xrange(0, amount):
            out.store(x, x, start)
            start -= step
    else:
        amount = int((stop-start)/step)
        out = matrix(amount, fake=fake)
        for x in xrange(0, amount):
            out.store(x, x, start)
            start += step
    return out

def totlen(inputlist):
    """Returns The Total Length Of An Object."""
    tot = 0.0
    for x in inputlist:
        if isinstance(x, matrix):
            tot += totlen(x.getitems())
        else:
            try:
                test = len(x)
            except:
                tot += 1.0
            else:
                tot += test
    return tot

def isnull(inputobject):
    """Determines If The Object Is An Empty Matrix."""
    return isinstance(inputobject, matrix) and len(inputobject) == 0

def nonull(inputlist):
    """Cleans The Input Of Empty Matrices."""
    return clean(inputlist, isnull, True)
