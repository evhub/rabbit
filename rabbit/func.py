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

from .matrix import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TailRecursion(BaseException):
    """A Stack-Killer Tail Recursion Exception."""
    def __init__(self, funcstr, variables=None):
        """Creates The Tail Recursion."""
        self.funcstr = funcstr
        self.variables = variables or {}

def collapse(item):
    """Collapses An Argument."""
    if isinstance(item, funcfloat):
        if item.reqargs > 0:
            raise ExecutionError("ArgumentError", "Not enough arguments supplied to collapse "+item.e.prepare(item, False, True, True))
        else:
            return item.calc()
    elif isinstance(item, codestr):
        return item.calc()
    else:
        return item

def isbuiltin(inputobject):
    """Checks Whether An Object Is A Builtin."""
    return isinstance(inputobject, funcfloat) and not isinstance(inputobject, strfunc)

def ismatrix(inputobject):
    """Checks Whether An Object Is A Matrix."""
    return hasmatrix(inputobject) and (not hasattr(inputobject, "notmatrix") or not inputobject.notmatrix)

def isprop(inputobject):
    """Checks Whether An Object Is A Property."""
    return hasnum(inputobject) and hasattr(inputobject, "isprop") and ((isinstance(inputobject.isprop, bool) and inputobject.isprop) or inputobject.isprop())

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
    if variables is None or islist(variables) or isinstance(variables, dict):
        return variables
    elif isinstance(variables, matrix):
        return variables.getitems()
    elif isinstance(variables, tuple):
        return list(variables)
    else:
        return [variables]

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

