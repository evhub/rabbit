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

def collapse(item):
    """Collapses An Argument."""
    if isinstance(item, funcfloat):
        return item.calc()
    else:
        return item

def ismatrix(inputobject):
    """Checks Whether An Object Is A Matrix."""
    return hasmatrix(inputobject) and not isinstance(inputobject, strcalc)

def getmatrix(inputobject, func=diagmatrixlist):
    """Converts The Object To A Matrix."""
    inputobject = collapse(inputobject)
    if isinstance(inputobject, matrix):
        return inputobject
    elif hasmatrix(inputobject):
        return inputobject.tomatrix()
    elif islist(inputobject):
        return func(inputobject)
    else:
        return matrix(1,1, inputobject, fake=(func==diagmatrixlist))

def getitems(inputobject):
    """Gets A List Of Items From A Possible Matrix."""
    item = getmatrix(inputobject)
    if item.onlydiag():
        return item.getdiag()
    else:
        return item.rows()

def merge(inputlist):
    """Merges Items."""
    out = []
    for x in inputlist:
        if islist(x):
            out += merge(x)
        elif ismatrix(x):
            out += merge(getmatrix(x).getitems())
        else:
            out.append(x)
    return out

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
        """Retrieves The Function String."""
        return self.funcstr
    def __float__(self):
        """Retrieves A Float."""
        return float(self.calc())
    def __int__(self):
        """Retrieves An Integer."""
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
    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")*("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, strfunc):
            return self.funcstr == other.funcstr
        elif isinstance(other, funcfloat):
            return self.func == other.func
        else:
            return False

class strfunc(funcfloat):
    """Allows A String Function To Be Callable."""
    def __init__(self, funcstr, e, variables=[], personals=None, name="func", overflow=None):
        """Creates A Callable String Function."""
        self.funcstr = str(funcstr)
        self.name = str(name)
        self.variables = variables[:]
        if self.allargs in self.variables:
            self.variables.remove(self.allargs)
            self.overflow = False
        elif overflow == None:
            self.overflow = True
        else:
            self.overflow = bool(overflow)
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.e = e
    def copy(self):
        """Copies The String Function."""
        return strfunc(self.funcstr, self.e, self.variables, self.personals, self.name, self.overflow)
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
        """Retrieves A Float."""
        if self.e.debug:
            self.e.info = " | float"
        return float(self.calc())
    def __int__(self):
        """Retrieves An Integer."""
        if self.e.debug:
            self.e.info = " | int"
        return int(self.calc())
    def __iadd__(self, other):
        """Performs Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+":"+strlist(self.variables,":")+")+("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __idiv__(self, other):
        """Performs Division."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+":"+strlist(self.variables,":")+")/("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __imul__(self, other):
        """Performs Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+":"+strlist(self.variables,":")+")*("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __ipow__(self, other):
        """Performs Exponentiation."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.name+":"+strlist(self.variables,":")+")^("+self.e.prepare(other, False, True)+")", self.e, self.variables, {self.name:self})
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")+("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")^("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")/("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})
    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfloat("("+self.e.prepare(other, False, True)+")*("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})
    def find(self):
        """Simplifies The Function String."""
        self.funcstr = self.e.find(self.funcstr, False, False)
    def getvars(self):
        """Returns The Original Variable List."""
        out = self.variables[:]
        if not self.overflow:
            out.append(self.allargs)
        return out
    def getpers(self):
        """Returns The Modified Personals List."""
        out = self.personals.copy()
        if classcalc.selfarg in out:
            out[classcalc.selfarg] = classcalc.selfarg
        return out
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, strfunc):
            return self.funcstr == other.funcstr and self.variables == other.variables and self.personals == other.personals and self.overflow == other.overflow
        elif isinstance(other, funcfloat):
            return self.funcstr == other.funcstr
        else:
            return False

class strfloat(strfunc):
    """Allows A String To Be Treated Like A Float."""
    def __init__(self, funcstr, e, variables=[], personals=None, check=True, name="func", overflow=None):
        """Initializes The String Float."""
        self.name = str(name)
        self.variables = variables[:]
        if self.allargs in self.variables:
            self.variables.remove(self.allargs)
            overflow = False
        elif overflow == None:
            overflow = True
        else:
            overflow = bool(overflow)
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
    check = 2
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
                elif x == "-":
                    if len(self.calcstr) > 0:
                        self.calcstr = self.calcstr[:-1]
                    x = ""
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
        """Retrieves A Representation."""
        return '"'+self.calcstr.replace("\\","\\\\").replace('"',"\\'").replace("\n","\\n")+'"'
    def __str__(self):
        """Retrieves The Evaluator String."""
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
            if other < 0:
                self.calcstr = self.calcstr[::-1]
                self *= -other
            else:
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
    def __cmp__(self, other):
        """Performs comparison."""
        if ismatrix(other):
            other = getmatrix(other).retrieve(0)
        if isinstance(other, strcalc):
            other = other.calcstr
        if self.calcstr == other:
            return 0
        elif self.calcstr > other:
            return -1
        else:
            return 1
    def __len__(self):
        """Performs len."""
        return len(self.calcstr)
    def __contains__(self, other):
        """Performs in."""
        return self.e.prepare(other, True, False) in self.calcstr
    def tomatrix(self):
        """Returns A Matrix Of The Characters."""
        out = []
        for x in self.calcstr:
            out.append(strcalc(x, self.e))
        return diagmatrixlist(out)

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
        params = varproc(params)
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
    def __init__(self, precall, e, funcstr="func"):
        """Constructs The Universalizer."""
        self.funcstr = str(funcstr)
        self.store = []
        self.precall = precall
        self.e = e
    def copy(self):
        """Copies The Universalizer Function."""
        return unifunc(self.precall, self.e, self.funcstr)
    def call(self, args):
        """Performs A Universalized Function Call."""
        args = varproc(args)
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

