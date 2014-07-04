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

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("find", self.funcstr)

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
    autoarg = "__auto__"

    def __init__(self, funcstr, e, variables=[], personals=None, name=None, overflow=None, allargs=None):
        """Creates A Callable String Function."""
        self.funcstr = str(funcstr)
        if name:
            self.name = str(name)
        else:
            self.name = self.autoarg
        if allargs != None:
            self.allargs = str(allargs)
        self.variables = variables[:]
        if overflow == None:
            self.overflow = True
        else:
            self.overflow = bool(overflow)
        if self.overflow and self.allargs in self.variables:
            self.variables.remove(self.allargs)
            self.overflow = False
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.e = e

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("strfunc", self.funcstr, self.variables, self.personals, self.name, self.overflow, self.allargs)

    def copy(self):
        """Copies The String Function."""
        return strfunc(self.funcstr, self.e, self.variables, self.personals, self.name, self.overflow, self.allargs)

    def calc(self, personals=True):
        """Calculates The String."""
        if personals:
            oldvars = self.e.setvars(self.personals)
        out = self.e.calc(self.funcstr)
        if personals:
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
                items, self.e.overflow = useparams(variables, self.variables, matrix(0))
            else:
                items, trash = useparams(variables, self.variables, matrix(0))
            items[self.allargs] = allvars
            for k in self.personals:
                if (not k in items) or isnull(items[k]):
                    items[k] = self.personals[k]
            oldvars = self.e.setvars(items)
            self.e.info = " \\>"
            out = self.calc(False)
            self.e.setvars(oldvars)
            return out

    def curry(self, arg):
        """Curries An Argument."""
        self.personals[self.variables.pop(0)] = arg

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
            if self.allargs == funcfloat.allargs:
                out.append(self.allargs)
            else:
                out.append("*"+self.allargs)
        return out

    def getpers(self):
        """Returns The Modified Personals List."""
        out = self.personals.copy()
        if "__self__" in out:
            del out["__self__"]
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
    def __init__(self, funcstr, e, variables=[], personals=None, check=True, name=None, overflow=None, allargs=None):
        """Initializes The String Float."""
        if name:
            self.name = str(name)
        else:
            self.name = self.autoarg
        if allargs != None:
            self.allargs = str(allargs)
        self.variables = variables[:]
        if overflow == None:
            overflow = True
        else:
            overflow = bool(overflow)
        if overflow and self.allargs in self.variables:
            self.variables.remove(self.allargs)
            overflow = False
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
        """Initializes An Evaluator String."""
        self.calcstr = ""
        func = False
        for x in str(calcstr):
            if func:
                func = False
                if x == "'":
                    x = '"'
                elif x == "-":
                    if len(self.calcstr) > 0:
                        self.calcstr = self.calcstr[:-1]
                    x = ""
                else:
                    self.calcstr += "\\"
            elif x == "\\":
                func = True
                x = ""
            self.calcstr += x
        self.calcstr = str(compute('"'+self.calcstr.replace('"', '\\"')+'"'))
        self.e = e

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("strcalc", self.calcstr)

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
        return '"'+repr(self.calcstr)[2:-1].replace("\\'", "'").replace('\\"', '"').replace('"', "\\'")+'"'

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
        if isinstance(other, strcalc):
            self += other
        else:
            other = getnum(other)
            if other and other != 1:
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

class rawstrcalc(strcalc):
    """A Raw Evaluator String."""
    def __init__(self, calcstr, e):
        """Initializes A Raw Evaluator String."""
        self.calcstr = str(calcstr)
        self.e = e

class usefunc(funcfloat):
    """Allows A Function To Be Used As A Variable."""
    def __init__(self, func, e, funcstr="func", variables=None, extras=None, overflow=False, evalinclude=False):
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
        self.evalinclude = evalinclude

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("usefunc", self.func, self.funcstr, self.variables, self.extras, self.overflow, self.evalinclude)

    def copy(self):
        """Copies The Function."""
        return usefunc(self.func, self.e, self.funcstr, self.variables, self.extras, self.overflow, self.evalinclude)

    def getextras(self):
        """Retrieves Extras."""
        out = self.extras.copy()
        if self.evalinclude:
            out[self.evalinclude] = self.e
        return out

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
        return self.func(*params, **self.getextras())