class funcfloat(numobject):
    """Allows The Creation Of A Float Function."""
    evaltype = "function"
    overflow = False
    memoize = True
    allargs = "__"
    reqargs = -1
    infix = True

    def __init__(self, func, e, funcstr=None, reqargs=None, memoize=None, memo=None):
        """Constructs The Float Function."""
        self.e = e
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.base_func = func
        if reqargs is not None:
            self.reqargs = reqargs

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("find", self.funcstr)

    def copy(self):
        """Returns A Copy Of The Float Function."""
        return funcfloat(self.base_func, self.e, self.funcstr, self.reqargs, self.memoize, self.memo)

    def keyhash(self, args):
        """Creates An Argument Hash."""
        if islist(args) or isinstance(args, tuple):
            new = []
            for item in args:
                new.append(self.keyhash(item))
            out = tuple(new)
        elif isinstance(args, dict):
            keys = []
            values = []
            for k,v in args.items():
                keys.append(k)
                values.append(self.keyhash(v))
            out = (tuple(keys), tuple(values))
        elif hasattr(args, "getstate"):
            out = self.keyhash(itemstate(args))
        else:
            out = args
        return out

    def func(self, *args, **kwargs):
        """Calls The Memoized Function."""
        arghash = None
        if len(self.memo) > 0:
            arghash = (self.keyhash(args), self.keyhash(kwargs))
            if arghash in self.memo:
                return self.memo[arghash]
        if self.memoize:
            returned = self.e.returned
            self.e.setreturned(False)
            try:
                out = self.base_func(*args, **kwargs)
            except Exception:
                self.e.setreturned()
                raise
            else:
                self.e.setreturned(returned or self.e.returned)
                if not self.e.returned:
                    if arghash is None:
                        arghash = (self.keyhash(args), self.keyhash(kwargs))
                    self.memo[arghash] = out
                return out
        else:
            return self.base_func(*args, **kwargs)

    def calc(self, variables=None):
        """Calculates The Float Function."""
        if variables is None:
            variables = []
        return self.func(variables)

    def call(self, variables):
        """Calls The Float Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif len(variables) < self.reqargs:
            out = self.copy()
            for arg in variables:
                out.curry(arg)
            return out
        else:
            return self.calc(variables)

    def curry(self, arg):
        """Curries An Argument."""
        old_func = self.func
        self.func = lambda variables: old_func([arg]+variables)
        self.reqargs -= 1
        self.funcstr += ":("+self.e.prepare(arg, False, True)+")"

    def __str__(self):
        """Retrieves The Function String."""
        return self.funcstr

    def __iadd__(self, other):
        """Performs Addition."""
        if other == 0.0 or isnull(other):
            return self
        else:
            return strfunc("("+self.funcstr+"("+self.allargs+"))+"+self.e.wrap(other), self.e, [self.allargs], {self.funcstr:self})

    def __idiv__(self, other):
        """Performs Division."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.funcstr+"("+self.allargs+"))/"+self.e.wrap(other), self.e, [self.allargs], {self.funcstr:self})

    def __imul__(self, other):
        """Performs Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.funcstr+"("+self.allargs+"))*"+self.e.wrap(other), self.e, [self.allargs], {self.funcstr:self})

    def __ipow__(self, other):
        """Performs Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.funcstr+"("+self.allargs+"))^"+self.e.wrap(other), self.e, [self.allargs], {self.funcstr:self})

    def __radd__(self, other):
        """Performs Reverse Addition."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"+("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"^("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"/("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"*("+self.funcstr+"("+self.allargs+"))", self.e, [self.allargs], {self.funcstr:self})

    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, funcfloat) and not isinstance(other, strfunc):
            return self.base_func == other.base_func and self.reqargs == other.reqargs
        else:
            return False

class strfunc(funcfloat):
    """Allows A String Function To Be Callable."""
    method = None
    lexical = True

    def __init__(self, funcstr, e, variables=None, personals=None, name=None, overflow=None, allargs=None, reqargs=None, memoize=None, memo=None, method=None):
        """Creates A Callable String Function."""
        self.e = e
        self.funcstr = self.e.namefind(str(funcstr))
        if name:
            self.name = str(name)
        else:
            self.name = self.e.unusedarg()
        if allargs is not None:
            self.allargs = str(allargs)
        if variables is None:
            self.variables = []
        else:
            self.variables = variables[:]
        if overflow is None:
            self.overflow = True
        else:
            self.overflow = bool(overflow)
        if self.overflow and self.allargs in self.variables:
            self.variables.remove(self.allargs)
            self.overflow = False
        if personals is None:
            self.personals = {}
        else:
            self.personals = dict(personals)
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        if reqargs is None:
            self.reqargs = len(self.variables)
        else:
            self.reqargs = reqargs
        if self.lexical:
            self.snapshot = self.e.variables.copy()
        else:
            self.snapshot = {}
        if method is not None:
            self.method = method

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if self.method:
            memo = None
        else:
            memo = getstates(self.memo)
        return ("strfunc", self.funcstr, self.variables, getstates(self.getpers()), self.name, self.overflow, self.allargs, self.reqargs, self.memoize, memo, self.method)

    def copy(self):
        """Copies The String Function."""
        return strfunc(self.funcstr, self.e, self.variables, self.personals, self.name, self.overflow, self.allargs, self.reqargs, self.memoize, self.memo, self.method)

    def calc(self, personals=None):
        """Calculates The String."""
        if personals is None:
            personals = self.personals
        return self.func(personals)

    def base_func(self, personals):
        """Allows For Tail Recursion."""
        funcstr = self.funcstr
        variables = self.snapshot.copy()
        variables.update(personals)
        out = None
        while out is None:
            if self.e.tailing and self.e.all_clean:
                newvars = self.e.variables.copy()
                newvars.update(variables)
                raise TailRecursion(funcstr, newvars)
            else:
                cleaned = self.e.clean_begin(True, True)
                tailing, self.e.tailing = self.e.tailing, True
                oldvars = self.e.setvars(variables)
                try:
                    out = self.e.calc(funcstr, " \\>")
                except TailRecursion as params:
                    if not self.e.returned and funcstr == params.funcstr and variables == params.variables:
                        raise ExecutionError("RuntimeError", "Illegal infinite recursive loop")
                    else:
                        funcstr = params.funcstr
                        variables = params.variables
                finally:
                    self.e.tailing = tailing
                    self.e.clean_end(cleaned)
                    self.e.setvars(oldvars)
        return out

    def call(self, variables):
        """Calls The String Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif len(variables) < self.reqargs:
            out = self.copy()
            for arg in variables:
                out.curry(arg)
            return out
        else:
            allvars = diagmatrixlist(variables)
            if self.overflow:
                items, self.e.overflow = useparams(variables, self.variables, matrix(0))
            else:
                items, _ = useparams(variables, self.variables, matrix(0))
            items[self.allargs] = allvars
            for k in self.personals:
                if (not k in items) or isnull(items[k]):
                    items[k] = self.personals[k]
            out = self.calc(items)
            return out

    def curry(self, arg):
        """Curries An Argument."""
        self.personals[self.variables.pop(0)] = arg
        self.reqargs -= 1

    def __iadd__(self, other):
        """Performs Addition."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")+"+self.e.wrap(other), self.e, self.variables, {self.name:self})

    def __idiv__(self, other):
        """Performs Division."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")/"+self.e.wrap(other), self.e, self.variables, {self.name:self})

    def __imul__(self, other):
        """Performs Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")*"+self.e.wrap(other), self.e, self.variables, {self.name:self})

    def __ipow__(self, other):
        """Performs Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")^"+self.e.wrap(other), self.e, self.variables, {self.name:self})

    def __radd__(self, other):
        """Performs Reverse Addition."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"+("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"^("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"/("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if other == 1.0 or isnull(other):
            return self
        else:
            return strfunc(self.e.wrap(other)+"*("+self.name+":"+strlist(self.variables,":")+")", self.e, self.variables, {self.name:self})

    def find(self):
        """Simplifies The Function String."""
        self.funcstr = self.e.find(self.funcstr, False)

    def getvars(self):
        """Returns The Original Variable List."""
        out = self.variables[:]
        for x in xrange(self.reqargs, len(out)):
            out[x] = "-"+out[x]
        if not self.overflow:
            if self.allargs == funcfloat.allargs:
                out.append(self.allargs)
            else:
                out.append("*"+self.allargs)
        return out

    def getpers(self):
        """Returns The Modified Personals List."""
        out = self.personals.copy()
        if self.method and self.method in out:
            del out[self.method]
        return out

    def getitem(self, test):
        """Retrieves A Personal At The Base Level."""
        if istext(self.personals[test]):
            self.personals[test] = self.e.calc(self.personals[test])
        return self.personals[test]

    def getmethod(self, key):
        """Retrieves A Personal."""
        test = delspace(self.e.prepare(key, False, False))
        if not self.e.isreserved(test) and test in self.personals:
            return self.getitem(test)
        else:
            return None

    def curryself(self, other):
        """Curries Self Into The Function."""
        self.method = self.method or other.selfvar
        if self.method in self.personals:
            self.personals[self.method] = other
        elif len(self.variables) > 0:
            self.personals[self.method] = other
            self.curry(self.method)
        else:
            raise ExecutionError("ClassError", "Methods must have self as their first argument")

    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, strfunc):
            return self.funcstr == other.funcstr and self.variables == other.variables and self.personals == other.personals and self.overflow == other.overflow and self.reqargs == other.reqargs and self.allargs == other.allargs and self.method == other.method
        else:
            return False

class strfloat(strfunc):
    """Allows A String To Be Treated Like A Float."""
    def __init__(self, funcstr, e, variables=None, personals=None, check=True, name=None, overflow=None, allargs=None, reqargs=None):
        """Initializes The String Float."""
        self.e = e
        if name:
            self.name = str(name)
        else:
            self.name = None
        if allargs is not None:
            self.allargs = str(allargs)
        if variables is None:
            variables = []
        else:
            variables = variables[:]
        if overflow is None:
            overflow = True
        else:
            overflow = bool(overflow)
        if overflow and self.allargs in variables:
            variables.remove(self.allargs)
            overflow = False
        if personals is None:
            personals = {}
        else:
            personals = dict(personals)
        if reqargs is None:
            self.reqargs = len(variables)
        else:
            self.reqargs = reqargs
        funcstr = self.e.namefind(str(funcstr))
        if check:
            test = self.e.find(funcstr, True)
        if check and isinstance(test, strfunc):
            self.name = self.name or test.name
            self.funcstr = test.funcstr
            self.overflow = overflow and test.overflow
            self.variables = variables
            self.reqargs += test.reqargs
            for x in test.variables:
                if not x in self.variables:
                    self.variables.append(x)
                else:
                    self.reqargs -= 1
            self.personals = test.personals
            for x,y in personals:
                if y != test:
                    self.personals[x] = y
            if allargs is None:
                self.allargs = test.allargs
            if self.overflow and self.allargs in self.variables:
                self.variables.remove(self.allargs)
                self.overflow = False
            self.memoize = test.memoize
            self.memo = test.memo
            self.snapshot = test.snapshot
            if self.lexical:
                self.snapshot.update(self.e.variables)
            self.method = test.method
        else:
            if self.name is None:
                self.name = self.e.unusedarg()
            self.funcstr = funcstr
            self.overflow = overflow
            self.variables = variables
            self.personals = personals
            self.memo = {}
            if self.lexical:
                self.snapshot = self.e.variables.copy()
            else:
                self.snapshot = {}

class strcalc(numobject):
    """Allows Strings Inside Evaluation."""
    evaltype = "string"
    notmatrix = True
    check = 2

    def __init__(self, calcstr, e):
        """Initializes An Evaluator String."""
        self.e = e
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
        if func:
            self.calcstr += "\\\\"
        self.calcstr = str(compute('"""'+self.calcstr.replace('"', '\\"')+'"""'))

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("strcalc", self.calcstr)

    def __hash__(self):
        """Returns A Hash Of The String."""
        return hash(self.calcstr)

    def copy(self):
        """Returns A Copy Of The Evaluator String."""
        return rawstrcalc(self.calcstr, self.e)

    def getfloat(self):
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
        out = []
        inside = False
        special = False
        for c in repr(self.calcstr):
            if special:
                if c not in "\"'":
                    out.append("\\")
                out.append(c)
                special = False
            elif c == "\\":
                special = True
            elif inside:
                if c == inside:
                    inside = False
                else:
                    out.append(c)
            elif c in "\"'":
                inside = c
        return '"'+"".join(out).replace('"', "\\'")+'"'

    def __str__(self):
        """Retrieves The Evaluator String."""
        return self.calcstr

    def __iadd__(self, other):
        """Performs Addition."""
        if not isnull(other):
            self.calcstr += self.e.prepare(other, True, False)
        return self

    def __radd__(self, other):
        """Performs Reverse Addition."""
        if not isnull(other):
            self.calcstr = self.e.prepare(other, True, False)+self.calcstr
        return self

    def __idiv__(self, other):
        """Performs Division."""
        if not isnull(other):
            self.calcstr = self.calcstr[:int(len(self.calcstr)/other)]
        return self

    def __imul__(self, other):
        """Performs Multiplication."""
        if isinstance(other, strcalc):
            self += other
        else:
            other = getnum(other)
            if not other:
                self.calcstr = ""
            elif other != 1:
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
        """Performs Comparison."""
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

    def __isub__(self, other):
        """Performs Subtraction."""
        self.calcstr.replace(self.e.prepare(other, True, False), "")

    def tomatrix(self):
        """Returns A Matrix Of The Characters."""
        out = []
        for x in self.calcstr:
            out.append(strcalc(x, self.e))
        return diagmatrixlist(out)

    def itemcall(self, params):
        """Performs A Colon Splice."""
        item = self.calcstr
        if len(params) == 0:
            value = rawstrcalc(item[-1], self)
        elif len(params) == 1:
            value = rawstrcalc(item[int(params[0])], self)
        else:
            value = rawstrcalc(item[int(params[0]):int(params[1])], self)
            self.e.overflow = params[2:]
        return value

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if bottom:
            return repr(self)
        else:
            return str(self)

    def __imod__(self, other):
        """Performs String Formatting."""
        if isinstance(other, dictionary):
            self.calcstr %= other.a
        elif ismatrix(other):
            self.calcstr %= tuple(getmatrix(other).getitems())
        else:
            raise TypeError("Strings can only be formatted by dictionaries and matrices")

class rawstrcalc(strcalc):
    """A Raw Evaluator String."""
    def __init__(self, calcstr, e):
        """Initializes A Raw Evaluator String."""
        self.e = e
        self.calcstr = str(calcstr)

class codestr(rawstrcalc):
    """A Code Evaluator String."""
    itemcall = None
    evaltype = "code"
    check = 1

    def __init__(self, calcstr, e):
        """Initializes A Code Evaluator String."""
        self.e = e
        self.calcstr = basicformat(calcstr)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("codestr", self.calcstr)

    def copy(self):
        """Returns A Copy Of The Code String."""
        return codestr(self.calcstr, self.e)

    def calc(self):
        """Calculates The Code String."""
        return self.e.calc(self.calcstr, " ::>")

    def call(self, variables):
        """Calls The Code String."""
        if variables is None:
            return self
        else:
            self.e.overflow = variables
            return self.calc()

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if bottom:
            return "\xab "+str(self)+" \xbb"
        else:
            return str(self)

class usefunc(funcfloat):
    """Allows A Function To Be Used As A Variable."""
    def __init__(self, func, e, funcstr=None, variables=None, extras=None, overflow=True, reqargs=None, evalinclude=False, memoize=None, memo=None):
        """Creates A Callable Function."""
        self.e = e
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        self.overflow = bool(overflow)
        if variables is None:
            self.variables = []
        else:
            self.variables = variables
        if extras is None:
            self.extras = {}
        else:
            self.extras = dict(extras)
        if reqargs is not None:
            self.reqargs = reqargs
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.base_func = func
        self.evalinclude = evalinclude

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if ismethod(self.base_func):
            return ("find", self.funcstr)
        else:
            return ("usefunc", self.base_func, self.funcstr, self.variables, self.extras, self.overflow, self.reqargs, self.evalinclude, self.memoize, getstates(self.memo))

    def copy(self):
        """Copies The Function."""
        return usefunc(self.base_func, self.e, self.funcstr, self.variables, self.extras, self.overflow, self.reqargs, self.evalinclude, self.memoize, self.memo)

    def getextras(self):
        """Retrieves Extras."""
        out = self.extras.copy()
        if self.evalinclude:
            out[self.evalinclude] = self.e
        return out

    def curry(self, arg):
        """Curries An Argument."""
        self.func = curry(self.func, arg)
        self.variables.pop(0)
        self.reqargs -= 1
        self.funcstr += ":("+self.e.prepare(arg, False, True)+")"

    def call(self, params):
        """Calls The Function."""
        params = varproc(params)
        if params is None:
            return strfunc(self.funcstr+":"+strlist(self.variables,":"), self.e, self.variables)
        elif len(params) < self.reqargs:
            out = self.copy()
            for arg in params:
                out.curry(arg)
            return out
        elif self.overflow and len(params) > len(self.variables):
            self.e.overflow = params[len(self.variables):]
            params = params[:len(self.variables)]
        return self.e.frompython(self.func(*params, **self.getextras()))

class unifunc(funcfloat):
    """Universalizes Function Calls."""
    def __init__(self, precall, e, funcstr=None):
        """Constructs The Universalizer."""
        self.e = e
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        self.store = []
        self.precall = precall

    def copy(self):
        """Copies The Universalizer Function."""
        return unifunc(self.precall, self.e, self.funcstr)

    def call(self, args):
        """Performs A Universalized Function Call."""
        args = varproc(args)
        if args is None:
            otherarg = self.e.unusedarg()
            return strfunc(self.funcstr+":"+otherarg, self.e, [otherarg])
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
    def __init__(self, func, e, funcstr=None, memoize=None, memo=None):
        """Initializes The Evaluator Function."""
        self.e = e
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.base_func = func

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if typestr(self.base_func) == "instancemethod":
            return ("find", self.funcstr)
        else:
            return ("makefunc", self.base_func, self.funcstr, self.memoize, getstates(self.memo))

    def copy(self):
        """Copies The Evaluator Function."""
        return makefunc(self.base_func, self.e, self.funcstr, self.memoize, self.memo)

    def call(variables):
        """Calls The Evaluator Function."""
        variables = varproc(variables)
        if variables is None:
            otherarg = self.e.unusedarg()
            return strfunc(self.funcstr+":"+otherarg, self.e, [otherarg])
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
        if x is None:
            return self.call([])
        else:
            items[self.variables[0]] = float(x)
            items[self.allargs] = matrix(1,1, x, fake=True)
            oldvars = self.e.setvars(items)
            try:
                out = self.e.calc(self.funcstr, " \\>")
            finally:
                self.e.setvars(oldvars)
            return out

    def call(self, variables):
        """Calls The Derivative Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif len(variables) == 0:
            return matrix(0)
        else:
            self.e.overflow = variables[1:]
            return self.func(float(variables[0]))

    def base_func(self, arg):
        """The Base Derivative Function."""
        return deriv(self.calc, arg, self.n, self.accuracy, self.scaledown)

