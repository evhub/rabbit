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

from .obj import *

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

old_round = round
def round(x, *args, **kwargs):
    """Wraps round."""
    if hasattr(x, "__round__"):
        return x.__round__(*args, **kwargs)
    else:
        return old_round(x, *args, **kwargs)

try:
    cmp
except NameError:
    def cmp(a, b):
        """Mimics cmp."""
        if hasattr(a, "__cmp__"):
            return a.__cmp__(b)
        elif hasattr(b, "__cmp__"):
            return b.__cmp__(a)
        else:
            return (a > b) - (a < b)

def rabbit(func):
    """Decorates A Method To Allow Its Use In Rabbit As A Pure Function."""
    if not hasattr(func, "__doc__") or not func.__doc__:
        func.__doc__ = "A Rabbit Object."
    func.__doc__ = "(|rabbit:=True|) "+func.__doc__
    return func

def dirty_rabbit(func):
    """Decorates A Method To Allow Its Use In Rabbit As An Impure Function."""
    if not hasattr(func, "__doc__") or not func.__doc__:
        func.__doc__ = "A Dirty Rabbit Object."
    func.__doc__ = "(|rabbit:=False|) "+func.__doc__
    return func

class evalobject(object):
    """A Base Class For Evaluator Objects."""
    check = 1

    @rabbit
    def __ne__(self, other):
        """Implements !=."""
        return not self == other

    @rabbit
    def __add__(self, other):
        """Performs Addition."""
        out = getcopy(self)
        out += other
        return out
    def __iadd__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Addition not defined for object")

    @rabbit
    def __sub__(self, other):
        """Performs Subtraction."""
        out = getcopy(self)
        out -= other
        return out
    def __isub__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Subtraction not defined for object")

    @rabbit
    def __mul__(self, other):
        """Performs Multiplication."""
        out = getcopy(self)
        out *= other
        return out
    def __imul__(self, other):
        """Performs *."""
        for x in xrange(0, int(other)):
            self += self
        return self

    @rabbit
    def __div__(self, other):
        """Performs Division."""
        out = getcopy(self)
        out /= other
        return out
    def __idiv__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Division not defined for object")

    @rabbit
    def __truediv__(self, other):
        """Wraps __div__."""
        return self.__div__(other)
    def __itruediv__(self, other):
        """Wraps __idiv__."""
        return self.__idiv__(other)
    @rabbit
    def __rtruediv__(self, other):
        """Wraps __rdiv__."""
        return self.__rdiv__(other)

    @rabbit
    def __floordiv__(self, other):
        """Performs Floor Division."""
        out = getcopy(self)
        out //= other
        return out
    def __ifloordiv__(self, other):
        """Performs //."""
        self /= other
        return int(self)

    @rabbit
    def __pow__(self, other, mod=None):
        """Performs Exponentiation."""
        out = getcopy(self)
        out **= other
        if mod is not None:
            out %= mod
        return out
    def __ipow__(self, other):
        """Performs **."""
        for x in xrange(0, int(other)):
            self *= self
        return self

    @rabbit
    def __mod__(self, other):
        """Performs Modulus."""
        out = getcopy(self)
        out %= other
        return out
    def __imod__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Modulus not defined for object")

    @rabbit
    def __or__(self, other):
        """Performs Bitwise Or."""
        out = getcopy(self)
        out |= other
        return out
    def __ior__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Bitwise or not defined for object")

    @rabbit
    def __and__(self, other):
        """Performs Bitwise And."""
        out = getcopy(self)
        out &= other
        return out
    def __iand__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Bitwise and not defined for object")

    @rabbit
    def __xor__(self, other):
        """Performs Bitwise Xor."""
        out = getcopy(self)
        out ^= other
        return out
    def __ixor__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Bitwise xor not defined for object")

    @rabbit
    def __rshift__(self, other):
        """Performs Bitwise Right Shift."""
        out = getcopy(self)
        out >>= other
        return out
    def __irshift__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Bitwise right shift not defined for object")

    @rabbit
    def __lshift__(self, other):
        """Performs Bitwise Left Shift."""
        out = getcopy(self)
        out <<= other
        return out
    def __ilshift__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Bitwise left shift not defined for object")

    @rabbit
    def __gt__(self, other):
        """Wraps cmp."""
        return self.__cmp__(other) > 0

    @rabbit
    def __lt__(self, other):
        """Wraps cmp."""
        return self.__cmp__(other) < 0

    @rabbit
    def __ge__(self, other):
        """Wraps cmp."""
        return self.__cmp__(other) >= 0

    @rabbit
    def __le__(self, other):
        """Wraps cmp."""
        return self.__cmp__(other) <= 0

    @rabbit
    def __eq__(self, other):
        """Wraps cmp."""
        return self.__cmp__(other) == 0

    def __cmp__(self, other):
        """Raises An Error."""
        raise ExecutionError("OperatorError", "Comparison not defined for object")

    @rabbit
    def __unicode__(self):
        """Converts To A String."""
        if hasattr(self, "__str__"):
            return self.__str__()
        else:
            return repr(self)

    @rabbit
    def __nonzero__(self):
        """Uses __bool__ If It Exists."""
        if hasattr(self, "__bool__"):
            return self.__bool__()
        elif hasattr(self, "__len__"):
            return bool(len(self))
        else:
            return True

    @rabbit
    def __index__(self):
        """Wraps int."""
        return int(self)

    @rabbit
    def __divmod__(self, other):
        """Performs Division With Remainder."""
        return self//other, self%other

    @rabbit
    def __rdivmod__(self, other):
        """Performs Reverse Division With Remainder."""
        return other//self, other%self

    @rabbit
    def __bin__(self):
        """Gets A Binary Representation."""
        return bin(self.__index__())

    @rabbit
    def __oct__(self):
        """Gets An Octal Representation."""
        return oct(self.__index__())

    @rabbit
    def __hex__(self):
        """Gets A Hex Representation."""
        return hex(self.__index__())

    def __call__(self, *args):
        """Calls The Rabbit Function."""
        return e.getcall(self)(list(map(e.frompython, args)))

    def __getitem__(self, *args):
        """Gets An Item."""
        return self.itemcall(list(map(e.frompython, args)))