class unifunc(funcfloat):
    """Universalizes Function Calls."""
    def __init__(self, precall, e, funcstr=None):
        """Constructs The Universalizer."""
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.autoarg
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
    def __init__(self, func, e, funcstr=None):
        """Initializes The Evaluator Function."""
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.autoarg
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
    def __init__(self, funcstr, n, accuracy, scaledown, e, varname="x", personals=None, name=None):
        """Creates The Derivative Function."""
        if name:
            self.name = str(name)
        else:
            self.name = self.autoarg
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

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("derivfunc", self.funcstr, self.n, self.accuracy, self.scaledown, self.varname, self.personals, self.name)

    def copy(self):
        """Returns A Copy Of The Derivative Function."""
        return derivfunc(self.funcstr, self.n, self.accuracy, self.scaledown, self.e, self.variables[0], self.personals, self.name)

class integfunc(integbase, strfunc):
    """Implements An Integral Function."""
    def __init__(self, funcstr, accuracy, e, varname="x", personals=None, name=None):
        """Creates The Integral Function."""
        if name:
            self.name = str(name)
        else:
            self.name = self.autoarg
        self.funcstr = str(funcstr)
        self.accuracy = float(accuracy)
        self.variables = [str(varname)]
        if personals == None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        self.overflow = True
        self.e = e

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("integfunc", self.funcstr, self.accuracy, self.varname, self.personals, self.name)

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfunc(self.funcstr, self.accuracy, self.e, self.variables[0], self.personals, self.name)

class derivfuncfloat(derivbase, funcfloat):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown, e, funcstr=None):
        """Creates The Derivative Function."""
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.autoarg
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
    def __init__(self, func, accuracy, e, funcstr=None):
        """Creates The Integral Float Function."""
        self.accuracy = float(accuracy)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.autoarg
        self.func = func
        self.e = e

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfuncfloat(self.func, self.accuracy, self.e, self.funcstr)