class integbase(derivbase):
    """Holdes Methods Used In Integral Functions."""

    def call(self, variables):
        """Calls The Integral Function."""
        if variables is None:
            return self
        elif len(variables) < 2:
            return matrix(0)
        else:
            self.e.overflow = variables[2:]
            return self.func(float(variables[0]), float(variables[1]))

    def base_func(self, arg1, arg2):
        """The Base Integral Function."""
        return defint(self.calc, arg1, arg2, self.accuracy)

class derivfunc(derivbase, strfunc):
    """Implements A Derivative Function."""
    def __init__(self, funcstr, n, accuracy, scaledown, e, varname="x", personals=None, name=None, memoize=None, memo=None):
        """Creates The Derivative Function."""
        self.e = e
        if name:
            self.name = str(name)
        else:
            self.name = self.e.unusedarg()
        self.funcstr = str(funcstr)
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        self.variables = [str(varname)]
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        if personals is None:
            self.personals = {}
        else:
            self.personals = dict(personals)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("derivfunc", self.funcstr, self.n, self.accuracy, self.scaledown, self.varname, self.personals, self.name, self.memoize, getstates(self.memo))

    def copy(self):
        """Returns A Copy Of The Derivative Function."""
        return derivfunc(self.funcstr, self.n, self.accuracy, self.scaledown, self.e, self.variables[0], self.personals, self.name, self.memoize, self.memo)

