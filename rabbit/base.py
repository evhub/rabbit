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

from .obj import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

old_round = round
def round(x, n=0):
    try:
        return x.__round__(n)
    except AttributeError:
        return old_round(x, n)

class evalobject(object):
    """A Base Class For Evaluator Objects."""
    check = 1

    def __ne__(self, other):
        """Implements !=."""
        return not self == other

    def __radd__(self, other):
        """Implements Reverse Addition."""
        return self + other

    def __rmul__(self, other):
        """Implements Reverse Multiplication."""
        return self*other

    def __add__(self, other):
        """Performs Addition."""
        out = self.copy()
        out += other
        return out

    def __sub__(self, other):
        """Performs Subtraction."""
        out = self.copy()
        out -= other
        return out

    def __mul__(self, other):
        """Performs Multiplication."""
        out = self.copy()
        out *= other
        return out

    def __div__(self, other):
        """Performs Division."""
        out = self.copy()
        out /= other
        return out

    def __pow__(self, other):
        """Performs Exponentiation."""
        out = self.copy()
        out **= other
        return out

    def __mod__(self, other):
        """Performs Modulus."""
        out = self.copy()
        out %= other
        return out

    def __imul__(self, other):
        """Performs *."""
        for x in xrange(0, int(other)):
            self += self
        return self

    def __ipow__(self, other):
        """Performs **."""
        for x in xrange(0, int(other)):
            self *= self
        return self

class numobject(evalobject):
    """A Base Class For Objects."""

    def __sub__(self, other):
        """Implements Subtraction."""
        return self + -1.0*other

    def __isub__(self, other):
        """Implements Subtraction In-Place."""
        self += -1.0*other
        return self

    def __rsub__(self, other):
        """Implements Reverse Subtraction."""
        return -1.0*self + other

    def __rdiv__(self, other):
        """Implements Reverse Division."""
        return other*self**-1.0

    def __float__(self):
        """Retrieves A Float."""
        return float(self.calc())

    def __int__(self):
        """Retrieves An Integer."""
        return int(self.calc())

    def __floordiv__(self, other):
        """Implements Floor Division."""
        return self.__div__(int(other))

    def __truediv__(self, other):
        """Implements Float Division."""
        return self.__div__(float(other))

    def __itruediv__(self, other):
        """Implements Float Division In-Place."""
        return self.__idiv__(float(other))

    def __ifloordiv__(self, other):
        """Implements Floor Divison In-Place."""
        return self.__idiv__(int(other))

    def __rfloordiv__(self, other):
        """Implements Reverse Floor Division."""
        return self.__rdiv__(int(other))

    def __rtruediv__(self, other):
        """Implements Reverse Float Division."""
        return self.__rdiv__(float(other))

    def __neg__(self):
        """Implements Unary -."""
        return self*-1.0

    def __pos__(self):
        """Implements Unary +."""
        return self*1.0

    def copy(self):
        """Makes A Copy."""
        return self.__pos__()

    def __long__(self):
        """Implements long."""
        return long(self.__int__())

    def __complex__(self):
        """Implements complex."""
        return complex(self.__float__())

    def __int__(self):
        """Implements int."""
        return int(self.__float__())

    def __imod__(self, other):
        """Implements Modulus In-Place."""
        while self >= other:
            self -= other
        return self

    def __rmod__(self, other):
        """Implements Reverse Modulus."""
        return other % float(self)

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        return float(self)+other

    def __idiv__(self, other):
        """Performs Division In-Place."""
        return float(self)/other

    def __rdiv__(self, other):
        """Performs Division In-Place."""
        return other/float(self)

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        return float(self)*other

    def __ipow__(self, other):
        """Performs Exponentiation In-Place."""
        self.code(lambda x: x**other)
        return self

    def __cmp__(self, other):
        """Performs Comparison."""
        test = float(self-float(other))
        if test > 0:
            return 1
        elif test < 0:
            return -1
        else:
            return 0

    def __eq__(self, other):
        """Performs ==."""
        try:
            test = self.__cmp__(other)
        except TypeError:
            return False
        except ValueError:
            return False
        else:
            return test == 0

    def __abs__(self):
        """Implements abs."""
        return abs(float(self))

    def __round__(self, n=0):
        """Implements round."""
        return round(float(self), n)

class cotobject(evalobject):
    """A Base Class For Container Objects."""
    check = 2

    def __iter__(self):
        """Iterates Over The Object."""
        return iter(self.items())

    def __reversed__(self):
        """Iterates Over The Object In Reverse."""
        return reversed(self.items())

    def __contains__(self, item):
        """Determines If An Item Is In The Object."""
        if item in self.items():
            return True
        else:
            return False

    def __len__(self):
        """Performs len."""
        return len(self.items())

    def __repr__(self):
        """Performs repr."""
        return repr(self.items())

    def __str__(self):
        """Performs str."""
        return str(self.items())

    def __getitem__(self, key):
        """Retrieves An Item."""
        return self.items()[key]

    def __delitem__(self, key):
        """Wraps remove."""
        self.remove(self[key])
        return self

    def __iadd__(self, other):
        """Wraps extend."""
        self.extend(other)
        return self

    def __isub__(self, other):
        """Wraps remove."""
        self.remove(other)
        return self

    def __eq__(self, other):
        """Performs ==."""
        try:
            test = other.items()
        except AttributeError:
            test = other
        if self.items() == test:
            return True
        else:
            return False

    def __cmp__(self, other):
        """Performs comparison."""
        try:
            test = tuple(other.items())
        except AttributeError:
            test = tuple(other)
        items = tuple(self.items())
        if items == test:
            return 0
        elif items > test:
            return 1
        else:
            return -1

class mctobject(cotobject, numobject):
    """A Base Class For Mathematical Container Objects."""

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        self.code(lambda x: x+other)
        return self

    def __isub__(self, other):
        """Performs Subtraction In-Place."""
        self.code(lambda x: x-other)
        return self

    def __idiv__(self, other):
        """Performs Division In-Place."""
        self.code(lambda x: x/other)
        return self

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        self.code(lambda x: x*other)
        return self

    def __ipow__(self, other):
        """Performs Exponentiation In-Place."""
        self.code(lambda x: x**other)
        return self

    def __imod__(self, other):
        """Performs Modulus In-Place."""
        self.code(lambda x: x%other)
        return self

    def __rmod__(self, other):
        """Implements Reverse Modulus."""
        self.code(lambda x: other%x)
        return self

    def __abs__(self):
        """Performs abs."""
        out = self.copy()
        out.code(lambda x: abs(x))
        return out

    def __round__(self, n=0):
        """Performs round."""
        out = self.copy()
        out.code(lambda x: round(x, n))
        return out
