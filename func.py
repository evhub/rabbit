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
    def __init__(self, func, funcstr=None):
        """Constructs The Float Function."""
        self.func = func
        if funcstr == None:
            self.funcstr = None
        else:
            self.funcstr = str(funcstr)
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
        out = "("
        if self.funcstr != None:
            out += self.funcstr
        return out+")"
    def __str__(self):
        """Retreives The Function String."""
        if self.funcstr == None:
            return "()"
        else:
            return self.funcstr
    def __float__(self):
        """Retreives A Float."""
        return float(self.calc())
    def __int__(self):
        """Retreives An Integer."""
        return int(self.calc())
    def __add__(self, other):
        """Performs Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return self.calc()+other
    def __div__(self, other):
        """Performs Division."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return self.calc()/other
    def __mul__(self, other):
        """Performs Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return self.calc()*other
    def __pow__(self, other):
        """Performs Exponentiation."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return self.calc()*other
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        return other**self.calc()
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        return other/self.calc()
    def __eq__(self, other):
        """Performs ==."""
        if self.funcstr != None:
            try:
                other.funcstr
            except AttributeError:
                return self.funcstr == other
            else:
                return self.funcstr == other.funcstr
        else:
            try:
                other.func
            except AttributeError:
                return self.func == other
            else:
                return self.func == other.func

class strfunc(funcfloat):
    """Allows A String Function To Be Callable."""
    def __init__(self, funcstr, e, variables=None, personals=None):
        """Creates A Callable String Function."""
        self.funcstr = str(funcstr)
        if variables == None:
            self.variables = ["x","y"]
        else:
            self.variables = variables
        if personals == None:
            self.personals = {}
        else:
            self.personals = personals
        self.e = e
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
            return strfloat(self.funcstr, self.e, self.variables, self.personals)
        items, self.e.overflow = useparams(variables, self.variables)
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
    def __add__(self, other):
        """Performs Addition."""
        if other == 0 or isnull(other):
            return self
        else:
            if self.e.debug:
                self.e.info = " | add"
            return self.calc()+other
    def __div__(self, other):
        """Performs Division."""
        if other == 1 or isnull(other):
            return self
        else:
            if self.e.debug:
                self.e.info = " | div"
            return self.calc()/other
    def __mul__(self, other):
        """Performs Multiplication."""
        if other == 1 or isnull(other):
            return self
        else:
            if self.e.debug:
                self.e.info = " | mul"
            return self.calc()*other
    def __pow__(self, other):
        """Performs Exponentiation."""
        if other == 1 or isnull(other):
            return self
        else:
            if self.e.debug:
                self.e.info = " | pow"
            return self.calc()*other
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if self.e.debug:
            self.e.info = " | rpow"
        return other**self.calc()
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if self.e.debug:
            self.e.info = " | rdiv"
        return other/self.calc()
    def find(self):
        """Simplifies The Function String."""
        self.funcstr = self.e.find(self.funcstr, False, False)

class strfloat(strfunc):
    """Allows A String To Be Treated Like A Float."""
    def __init__(self, funcstr, e, variables=None, personals=None, check=True):
        """Initializes The String Float."""
        self.e = e
        if variables == None:
            variables = []
        if personals == None:
            personals = {}
        if check:
            test = self.e.find(funcstr, True, False)
        if check and isinstance(test, strfunc):
            self.funcstr = test.funcstr
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
            self.variables = variables
            self.personals = personals

class strcalc(numobject):
    """Allows Strings Inside Evaluation."""
    def __init__(self, calcstr, e):
        """Initializes The Evaluator String."""
        self.calcstr = str(calcstr).replace("\\n", "\n").replace("\\'", '"')
        self.e = e
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
        return '"'+self.calcstr+'"'
    def __str__(self):
        """Retreives The Evaluator String."""
        return self.calcstr
    def __add__(self, other):
        """Performs Addition."""
        if other != 0 and not isnull(other):
            self.calcstr += self.e.prepare(other, True, False)
        return self
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if other != 0 and not isnull(other):
            self.calcstr = self.e.prepare(other, True, False)+self.calcstr
        return self
    def __div__(self, other):
        """Performs Division."""
        if other != 1 and not isnull(other):
            raise ValueError
        return self
    def __mul__(self, other):
        """Performs Multiplication."""
        if other != 1 and not isnull(other):
            self.calcstr *= int(other)
        return self
    def __pow__(self, other):
        """Performs Exponentiation."""
        if other != 1 and not isnull(other):
            raise ValueError
        return self
    def __eq__(self, other):
        """Performs ==."""
        return self.calcstr == other
    def __len__(self):
        """Performs len."""
        return len(self.calcstr)
    def __contains__(self, other):
        """Performs in."""
        return self.e.prepare(other, True, False) in self.calcstr