class integfunc(integbase, strfunc):
    """Implements An Integral Function."""
    def __init__(self, funcstr, accuracy, e, varname="x", personals=None, name=None, memoize=None, memo=None):
        """Creates The Integral Function."""
        self.e = e
        if name:
            self.name = str(name)
        else:
            self.name = self.e.unusedarg()
        self.funcstr = str(funcstr)
        self.accuracy = float(accuracy)
        self.variables = [str(varname)]
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        if personals is None:
            self.personals = {}
        else:
            self.personals = dict(personals)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("integfunc", self.funcstr, self.accuracy, self.varname, self.personals, self.name, self.memoize, getstates(self.memo))

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfunc(self.funcstr, self.accuracy, self.e, self.variables[0], self.personals, self.name, self.memoize, self.memo)

class derivfuncfloat(derivbase, funcfloat):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown, e, funcstr=None, memoize=None, memo=None):
        """Creates The Derivative Function."""
        self.e = e
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.other_func = func

    def copy(self):
        """Returns A Copy Of The Derivative Float Function."""
        return integfunc(self.other_func, self.n, self.accuracy, self.scaledown, self.e, self.funcstr, self.memoize, self.memo)

    def calc(self, x=None):
        """Calculates The Derivative Function."""
        if x is None:
            return self.other_func.call([])
        else:
            return self.other_func.call([x])

class integfuncfloat(integbase, funcfloat):
    """Implements An Integral Function Of A Fake Function."""
    def __init__(self, func, accuracy, e, funcstr=None, memoize=None, memo=None):
        """Creates The Integral Float Function."""
        self.e = e
        self.accuracy = float(accuracy)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = self.e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.other_func = func

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfuncfloat(self.other_func, self.accuracy, self.e, self.funcstr, self.memoize, self.memo)