class numobject(evalobject):
    """A Base Class For Objects."""

    @rabbit
    def __radd__(self, other):
        """Implements Reverse Addition."""
        return self + other

    @rabbit
    def __rmul__(self, other):
        """Implements Reverse Multiplication."""
        return self * other

    @rabbit
    def __sub__(self, other):
        """Implements Subtraction."""
        return self + -1.0*other

    def __isub__(self, other):
        """Implements Subtraction In-Place."""
        self += -1.0*other
        return self

    @rabbit
    def __rsub__(self, other):
        """Implements Reverse Subtraction."""
        return -1.0*self + other

    @rabbit
    def __rdiv__(self, other):
        """Implements Reverse Division."""
        return other*self**-1.0

    @rabbit
    def __float__(self):
        """Retrieves A Float."""
        return old_float(self.getfloat())

    @rabbit
    def getfloat(self):
        """Retrieves A Number."""
        return float(self.calc())

    @rabbit
    def __int__(self):
        """Retrieves An Integer."""
        return int(self.calc())

    @rabbit
    def __neg__(self):
        """Implements Unary -."""
        return self*-1.0

    @rabbit
    def __pos__(self):
        """Implements Unary +."""
        return self*1.0

    @rabbit
    def copy(self):
        """Makes A Copy."""
        return self.__pos__()

    @rabbit
    def __long__(self):
        """Implements long."""
        return long(int(self))

    @rabbit
    def __complex__(self):
        """Implements complex."""
        return complex(float(self))

    @rabbit
    def __int__(self):
        """Implements int."""
        return int(float(self))

    def __imod__(self, other):
        """Implements Modulus In-Place."""
        while self >= other:
            self -= other
        return self

    @rabbit
    def __rmod__(self, other):
        """Implements Reverse Modulus."""
        return other % float(self)

    def __iadd__(self, other):
        """Performs Addition In-Place."""
        return float(self) + other

    def __idiv__(self, other):
        """Performs Division In-Place."""
        return float(self) / other

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        return float(self) * other

    def __ipow__(self, other):
        """Performs Exponentiation In-Place."""
        return float(self) ** other

    def __rpow__(self, other):
        """Performs Reverse Exponentiation In-Place."""
        return other ** float(self)

    @rabbit
    def __cmp__(self, other):
        """Performs Comparison."""
        test = float(self-float(other))
        if test > 0:
            return 1
        elif test < 0:
            return -1
        else:
            return 0

    @rabbit
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

    @rabbit
    def __abs__(self):
        """Implements abs."""
        return abs(float(self))

    @rabbit
    def __round__(self, n=0):
        """Implements round."""
        return round(float(self), n)

    def __ior__(self, other):
        """Performs Bitwise Or In-Place."""
        return float(self) | other

    def __iand__(self, other):
        """Performs Bitwise And In-Place."""
        return float(self) & other

    def __ixor__(self, other):
        """Performs Bitwise Xor In-Place."""
        return float(self) ^ other

    def __irshift__(self, other):
        """Performs Bitwise Right Shift In-Place."""
        return float(self) >> other

    def __ilshift__(self, other):
        """Performs Bitwise Left Shift In-Place."""
        return float(self) << other