class usefunc(object):
    """Allows A Function To Be Used As A Variable."""
    def __init__(self, dofunc, e, name=None, variables=None, extras=None, overflow=False):
        """Creates A Callable Function."""
        self.overflow = bool(overflow)
        self.dofunc = dofunc
        self.e = e
        if variables == None:
            self.variables = ["x"]
        else:
            self.variables = variables
        self.name = name
        if extras == None:
            self.extras = {}
        else:
            self.extras = dict(extras)
    def call(self, params):
        """Calls The Function."""
        if params == None:
            if self.name == None:
                return matrix(0)
            else:
                return strfloat(self.name+":"+strlist(self.variables,":"), self.e, self.variables)
        elif len(params) < len(self.variables):
            for x in xrange(len(params), len(self.variables)):
                if self.variables[x] in self.e.variables:
                    params.append(self.e.eval_call(self.variables[x]))
                else:
                    break
        elif not self.overflow and len(params) > len(self.variables):
            self.e.overflow = params[len(self.variables):]
            params = params[:len(self.variables)]
        return self.dofunc(*params, **self.extras)

class unifunc(object):
    """Universalizes Function Calls."""
    def __init__(self, func, e, name=None):
        """Constructs The Universalizer."""
        self.name = name
        self.store = []
        self.precall = func
        self.e = e
    def call(self, args):
        """Performs A Universalized Function Call."""
        if args == None:
            if self.name == None:
                return matrix(0)
            else:
                return strfloat(self.name+":x", self.e, ["x"])
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

class makefunc(object):
    """Creates A Normal Single-Variable Evaluator Function."""
    def __init__(self, dofunc, e, name=None):
        """Initializes The Evaluator Function."""
        self.dofunc = dofunc
        self.e = e
        self.name = name
    def call(variables):
        """Calls The Evaluator Function."""
        variables = varproc(variables)
        if variables == None:
            if self.name == None:
                return matrix(0)
            else:
                return strfloat(self.name+":x", self.e, ["x"])
        elif len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return self.dofunc(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.dofunc(x))
            return diagmatrixlist(out)

def collapse(item):
    """Collapses An Argument."""
    if isinstance(item, funcfloat):
        return item.calc()
    else:
        return item

class derivfunc(funcfloat):
    """Implements A Derivative Function."""
    def __init__(self, funcstr, n, accuracy, scaledown, e, varname="x", personals=None):
        """Creates The Derivative Function."""
        self.e = e
        self.funcstr = funcstr
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        self.variables = [varname]
        if personals == None:
            self.personals = {}
        else:
            self.personals = personals
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        items = dict(self.personals)
        if x == None:
            return self.call([])
        else:
            items[self.variables[0]] = float(x)
        oldvars = self.e.setvars(items)
        out = self.e.calc(self.funcstr)
        self.e.setvars(oldvars)
        return out
    def call(self, variables):
        """Calls The Derivative Function."""
        if variables == None:
            return self
        elif len(variables) == 0:
            return matrix(0)
        else:
            return deriv(self.calc, float(variables[0]), self.n, self.accuracy, self.scaledown)

class integfunc(derivfunc):
    """Implements An Integral Function."""
    def __init__(self, funcstr, accuracy, e, varname="x", personals=None):
        """Creates The Integral Function."""
        self.e = e
        self.funcstr = funcstr
        self.accuracy = float(accuracy)
        self.variables = [varname]
        if personals == None:
            self.personals = {}
        else:
            self.personals = personals
    def call(self, variables):
        """Calls The Integral Function."""
        if variables == None:
            return self
        elif len(variables) < 2:
            return matrix(0)
        else:
            return defint(self.calc, float(variables[0]), float(variables[1]), self.accuracy)

class derivfuncfloat(derivfunc):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown):
        """Creates The Derivative Function."""
        self.func = func
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        if x == None:
            return self.func.call([])
        else:
            return self.func.call([x])

class integfuncfloat(integfunc, derivfuncfloat):
    """Implements An Integral Function Of A Fake Function."""
    def __init__(self, func, accuracy):
        """Creates The Integral Function."""
        self.func = func
        self.accuracy = float(accuracy)
