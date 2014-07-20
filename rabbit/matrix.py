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

from __future__ import with_statement, absolute_import, print_function, unicode_literals

from .carrot.format import *
from .carrot.rand import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class matrix(mctobject):
    """Implements A Mathematical Matrix."""

    def __init__(self, y, x=None, empty=0.0, converter=float, fake=False):
        """Constructs The Matrix."""
        self.y = int(y)
        if x is None:
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

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        out = []
        for row in self.a:
            out.append([])
            for item in row:
                try:
                    item.getstate
                except AttributeError:
                    value = item
                else:
                    value = item.getstate()
                out[-1].append(value)
        return ("matrix", out, self.y, self.x, self.converter, self.onlydiag())

    def new(self, y=None, x=None, fake=None):
        """Creates A New Matrix With The Same Basic Attributes."""
        if fake is None:
            fake = self.onlydiag()
        return matrix(y or self.y, x or self.x, converter=self.converter, fake=fake)

    def copy(self, fake=None):
        """Creates A Copy Of The Matrix."""
        out = self.new(fake=fake)
        for y,x in self.coords():
            item = self.retrieve(y,x)
            out.store(y,x, getcopy(item))
        return out

    def calc(self):
        """Retrieves A Boolean."""
        return self.y != 0

    def code(self, func):
        """Codes A Function Over The Matrix."""
        for y,x in self.coords():
            self.store(y,x, func(self.retrieve(y,x)))

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
        if converter is not None:
            self.converter = converter
        self.code(self.prepare)

    def store(self, y, x, v):
        """Stores A Value."""
        self.a[int(y)][int(x)] = self.prepare(v)

    def retrieve(self, y=0, x=None):
        """Retrieves A Value."""
        if x is None:
            x = y
        return self.a[int(y)][int(x)]

    def items(self):
        """Returns A List Of All Items In A Matrix."""
        out = []
        for y,x in self.coords():
            out.append(self.retrieve(y, x))
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
        """Retrieves A Row."""
        return self.a[y][:]

    def __mul__(self, other):
        """Performs Multiplication."""
        if isinstance(other, matrix):
            if self.x == other.y:
                out = self.new(self.y, other.x)
                for y,x in out.coords():
                    v = 0
                    for z in xrange(0, self.x):
                        v += self.retrieve(y, z)*other.retrieve(z, x)
                    out.store(y, x, v)
            else:
                try:
                    out = self.dot(other)
                except IndexError:
                    raise IndexError("Matrix multiplication invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))
        else:
            out = self.new()
            for y,x in self.coords():
                out.store(y, x, self.retrieve(y, x)*other)
        return out

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        if isinstance(other, matrix):
            self = self*other
        else:
            for y,x in self.coords():
                self.store(y, x, self.retrieve(y, x)*other)
        return self

    def __add__(self, other):
        """Performs Addition."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                out = self.new()
                for y,x in self.coords():
                    out.store(y, x, self.retrieve(y, x)+other.retrieve(y, x))
            else:
                raise IndexError("Matrix addition invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))
        elif other == 0:
            out = self.copy()
        elif self.onlydiag():
            length = self.lendiag()
            out = self.new(length, length)
            for x in xrange(0, length):
                out.store(x, x, self.retrieve(x)+other)
        else:
            out = self.new()
            for y in xrange(0, self.y):
                for x in xrange(0, self.x):
                    out.store(y, x, self.retrieve(y, x)+other)
        return out

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                for y,x in self.coords():
                    self.store(y, x, self.retrieve(y, x)+other.retrieve(y, x))
            else:
                raise IndexError("Matrix addition invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))
        elif other != 0 and self.onlydiag():
            for x in xrange(0, self.lendiag()):
                self.store(x, x, self.retrieve(x)+other)
        elif other != 0:
            for y,x in self.coords():
                self.store(y, x, self.retrieve(y, x)+other)
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
            else:
                return self.inv()**(-other)
        else:
            raise TypeError("Matrix exponentiation invalid with "+repr(other))

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
                self **= -other
            return self
        else:
            raise TypeError("Matrix exponentiation invalid with "+repr(other))

    def __div__(self, other):
        """Performs Division."""
        if hasnum(other):
            out = self.new()
            for y,x in self.coords():
                out.store(y, x, self.retrieve(y, x)/other)
            return out
        else:
            raise TypeError("Matrix division invalid with "+repr(other))

    def __idiv__(self, other):
        """Performs Division In-Place."""
        if hasnum(other):
            for y,x in self.coords():
                self.store(y, x, self.retrieve(y, x)/other)
            return self
        else:
            raise TypeError("Matrix division invalid with "+repr(other))

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
                out.store(y, x, self.retrieve(y, x)%other)
        return out

    def __abs__(self):
        """Performs abs."""
        out = self**2.0
        if isinstance(out, matrix):
            out = sum(out.items())
        return out**0.5

    def entries(self):
        """Returns A List Of Items With Coordinates."""
        out = []
        for y,x in self.coords():
            out.append((y,x,self.retrieve(y,x)))
        return out

    def coords(self):
        """Returns A List Of Coordinates."""
        out = []
        for y in xrange(0, self.y):
            for x in xrange(0, self.x):
                out.append((y,x))
        return out

    def scaledrow(self, y, scaler=1.0):
        """Retrieves A Scaled Row."""
        out = self[y]
        for x in xrange(0, len(out)):
            out[x] = out[x]*scaler
        return out

    def scalerow(self, y, scaler=1.0):
        """Scales A Row."""
        for x in xrange(0, self.x):
            self.store(y,x, self.retrieve(y,x)*scaler)

    def addrow(self, y, addlist):
        """Adds A Row With A List."""
        for x in xrange(0, self.x):
            self.store(y,x, self.retrieve(y,x)+addlist[x])

    def addedrow(self, y, addlist):
        """Retrieves A Row Added With A List."""
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
        if len(rowlist) > 0:
            if islist(rowlist[0]):
                for row in rowlist:
                    self.newrow(row)
            elif len(rowlist) == self.x:
                for x in xrange(0, len(rowlist)):
                    rowlist[x] = self.prepare(rowlist[x])
                self.a.append(rowlist)
                self.y += 1
            else:
                raise IndexError("Unequal matrix row lengths for newrow of "+str(self.x)+" and "+str(len(rowlist)))

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

    def dot(self, other):
        """Finds The Dot Product With Another Matrix."""
        if self.onlyrow() and other.onlyrow() and self.x == other.x:
            out = self*other.trans()
            return out.retrieve(0, 0)
        else:
            raise IndexError("Matrix dot product invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    def cross(self, other):
        """Finds The Cross Product With Another Matrix."""
        if self.x == other.x:
            if self.x == 0:
                return other
            else:
                cross = self.copy()
                for row in other.a:
                    cross.newrow(row)
                cross.newrow([self.prepare(1.0)]*cross.x)
                out = cross.new(1)
                for x in xrange(0, out.x):
                    out.store(0,x, cross.minor(cross.y-1, x).det())
                return out
        else:
            raise IndexError("Matrix cross product invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    def C(self, y, x):
        """Finds The Cofactor For The Given Row And Column."""
        return self.minor(y,x).det()*(-1.0)**(y+x+2.0)

    def det(self):
        """Finds The Determinant Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return None
        elif self.x == 1 or self.y == 1:
            return self.retrieve(0,0)
        else:
            out = 0.0
            for x in xrange(0, self.x):
                out += self.retrieve(1,x)*self.C(1,x)
            return out

    def inv(self, check=True, maxtries=float("inf"), debug=False):
        """Finds The Inverse Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return matrix(0)
        elif self.x == 1 or self.y == 1:
            return self*self.retrieve(0,0)**-1.0
        elif not (check and self.det() == 0.0):
            size = self.y
            out = self.copy()
            out.augment(diagmatrix(size))
            out.keepsolvingfull(False, maxtries, debug)
            return matrixlist(out.getaugment(size), self.converter).trans()
        else:
            raise IndexError("Matrix inverse does not exist because of 0 determinant")

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
        if auglen is None:
            auglen = self.x-self.y
        else:
            auglen = int(auglen)
        return self.trans().a[-auglen:]

    def solve(self, debug=False):
        """Solves The Matrix As An Augmented Matrix."""
        for y,x in self.coords():
            if x == y:
                if debug:
                    print("Scale Row "+str(y)+" By 1/"+str(self.retrieve(y,x)))
                self.scalerow(y, 1.0/self.retrieve(y,x))
                if debug > 1:
                    print(self)
            elif x < y:
                if debug:
                    print("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retrieve(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retrieve(y,x)))
                if debug > 1:
                    print(self)

    def solvetop(self, debug=False):
        """Solves The Top Of The Matrix As An Augmented Matrix."""
        for y,x in reversed(self.coords()):
            if x == y:
                if debug:
                    print("Scale Row "+str(y)+" By 1/"+str(self.retrieve(y,x)))
                self.scalerow(y, 1.0/self.retrieve(y,x))
                if debug > 1:
                    print(self)
            elif x < self.y and x > y:
                if debug:
                    print("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retrieve(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retrieve(y,x)))
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
            raise ValueError("Matrix cannot be solved on bottom because of 0 determinant")
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
            raise ValueError("Matrix cannot be solved on top because of 0 determinant")
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
            raise ValueError("Matrix cannot be solved because of 0 determinant")
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
        """Retrieves The Solutions For A Solved Augmented Matrix."""
        answers = []
        for y in reversed(xrange(0, self.y)):
            answer = self.retrieve(y,self.y)
            i = 0
            for x in reversed(xrange(y+1, self.y)):
                answer -= self.retrieve(y,x)*answers[i]
                i += 1
            answers.append(answer)
        answers.reverse()
        return answers

    def topsolutions(self):
        """Retrieves The Solutions For A Top Solved Augmented Matrix."""
        answers = []
        for y in xrange(0, self.y):
            answer = self.retrieve(y,self.y)
            i = 0
            for x in xrange(0,y):
                answer -= self.retrieve(y,x)*answers[i]
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
            out.append(self.retrieve(x))
        return out

    def onlydiag(self):
        """Determines If The Matrix Is A Diagonal List."""
        for y in xrange(0, len(self.a)):
            if not (isinstance(self.a[y], fakelist) and (len(self.a[y].a) == 0 or (len(self.a[y].a) == 1 and y in self.a[y].a))):
                return False
        return True

    def rows(self):
        """Returns The Rows As Matrices."""
        out = []
        for row in self.a:
            new = self.new(1, len(row), fake=False)
            new.a[0] = row
            out.append(new)
        return out

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
            out.store(y,x, round(out.retrieve(y,x), n))
        return out

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
        if expected is None:
            expected = self.indep()
        if self.y == expected.y and self.x == expected.x:
            tot = 0.0
            for y,x in self.coords():
                tot += float(self.retrieve(y,x)-expected.retrieve(y,x))**2.0/float(expected.retrieve(y,x))
            return tot
        else:
            raise IndexError("Matrix Chi Squared invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    def tomatrix(self):
        """Returns self."""
        return self

def diagmatrix(size=2, full=1.0, empty=0.0, converter=float, fake=True):
    """Constructs Matrix I."""
    size = int(size)
    I = matrix(size, size, empty, converter, fake)
    for x in xrange(0, size):
        I.store(x, x, full)
    return I

def matrixitems(inputitems, y, x=None, converter=float, fake=False):
    """Constructs A Matrix From Items."""
    if x is None:
        x = len(inputitems)/y
    out = matrix(y, x, converter=converter, fake=fake)
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

def isnull(inputobject):
    """Determines If The Object Is An Empty Matrix."""
    return isinstance(inputobject, matrix) and inputobject.y == 0

def nonull(inputlist):
    """Cleans The Input Of Empty Matrices."""
    return clean(inputlist, isnull, True)

def diagmatrixlist(inputlist, converter=float, func=None, fake=True, clean=True):
    """Constructs A Diagonal Matrix From A List."""
    if func is None:
        func = diagmatrixlist
    out = matrix(len(inputlist), converter=converter, fake=fake)
    for x in xrange(0, len(inputlist)):
        if islist(inputlist[x]):
            inputlist[x] = func(inputlist[x])
        if not clean or not isnull(inputlist[x]):
            out.store(x,x, inputlist[x])
    return out

def rowmatrixlist(inputlist, converter=float, func=None, fake=False, clean=True):
    """Constructs A Row Matrix From A List."""
    if func is None:
        func = rowmatrixlist
    out = matrix(1, len(inputlist), converter=converter, fake=fake)
    for x in xrange(0, len(inputlist)):
        if islist(inputlist[x]):
            inputlist[x] = func(inputlist[x])
        if not clean or not isnull(inputlist[x]):
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
    if converter is None:
        converter = type(inputlist[0][0])
    xlen = len(inputlist[0])
    for x in xrange(1,len(inputlist)):
        if len(inputlist[x]) != xlen:
            raise IndexError("Unequal matrix row lengths for matrixlist of "+str(xlen)+" and "+str(len(inputlist[x])))
    out = matrix(len(inputlist), xlen, converter=converter, fake=bool(fake))
    out.a = inputlist[:]
    out.convert()
    return out

def rangematrix(start, stop, step=1.0, fake=True, converter=float):
    """Constructs A Matrix On A Range."""
    start = float(start)
    stop = float(stop)
    step = float(step)
    if step == 0:
        return matrix(0)
    else:
        rev = False
        if step < 0:
            step = -step
            rev = True
        out = []
        if stop < start:
            while start > stop:
                out.append(start)
                start -= step
        else:
            while start < stop:
                out.append(start)
                start += step
        if rev:
            out.reverse()
        return diagmatrixlist(out, converter=converter, fake=fake)

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
