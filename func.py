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

from .matrix import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def varproc(variables):
    """Processes A Set Of Variables."""
    if variables == None or islist(variables) or isinstance(variables, dict):
        return variables
    elif isinstance(variables, matrix):
        return variables.getitems()
    elif isinstance(variables, tuple):
        return list(variables)
    else:
        return [variables]

class funcfloat(numobject):
    """Allows The Creation Of A Float Function."""
    allargs = "__"

    def __init__(self, func, e, funcstr="func"):
        """Constructs The Float Function."""
        self.funcstr = str(funcstr)
        self.func = func
        self.e = e
    def copy(self):
        """Returns A Copy Of The Float Function."""
        return funcfloat(self.func, self.e, self.funcstr)
    def calc(self):
        """Calculates The Float Function."""
        return self.func(None)
    def call(self, variables):
        """Calls The Float Function."""
        variables = varproc(variables)
        if variables == None:
            return self
        else:
            return self.func(variables)
    def __repr__(self):
        """Returns A String Representation."""
        return "("+self.funcstr+")"
    def __str__(self):
        """Retreives The Function String."""
        return self.funcstr
    def __float__(self):
        """Retreives A Float."""
        return float(self.calc())
    def __int__(self):
        """Retreives An Integer."""
        return int(self.calc())
    def __iadd__(self, other):
        """Performs Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.funcstr+"("+self.allargs+"))+("+self.e.prepare(other, False, True)+")", self.e, [self.allargs], {self.funcstr:self})
    def __idiv__(self, other):
        """Performs Division."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.funcstr+"("+self.allargs+"))/("+self.e.prepare(other, False, True)+")", self.e, [self.allargs], {self.funcstr:self})
    def __imul__(self, other):
        """Performs Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.funcstr+"("+self.allargs+"))*("+self.e.prepare(other, False, True)+")", self.e, [self.allargs], {self.funcstr:self})
    def __ipow__(self, other):
        """Performs Exponentiation."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.funcstr+"("+self.allargs+"))^("+self.e.prepare(other, False, True)+")", self.e, [self.allargs], {self.funcstr:self})
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")+("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")^("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")/("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})
    def __eq__(self, other):
        """Performs ==."""
        try:
            other.funcstr
        except AttributeError:
            return self.funcstr == other
        else:
            return self.funcstr == other.funcstr

class strfunc(funcfloat):
    """Allows A String Function To Be Callable."""
    def __init__(self, funcstr, e, variables=None, personals=None, name="func"):
        """Creates A Callable String Function."""
        self.funcstr = str(funcstr)
        self.name = str(name)
        if not variables:
            self.variables = ["x", "y"]
            self.overflow = False
        else:
            self.variables = variables[:]
            if self.allargs in self.variables:
                self.variables.remove(self.allargs)
                self.overflow = False
            else:
                self.overflow = True
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.e = e
    def copy(self):
        """Copies The String Function."""
        return strfloat(self.funcstr, self.e, self.variables, self.personals)
    def calc(self):
        """Calculates The String."""
        oldvars = self.e.setvars(self.personals)
        out = self.e.calc(self.funcstr)
        self.e.setvars(oldvars)
        return out
    def call(self, variables):
        """Calls The String Function."""
        variables = varproc(variables)
        if variables == None:
            return self
        else:
            allvars = diagmatrixlist(variables)
            if self.overflow:
                items, self.e.overflow = useparams(variables, self.variables)
            else:
                items, trash = useparams(variables, self.variables)
            items[self.allargs] = allvars
            for k in self.personals:
                if (not k in items) or items[k] == None:
                    items[k] = self.personals[k]
            oldvars = self.e.setvars(items)
            self.e.info = " \\>"
            out = self.calc()
            self.e.setvars(oldvars)
            return out
    def __float__(self):
        """Retreives A Float."""
        if self.e.debug:
            self.e.info = " | float"
        return float(self.calc())
    def __int__(self):
        """Retreives An Integer."""
        if self.e.debug:
            self.e.info = " | int"
        return int(self.calc())
    def __iadd__(self, other):
        """Performs Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+"("+strlist(self.variables,",")+"))+("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __idiv__(self, other):
        """Performs Division."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+"("+strlist(self.variables,",")+"))/("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __imul__(self, other):
        """Performs Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+"("+strlist(self.variables,",")+"))*("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __ipow__(self, other):
        """Performs Exponentiation."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+"("+strlist(self.variables,",")+"))^("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")+("+self.name+"("+strlist(self.variables,",")+"))", self.e, self.variables, {self.name:self})
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")^("+self.name+"("+strlist(self.variables,",")+"))", self.e, self.variables, {self.name:self})
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")/("+self.name+"("+strlist(self.variables,",")+"))", self.e, self.variables, {self.name:self})
    def find(self):
        """Simplifies The Function String."""
        self.funcstr = self.e.find(self.funcstr, False, False)