class classcalc(cotobject):
    """Implements An Evaluator Class."""
    def __init__(self, e, variables=None):
        """Initializes The Class."""
        self.e = e
        self.variables = {"__self__": self}
        if variables != None:
            self.add(variables)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("classcalc", self.e.processor.getstates(self.getvars()))

    def copy(self):
        """Copies The Class."""
        return classcalc(self.e, self.variables)

    def process(self, command):
        """Processes A Command And Puts The Result In The Variables."""
        returned = self.e.processor.returned
        oldshow = self.e.processor.doshow
        self.e.processor.doshow = False
        oldclass = self.e.processor.useclass
        self.e.processor.useclass = "__self__"

        oldvars = self.e.setvars(self.variables)
        self.e.processor.process(str(command))
        self.e.setvars(oldvars)

        self.e.processor.useclass = oldclass
        self.e.processor.doshow = oldshow
        self.e.processor.returned = returned

    def calc(self, inputstring):
        """Calculates A String In The Environment Of The Class."""
        oldvars = self.e.setvars(self.variables)
        self.e.info = " | class"
        out = self.e.calc(inputstring)
        self.e.setvars(oldvars)
        return out

    def __len__(self):
        """Finds The Number Of Variables."""
        return len(self.variables)

    def items(self):
        """Returns The Variables."""
        return self.variables.items()

    def __repr__(self):
        """Finds A Representation."""
        return '{ "CLASS" }'

    def store(self, key, value, bypass=False):
        """Stores An Item."""
        test = delspace(self.e.prepare(key, False, False))
        if bypass or not self.e.isreserved(test, allowed=string.digits):
            self.variables[test] = value
        else:
            raise ExecutionError("ClassError", "Could not store "+test+" in "+self.e.prepare(self, False, True, True))

    def tryget(self, key):
        """Attempts To Get An Item."""
        try:
            out = self.retrieve(key)
        except ExecutionError as detail:
            if detail.name == "ClassError" and detail.message.startswith("Could not find ") and detail.message.endswith(" in the class"):
                out = None
            else:
                raise
        return out

    def getitem(self, test):
        """Retrieves An Item At The Base Level."""
        if istext(self.variables[test]):
            return self.calc(self.variables[test])
        else:
            return self.variables[test]

    def retrieve(self, key):
        """Retrieves An Item."""
        test = delspace(self.e.prepare(key, False, False))
        if not self.e.isreserved(test, allowed=string.digits):
            if test in self.variables:
                return self.getitem(test)
            else:
                raise ExecutionError("ClassError", "Could not find "+test+" in "+self.e.prepare(self, False, True, True))
        else:
            raise ExecutionError("ClassError", "Invalid class key of "+test)

    def call(self, variables):
        """Calculates An Item."""
        variables = varproc(variables)
        return self.toinstance().init(variables)

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
            raise ExecutionError("ClassError", "Could not remove "+test+" from "+self.e.prepare(self, False, True, True))

    def extend(self, other):
        """Extends The Class."""
        if isinstance(other, (dict, classcalc)):
            self.add(other.variables)
            return self
        elif other == 0:
            return self
        else:
            raise ExecutionError("ClassError", "Could not extend class with "+repr(other))

    def add(self, other):
        """Adds Variables."""
        for k,v in other.items():
            self.store(k, v, True)

    def getvars(self):
        """Gets Original Variables."""
        out = self.variables.copy()
        del out["__self__"]
        return out

    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, classcalc):
            return self.variables["__self__"] is other.variables["__self__"] or self.getvars() == other.getvars()
        else:
            return False

    def __imul__(self, other):
        """Performs Multiplication In-Place."""
        self.extend(other)

    def toinstance(self):
        """Creates An Instance Of The Class."""
        return instancecalc(self.e, self.variables)

    def tomatrix(self):
        """Returns A Matrix Of The Variables."""
        out = []
        for key in self.getvars().keys():
            out.append(strcalc(key, self.e))
        return diagmatrixlist(out)

