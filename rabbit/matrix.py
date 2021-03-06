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

from .carrot.rand import *
from .carrot.format import *

global e
try:
    set_e
except:
    old_set_e = None
else:
    old_set_e = set_e
def set_e(new_e):
    """Sets The Evaluator Global."""
    global e
    if old_set_e is not None:
        old_set_e(new_e)
    e = new_e

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def proper(inputnum):
    """Puts A Number In Its Proper Form."""
    if isinstance(inputnum, (bool, complex)):
        return inputnum
    else:
        return float(inputnum)

class matrix(mctobject):
    """Implements A Mathematical Matrix."""

    def __init__(self, y, x=None, empty=0.0, converter=proper, fake=False):
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
                out[-1].append(itemstate(item))
        return ("matrix", out, self.y, self.x, self.converter, self.onlydiag())

    @rabbit
    def new(self, y=None, x=None, fake=None):
        """Creates A New Matrix With The Same Basic Attributes."""
        if y is None:
            y = self.y
        if x is None:
            x = self.x
        if fake is None:
            fake = self.onlydiag()
        return matrix(y, x, converter=self.converter, fake=fake)

    def copy(self, fake=None):
        """Creates A Copy Of The Matrix."""
        out = self.new(fake=fake)
        for y,x in self.coords(None):
            out.store(y,x, getcopy(self.retrieve(y,x)))
        return out

    def itemcall(item, params):
        """Retrieves Items."""
        e.overflow = params[2:]
        if not params:
            value = item.retrieve(0)
        elif len(params) == 1:
            if isinstance(params[0], matrix):
                value = item.retrieve(params[0].retrieve(0), params[0].retrieve(1))
            elif item.onlyrow():
                value = item.retrieve(0, params[0])
            else:
                value = item.retrieve(params[0])
        elif isinstance(params[0], matrix) and isinstance(params[1], matrix):
            if params[0].retrieve(0) < 0:
                params[0].store(0,0, params[0].retrieve(0)+item.y+1)
            if params[0].retrieve(1) < 0:
                params[0].store(1,1, params[0].retrieve(1)+item.x+1)
            if params[1].retrieve(0) < 0:
                params[1].store(0,0, params[1].retrieve(0)+item.y+1)
            if params[1].retrieve(1) < 0:
                params[1].store(1,1, params[1].retrieve(1)+item.x+1)
            if params[0].getdiag() == params[1].getdiag():
                value = matrix(1,1, item.retrieve(params[0].retrieve(0), params[0].retrieve(1)), fake=True)
            elif params[0].retrieve(0) == params[1].retrieve(0):
                out = item[params[0].retrieve(0)][params[0].retrieve(1):params[1].retrieve(1)+1]
                value = diagmatrixlist(out)
            elif params[0].retrieve(1) == params[1].retrieve(1):
                item.flip()
                out = item[params[0].retrieve(1)][params[0].retrieve(0):params[1].retrieve(0)+1]
                value = diagmatrixlist(out)
            else:
                out = []
                if params[0].retrieve(0) <= params[1].retrieve(0):
                    ymin, ymax = params[0].retrieve(0), params[1].retrieve(0)
                else:
                    ymin, ymax = params[1].retrieve(0), params[0].retrieve(0)
                if params[0].retrieve(1) <= params[1].retrieve(1):
                    xmin, xmax = params[0].retrieve(1), params[1].retrieve(1)
                else:
                    xmin, xmax = params[1].retrieve(1), params[0].retrieve(1)
                for y in xrange(ymin, ymax+1):
                    out.append([])
                    for x in xrange(xmin, xmax+1):
                        out[-1].append(item.retrieve(y,x))
                value = matrixlist(out)
        else:
            length = item.lendiag()
            if params[0] < 0:                
                params[0] += length+1
            if params[1] < 0:
                params[1] += length+1
            if params[0] == params[1]:
                value = matrix(1,1, item.retrieve(params[0]), fake=True)
            elif params[0] < params[1]:
                out = item.getdiag()[params[0]:params[1]]
                value = diagmatrixlist(out)
            else:
                out = item.getdiag()[params[1]:params[0]]
                out.reverse()
                value = diagmatrixlist(out)
        return value

    def calc(self):
        """Retrieves A Boolean."""
        return self.y != 0

    def code(self, func, diag=None):
        """Codes A Function Over The Matrix."""
        for y,x in self.coords(diag):
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

    @rabbit
    def retrieve(self, y=0, x=None):
        """Retrieves A Value."""
        if x is None:
            x = y
        return self.a[int(y)][int(x)]

    @rabbit
    def items(self):
        """Returns A List Of All Items In A Matrix."""
        out = []
        for y,x in self.coords(False):
            out.append(self.retrieve(y, x))
        return out

    @rabbit
    def trans(self):
        """Finds The Transpose."""
        out = getcopy(self)
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

    @rabbit
    def __len__(self):
        """Performs len."""
        return self.y*self.x

    @rabbit
    def __repr__(self):
        """Gets A Representation."""
        return str(self.a)

    @rabbit
    def __str__(self):
        """Performs str."""
        return strlist(self.a, "\n")

    @rabbit
    def __getitem__(self, y):
        """Retrieves A Row."""
        return self.a[y][:]

    @rabbit
    def __mul__(self, other):
        """Performs Multiplication."""
        if isinstance(other, matrix):
            if not len(self) and not len(other):
                if self.onlydiag():
                    return matrix(0)
                else:
                    return rowmatrixlist()
            elif not len(self) or not len(other):
                raise IndexError("Matrix multiplication invalid between empty matrix and non-empty matrix")
            elif self.x == other.y:
                out = self.new(self.y, other.x)
                for y,x in out.coords(False):
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
            out = getcopy(self)
            out.code(lambda x: x*other)
        return out

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        if isinstance(other, matrix):
            self = self*other
        else:
            self.code(lambda x: x*other)
        return self

    @rabbit
    def __add__(self, other):
        """Performs Addition."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                out = self.new()
                for y,x in self.coords(False):
                    out.store(y, x, self.retrieve(y, x)+other.retrieve(y, x))
            else:
                raise IndexError("Matrix addition invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))
        else:
            out = getcopy(self)
            out.code(lambda x: x+other)
        return out

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        if isinstance(other, matrix):
            if self.y == other.y and self.x == other.x:
                for y,x in self.coords(None):
                    self.store(y, x, self.retrieve(y, x)+other.retrieve(y, x))
            else:
                raise IndexError("Matrix addition invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))
        else:
            self.code(lambda x: x+other)
        return self

    @rabbit
    def __pow__(self, other):
        """Performs Exponentiation."""
        if hasnum(other):
            other = int(other)
            if other > 0:
                out = getcopy(self)
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

    def __idiv__(self, other):
        """Performs Division In-Place."""
        if hasnum(other):
            self.code(lambda x: x/other)
            return self
        else:
            raise TypeError("Matrix division invalid with "+repr(other))

    @rabbit
    def __mod__(self, other):
        """Performs Modulus."""
        if isinstance(other, matrix):
            out = self.cross(other)
        else:
            out = getcopy(self)
            out.code(lambda x: x%other)
        return out

    def __imod__(self, other):
        """Performs Modulus In-Place."""
        if isinstance(other, matrix):
            self = self.cross(other)
        else:
            self.code(lambda x: x%other)
        return self

    @rabbit
    def __abs__(self):
        """Performs abs."""
        out = self**2.0
        if isinstance(out, matrix):
            out = sum(out.items())
        return out**0.5

    @rabbit
    def entries(self):
        """Returns A List Of Items With Coordinates."""
        out = []
        for y,x in self.coords(False):
            out.append((y,x,self.retrieve(y,x)))
        return out

    @rabbit
    def coords(self, diag=False):
        """Returns A List Of Coordinates."""
        if diag is None:
            diag = self.onlydiag()
        out = []
        for y in xrange(0, self.y):
            if not diag:
                for x in xrange(0, self.x):
                    out.append((y,x))
            elif y < self.x:
                out.append((y,y))
        return out

    @rabbit
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

    @rabbit
    def addedrow(self, y, addlist):
        """Retrieves A Row Added With A List."""
        out = self[y]
        for x in xrange(0, len(out)):
            out[x] = out[x]+addlist[x]
        return out

    @rabbit
    def filled(self, *args, **kwargs):
        """Returns A Filled Matrix."""
        out = getcopy(self)
        out.fill(*args, **kwargs)
        return out

    def fill(self, func=lambda: random().getdigits(1), diag=None):
        """Fills The Matrix With The Results From A Function."""
        for y,x in self.coords(diag):
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

    @rabbit
    def minor(self, y, x):
        """Returns The Minor Matrix Without The Given Row And Column."""
        out = getcopy(self)
        out.delrow(y)
        out.delcol(x)
        return out

    @rabbit
    def dot(self, other):
        """Finds The Dot Product With Another Matrix."""
        if self.onlyrow() and other.onlyrow() and self.x == other.x:
            out = self*other.trans()
            return out.retrieve(0, 0)
        else:
            raise IndexError("Matrix dot product invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    @rabbit
    def cross(self, other):
        """Finds The Cross Product With Another Matrix."""
        if self.x == other.x:
            if self.x == 0:
                return other
            else:
                cross = getcopy(self)
                for row in other.a:
                    cross.newrow(row)
                cross.newrow([self.prepare(1.0)]*cross.x)
                out = cross.new(1)
                for x in xrange(0, out.x):
                    out.store(0,x, cross.minor(cross.y-1, x).det())
                return out
        else:
            raise IndexError("Matrix cross product invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    @rabbit
    def C(self, y, x):
        """Finds The Cofactor For The Given Row And Column."""
        return self.minor(y,x).det()*(-1.0)**(y+x+2.0)

    @rabbit
    def det(self):
        """Finds The Determinant Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return None
        elif self.x == 1 or self.y == 1:
            return self.retrieve(0,0)
        else:
            out = 0.0
            for x in xrange(0, self.x):
                out += self.retrieve(0,x)*self.C(0,x)
            return out

    @rabbit
    def inv(self, check=True, maxtries=float("inf"), debug=False):
        """Finds The Inverse Of The Matrix."""
        if self.x == 0 or self.y == 0:
            return matrix(0)
        elif self.x == 1 or self.y == 1:
            return self*self.retrieve(0,0)**-1.0
        elif not (check and self.det() == 0.0):
            size = self.y
            out = getcopy(self)
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

    @rabbit
    def augmented(self, aug):
        """Gets The Augmented Matrix."""
        out = getcopy(self)
        out.augment(aug)
        return out

    @rabbit
    def getaugment(self, auglen=None):
        """Gets The Augment."""
        if auglen is None:
            auglen = self.x-self.y
        else:
            auglen = int(auglen)
        return self.trans().a[-auglen:]

    def solve(self, debug=False, debugfunc=print):
        """Solves The Matrix As An Augmented Matrix."""
        for y,x in self.coords(False):
            if x == y:
                if debug:
                    debugfunc("Scale Row "+str(y)+" By 1/"+str(self.retrieve(y,x)))
                self.scalerow(y, 1.0/self.retrieve(y,x))
                if debug > 1:
                    debugfunc(self)
            elif x < y:
                if debug:
                    debugfunc("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retrieve(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retrieve(y,x)))
                if debug > 1:
                    debugfunc(self)

    solvetypes = {
        "solve": lambda out, *args, **kwargs: out.solve(*args, **kwargs),
        "solve top": lambda out, *args, **kwargs: out.solvetop(*args, **kwargs),
        "solve full": lambda out, *args, **kwargs: out.solvefull(*args, **kwargs),
        "keep solving": lambda out, *args, **kwargs: out.keepsolving(*args, **kwargs),
        "keep solving top": lambda out, *args, **kwargs: out.keepsolvingtop(*args, **kwargs),
        "keep solving full": lambda out, *args, **kwargs: out.keepsolvingfull(*args, **kwargs)
        }

    @rabbit
    def solved(self, solvetype="solve", debug=False, debugfunc=print):
        """Gets A Solved Matrix."""
        if debugfunc is print:
            e.setreturned()
        out = getcopy(self)
        if solvetype in self.solvetypes:
            self.solvetypes[solvetype](out, debug, debugfunc)
        else:
            raise ExecutionError("KeyError", "Unrecognized solve type "+solvetype)
        return out

    def solvetop(self, debug=False, debugfunc=print):
        """Solves The Top Of The Matrix As An Augmented Matrix."""
        for y,x in reversed(self.coords(False)):
            if x == y:
                if debug:
                    debugfunc("Scale Row "+str(y)+" By 1/"+str(self.retrieve(y,x)))
                self.scalerow(y, 1.0/self.retrieve(y,x))
                if debug > 1:
                    debugfunc(self)
            elif x < self.y and x > y:
                if debug:
                    debugfunc("Add To Row "+str(y)+" Row "+str(x)+" Scaled By "+str(-1.0*self.retrieve(y,x)))
                self.addrow(y, self.scaledrow(x, -1.0*self.retrieve(y,x)))
                if debug > 1:
                    debugfunc(self)

    def solvefull(self, debug=False, debugfunc=print):
        """Fully Solves The Matrix As An Augmented Matrix."""
        self.solvetop(debug, debugfunc)
        self.solve(debug, debugfunc)

    def mixrows(self, func=lambda a: random().scramble(a)):
        """Scrambles The Rows Using A Function."""
        self.a = func(self.a)

    @rabbit
    def mixedrows(self, func=lambda a: random().scramble(a)):
        """Gets A Scrambled Matrix."""
        out = getcopy(self)
        out.mixrows(func)
        return out

    def keepsolving(self, check=True, maxtries=float("inf"), debug=False, debugfunc=print):
        """Recursively Solves The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError("Matrix cannot be solved on bottom because of 0 determinant")
        elif maxtries > 0:
            try:
                self.solve(debug, debugfunc)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    debugfunc("Mix Rows")
                    debugfunc(self)
                self.keepsolving(False, maxtries-1.0, debug, debugfunc)

    def keepsolvingtop(self, check=True, maxtries=float("inf"), debug=False, debugfunc=print):
        """Recursively Solves The Top Of The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError("Matrix cannot be solved on top because of 0 determinant")
        elif maxtries > 0:
            try:
                self.solvetop(debug, debugfunc)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    debugfunc("Mix Rows")
                    debugfunc(self)
                self.keepsolvingtop(False, maxtries-1.0, debug, debugfunc)

    def keepsolvingfull(self, check=True, maxtries=float("inf"), debug=False, debugfunc=print):
        """Recursively Fully Solves The Matrix As An Augmented Matrix."""
        if check and self.det() == 0.0:
            raise ValueError("Matrix cannot be solved because of 0 determinant")
        elif maxtries > 0:
            try:
                self.solvefull(debug, debugfunc)
            except ZeroDivisionError:
                self.mixrows()
                if debug:
                    debugfunc("Mix Rows")
                    debugfunc(self)
                self.keepsolvingfull(False, maxtries-1.0, debug, debugfunc)

    @rabbit
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

    @rabbit
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

    @rabbit
    def swappedrows(self, ya, yb):
        """Gets A Matrix With The Swap Done."""
        out = getcopy(self)
        out.swaprows(ya, yb)
        return out

    @rabbit
    def lendiag(self):
        """Returns The Length Of The Main Diagonal."""
        if self.y <= self.x:
            return self.y
        else:
            return self.x

    @rabbit
    def getdiag(self):
        """Returns The Main Diagonal."""
        out = []
        for x in xrange(0, self.lendiag()):
            out.append(self.retrieve(x))
        return out

    @rabbit
    def onlydiag(self):
        """Determines If The Matrix Is A Diagonal List."""
        for y in xrange(0, len(self.a)):
            if not (isinstance(self.a[y], fakelist) and (len(self.a[y].a) == 0 or (len(self.a[y].a) == 1 and y in self.a[y].a))):
                return False
        return True

    @rabbit
    def rows(self):
        """Returns The Rows As Matrices."""
        out = []
        for row in self.a:
            new = self.new(1, len(row), fake=False)
            new.a[0] = row
            out.append(new)
        return out

    @rabbit
    def onlyrow(self):
        """Determines If The Matrix Is A Row List."""
        return self.y <= 1

    @rabbit
    def getitems(self):
        """Gets Items Or The Diagonal."""
        if self.onlydiag():
            return self.getdiag()
        else:
            return self.items()

    @rabbit
    def getlen(self):
        """Gets The Length Of Items Or The Diagonal."""
        if self.onlydiag():
            return self.lendiag()
        else:
            return len(self)

    @rabbit
    def __round__(self, n=0):
        """Performs round."""
        out = getcopy(self)
        out.code(lambda x: round(x, n))
        return out

    @rabbit
    def df(self):
        """Finds The Degrees Of Freedom."""
        return (self.x-1.0)*(self.y-1.0)

    @rabbit
    def ymarg(self, y):
        """Calculates A Marginal For The Given Row."""
        return sum(self.a[y])

    @rabbit
    def xmarg(self, x):
        """Calculates A Marginal For The Given Column."""
        self.flip()
        out = self.ymarg(x)
        self.flip()
        return out

    @rabbit
    def sum(self):
        """Calculates The Sum Of All The Items."""
        return sum(self.items())

    @rabbit
    def indep(self):
        """Returns Expected Values For A Chi Squared Independence Test."""
        out = self.new()
        for y,x in self.coords(False):
            out.store(y,x, float(self.xmarg(x)*self.ymarg(y))/float(self.sum()))
        return out

    @rabbit
    def chisq(self, expected=None):
        """Calculates Chi Squared For Independence."""
        if expected is None:
            expected = self.indep()
        if self.y == expected.y and self.x == expected.x:
            tot = 0.0
            for y,x in self.coords(False):
                tot += float(self.retrieve(y,x)-expected.retrieve(y,x))**2.0/float(expected.retrieve(y,x))
            return tot
        else:
            raise IndexError("Matrix Chi Squared invalid for dimensions "+str(self.y)+"x"+str(self.x)+" and "+str(other.y)+"x"+str(other.x))

    def tomatrix(self):
        """Returns self."""
        return self

    def evaltype(item):
        """Calculates The Type."""
        if item.onlydiag():
            return "list"
        elif item.onlyrow():
            return "row"
        else:
            return "matrix"

    @rabbit
    def dimensions(self):
        """Gets The Dimensions."""
        return (self.y, self.x)

    @rabbit
    def __eq__(self, other):
        """Determines Equality."""
        if isinstance(other, matrix) and self.y == other.y and self.x == other.x:
            return self.items() == other.items()
        else:
            return False

def diagmatrix(size=2, full=1.0, empty=0.0, converter=proper, fake=True):
    """Constructs Matrix I."""
    size = int(size)
    I = matrix(size, size, empty, converter, fake)
    for x in xrange(0, size):
        I.store(x, x, full)
    return I

def matrixitems(inputitems, y, x=None, converter=proper, fake=False):
    """Constructs A Matrix From Items."""
    if x is None:
        x = len(inputitems)/y
    out = matrix(y, x, converter=converter, fake=fake)
    z = 0
    for y,x in out.coords(False):
        out.store(y,x, inputitems[z])
        z += 1
    return out

def domatrixlist(inputlist, converter=proper):
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

def diagmatrixlist(inputlist=None, converter=proper, func=None, fake=True, clean=False):
    """Constructs A Diagonal Matrix From A List."""
    if inputlist is None:
        inputlist = []
    if func is None:
        func = diagmatrixlist
    outlist = []
    for item in inputlist:
        if islist(item):
            item = func(item)
        if not clean or not isnull(item):
            outlist.append(item)
    out = matrix(len(outlist), converter=converter, fake=fake)
    for x in xrange(0, len(outlist)):
        out.store(x,x, outlist[x])
    return out

def rowmatrixlist(inputlist=None, converter=proper, func=None, fake=False, clean=False):
    """Constructs A Row Matrix From A List."""
    if inputlist is None:
        inputlist = []
    if func is None:
        func = rowmatrixlist
    outlist = []
    for item in inputlist:
        if islist(item):
            item = func(item)
        if not clean or not isnull(item):
            outlist.append(item)
    out = matrix(1, len(outlist), converter=converter, fake=fake)
    for x in xrange(0, len(outlist)):
        out.store(0,x, outlist[x])
    return out

def matrixstr(inputstr, converter=proper):
    """Converts A Matrix String Back Into A Matrix."""
    ys = basicformat(inputstr).split("\n")
    for x in xrange(0,len(ys)):
        ys[x] = basicformat(ys[x])[1:-1].split(",")
        for z in xrange(0, len(ys[x])):
            ys[x][z] = converter(ys[x][z])
    return matrixlist(ys, converter)

def matrixlist(inputlist, converter=proper, fake=False):
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

def rangematrix(start, stop, step=1.0, fake=True, converter=proper):
    """Constructs A Matrix On A Range."""
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