class strfloat(strfunc):
    """Allows A String To Be Treated Like A Float."""
    def __init__(self, funcstr, e, variables=None, personals=None, check=True, name="func"):
        """Initializes The String Float."""
        self.name = str(name)
        if not variables:
            variables = ["x", "y"]
            overflow = False
        else:
            variables = variables[:]
            if self.allargs in variables:
                variables.remove(self.allargs)
                overflow = False
            else:
                overflow = True
        if personals == None:
            personals = {}
        else:
            personals = dict(personals)
        self.e = e
        if check:
            test = self.e.find(funcstr, True, False)
        if check and isinstance(test, strfunc):
            self.funcstr = test.funcstr
            self.overflow = overflow and test.overflow
            self.variables = variables
            for x in test.variables:
                if not x in self.variables:
                    self.variables.append(x)
            self.personals = test.personals
            for x,y in personals:
                if y != test:
                    self.personals[x] = y
        else:
            self.funcstr = str(funcstr)
            self.overflow = overflow
            self.variables = variables
            self.personals = personals

class strcalc(numobject):
    """Allows Strings Inside Evaluation."""
    def __init__(self, calcstr, e):
        """Initializes The Evaluator String."""
        self.calcstr = ""
        func = False
        for x in str(calcstr):
            if func:
                func = False
                if x == "'":
                    x = '"'
                elif x == "n":
                    x = "\n"
            elif x == "\\":
                func = True
                x = ""
            self.calcstr += x
        self.e = e
    def copy(self):
        """Returns A Copy Of The Evaluator String."""
        return strcalc(self.calcstr, self.e)
    def __float__(self):
        """Attempts To Get A Float."""
        return float(self.calcstr)
    def __int__(self):
        """Attempts To Get An Integer."""
        return int(self.calcstr)
    def __round__(self, n=None):
        """Performs round."""
        return self
    def __repr__(self):
        """Retreives A Representation."""
        return '"'+self.calcstr.replace("\\","\\\\").replace('"',"\\'").replace("\n","\\n")+'"'
    def __str__(self):
        """Retreives The Evaluator String."""
        return self.calcstr
    def __iadd__(self, other):
        """Performs Addition."""
        if other != 0 and not isnull(other):
            self.calcstr += self.e.prepare(other, True, False)
        return self
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if other != 0 and not isnull(other):
            self.calcstr = self.e.prepare(other, True, False)+self.calcstr
        return self
    def __idiv__(self, other):
        """Performs Division."""
        if other != 1 and not isnull(other):
            self.calcstr = self.calcstr[:int(len(self.calcstr)/other)]
        return self
    def __imul__(self, other):
        """Performs Multiplication."""
        if other != 1 and not isnull(other):
            self.calcstr = self.calcstr*int(other)+self.calcstr[:int(len(self.calcstr)*(other-int(other)))]
        return self
    def __ipow__(self, other):
        """Performs Exponentiation."""
        if other != 1 and not isnull(other):
            self *= len(self)**(other-1.0)
        return self
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, strcalc):
            other = other.calcstr
        return self.calcstr == other
    def __len__(self):
        """Performs len."""
        return len(self.calcstr)
    def __contains__(self, other):
        """Performs in."""
        return self.e.prepare(other, True, False) in self.calcstr

class usefunc(funcfloat):
    """Allows A Function To Be Used As A Variable."""
    def __init__(self, func, e, funcstr="func", variables=None, extras=None, overflow=False):
        """Creates A Callable Function."""
        self.overflow = bool(overflow)
        self.funcstr = str(funcstr)
        if variables == None:
            self.variables = ["x"]
        else:
            self.variables = variables
        if extras == None:
            self.extras = {}
        else:
            self.extras = dict(extras)
        self.func = func
        self.e = e
    def copy(self):
        """Copies The Function."""
        return usefunc(self.func, self.e, self.funcstr, self.variables, self.extras, self.overflow)
    def call(self, params):
        """Calls The Function."""
        if params == None:
            return strfloat(self.funcstr+":"+strlist(self.variables,":"), self.e, self.variables)
        elif len(params) < len(self.variables):
            for x in xrange(len(params), len(self.variables)):
                if self.variables[x] in self.e.variables:
                    params.append(self.e.eval_call(self.variables[x]))
                else:
                    break
        elif not self.overflow and len(params) > len(self.variables):
            self.e.overflow = params[len(self.variables):]
            params = params[:len(self.variables)]
        return self.func(*params, **self.extras)