class derivbase(object):
    """Holds Methods Used In Derivative Functions."""
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        items = dict(self.personals)
        if x == None:
            return self.call([])
        else:
            items[self.variables[0]] = float(x)
            items[self.allargs] = matrix(1,1, x, fake=True)
            oldvars = self.e.setvars(items)
            self.e.info = " \\>"
            out = self.e.calc(self.funcstr)
            self.e.setvars(oldvars)
            return out
    def call(self, variables):
        """Calls The Derivative Function."""
        variables = varproc(variables)
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

class derivfunc(derivbase, strfunc):
    """Implements A Derivative Function."""
    def __init__(self, funcstr, n, accuracy, scaledown, e, varname="x", personals=None, name="derivfunc"):
        """Creates The Derivative Function."""
        self.name = str(name)
        self.funcstr = str(funcstr)
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        self.variables = [str(varname)]
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.overflow = True
        self.e = e
    def copy(self):
        """Returns A Copy Of The Derivative Function."""
        return derivfunc(self.funcstr, self.n, self.accuracy, self.scaledown, self.e, self.variables[0], self.personals, self.name)

class integfunc(integbase, strfunc):
    """Implements An Integral Function."""
    def __init__(self, funcstr, accuracy, e, varname="x", personals=None, name="integfunc"):
        """Creates The Integral Function."""
        self.name = str(name)
        self.funcstr = str(funcstr)
        self.accuracy = float(accuracy)
        self.variables = [str(varname)]
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.overflow = True
        self.e = e
    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfunc(self.funcstr, self.accuracy, self.e, self.variables[0], self.personals, self.name)

class derivfuncfloat(derivbase, funcfloat):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown, e, funcstr="derivfunc"):
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

class integfuncfloat(integbase, funcfloat):
    """Implements An Integral Function Of A Fake Function."""
    def __init__(self, func, accuracy, e, funcstr="integfunc"):
        """Creates The Integral Float Function."""
        self.accuracy = float(accuracy)
        self.funcstr = str(funcstr)
        self.func = func
        self.e = e
    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfuncfloat(self.func, self.accuracy, self.e, self.funcstr)

class classcalc(cotobject):
    """Implements An Evaluator Dictionary."""
    selfarg = "self"
    check = 1

    def __init__(self, e, variables=None):
        """Initializes The Dictionary."""
        self.variables = {}
        self.e = e
        if variables != None:
            self.add(variables)
    def copy(self):
        """Copies The Dictionary."""
        return classcalc(self.e, self.variables)
    def process(self, command, methods=True):
        """Processes A Command And Puts The Result In The Variables."""
        oldvars = self.e.variables.copy()
        returned = self.e.processor.returned
        self.e.setvars(self.variables)
        self.e.processor.process(str(command))
        self.e.processor.returned = returned
        for v in self.e.variables:
            if self.e.isreserved(v):
                oldvars[v] = self.e.variables[v]
            elif not v in oldvars or not self.e.variables[v] is oldvars[v]:
                self.store(v, self.e.variables[v], True, methods)
        self.e.variables = oldvars
    def calc(self, inputstring):
        """Calculates A String In The Environment Of The Dictionary."""
        oldvars = self.e.setvars(self.variables)
        self.e.info = " | class"
        out = self.e.calc(inputstring)
        self.e.setvars(oldvars)
        return out
    def items(self):
        """Returns The Variables."""
        return self.variables.items()
    def store(self, key, value, bypass=False, methods=True):
        """Stores An Item."""
        test = self.e.prepare(key, False, False)
        if bypass or not self.e.isreserved(test):
            if methods and isinstance(value, strfunc):
                value.personals[self.selfarg] = self
            self.variables[delspace(test)] = value
        else:
            self.e.processor.adderror("ClassError", "Could not store "+test+" in "+self.e.prepare(self, False, True, True))
    def retrieve(self, key):
        """Retrieves An Item."""
        test = self.e.prepare(key, False, False)
        if not self.e.isreserved(test) and test in self.variables:
            if istext(self.variables[test]):
                return self.calc(self.variables[test])
            else:
                return self.variables[test]
        else:
            self.e.processor.adderror("ClassError", "Could not find "+test+" in "+self.e.prepare(self, False, True, True))
            return matrix(0)
    def call(self, variables):
        """Calculates An Item."""
        variables = varproc(variables)
        if variables == None:
            return self
        elif len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return self.calc(self.e.prepare(variables[0], False, False))
        else:
            self.store(variables[0], variables[1])
            self.e.overflow = variables[2:]
            return self
    def __delitem__(self, key):
        """Wraps remove."""
        self.remove(key)
        return self
    def remove(self, key):
        """Removes An Item."""
        test = self.e.prepare(key, False, False)
        if not self.e.isreserved(test) and test in self.variables:
            del self.variables[test]
        else:
            self.e.processor.adderror("ClassError", "Could not remove "+test+" from "+self.e.prepare(self, False, True, True))
            return matrix(0)
    def extend(self, other):
        """Extends The Dictionary."""
        if isinstance(other, classcalc):
            self.add(other.variables)
            return self
        elif other == 0:
            return self
        else:
            raise TypeError("Could not extend fake list with "+repr(other))
    def add(self, other):
        """Adds Variables."""
        for k,v in other.items():
            self.store(k, v, True)
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, classcalc):
            return self.variables == other.variables
        else:
            return False