class classcalc(cotobject):
    """Implements An Evaluator Class."""
    evaltype = "class"
    notmatrix = True
    doset = False
    selfvar = "__self__"
    restricted = [selfvar]

    def __init__(self, e, variables=None, name=None):
        """Initializes The Class."""
        self.e = e
        self.variables = {
            self.selfvar : self
            }
        if variables is not None:
            self.add(variables, name=name)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("classcalc", getstates(self.getvars()))

    def copy(self):
        """Copies The Class."""
        return classcalc(self.e, getcopy(self.getvars()))

    def process(self, command, inglobal=False):
        """Processes A Command And Puts The Result In The Variables."""
        self.calc(command, inglobal, self.e.process)

    def begin(self, inglobal=False):
        """Enters The Class."""
        if inglobal:
            oldset = self.e.setvars(self.variables)
            oldclass = False
        else:
            oldclass, self.e.useclass = self.e.useclass, self.selfvar
            oldset, self.doset = self.doset, self.e.setvars(self.variables)
        return oldset, oldclass

    def end(self, params):
        """Exits The Class."""
        oldset, oldclass = params
        if oldclass is False:
            self.e.setvars(oldset)
            return True
        else:
            self.e.setvars(self.doset)
            self.doset = oldset
            self.e.useclass = oldclass
            return False

    def calc(self, command, inglobal=False, func=None):
        """Calculates A String In The Environment Of The Class."""
        if func is None:
            func = self.e.calc
        command = self.e.namefind(basicformat(command))
        params = self.begin(inglobal)
        try:
            out = func(command, " | class")
        finally:
            self.end(params)
        return out

    def __len__(self):
        """Finds The Number Of Variables."""
        return len(self.variables)

    def items(self):
        """Returns The Variables."""
        return self.variables.items()

    def getrepr(self, top=True, bottom=True, indebug=True, maxrecursion=5):
        """Finds A Representation."""
        out = "class \xab"
        if top:
            out += "\n"
        variables = self.getvars()
        for k,v in variables.items():
            out += " "+k+" "
            if istext(v):
                out += "= "+v
            else:
                out += ":= "
                if self is v:
                    out += self.selfvar
                elif maxrecursion <= 0 and isinstance(v, classcalc):
                    out += self.e.speedyprep(v, False, bottom, indebug, maxrecursion)
                else:
                    out += self.e.prepare(v, False, True, indebug, maxrecursion)
            if top:
                out += "\n"
            else:
                out += " ;;"
        if top:
            if not variables:
                out = out[:-1]
        elif variables:
            out = out[:-3]
        out += " \xbb"
        return out

    def store(self, key, value, bypass=False, name=None):
        """Stores An Item."""
        test = delspace(self.e.prepare(key, False, False))
        if test in self.restricted:
            raise ExecutionError("RedefinitionError", "The "+test+" variable cannot be redefined")
        elif not bypass and self.e.isreserved(test):
            raise ExecutionError("ClassError", "Could not store "+test+" in "+self.e.prepare(self, False, True, True))
        else:
            if name is not None and isinstance(value, funcfloat) and not isinstance(value, strfunc):
                value.funcstr = str(name)+"."+value.funcstr
            self.variables[test] = value
            if self.doset:
                self.doset[test] = haskey(self.e.variables, test)
                self.e.variables[test] = self.variables[test]

    def tryget(self, key):
        """Attempts To Get An Item."""
        if istext(key):
            test = key
        else:
            test = delspace(self.e.prepare(key, False, False))
        if not self.e.isreserved(test) and test in self.variables:
            return self.getitem(test)
        else:
            return None

    def getitem(self, test):
        """Retrieves An Item At The Base Level."""
        if istext(self.variables[test]):
            out = self.calc(self.variables[test])
            self.store(test, out)
        elif self.variables[test] is None:
            out = matrix(0)
        else:
            out = self.variables[test]
        return self.e.deprop(out)

    def retrieve(self, key):
        """Retrieves An Item."""
        test = self.tryget(key)
        if test is None:
            raise ExecutionError("ClassError", "Could not find "+key+" in "+self.e.prepare(self, False, True, True))
        else:
            return test

    def getmethod(self, key):
        """Retrieves A Method."""
        return self.retrieve(key)

    def call(self, variables):
        """Calculates An Item."""
        if variables is None:
            return self
        else:
            return self.init(varproc(variables))

    def domethod(self, item, args=[]):
        """Calls A Method Function."""
        if isfunc(item):
            if not islist(args) and args is not None:
                args = [args]
            if isinstance(item, strfunc):
                item.curryself(self)
                if item.overflow and args is not None and len(args) > len(item.variables):
                    args = args[:len(item.variables)-1] + [diagmatrixlist(args[len(item.variables)-1:])]
            return self.e.getcall(item)(args)
        else:
            return item

    def init(self, params):
        """Initializes The Instance."""
        if "__new__" in self.variables:
            item = self.calc("__new__")
            if isfunc(item):
                value = self.domethod(item, params)
            else:
                self.e.overflow = params
                value = item
        else:
            self.e.overflow = params
            value = self
        if isinstance(value, classcalc) and not isinstance(value, instancecalc):
            return value.toinstance()
        else:
            raise ExecutionError("ClassError", "Constructor returned non-class object "+self.e.prepare(value, False, True, True))

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
            self.add(other.getvars())
            return self
        else:
            raise ExecutionError("ClassError", "Could not extend class with "+repr(other))

    def add(self, other, bypass=True, name=None):
        """Adds Variables."""
        for k,v in other.items():
            self.store(k, v, bypass, name)

    def getvars(self):
        """Gets Original Variables."""
        out = self.variables.copy()
        for var in self.restricted:
            del out[var]
        return out

    def calcall(self):
        """Calculates All Strings."""
        for item in self.variables:
            self.getitem(item)

    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, classcalc):
            if self.variables[self.selfvar] is other.variables[self.selfvar]:
                return True
            else:
                self.calcall()
                other.calcall()
                return self.getvars() == other.getvars()
        else:
            return False

    def __cmp__(self, other):
        """Performs Comparison."""
        if isinstance(other, classcalc):
            self.calcall()
            other.calcall()
            return cmp(self.variables, other.variables)
        else:
            raise ExecutionError("TypeError", "Classes can only be compared with other classes")

    def __gt__(self, other):
        """Determines If Proper Subset."""
        if isinstance(other, classcalc):
            if len(self.variables) > len(other.variables):
                return self >= other
            else:
                return False
        else:
            raise ExecutionError("TypeError", "Classes can only be compared with other classes")

    def __ge__(self, other):
        """Determines If Subset."""
        if isinstance(other, classcalc):
            self.calcall()
            other.calcall()
            for item in other.variables:
                if not item in self.variables:
                    return False
            return True
        else:
            raise ExecutionError("TypeError", "Classes can only be compared with other classes")

    def __lt__(self, other):
        """Wraps Greater Than."""
        if isinstance(other, classcalc):
            return other > self
        else:
            raise ExecutionError("TypeError", "Classes can only be compared with other classes")

    def __le__(self, other):
        """Wraps Greater Than Or Equal."""
        if isinstance(other, classcalc):
            return other >= self
        else:
            raise ExecutionError("TypeError", "Classes can only be compared with other classes")

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

    def __contains__(self, item):
        """Determines Whether Another Class Is In This One."""
        if isinstance(item, classcalc):
            return self >= item
        else:
            return False

class namespace(classcalc):
    """A Class For Namespaces."""
    evaltype = "namespace"

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("namespace", getstates(self.getvars()))

    def copy(self):
        """Copies The Class."""
        return namespace(self.e, getcopy(self.getvars()))

    def getrepr(self, *args, **kwargs):
        """Wraps classcalc.getrepr."""
        return "namespace: "+classcalc.getrepr(self, *args, **kwargs)

    def call(self, variables):
        """Calls The Namespace."""
        if not variables:
            return self
        else:
            self.e.overflow = variables[1:]
            return self.calc(self.e.prepare(variables[0], True, False))