class unifunc(funcfloat):
    """Universalizes Function Calls."""
    def __init__(self, func, e, funcstr="func"):
        """Constructs The Universalizer."""
        self.funcstr = str(funcstr)
        self.store = []
        self.precall = func
        self.e = e
    def copy(self):
        """Copies The Universalizer Function."""
        return unifunc(self.func, self.e, self.funcstr)
    def call(self, args):
        """Performs A Universalized Function Call."""
        if args == None:
            return strfloat(self.funcstr+":x", self.e, ["x"])
        elif islist(args):
            x = args[0]
            if len(args) > 1:
                self.e.overflow = []
                for x in xrange(1, len(args)):
                    self.e.overflow.append(args[x])
        x = getint(x)
        try:
            self.store[x]
        except IndexError:
            while len(self.store) <= x:
                self.store.append(self.precall())
        return self.store[x]

class makefunc(funcfloat):
    """Creates A Normal Single-Variable Evaluator Function."""
    def __init__(self, func, e, funcstr="func"):
        """Initializes The Evaluator Function."""
        self.funcstr = str(funcstr)
        self.func = func
        self.e = e
    def copy(self):
        """Copies The Evaluator Function."""
        return makefunc(self.func, self.e, self.funcstr)
    def call(variables):
        """Calls The Evaluator Function."""
        variables = varproc(variables)
        if variables == None:
            return strfloat(self.funcstr+":x", self.e, ["x"])
        elif len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return self.func(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.func(x))
            return diagmatrixlist(out)

def collapse(item):
    """Collapses An Argument."""
    if isinstance(item, funcfloat):
        return item.calc()
    else:
        return item

class derivbase(object):
    """Holds Methods Used In Derivative Functions."""
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        items = dict(self.personals)
        if x == None:
            return self.call([])
        else:
            items[self.variables[0]] = float(x)
            items[self.allargs] = matrix(1,1, x)
            oldvars = self.e.setvars(items)
            self.e.info = " \\>"
            out = self.e.calc(self.floatstr)
            self.e.setvars(oldvars)
            return out
    def call(self, variables):
        """Calls The Derivative Function."""
        if variables == None:
            return self
        elif len(variables) == 0:
            return matrix(0)
        else:
            self.e.overflow = variables[1:]
            return deriv(self.calc, float(variables[0]), self.n, self.accuracy, self.scaledown)

class integbase(derivbase):
    """Holdes Methods Used In Integral Functions."""
    def call(self, variables):
        """Calls The Integral Function."""
        if variables == None:
            return self
        elif len(variables) < 2:
            return matrix(0)
        else:
            self.e.overflow = variables[2:]
            return defint(self.calc, float(variables[0]), float(variables[1]), self.accuracy)

class derivfunc(strfunc, derivbase):
    """Implements A Derivative Function."""
    def __init__(self, funcstr, n, accuracy, scaledown, e, varname="x", personals=None, name="func"):
        """Creates The Derivative Function."""
        self.name = str(name)
        self.funcstr = str(funcstr)
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        self.variables = [varname]
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.e = e
    def copy(self):
        """Returns A Copy Of The Derivative Function."""
        return derivfunc(self.funcstr, self.n, self.accuracy, self.scaledown, self.e, self.variables[0], self.personals, self.name)

class integfunc(strfunc, integbase):
    """Implements An Integral Function."""
    def __init__(self, funcstr, accuracy, e, varname="x", personals=None, name="func"):
        """Creates The Integral Function."""
        self.name = str(name)
        self.funcstr = str(funcstr)
        self.accuracy = float(accuracy)
        self.variables = [varname]
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.e = e
    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfunc(self.funcstr, self.accuracy, self.e, self.variables[0], self.personals, self.name)

class derivfuncfloat(funcfloat, derivbase):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown, e, funcstr="func"):
        """Creates The Derivative Function."""
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        self.funcstr = str(funcstr)
        self.func = func
        self.e = e
    def copy(self):
        """Returns A Copy Of The Derivative Float Function."""
        return integfunc(self.func, self.n, self.accuracy, self.scaledown, self.e, self.funcstr)
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        if x == None:
            return self.func.call([])
        else:
            return self.func.call([x])

class integfuncfloat(funcfloat, integbase):
    """Implements An Integral Function Of A Fake Function."""
    def __init__(self, func, accuracy, e, funcstr="func"):
        """Creates The Integral Float Function."""
        self.accuracy = float(accuracy)
        self.funcstr = str(funcstr)
        self.func = func
        self.e = e
    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfuncfloat(self.func, self.accuracy, self.e, self.funcstr)