class cotobject(evalobject):
    """A Base Class For Container Objects."""
    check = 2

    @rabbit
    def __iter__(self):
        """Iterates Over The Object."""
        return iter(self.items())

    @rabbit
    def __reversed__(self):
        """Iterates Over The Object In Reverse."""
        return reversed(self.items())

    @rabbit
    def __contains__(self, item):
        """Determines If An Item Is In The Object."""
        return item in self.items()

    @rabbit
    def __len__(self):
        """Performs len."""
        return len(self.items())

    @rabbit
    def __repr__(self):
        """Performs repr."""
        return repr(self.items())

    @rabbit
    def __str__(self):
        """Performs str."""
        return str(self.items())

    @rabbit
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

    @rabbit
    def __radd__(self, other):
        """Performs Reverse Extension."""
        return other + self.items()

    def __isub__(self, other):
        """Wraps remove."""
        self.remove(other)
        return self

    @rabbit
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

    @rabbit
    def __cmp__(self, other):
        """Performs Comparison."""
        try:
            test = tuple(other.items())
        except AttributeError:
            test = (other,)
        items = tuple(self.items())
        if items == test:
            return 0
        elif items > test:
            return 1
        else:
            return -1

    @rabbit
    def tomatrix(self):
        """Converts To A Matrix."""
        return diagmatrixlist(self.items())

    @rabbit
    def __hash__(self):
        """Returns A Hash."""
        out = 0
        for item in self.items():
            out ^= hash(item)
        return out

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

    @rabbit
    def __rmod__(self, other):
        """Implements Reverse Modulus."""
        out = getcopy(self)
        out.code(lambda x: other%x)
        return out

    @rabbit
    def __rdiv__(self, other):
        """Implements Reverse Division."""
        out = getcopy(self)
        out.code(lambda x: other/x)
        return out

    @rabbit
    def __rpow__(self, other):
        """Implements Reverse Exponentiation."""
        out = getcopy(self)
        out.code(lambda x: other**x)
        return out

    @rabbit
    def __abs__(self):
        """Performs abs."""
        out = getcopy(self)
        out.code(lambda x: abs(x))
        return out

    @rabbit
    def __round__(self, n=0):
        """Performs round."""
        out = getcopy(self)
        out.code(lambda x: round(x, n))
        return out

    def __ior__(self, other):
        """Performs Bitwise Or In-Place."""
        self.code(lambda x: x|other)
        return self

    def __iand__(self, other):
        """Performs Bitwise And In-Place."""
        self.code(lambda x: x&other)
        return self

    def __ixor__(self, other):
        """Performs Bitwise Xor In-Place."""
        self.code(lambda x: x^other)
        return self

    def __irshift__(self, other):
        """Performs Bitwise Right Shift In-Place."""
        self.code(lambda x: x>>other)
        return self

    def __ilshift__(self, other):
        """Performs Bitwise Left Shift In-Place."""
        self.code(lambda x: x<<other)
        return self

class ExecutionError(Exception):
    """A Base Class For Rabbit Errors."""
    def __init__(self, name="ExecutionError", message="An error occured", fatal=True, instance=None):
        """Creates The Error."""
        self.name = str(name)
        self.message = str(message)
        self.fatal = bool(fatal)
        self.instance = instance
    def __repr__(self):
        """Creates A Representation Of The Error."""
        return self.name+": "+self.message
    __str__ = __repr__