class instancecalc(numobject, classcalc):
    """An Evaluator Class Instance."""
    evaltype = "instance"
    parentvar = "__parent__"

    def __init__(self, e, variables=None, parent=None, name=None):
        """Creates An Instance Of An Evaluator Class."""
        self.e = e
        if parent is None:
            parent = classcalc(self.e)
            parent.variables = variables
            variables = None
        self.variables = {
            self.selfvar : self,
            self.parentvar : parent
            }
        if variables is not None:
            self.add(variables, name=name)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("instancecalc", getstates(self.getvars()), getstates(self.getparent().getvars()))

    def copy(self):
        """Copies The Instance."""
        return instancecalc(self.e, getcopy(self.getvars()), self.getparent())

    def getparent(self):
        """Reconstructs The Parent Class."""
        return self.variables[self.parentvar]

    def toclass(self):
        """Converts To A Normal Class."""
        out = classcalc(self.e, self.getvars())
        return out

    def isfrom(self, parent):
        """Determines Whether The Instance Is From The Parent."""
        if isinstance(parent, classcalc):
            return self.getparent() == parent
        else:
            return False

    def tryget(self, key):
        """Attempts To Get An Item."""
        if istext(key):
            test = key
        else:
            test = delspace(self.e.prepare(key, False, False))
        if not self.e.isreserved(test) and test in self.variables:
            return self.getitem(test)
        elif "__get__" in self.variables:
            return self.domethod(self.getitem("__get__"), rawstrcalc(test, self.e))
        else:
            return self.getparent().tryget(test)

    def getitem(self, test):
        """Retrieves An Item At The Base Level."""
        if istext(self.variables[test]):
            out = self.calc(self.variables[test])
            self.store(test, out)
        elif self.variables[test] is None:
            out = matrix(0)
        else:
            if isinstance(self.variables[test], strfunc):
                self.variables[test].curryself(self)
            out = self.variables[test]
        return self.e.deprop(out)

    def store(self, key, value, bypass=False, name=None):
        """Stores An Item."""
        test = delspace(self.e.prepare(key, False, False))
        value = getcopy(value)
        if test in self.restricted:
            raise ExecutionError("RedefinitionError", "The "+test+" variable cannot be redefined.")
        elif not bypass and self.e.isreserved(test):
            raise ExecutionError("ClassError", "Could not store "+test+" in "+self.e.prepare(self, False, True, True))
        else:
            if isinstance(value, strfunc):
                value.curryself(self)
            elif name is not None and isinstance(value, funcfloat):
                value.funcstr = str(name)+"."+value.funcstr
            self.variables[test] = value
            if self.doset:
                self.doset[test] = haskey(self.e.variables, test)
                self.e.variables[test] = self.variables[test]

    def isprop(self):
        """Determines Whether The Class Is A Property."""
        return bool(self.tryget("__value__"))

    def isfunc(self):
        """Determines Whether The Class Is A Function."""
        return bool(self.tryget("__call__"))

    def call(self, variables):
        """Calls The Function."""
        if variables is None:
            func = self.tryget("__value__")
            if func is None:
                return self
            else:
                self.e.setreturned()
                return self.domethod(func)
        else:
            func = self.tryget("__call__")
            if func is None:
                raise ExecutionError("ClassError", "The class being called has no __call__ method")
            else:
                return self.domethod(func, varproc(variables))

    def ismatrix(self):
        """Determines Whether The Class Can Be A Matrix."""
        return bool(self.tryget("__cont__"))

    def tomatrix(self):
        """Converts To Matrix."""
        func = self.tryget("__cont__")
        if func is None:
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
        raise ExecutionError("TypeError", "Insufficient methods defined for addition")

    def __isub__(self, other):
        """Performs Subtraction."""
        check_sub = self.tryget("__sub__")
        if check_sub:
            return self.domethod(check_sub, other)
        check_add = self.tryget("__add__")
        if check_add:
            return self.domethod(check_add, -other)
        raise ExecutionError("TypeError", "Insufficient methods defined for subtraction")

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
        raise ExecutionError("TypeError", "Insufficient methods defined for multiplication")

    def __idiv__(self, other):
        """Performs Division."""
        check_div = self.tryget("__div__")
        if check_div:
            return self.domethod(check_div, other)
        check_mul = self.tryget("__mul__")
        if check_mul:
            return self.domethod(check_mul, 1.0/other)
        check_fdiv = self.tryget("__fdiv__")
        if check_fdiv:
            check_mod = self.tryget("__mod__")
            if check_mod:
                return self.domethod(check_fdiv, other)+self.domethod(check_mod, other)/other
        other = 1.0/other
        if other == int(other):
            try:
                for x in xrange(0, int(other)):
                    self += self
            except ExecutionError:
                pass
            else:
                return self
        raise ExecutionError("TypeError", "Insufficient methods defined for division")

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        check_rdiv = self.tryget("__rdiv__")
        if check_rdiv:
            return self.domethod(check_rdiv, other)
        check_pow = self.tryget("__pow__")
        if check_pow:
            return other*self.domethod(check_pow, -1.0)
        raise ExecutionError("TypeError", "Insufficient methods defined for division")

    def __ifloordiv__(self, other):
        """Performs Floor Division."""
        check_fdiv = self.tryget("__fdiv__")
        if check_fdiv:
            return self.domethod(check_fdiv, other)
        else:
            try:
                self /= other
                out = int(self)
            except ExecutionError:
                raise ExecutionError("TypeError", "Insufficient methods defined for floor division")
            else:
                return out

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
                raise ExecutionError("TypeError", "Insufficient methods defined for modulus")
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
            else:
                return self
        raise ExecutionError("TypeError", "Insufficient methods defined for exponentiation")

    def __rfloordiv__(self, other):
        """Performs Reverse Floor Division."""
        check_rfdiv = self.tryget("__rfdiv__")
        if check_rfdiv:
            return self.domethod(check_rfdiv, other)
        else:
            return int(other / self)

    def __rmod__(self, other):
        """Performs Reverse Modulo."""
        check_rmod = self.tryget("__rmod__")
        if check_rmod:
            return self.domethod(check_rmod, other)
        raise ExecutionError("TypeError", "Insufficient methods defined for reverse modulus")

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        check_rpow = self.tryget("__rpow__")
        if check_rpow:
            return self.domethod(check_rpow, other)
        raise ExecutionError("TypeError", "Insufficient methods defined for reverse exponentiation")

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        check_rmul = self.tryget("__rmul__")
        if check_rmul:
            return self.domethod(check_rmul, other)
        else:
            return self*other

    def __radd__(self, other):
        """Performs Reverse Addition."""
        check_radd = self.tryget("__radd__")
        if check_radd:
            return self.domethod(check_radd, other)
        else:
            return self+other

    def __rsub__(self, other):
        """Performs Reverse Subtraction."""
        check_rsub = self.tryget("__rsub__")
        if check_rsub:
            return self.domethod(check_rsub, other)
        else:
            return other + -self

    def getfloat(self):
        """Retrieves A Float."""
        return float(getnum(self.tonum()))

    def __int__(self):
        """Retrieves An Integer."""
        return getint(self.tonum())

    def tonum(self):
        """Converts To Float."""
        check_num = self.tryget("__num__")
        if check_num:
            return self.domethod(check_num)
        raise ExecutionError("TypeError", "Insufficient methods defined for conversion to number")

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
        else:
            check_eq = self.tryget("__eq__")
            if check_eq:
                return self.domethod(check_eq, other)
            check_ne = self.tryget("__ne__")
            if check_ne:
                return not self.domethod(check_ne, other)
            check_cmp = self.tryget("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
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
        else:
            check_ne = self.tryget("__ne__")
            if check_ne:
                return self.domethod(check_ne, other)
            check_eq = self.tryget("__eq__")
            if check_eq:
                return not self.domethod(check_eq, other)
            check_cmp = self.tryget("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
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
        if not hasnum(other):
            return False
        else:
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
            raise ExecutionError("TypeError", "Insufficient methods defined for greater than")

    def __lt__(self, other):
        """Performs Less Than."""
        if not hasnum(other):
            return False
        else:
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
            raise ExecutionError("TypeError", "Insufficient methods defined for less than")

    def __ge__(self, other):
        """Performs Greater Than Or Equal."""
        if not hasnum(other):
            return False
        else:
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
            raise ExecutionError("TypeError", "Insufficient methods defined for greater than or equal")

    def __le__(self, other):
        """Performs Less Than Or Equal."""
        if not hasnum(other):
            return False
        else:
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
            raise ExecutionError("TypeError", "Insufficient methods defined for less than or equal")

    def __str__(self):
        """Retrieves A String."""
        check_str = self.tryget("__str__")
        if check_str:
            return self.e.prepare(self.domethod(check_str), True, False)
        else:
            return self.getrepr(True)

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
        if out is None:
            raise ExecutionError("ClassError", "Insufficient methods defined for len")
        else:
            return getint(out)

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
        if out is None:
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

    def op_repeat(self, other):
        """Performs **."""
        item = self.tryget("__rep__")
        if item:
            return self.domethod(item, other)
        else:
            return NotImplemented

    def rop_repeat(self, other):
        """Performs Reverse **."""
        item = self.tryget("__rrep__")
        if item:
            return self.domethod(item, other)
        else:
            return NotImplemented

    def op_join(self, params):
        """Performs ++."""
        item = self.tryget("__join__")
        if item:
            return self.domethod(item, params)
        else:
            return NotImplemented

    def rop_join(self, params):
        """Performs Reverse ++."""
        item = self.tryget("__rjoin__")
        if item:
            return self.domethod(item, params)
        else:
            return NotImplemented

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if maxrecursion <= 0:
            return self.speedyprep(self, False, bottom, indebug, maxrecursion)
        elif not indebug and not bottom:
            return str(self)
        else:
            check_repr = self.tryget("__repr__")
            if check_repr:
                return self.e.prepare(self.domethod(check_repr), top, False, indebug, maxrecursion)
            else:
                return classcalc.getrepr(self, top, bottom, indebug, maxrecursion)+" ( )"

    def include(self):
        """Returns A Class For Inclusion."""
        item = self.tryget("__include__")
        if item:
            return self.domethod(item)
        else:
            raise ExecutionError("TypeError", "Insufficient methods defined for include")

class atom(evalobject):
    """Implements Atoms."""
    evaltype = "atom"

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("atom", )

    def copy(self):
        """Makes Another Atom."""
        return atom()

    def calc(self):
        """Converts To Nothing."""
        return matrix(0)

    def __eq__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __ne__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __gt__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __lt__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __ge__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __le__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __iadd__(self, other):
        """Always Returns self."""
        return self

    def __radd__(self, other):
        """Always Returns self."""
        return self

    def __isub__(self, other):
        """Always Returns self."""
        return self

    def __rsub__(self, other):
        """Always Returns self."""
        return self

    def __imul__(self, other):
        """Always Returns self."""
        return self

    def __rmul__(self, other):
        """Always Returns self."""
        return self

    def __idiv__(self, other):
        """Always Returns self."""
        return self

    def __rdiv__(self, other):
        """Always Returns self."""
        return self

    def __ipow__(self, other):
        """Always Returns self."""
        return self

    def __rpow__(self, other):
        """Always Returns self."""
        return self

    def __imod__(self, other):
        """Always Returns self."""
        return self

    def __rmod__(self, other):
        """Always Returns self."""
        return self

    def __str__(self):
        """Gets A Representation."""
        return "_"

class rollfunc(strfunc):
    """Implements A Random Number Generator Object."""
    memoize = False
    variables = ["__times__"]

    def __init__(self, stop, e, key=None, name=None, counter=None):
        """Creates The Random Number Generator."""
        self.e = e
        self.gen = random(key)
        if counter is not None:
            self.gen.counter = int(counter)
        self.stop = getnum(stop)
        self.funcstr = str(self.stop)
        if name:
            self.name = str(name)
        else:
            self.name = self.e.unusedarg()

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("rollfunc", self.stop, self.gen.key, self.name, self.gen.counter)

    def copy(self):
        """Copies The Random Number Generator."""
        return rollfunc(self.stop, self.e, self.gen.key, self.name, self.gen.counter)

    def calc(self, m=1.0):
        """Generates A Random Number."""
        self.e.setreturned()
        stop = self.stop*m
        if stop > 1 and stop == int(stop):
            return 1+self.gen.chooseint(int(stop))
        else:
            return self.gen.choosefloat(float(stop))

    def call(self, variables):
        """Generates Random Numbers."""
        variables = varproc(variables)
        if variables is None:
            out = self
        elif len(variables) == 0 or (len(variables) == 1 and isnull(variables[0])):
            out = self.call([1.0])
        elif len(variables) > 1:
            out = self.call([diagmatrixlist(variables)])
        elif ismatrix(variables[0]):
            out = variables[0].code(lambda x: self.call([x]))
        else:
            stop = getnum(variables[0])
            out = 0.0
            for x in xrange(0, int(stop)):
                out += self.calc()
            if stop > int(stop):
                out += self.calc(stop-int(stop))
        return out

    def __eq__(self, other):
        """Performs Equals."""
        if isinstance(other, rollfunc):
            return self.stop == other.stop and self.name == other.name and self.gen.key == other.gen.key and self.gen.counter == other.gen.counter
        else:
            return False

class pair(cotobject):
    """A Key-Value Pair."""
    evaltype = "pair"
    notmatrix = True

    def __init__(self, e, key, value):
        """Creates The Key-Value Pair."""
        self.e = e
        self.k = key
        self.v = value

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("pair", itemstate(self.k), itemstate(self.v))

    def copy(self):
        """Copies The Key-Value Pair."""
        return pair(self.e, getcopy(self.k), getcopy(self.v))

    def call(self, variables):
        """Retrieves A Value."""
        self.e.overflow = variables[1:]
        if not variables:
            return self
        elif self.k == variables[0]:
            return self.v
        else:
            raise ExecutionError("KeyError", "Could not find key "+self.e.prepare(variables[0])+" in "+self.e.prepare(self))

    def items(self):
        """Gets A List Containing The Key And The Value."""
        return [self.k, self.v]

    def remove(self, item):
        """Removes An Item."""
        raise TypeError("Pairs don't support subtraction")

    def __iadd__(self, item):
        """Extends With An Item."""
        if isinstance(item, dictionary):
            out = item.copy()
            out.store(self.k, self.v)
            return out
        elif isinstance(item, pair):
            out = {
                self.k : self.v,
                item.k : item.v
                }
            return dictionary(self.e, out)
        else:
            raise TypeError("Pairs only support addition by other pairs")

    def __imul__(self, item):
        """Extends With An Item."""
        self += item
        return self

    def __eq__(self, other):
        """Performs Equality."""
        if isinstance(other, pair) and not isinstance(other, dictionary):
            return self.k == other.k and self.v == other.v
        else:
            return False

class dictionary(pair):
    """A Key-Value Dictionary."""
    evaltype = "dictionary"

    def __init__(self, e, items=None):
        """Creates The Dictionary."""
        self.e = e
        if items is None:
            self.a = {}
        else:
            self.a = items.copy()

    def copy(self):
        """Copies The Dictionary."""
        return dictionary(self.e, self.a)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("dictionary", getstates(self.a))

    def store(self, key, value):
        """Stores An Item."""
        self.a[key] = value

    def items(self):
        """Gets Items."""
        return self.a.items()

    def call(self, variables):
        """Retrieves A Value."""
        self.e.overflow = variables[1:]
        if not variables:
            return self
        elif variables[0] in self.a:
            return self.a[variables[0]]
        else:
            raise ExecutionError("KeyError", "Could not find key "+self.e.prepare(variables[0])+" in "+self.e.prepare(self))

    def remove(self, arg):
        """Removes An Item."""
        if arg in self.a:
            del self.a[arg]

    def __iadd__(self, other):
        """Wraps extend."""
        self.update(other)
        return self

    def update(self, item):
        """Extends The Dictionary."""
        if isinstance(item, dictionary):
            self.a.update(item.a)
        elif isinstance(item, pair):
            self.store(item.k, item.v)
        else:
            raise TypeError("Dictionaries only support addition with pairs and other dictionaries")

    def __eq__(self, other):
        """Performs Equality."""
        if isinstance(other, dictionary):
            return self.a == other.a
        else:
            return False

    def __len__(self):
        """Finds A Length."""
        return len(self.a)

    def __contains__(self, other):
        """Performs in."""
        return other in self.a

    def tomatrix(self):
        """Converts To A Matrix."""
        items = self.a.items()
        out = matrix(len(items), 2)
        for x in xrange(0, len(items)):
            out.store(x, 0, items[x][0])
            out.store(x, 1, items[x][1])
        return out

    def __delitem__(self, key):
        """Deletes An Item."""
        del self.a[key]

    def __cmp__(self, other):
        """Performs Comparison."""
        if isinstance(other, dictionary):
            return cmp(self.a, other.a)
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    def __gt__(self, other):
        """Determines If Proper Subset."""
        if isinstance(other, dictionary):
            if len(self.a) > len(other.a):
                return self >= other
            else:
                return False
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    def __ge__(self, other):
        """Determines If Subset."""
        if isinstance(other, dictionary):
            for item in other.a:
                if not item in self.a:
                    return False
            return True
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    def __lt__(self, other):
        """Wraps Greater Than."""
        if isinstance(other, dictionary):
            return other > self
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    def __le__(self, other):
        """Wraps Greater Than Or Equal."""
        if isinstance(other, dictionary):
            return other >= self
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")


class bracket(object):
    """A To-Be-Calculated Row."""
    def __init__(self, e, items):
        """Constructs The Row."""
        self.e = e
        self.items = items

    def calc(self):
        """Calculates The Row."""
        out = []
        for item in self.items:
            item = basicformat(item)
            if item:
                out.append(self.e.calc(item))
        return rowmatrixlist(out)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("bracket", self.items)

class brace(bracket):
    """A To-Be-Calculated Dictionary."""

    def calc(self):
        """Calculates The Dictionary."""
        out = {}
        for item in self.items:
            item = basicformat(item)
            if item:
                value = self.e.calc(item)
                if isinstance(value, dictionary):
                    out.update(value.a)
                elif isinstance(value, pair):
                    out[value.k] = value.v
                else:
                    raise ValueError("Dictionary got non-pair item "+self.e.prepare(value, False, True, True))
        return dictionary(self.e, out)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("brace", self.items)

class evalwrap(evalobject):
    """A Wrapper For Converting An Arbitrary Python Object Into A Rabbit Object."""
    def __init__(self, inputobj):
        """Constructs The Wrapper."""
        self.obj = inputobj

# Need to be directly implemented:
##    getstate
##    copy
##    check
##    getcall
##    call
##    isfunc
##    ismatrix
##    tomatrix
##    notmatrix
##    isprop
##    getrepr
##    op_repeat
##    rop_repeat
##    itemcall
##    getmethod
##    evaltype
##    __hash__
##    __lt__
##    __gt__
##    __le__
##    __ge__
##    __eq__
##    __ne__
##    __cmp__
##    __nonzero__
##    __len__
##    __add__
##    __iadd__
##    __radd__
##    __sub__
##    __isub__
##    __rsub__
##    __mul__
##    __imul__
##    __rmul__
##    __floordiv__
##    __ifloordiv__
##    __rfloordiv__
##    __mod__
##    __imod__
##    __rmod__
##    __pow__
##    __ipow__
##    __rpow__
##    __lshift__
##    __ilshift__
##    __rlshift__
##    __rshift__
##    __irshift__
##    __rrshift__
##    __and__
##    __iand__
##    __rand__
##    __or__
##    __ior__
##    __ror__
##    __xor__
##    __ixor__
##    __rxor__
##    __neg__
##    __pos__
##    __abs__
##    __invert__
##    __complex__
##    __int__
##    __long__
##    __float__
##    __oct__
##    __hex__
##    __index__

# Need to be indirectly implemented:
##    __getitem__
##    __setitem__
##    __delitem__
##    __getattr__
##    __setattr__
##    __delattr__
##    __get__
##    __set__
##    __delete__
##    __metaclass__
##    __instancecheck__
##    __subclasscheck__
##    __iter__
##    __contains__
##    __enter__
##    __exit__