class instancecalc(numobject, classcalc):
    """An Evaluator Class Instance."""
    def __init__(self, e, variables, parent=None):
        """Creates An Instance Of An Evaluator Class."""
        self.e = e
        if parent == None:
            self.parent = variables
        else:
            self.parent = parent
        self.variables = variables.copy()

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("instancecalc", self.e.processor.getstates(self.getvars()), self.e.processor.getstates(self.parent))

    def copy(self):
        """Copies The Instance."""
        return instancecalc(self.e, self.variables, self.parent)

    def getparent(self):
        """Reconstructs The Parent Class."""
        return classcalc(self.e, self.parent)

    def toclass(self):
        """Converts To A Normal Class."""
        return classcalc(self.e, self.variables)

    def isfrom(self, parent):
        """Determines Whether The Instance Is From The Parent."""
        if isinstance(parent, classcalc):
            parent = parent.variables
        elif not isinstance(parent, dict):
            return False
        if parent["__self__"] is self.variables["__self__"]:
            return True
        parent = parent.copy()
        del parent["__self__"]
        variables = self.variables.copy()
        del variables["__self__"]
        return variables == parent

    def domethod(self, item, args=[]):
        """Calls A Method Function."""
        if isfunc(item):
            if not islist(args):
                args = [args]
            if isinstance(item, strfunc):
                self.selfcurry(item)
                if item.overflow and len(args) > len(item.variables):
                    args = args[:len(item.variables)-1] + [diagmatrixlist(args[len(item.variables)-1:])]
            return getcall(item)(args)
        else:
            return item

    def selfcurry(self, out):
        """Curries Self Into The Function."""
        if "__self__" in out.personals:
            out.personals["__self__"] = self
        elif len(out.variables) > 0:
            out.personals["__self__"] = self
            out.curry("__self__")
        else:
            raise ExecutionError("ClassError", "Methods must have self as their first argument")

    def retrieve(self, key):
        """Retrieves An Item."""
        test = delspace(self.e.prepare(key, False, False))
        if not self.e.isreserved(test, allowed=string.digits):
            if test in self.variables:
                out = self.getitem(test)
            elif "__get__" in self.variables:
                out = self.domethod(self.getitem("__get__"), strcalc(test, self.e))
            else:
                raise ExecutionError("ClassError", "Could not find "+test+" in the class")
            if isinstance(out, strfunc):
                self.selfcurry(out)
            return out
        else:
            raise ExecutionError("ClassError", "Invalid class key of "+test)

    def store(self, key, value, bypass=False):
        """Stores An Item."""
        test = delspace(self.e.prepare(key, False, False))
        if bypass:
            self.variables[test] = value
        else:
            check_set = self.tryget("__set__")
            if check_set:
                self = self.domethod(check_set, [strcalc(key, self.e), value])
            elif not self.e.isreserved(test, allowed=string.digits):
                if isinstance(value, strfunc):
                    self.selfcurry(value)
                self.variables[test] = value
            else:
                raise ExecutionError("ClassError", "Could not store "+test+" in "+self.e.prepare(self, False, True, True))

    def init(self, params):
        """Initializes The Instance."""
        if "__init__" in self.variables:
            item = self.calc("__init__")
            if isfunc(item):
                value = self.domethod(item, params)
            else:
                self.e.overflow = params
                value = item
            if isinstance(value, instancecalc):
                return value
            else:
                raise ExecutionError("ClassError", "The class's __init__ method returned the non-class object "+self.e.prepare(value, False, True, True))
        else:
            return self

    def isfunc(self):
        """Determines Whether The Class Is A Function."""
        return bool(self.tryget("__call__"))

    def call(self, variables):
        """Calls The Function."""
        func = self.tryget("__call__")
        if func == None:
            raise ExecutionError("ClassError", "The class being called has no __call__ method")
        else:
            return self.domethod(func, variables)

    def ismatrix(self):
        """Determines Whether The Class Can Be A Matrix."""
        return bool(self.tryget("__cont__"))

    def tomatrix(self):
        """Converts To Matrix."""
        func = self.tryget("__cont__")
        if func == None:
            raise ExecutionError("ClassError", "The class being converted to a container has no __cont__ method")
        else:
            return self.domethod(func)

    def __iadd__(self, other):
        """Performs Addition."""
        check_add = self.tryget("__add__")
        if check_add:
            return self.domethod(check_add, other)
        check_sub = self.tryget("__sub__")
        if check_sub:
            return self.domethod(check_sub, -other)
        raise ExecutionError("ClassError", "Insufficient methods defined for addition")

    def __isub__(self, other):
        """Performs Subtraction."""
        check_sub = self.tryget("__sub__")
        if check_sub:
            return self.domethod(check_sub, other)
        check_add = self.tryget("__add__")
        if check_add:
            return self.domethod(check_add, -other)
        raise ExecutionError("ClassError", "Insufficient methods defined for subtraction")

    def __imul__(self, other):
        """Performs Multiplication."""
        check_mul = self.tryget("__mul__")
        if check_mul:
            return self.domethod(check_mul, other)
        check_div = self.tryget("__div__")
        if check_div:
            return self.domethod(check_div, 1.0/other)
        if other == int(other):
            try:
                for x in xrange(0, int(other)):
                    self += self
            except ExecutionError:
                pass
        raise ExecutionError("ClassError", "Insufficient methods defined for multiplication")

    def __idiv__(self, other):
        """Performs Division."""
        check_div = self.tryget("__div__")
        if check_div:
            return self.domethod(check_div, other)
        check_mul = self.tryget("__mul__")
        if check_mul:
            return self.domethod(check_mul, 1.0/other)
        other = 1.0/other
        if other == int(other):
            try:
                for x in xrange(0, int(other)):
                    self += self
            except ExecutionError:
                pass
        raise ExecutionError("ClassError", "Insufficient methods defined for division")

    def __imod__(self, other):
        """Performs Moduluo."""
        check_mod = self.tryget("__mod__")
        if check_mod:
            self = self.domethod(check_mod, other)
        try:
            while self >= other:
                self -= other
        except ExecutionError:
            try:
                result = float(self/other)
                self = (result-int(result))*other
            except ExecutionError:
                raise ExecutionError("ClassError", "Insufficient methods defined for modulo")
        return self

    def __ipow__(self, other):
        """Performs Exponentiation."""
        check_pow = self.tryget("__pow__")
        if check_pow:
            return self.domethod(check_pow, other)
        if other == int(other):
            try:
                for x in xrange(0, int(other)):
                    self *= self
            except ExecutionError:
                pass
        raise ExecutionError("ClassError", "Insufficient methods defined for exponentiation")

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        check_rdiv = self.tryget("__rdiv__")
        if check_rdiv:
            return self.domethod(check_rdiv, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for reverse division")

    def __rmod__(self, other):
        """Performs Reverse Modulo."""
        check_rmod = self.tryget("__rmod__")
        if check_rmod:
            return self.domethod(check_rmod, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for reverse modulo")

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        check_rpow = self.tryget("__rpow__")
        if check_rpow:
            return self.domethod(check_rpow, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for reverse exponentiation")

    def __float__(self):
        """Retrieves A Float."""
        return float(self.tonum())

    def __int__(self):
        """Retrieves An Integer."""
        return int(self.tonum())

    def tonum(self):
        """Converts To Float."""
        check_num = self.tryget("__num__")
        if check_num:
            return self.domethod(check_num)
        raise ExecutionError("ClassError", "Insufficient methods defined for conversion to number")

    def __abs__(self):
        """Performs Absolute Value."""
        check_abs = self.tryget("__abs__")
        if check_abs:
            return self.domethod(check_abs)
        if self < 0:
            return -self
        else:
            return self

    def __cmp__(self, other):
        """Performs Comparison."""
        check_cmp = self.tryget("__cmp__")
        if check_cmp:
            return self.domethod(check_cmp, other)
        if self == other:
            return 0
        elif self > other:
            return 1
        else:
            return -1

    def __eq__(self, other):
        """Performs Equal."""
        if not hasnum(other):
            return False
        elif self is other:
            return True
        else:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_eq, other)
            check_cmp = self.tryget("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
            check_ne = self.tryget("__ne__")
            if check_ne:
                return not self.domethod(check_ne, other)
            check_gt = self.tryget("__gt__")
            if check_gt:
                check_lt = self.tryget("__lt__")
                if check_lt:
                    return not self.domethod(check_gt, other) and not self.domethod(check_lt, other)
            check_ge = self.tryget("__ge__")
            if check_ge:
                check_le = self.tryget("__le__")
                if check_le:
                    return self.domethod(check_ge, other) and self.domethod(check_le, other)
            return self.toclass() == other

    def __ne__(self, other):
        """Performs Not Equal."""
        if not hasnum(other):
            return True
        elif self is other:
            return False
        else:
            check_ne = self.tryget("__ne__")
            if check_ne:
                return self.domethod(check_ne, other)
            check_cmp = self.tryget("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
            check_eq = self.tryget("__eq__")
            if check_eq:
                return not self.domethod(check_eq, other)
            check_gt = self.tryget("__gt__")
            if check_gt:
                check_lt = self.tryget("__lt__")
                if check_lt:
                    return not self.domethod(check_gt, other) and not self.domethod(check_lt, other)
            check_ge = self.tryget("__ge__")
            if check_ge:
                check_le = self.tryget("__le__")
                if check_le:
                    return not (self.domethod(check_ge, other) and self.domethod(check_le, other))
            return self.toclass() != other

    def __gt__(self, other):
        """Performs Greater Than."""
        check_gt = self.tryget("__gt__")
        if check_gt:
            return self.domethod(check_gt, other)
        check_cmp = self.tryget("__cmp__")
        if check_cmp:
            return self.domethod(check_cmp, other) > 0.0
        check_le = self.tryget("__le__")
        if check_le:
            return not self.domethod(check_le, other)
        check_ge = self.tryget("__ge__")
        if check_ge:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_ge, other) and not self.domethod(check_eq, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for greater than")

    def __lt__(self, other):
        """Performs Less Than."""
        check_lt = self.tryget("__lt__")
        if check_lt:
            return self.domethod(check_lt, other)
        check_cmp = self.tryget("__cmp__")
        if check_cmp:
            return self.domethod(check_cmp, other) < 0.0
        check_ge = self.tryget("__ge__")
        if check_ge:
            return not self.domethod(check_ge, other)
        check_le = self.tryget("__le__")
        if check_le:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_le, other) and not self.domethod(check_eq, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for less than")

    def __ge__(self, other):
        """Performs Greater Than Or Equal."""
        check_ge = self.tryget("__ge__")
        if check_ge:
            return self.domethod(check_ge, other)
        check_cmp = self.tryget("__cmp__")
        if check_cmp:
            return self.domethod(check_cmp, other) >= 0.0
        check_lt = self.tryget("__lt__")
        if check_lt:
            return not self.domethod(check_lt, other)
        check_gt = self.tryget("__gt__")
        if check_gt:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_gt, other) or self.domethod(check_eq, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for greater than or equal")

    def __le__(self, other):
        """Performs Less Than Or Equal."""
        check_le = self.tryget("__le__")
        if check_le:
            return self.domethod(check_le, other)
        check_cmp = self.tryget("__cmp__")
        if check_cmp:
            return self.domethod(check_cmp, other) <= 0.0
        check_gt = self.tryget("__gt__")
        if check_gt:
            return not self.domethod(check_gt, other)
        check_lt = self.tryget("__lt__")
        if check_lt:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_lt, other) or self.domethod(check_eq, other)
        raise ExecutionError("ClassError", "Insufficient methods defined for less than or equal")

    def __str__(self):
        """Retrieves A String."""
        out = None
        check_str = self.tryget("__str__")
        if check_str:
            out = self.domethod(check_str)
        else:
            check_repr = self.tryget("__repr__")
            if check_repr:
                out = self.domethod(check_repr)
        if out == None:
            return self.e.prepare(self.toclass(), True, False)+" ( )"
        else:
            return self.e.prepare(out, True, False)

    def getrepr(self, maxrecursion=10):
        """Retrieves A Representation."""
        out = None
        check_repr = self.tryget("__repr__")
        if check_repr:
            out = self.domethod(check_repr)
        else:
            check_str = self.tryget("__str__")
            if check_str:
                out = self.domethod(check_str)
        if out == None:
            return self.e.prepare(self.toclass(), False, True, maxrecursion=maxrecursion-1)+"( )"
        else:
            return self.e.prepare(out, False, False, maxrecursion=maxrecursion-1)

    def __len__(self):
        """Retrieves The Length."""
        out = None
        check_len = self.tryget("__len__")
        if check_len:
            out = self.domethod(check_len)
        else:
            check_cont = self.tryget("__cont__")
            if check_cont:
                out = len(self.domethod(check_cont))
        if out == None:
            raise ExecutionError("ClassError", "Insufficient methods defined for length")
        else:
            return int(out)

    def __bool__(self):
        """Converts To A Boolean."""
        out = None
        check_bool = self.tryget("__bool__")
        if check_bool:
            out = self.domethod(check_bool)
        else:
            check_num = self.tryget("__num__")
            if check_num:
                out = self.domethod(check_num)
        if out == None:
            try:
                out = len(self) > 0
            except ExecutionError:
                raise ExecutionError("ClassError", "Insufficient methods defined for bool")
        return bool(out)

    def typecalc(self):
        """Finds The Type Of The Instance."""
        item = self.tryget("__type__")
        if item:
            return self.domethod(item)
        else:
            return strcalc("instance", self.e)
