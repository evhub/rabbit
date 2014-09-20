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
            raise ExecutionError("ArgumentError", "Not enough arguments supplied to collapse "+e.prepare(item, False, True, True))
        else:
            return item.calc()
    elif isinstance(item, codestr):
        return item.calc()
    else:
        return item

def hasitemcall(inputobject):
    """Determines Whether An Object Is Item-Callable."""
    return hasattr(inputobject, "itemcall") and inputobject.itemcall is not None and (not hasattr(inputobject, "hasitemcall") or inputobject.hasitemcall())

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

    @rabbit
    def calc(self):
        """Calculates The Negative Object."""
        return -self.n

    @rabbit
    def __iadd__(self, other):
        """Does The Curried Subtraction."""
        return other - self.n

class funcfloat(numobject):
    """Allows The Creation Of A Float Function."""
    allownone = False
    evaltype = "function"
    overflow = False
    memoize = True
    allargs = "__"
    reqargs = -1

    def __init__(self, func, name=None, reqargs=None, memoize=None, memo=None, funcstr=None, curried=None):
        """Constructs The Float Function."""
        if name:
            self.name = str(name)
        else:
            self.name = e.unusedarg()
        if funcstr is None:
            self.funcstr = self.name
        else:
            self.funcstr = str(funcstr)
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.base_func = func
        if reqargs is not None:
            self.reqargs = reqargs
        if curried is None:
            self.curried = []
        else:
            self.curried = curried

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("find", self.funcstr)

    def copy(self):
        """Returns A Copy Of The Float Function."""
        return funcfloat(self.base_func, self.name, self.reqargs, self.memoize, self.memo, self.funcstr, self.curried[:])

    @rabbit
    def __hash__(self):
        """Returns A Hash."""
        return hash(self.funcstr)

    @rabbit
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
            returned = e.returned
            e.setreturned(False)
            try:
                out = self.base_func(*args, **kwargs)
            except:
                raise
            else:
                if not returned and not e.returned:
                    if arghash is None:
                        arghash = (self.keyhash(args), self.keyhash(kwargs))
                    self.memo[arghash] = out
            finally:
                e.returned = e.returned or returned
        else:
            out = self.base_func(*args, **kwargs)
        if out is not None:
            return out
        elif self.allownone:
            return matrix(0)
        else:
            raise SyntaxError("Functions should never return Python None")

    @rabbit
    def calc(self, variables=None):
        """Calculates The Float Function."""
        if variables is None:
            variables = []
        return self.func(self.curried+variables)

    def call(self, variables):
        """Calls The Float Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif not variables and self.reqargs > 0:
            raise ExecutionError("ArgumentError", "No arguments were passed to a function that requires arguments")
        elif len(variables) < self.reqargs:
            out = getcopy(self)
            for arg in variables:
                out.curry(arg)
            return out
        else:
            return self.calc(variables)

    def curry(self, arg):
        """Curries An Argument."""
        self.curried.append(arg)
        self.reqargs -= 1
        self.funcstr += ":("+e.prepare(arg, False, True)+")"

    @rabbit
    def __str__(self):
        """Retrieves The Function String."""
        return self.funcstr

    def __iadd__(self, other):
        """Performs Addition."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+"("+self.allargs+"))+"+e.wrap(other), [self.allargs], {self.name:self})

    def __idiv__(self, other):
        """Performs Division."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+"("+self.allargs+"))/"+e.wrap(other), [self.allargs], {self.name:self})

    def __imul__(self, other):
        """Performs Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+"("+self.allargs+"))*"+e.wrap(other), [self.allargs], {self.name:self})

    def __ipow__(self, other):
        """Performs Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+"("+self.allargs+"))^"+e.wrap(other), [self.allargs], {self.name:self})

    @rabbit
    def __radd__(self, other):
        """Performs Reverse Addition."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"+("+self.name+"("+self.allargs+"))", [self.allargs], {self.name:self})

    @rabbit
    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"^("+self.name+"("+self.allargs+"))", [self.allargs], {self.name:self})

    @rabbit
    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"/("+self.name+"("+self.allargs+"))", [self.allargs], {self.name:self})

    @rabbit
    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"*("+self.name+"("+self.allargs+"))", [self.allargs], {self.name:self})

    @rabbit
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, funcfloat) and not isinstance(other, strfunc):
            return self.base_func == other.base_func and self.reqargs == other.reqargs
        else:
            return False

class strfunc(funcfloat):
    """Allows A String Function To Be Callable."""
    funcvar = "__func__"
    snapshotvar = "__closure__"
    personalsvar = "__class__"
    method = None

    def __init__(self, funcstr, variables=None, personals=None, name=None, overflow=None, allargs=None, reqargs=None, memoize=None, memo=None, method=None, lexical=True):
        """Creates A Callable String Function."""
        self.funcstr = e.namefind(str(funcstr))
        if name:
            self.name = str(name)
        else:
            self.name = e.unusedarg()
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
        if reqargs is None:
            self.reqargs = len(self.variables)
        else:
            self.reqargs = reqargs
        if method is not None:
            self.method = method
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        if isinstance(personals, classcalc):
            self.personals = personals
        else:
            if personals is None:
                childvars = {}
            else:
                childvars = personals.copy()
            if not lexical:
                parentvars = {}
            else:
                parentvars = e.variables.copy()
            self.personals = instancecalc(childvars, namespace(parentvars, selfvar=self.personalsvar), top=False, selfvar=self.personalsvar, parentvar=self.snapshotvar)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if self.method:
            memo = None
        else:
            memo = getstates(self.memo)
        return ("strfunc", self.funcstr, self.variables, getstates(self.getpers()), self.name, self.overflow, self.allargs, self.reqargs, self.memoize, memo, self.method)

    def copy(self):
        """Copies The String Function."""
        return strfunc(self.funcstr, self.variables[:], getcopy(self.personals), self.name, self.overflow, self.allargs, self.reqargs, self.memoize, self.memo, self.method, False)

    def calc(self, personals=None):
        """Calculates The String."""
        if personals is None:
            personals = self.getpers()
        return self.func(personals)

    def base_func(self, personals):
        """Allows For Tail Recursion."""
        variables = self.personals.getparent().getvars()
        if self.method:
            variables[self.method] = self.personals.variables[self.method]
        variables.update(personals)
        funcstr = self.funcstr
        out = None
        while out is None:
            if e.tailing and e.all_clean:
                newvars = e.variables.copy()
                newvars.update(variables)
                raise TailRecursion(funcstr, newvars)
            else:
                cleaned = e.clean_begin(True, True)
                tailing, e.tailing = e.tailing, True
                oldvars = e.setvars(variables)
                try:
                    out = e.calc(funcstr, " \\>")
                except TailRecursion as params:
                    if not e.returned and funcstr == params.funcstr and variables == params.variables:
                        raise ExecutionError("LoopError", "Illegal infinite recursive loop in "+funcstr)
                    else:
                        funcstr = params.funcstr
                        variables = params.variables
                finally:
                    e.tailing = tailing
                    e.clean_end(cleaned)
                    e.setvars(oldvars)
        return out

    def call(self, variables):
        """Calls The String Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif not variables and self.reqargs > 0:
            raise ExecutionError("ArgumentError", "No arguments were passed to a function that requires arguments")
        elif len(variables) < self.reqargs:
            out = getcopy(self)
            for arg in variables:
                out.curry(arg)
            return out
        else:
            allvars = diagmatrixlist(variables)
            if self.overflow:
                items, e.overflow = useparams(variables, self.variables, matrix(0))
            else:
                items, _ = useparams(variables, self.variables, matrix(0))
            items[self.allargs] = allvars
            personals = self.getpers()
            for k in personals:
                if (not k in items) or isnull(items[k]):
                    items[k] = personals[k]
            out = self.calc(items)
            return out

    def curry(self, arg):
        """Curries An Argument."""
        self.personals.store(self.variables.pop(0), arg)
        self.reqargs -= 1

    def __iadd__(self, other):
        """Performs Addition."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")+"+e.wrap(other), self.variables, {self.name:self})

    def __idiv__(self, other):
        """Performs Division."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")/"+e.wrap(other), self.variables, {self.name:self})

    def __imul__(self, other):
        """Performs Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")*"+e.wrap(other), self.variables, {self.name:self})

    def __ipow__(self, other):
        """Performs Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc("("+self.name+":"+strlist(self.variables,":")+")^"+e.wrap(other), self.variables, {self.name:self})

    def __radd__(self, other):
        """Performs Reverse Addition."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"+("+self.name+":"+strlist(self.variables,":")+")", self.variables, {self.name:self})

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"^("+self.name+":"+strlist(self.variables,":")+")", self.variables, {self.name:self})

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"/("+self.name+":"+strlist(self.variables,":")+")", self.variables, {self.name:self})

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        if isnull(other):
            return self
        else:
            return strfunc(e.wrap(other)+"*("+self.name+":"+strlist(self.variables,":")+")", self.variables, {self.name:self})

    def find(self):
        """Simplifies The Function String."""
        self.funcstr = e.find(self.funcstr, False)

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

    def didsnapshot(self):
        """Determines Whether A Snapshot Was Taken."""
        return bool(len(self.personals.getparent()))

    def getpers(self):
        """Returns The Modified Personals Dictionary."""
        out = self.personals.getvars()
        del out[self.snapshotvar]
        if self.method and self.method in out:
            del out[self.method]
        return out

    def getmethod(self, key):
        """Retrieves A Personal."""
        return self.personals.getmethod(key)

    def curryself(self, other):
        """Curries Self Into The Function."""
        if self.personalsvar != other.selfvar:
            self.method = self.method or other.selfvar
            if self.method in self.personals.variables:
                self.personals.store(self.method, other)
            elif len(self.variables) > 0:
                self.personals.store(self.method, other)
                self.curry(self.method)
            else:
                raise ExecutionError("ClassError", "Methods must have self as their first argument")

    def __eq__(self, other, personals=None):
        """Performs ==."""
        if isinstance(other, strfunc):
            if personals is None:
                personals = self.getpers()
            return (self.funcstr == other.funcstr and
                    self.overflow == other.overflow and
                    self.reqargs == other.reqargs and
                    self.allargs == other.allargs and
                    self.method == other.method and
                    self.variables == other.variables and
                    personals == other.getpers())
        else:
            return False

    def merge(self, test):
        """Merges With test."""
        self.name = self.name or test.name
        self.funcstr = test.funcstr
        self.overflow = self.overflow and test.overflow
        self.reqargs += test.reqargs
        for x in test.variables:
            if not x in self.variables:
                self.variables.append(x)
            else:
                self.reqargs -= 1
        self.personals.merge(test.personals)
        if strfunc.allargs == self.allargs:
            self.allargs = test.allargs
        self.memoize = self.memoize and test.memoize
        self.memo.update(test.memo)
        self.method = self.method or test.method

class strfloat(strfunc):
    """Allows A String To Be Treated Like A Float."""
    def __init__(self, *args, **kwargs):
        """Initializes The String Float."""
        strfunc.__init__(self, *args, **kwargs)
        test = e.find(self.funcstr, True)
        if isinstance(test, strfunc):
            self.merge(test)

class strcalc(numobject):
    """Allows Strings Inside Evaluation."""
    evaltype = "str"
    notmatrix = True
    check = 2

    def __init__(self, calcstr):
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
        return rawstrcalc(self.calcstr)

    def getfloat(self):
        """Attempts To Get A Float."""
        return float(self.calcstr)

    def __int__(self):
        """Attempts To Get An Integer."""
        return int(self.calcstr)

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
            self.calcstr += e.prepare(other, True, False)
        return self

    def __radd__(self, other):
        """Performs Reverse Addition."""
        if not isnull(other):
            self.calcstr = e.prepare(other, True, False)+self.calcstr
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
        return e.prepare(other, True, False) in self.calcstr

    def __isub__(self, other):
        """Performs Subtraction."""
        self.calcstr.replace(e.prepare(other, True, False), "")

    def tomatrix(self):
        """Returns A Matrix Of The Characters."""
        out = []
        for x in self.calcstr:
            out.append(rawstrcalc(x))
        return diagmatrixlist(out)

    def itemcall(self, params):
        """Performs A Colon Splice."""
        item = self.calcstr
        if len(params) == 0:
            value = rawstrcalc(item[-1])
        elif len(params) == 1:
            value = rawstrcalc(item[int(params[0])])
        else:
            value = rawstrcalc(item[int(params[0]):int(params[1])])
            e.overflow = params[2:]
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

    def getmethod(self, key):
        """Gets A Method."""
        if hasattr(self.calcstr, key):
            return evalwrap(getattr(self.calcstr, key), repr(self)+"."+key, True)
        else:
            return None

class rawstrcalc(strcalc):
    """A Raw Evaluator String."""
    def __init__(self, calcstr):
        """Initializes A Raw Evaluator String."""
        self.calcstr = str(calcstr)

class codestr(rawstrcalc):
    """A Code Evaluator String."""
    itemcall = None
    evaltype = "code"
    check = 1

    def __init__(self, calcstr):
        """Initializes A Code Evaluator String."""
        self.calcstr = basicformat(calcstr)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("codestr", self.calcstr)

    def copy(self):
        """Returns A Copy Of The Code String."""
        return codestr(self.calcstr)

    def calc(self):
        """Calculates The Code String."""
        return e.calc(self.calcstr, " ::>")

    def call(self, variables):
        """Calls The Code String."""
        if variables is None:
            return self
        else:
            e.overflow = variables
            return self.calc()

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if bottom:
            return "\xab "+str(self)+" \xbb"
        else:
            return str(self)

class usefunc(funcfloat):
    """Allows A Function To Be Used As A Variable."""
    allownone = True

    def __init__(self, func, funcstr=None, variables=None, extras=None, overflow=True, reqargs=None, evalinclude=False, memoize=None, memo=None, curried=None):
        """Creates A Callable Function."""
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = e.unusedarg()
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
        if curried is None:
            self.curried = []
        else:
            self.curried = curried
        self.evalinclude = evalinclude

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if ismethod(self.base_func):
            return ("find", self.funcstr)
        else:
            return ("usefunc", self.base_func, self.funcstr, self.variables, self.extras, self.overflow, self.reqargs, self.evalinclude, self.memoize, getstates(self.memo), liststate(self.curried))

    def copy(self):
        """Copies The Function."""
        return usefunc(self.base_func, self.funcstr, self.variables[:], self.extras, self.overflow, self.reqargs, self.evalinclude, self.memoize, self.memo, self.curried[:])

    def getextras(self):
        """Retrieves Extras."""
        out = self.extras.copy()
        if self.evalinclude:
            out[self.evalinclude] = e
        return out

    def curry(self, arg):
        """Curries An Argument."""
        self.curried.append(arg)
        self.variables.pop(0)
        self.reqargs -= 1
        self.funcstr += ":("+e.prepare(arg, False, True)+")"

    def call(self, params):
        """Calls The Function."""
        params = varproc(params)
        if params is None:
            return strfunc(self.funcstr+":"+strlist(self.variables,":"), self.variables)
        elif not params and self.reqargs > 0:
            raise ExecutionError("ArgumentError", "No arguments were passed to a function that requires arguments")
        elif len(params) < self.reqargs:
            out = getcopy(self)
            for arg in params:
                out.curry(arg)
            return out
        elif self.overflow and len(params) > len(self.variables):
            e.overflow = params[len(self.variables):]
            params = params[:len(self.variables)]
        return e.frompython(self.calc(params))

    def calc(self, params):
        """Calcs The Function."""
        if params is None:
            params = []
        return self.func(*(self.curried+params), **self.getextras())

class unifunc(funcfloat):
    """Universalizes Function Calls."""
    def __init__(self, precall, funcstr=None):
        """Constructs The Universalizer."""
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = e.unusedarg()
        self.store = []
        self.precall = precall

    def copy(self):
        """Copies The Universalizer Function."""
        return unifunc(self.precall, self.funcstr)

    def call(self, args):
        """Performs A Universalized Function Call."""
        args = varproc(args)
        if args is None:
            otherarg = e.unusedarg()
            return strfunc(self.funcstr+":"+otherarg, [otherarg])
        elif islist(args):
            x = args[0]
            if len(args) > 1:
                e.overflow = []
                for x in xrange(1, len(args)):
                    e.overflow.append(args[x])
        x = getint(x)
        try:
            self.store[x]
        except IndexError:
            while len(self.store) <= x:
                self.store.append(self.precall())
        return self.store[x]

class derivbase(object):
    """Holds Methods Used In Derivative Functions."""

    @rabbit
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        items = dict(self.personals)
        if x is None:
            return self.call([])
        else:
            items[self.variables[0]] = float(x)
            items[self.allargs] = matrix(1,1, x, fake=True)
            oldvars = e.setvars(items)
            try:
                out = e.calc(self.funcstr, " \\>")
            finally:
                e.setvars(oldvars)
            return out

    def call(self, variables):
        """Calls The Derivative Function."""
        variables = varproc(variables)
        if variables is None:
            return self
        elif not variables:
            raise ExecutionError("ArgumentError", "No arguments were passed to a function that requires arguments")
        else:
            e.overflow = variables[1:]
            return self.func(variables[0])

    @rabbit
    def base_func(self, arg):
        """The Base Derivative Function."""
        return deriv(self.calc, arg, self.n, self.accuracy, self.scaledown)

class integbase(derivbase):
    """Holdes Methods Used In Integral Functions."""
    bound = None

    def call(self, variables):
        """Calls The Integral Function."""
        if variables is None:
            return self
        elif not variables:
            raise ExecutionError("ArgumentError", "No arguments were passed to a function that requires arguments")
        elif self.bound is not None:
            e.overflow = variables[1:]
            return self.func(self.bound, variables[0])
        elif len(variables) == 1:
            out = getcopy(self)
            out.bound = variables[0]
            return out
        else:
            e.overflow = variables[2:]
            return self.func(variables[0], variables[1])

    @rabbit
    def base_func(self, arg1, arg2):
        """The Base Integral Function."""
        return defint(self.calc, arg1, arg2, self.accuracy)

class derivfunc(derivbase, strfunc):
    """Implements A Derivative Function."""
    def __init__(self, *args, **kwargs):
        """Creates The Derivative Function."""
        if "n" in kwargs:
            self.n = int(kwargs["n"])
            del kwargs["n"]
        else:
            raise SyntaxError("Expected keyword argument n to derivfunc")
        if "accuracy" in kwargs:
            self.accuracy = float(kwargs["accuracy"])
            del kwargs["accuracy"]
        else:
            raise SyntaxError("Expected keyword argument accuracy to derivfunc")
        if "scaledown" in kwargs:
            self.scaledown = float(kwargs["scaledown"])
            del kwargs["scaledown"]
        else:
            raise SyntaxError("Expected keyword argument scaledown to derivfunc")
        if "varname" in kwargs:
            varname = str(kwargs["varname"])
            if "variables" in kwargs:
                kwargs["variables"].append(varname)
            else:
                kwargs["variables"] = [varname]
            del kwargs["varname"]
        strfunc.__init__(self, *args, **kwargs)

    def copy(self):
        """Returns A Copy Of The Derivative Function."""
        return derivfunc(self.funcstr,
                         self.variables,
                         self.personals,
                         self.name,
                         self.overflow,
                         self.allargs,
                         self.reqargs,
                         self.memoize,
                         self.memo,
                         self.method,
                         n=self.n,
                         accuracy=self.accuracy,
                         scaledown=self.scaledown
                         )

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        state = list(strfunc.getstate(self))
        state[0] = "derivfunc"
        state.extend([
            self.n,
            self.accuracy,
            self.scaledown
            ])
        return tuple(state)

class integfunc(integbase, strfunc):
    """Implements An Integral Function."""
    def __init__(self, *args, **kwargs):
        """Creates The Integral Function."""
        if "accuracy" in kwargs:
            self.accuracy = float(kwargs["accuracy"])
            del kwargs["accuracy"]
        else:
            raise SyntaxError("Expected keyword argument accuracy to derivfunc")
        if "varname" in kwargs:
            varname = str(kwargs["varname"])
            if "variables" in kwargs:
                kwargs["variables"].append(varname)
            else:
                kwargs["variables"] = [varname]
            del kwargs["varname"]
        strfunc.__init__(self, *args, **kwargs)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        state = list(strfunc.getstate(self))
        state[0] = "integfunc"
        state.append(self.accuracy)
        return tuple(state)

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfunc(self.funcstr,
                         self.variables,
                         self.personals,
                         self.name,
                         self.overflow,
                         self.allargs,
                         self.reqargs,
                         self.memoize,
                         self.memo,
                         self.method,
                         accuracy=self.accuracy
                         )

class derivfuncfloat(derivbase, funcfloat):
    """Implements A Derivative Function Of A Fake Function."""
    def __init__(self, func, n, accuracy, scaledown, funcstr=None, memoize=None, memo=None):
        """Creates The Derivative Function."""
        self.n = int(n)
        self.accuracy = float(accuracy)
        self.scaledown = float(scaledown)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.other_func = func

    def copy(self):
        """Returns A Copy Of The Derivative Float Function."""
        return integfunc(self.other_func, self.n, self.accuracy, self.scaledown, self.funcstr, self.memoize, self.memo)

    @rabbit
    def calc(self, x=None):
        """Calculates The Derivative Function."""
        if x is None:
            return self.other_func.call([])
        else:
            return self.other_func.call([x])

class integfuncfloat(integbase, funcfloat):
    """Implements An Integral Function Of A Fake Function."""
    def __init__(self, func, accuracy, funcstr=None, memoize=None, memo=None):
        """Creates The Integral Float Function."""
        self.accuracy = float(accuracy)
        if funcstr:
            self.funcstr = str(funcstr)
        else:
            self.funcstr = e.unusedarg()
        if memoize is not None:
            self.memoize = memoize
        if memo is None:
            self.memo = {}
        else:
            self.memo = memo
        self.other_func = func

    def copy(self):
        """Returns A Copy Of The Integral Function."""
        return integfuncfloat(self.other_func, self.accuracy, self.funcstr, self.memoize, self.memo)

class classcalc(cotobject):
    """Implements An Evaluator Class."""
    evaltype = "class"
    notmatrix = True
    doset = False
    selfvar = "__self__"

    def __init__(self, variables=None, name=None, selfvar=None, restricted=None):
        """Initializes The Class."""
        if selfvar is not None:
            self.selfvar = str(selfvar)
        if restricted is None:
            self.restricted = [self.selfvar]
        else:
            self.restricted = restricted
        self.variables = {
            self.selfvar : self
            }
        if variables is not None:
            self.add(variables, name=name)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("classcalc", getstates(self.getvars()), self.selfvar, self.restricted)

    def copy(self):
        """Copies The Class."""
        return classcalc(getcopy(self.getvars()), selfvar=self.selfvar, restricted=self.restricted)

    def process(self, command, inglobal=False):
        """Processes A Command And Puts The Result In The Variables."""
        self.calc(command, inglobal, e.process)

    def begin(self, inglobal=False):
        """Enters The Class."""
        if inglobal:
            oldset = e.setvars(self.variables)
            oldclass = False
        else:
            oldclass, e.useclass = e.useclass, self.selfvar
            oldset, self.doset = self.doset, e.setvars(self.variables)
        return oldset, oldclass

    def end(self, params):
        """Exits The Class."""
        oldset, oldclass = params
        if oldclass is False:
            e.setvars(oldset)
            return True
        else:
            e.setvars(self.doset)
            self.doset = oldset
            e.useclass = oldclass
            return False

    def calc(self, command, inglobal=False, func=None):
        """Calculates A String In The Environment Of The Class."""
        if func is None:
            func = e.calc
        command = e.namefind(basicformat(command))
        params = self.begin(inglobal)
        try:
            out = func(command, " | class")
        finally:
            self.end(params)
        return out

    def __len__(self):
        """Finds The Number Of Variables."""
        return len(self.variables)-1

    def items(self):
        """Returns The Variables."""
        return list(self.variables.items())

    def __repr__(self):
        """Gets A Representation."""
        return repr(self.getvars())

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
                    out += e.speedyprep(v, False, bottom, indebug, maxrecursion)
                else:
                    out += e.prepare(v, False, True, indebug, maxrecursion)
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
        test = basicformat(e.prepare(key, False, False))
        if test in self.restricted:
            raise ExecutionError("RedefinitionError", "The "+test+" variable cannot be redefined")
        elif not bypass and not e.validvar(test):
            raise ExecutionError("ClassError", "Could not store "+test+" in "+e.prepare(self, False, True, True))
        else:
            if name is not None and isinstance(value, funcfloat) and not isinstance(value, strfunc):
                value.funcstr = str(name)+"."+value.funcstr
            self.variables[test] = value
            if self.doset:
                self.doset[test] = haskey(e.variables, test)
                e.variables[test] = self.variables[test]

    def getmethod(self, key):
        """Attempts To Get An Item."""
        if istext(key):
            test = key
        else:
            test = basicformat(e.prepare(key, False, False))
        if e.validvar(test) and test in self.variables:
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
        return e.deprop(out)

    def retrieve(self, key):
        """Retrieves An Item."""
        test = self.getmethod(key)
        if test is None:
            raise ExecutionError("ClassError", "Could not find "+key+" in "+e.prepare(self, False, True, True))
        else:
            return test

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
            return e.getcall(item)(args)
        else:
            return item

    def init(self, params):
        """Initializes The Instance."""
        if "__new__" in self.variables:
            item = self.calc("__new__")
            if isfunc(item):
                value = self.domethod(item, params)
            else:
                e.overflow = params
                value = item
        else:
            e.overflow = params
            value = self
        if isinstance(value, classcalc) and not isinstance(value, instancecalc):
            return value.toinstance()
        else:
            raise ExecutionError("ClassError", "Constructor returned non-class object "+e.prepare(value, False, True, True))

    def __delitem__(self, key):
        """Wraps remove."""
        self.remove(key)
        return self

    def remove(self, key):
        """Removes An Item."""
        test = e.prepare(key, False, False)
        if e.validvar(test) and test in self.variables:
            del self.variables[test]
        else:
            raise ExecutionError("ClassError", "Could not remove "+test+" from "+e.prepare(self, False, True, True))

    def extend(self, other):
        """Extends The Class."""
        if isinstance(other, classcalc):
            self.add(other.getvars(True))
            return self
        else:
            raise ExecutionError("ClassError", "Could not extend class with "+repr(other))

    def add(self, other, bypass=True, name=None):
        """Adds Variables."""
        for k,v in other.items():
            self.store(k, v, bypass, name)

    def getvars(self, merge=None):
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
            if self.variables[self.selfvar] is other.variables[other.selfvar]:
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
        return instancecalc(self.variables)

    def tomatrix(self):
        """Returns A Matrix Of The Variables."""
        out = []
        for key in self.getvars().keys():
            out.append(rawstrcalc(key))
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
        return ("namespace", getstates(self.getvars()), self.selfvar, self.restricted)

    def copy(self):
        """Copies The Class."""
        return namespace(getcopy(self.getvars()), selfvar=self.selfvar, restricted=self.restricted)

    def getrepr(self, *args, **kwargs):
        """Wraps classcalc.getrepr."""
        return "namespace: "+classcalc.getrepr(self, *args, **kwargs)

    def call(self, variables):
        """Calls The Namespace."""
        if not variables:
            return self
        else:
            e.overflow = variables[1:]
            return self.calc(e.prepare(variables[0], True, False))

class instancecalc(numobject, classcalc):
    """An Evaluator Class Instance."""
    evaltype = "instance"
    parentvar = "__parent__"

    def __init__(self, variables=None, parent=None, name=None, top=True, selfvar=None, parentvar=None, restricted=None):
        """Creates An Instance Of An Evaluator Class."""
        if selfvar is not None:
            self.selfvar = str(selfvar)
        if restricted is None:
            self.restricted = [self.selfvar]
        else:
            self.restricted = restricted
        if parentvar is not None:
            self.parentvar = str(parentvar)
        if parent is None:
            variables = variables.copy()
            if not top and self.parentvar in variables:
                parent = variables[self.parentvar]
                del variables[self.parentvar]
            else:
                if classcalc.selfvar in variables:
                    del variables[classcalc.selfvar]
                parent = classcalc(variables)
                variables = None
        self.variables = {
            self.selfvar : self,
            self.parentvar : parent
            }
        if variables is not None:
            self.add(variables, name=name)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("instancecalc", getstates(self.getvars()), self.selfvar, self.parentvar, self.restricted)

    def copy(self):
        """Copies The Instance."""
        return instancecalc(getcopy(self.getvars()), top=False, selfvar=self.selfvar, parentvar=self.parentvar, restricted=self.restricted)

    def getparent(self):
        """Reconstructs The Parent Class."""
        return self.variables[self.parentvar]

    def toclass(self):
        """Converts To A Normal Class."""
        out = classcalc(self.getvars(True))
        return out

    def isfrom(self, parent):
        """Determines Whether The Instance Is From The Parent."""
        if isinstance(parent, classcalc):
            return self.getparent() == parent
        else:
            return False

    def getmethod(self, key):
        """Attempts To Get An Item."""
        if istext(key):
            test = key
        else:
            test = basicformat(e.prepare(key, False, False))
        if e.validvar(test) and test in self.variables:
            return self.getitem(test)
        elif "__get__" in self.variables:
            return self.domethod(self.getitem("__get__"), rawstrcalc(test))
        else:
            return self.getparent().getmethod(test)

    def getitem(self, test):
        """Retrieves An Item At The Base Level."""
        if istext(self.variables[test]):
            out = self.calc(self.variables[test])
            if isinstance(out, strfunc):
                out.curryself(self)
            self.store(test, out)
        elif self.variables[test] is None:
            out = matrix(0)
        else:
            if isinstance(self.variables[test], strfunc):
                self.variables[test].curryself(self)
            out = self.variables[test]
        return e.deprop(out)

    def store(self, key, value, bypass=False, name=None):
        """Stores An Item."""
        test = basicformat(e.prepare(key, False, False))
        value = getcopy(value)
        if test in self.restricted:
            raise ExecutionError("RedefinitionError", "The "+test+" variable cannot be redefined.")
        elif not bypass and not e.validvar(test):
            raise ExecutionError("ClassError", "Could not store "+test+" in "+e.prepare(self, False, True, True))
        else:
            if isinstance(value, strfunc):
                value.curryself(self)
            elif name is not None and isinstance(value, funcfloat):
                value.funcstr = str(name)+"."+value.funcstr
            self.variables[test] = value
            if self.doset:
                self.doset[test] = haskey(e.variables, test)
                e.variables[test] = self.variables[test]

    def isprop(self):
        """Determines Whether The Class Is A Property."""
        return bool(self.getmethod("__value__"))

    def isfunc(self):
        """Determines Whether The Class Is A Function."""
        return bool(self.getmethod("__call__"))

    def getvars(self, merge=False):
        """Gets Original Variables."""
        if merge:
            out = self.getparent().getvars(True)
            out.update(self.variables)
        else:
            out = self.variables.copy()
        for var in self.restricted:
            del out[var]
        return out

    def call(self, variables):
        """Calls The Function."""
        if variables is None:
            func = self.getmethod("__value__")
            if func is None:
                return self
            else:
                e.setreturned()
                return self.domethod(func)
        else:
            func = self.getmethod("__call__")
            if func is None:
                raise ExecutionError("ClassError", "The class being called has no __call__ method")
            else:
                return self.domethod(func, varproc(variables))

    def ismatrix(self):
        """Determines Whether The Class Can Be A Matrix."""
        return bool(self.getmethod("__matrix__"))

    def tomatrix(self):
        """Converts To Matrix."""
        func = self.getmethod("__matrix__")
        if func is None:
            raise ExecutionError("ClassError", "The class being converted to a matrix has no __matrix__ method")
        else:
            return self.domethod(func)

    def __contains__(self, item):
        """Determines Whether item in self."""
        check_in = self.getmethod("__in__")
        if check_in:
            return self.domethod(check_in, item)
        check_cont = self.getmethod("__matrix__")
        if check_cont:
            return item in self.domethod(check_cont)
        raise ExecutionError("TypeError", "Insufficient methods defined for in")

    def __iadd__(self, other):
        """Performs Addition."""
        check_add = self.getmethod("__add__")
        if check_add:
            return self.domethod(check_add, other)
        check_sub = self.getmethod("__sub__")
        if check_sub:
            return self.domethod(check_sub, -other)
        raise ExecutionError("TypeError", "Insufficient methods defined for addition")

    def __isub__(self, other):
        """Performs Subtraction."""
        check_sub = self.getmethod("__sub__")
        if check_sub:
            return self.domethod(check_sub, other)
        check_add = self.getmethod("__add__")
        if check_add:
            return self.domethod(check_add, -other)
        raise ExecutionError("TypeError", "Insufficient methods defined for subtraction")

    def __imul__(self, other):
        """Performs Multiplication."""
        check_mul = self.getmethod("__mul__")
        if check_mul:
            return self.domethod(check_mul, other)
        check_div = self.getmethod("__div__")
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
        check_div = self.getmethod("__div__")
        if check_div:
            return self.domethod(check_div, other)
        check_mul = self.getmethod("__mul__")
        if check_mul:
            return self.domethod(check_mul, 1.0/other)
        check_fdiv = self.getmethod("__fdiv__")
        if check_fdiv:
            check_mod = self.getmethod("__mod__")
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
        check_rdiv = self.getmethod("__rdiv__")
        if check_rdiv:
            return self.domethod(check_rdiv, other)
        check_pow = self.getmethod("__pow__")
        if check_pow:
            return other*self.domethod(check_pow, -1.0)
        raise ExecutionError("TypeError", "Insufficient methods defined for division")

    def __ifloordiv__(self, other):
        """Performs Floor Division."""
        check_fdiv = self.getmethod("__fdiv__")
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
        check_mod = self.getmethod("__mod__")
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
        check_pow = self.getmethod("__pow__")
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
        check_rfdiv = self.getmethod("__rfdiv__")
        if check_rfdiv:
            return self.domethod(check_rfdiv, other)
        else:
            return int(other / self)

    def __rmod__(self, other):
        """Performs Reverse Modulo."""
        check_rmod = self.getmethod("__rmod__")
        if check_rmod:
            return self.domethod(check_rmod, other)
        raise ExecutionError("TypeError", "Insufficient methods defined for reverse modulus")

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        check_rpow = self.getmethod("__rpow__")
        if check_rpow:
            return self.domethod(check_rpow, other)
        raise ExecutionError("TypeError", "Insufficient methods defined for reverse exponentiation")

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        check_rmul = self.getmethod("__rmul__")
        if check_rmul:
            return self.domethod(check_rmul, other)
        else:
            return self*other

    def __radd__(self, other):
        """Performs Reverse Addition."""
        check_radd = self.getmethod("__radd__")
        if check_radd:
            return self.domethod(check_radd, other)
        else:
            return self+other

    def __rsub__(self, other):
        """Performs Reverse Subtraction."""
        check_rsub = self.getmethod("__rsub__")
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
        check_num = self.getmethod("__num__")
        if check_num:
            return self.domethod(check_num)
        raise ExecutionError("TypeError", "Insufficient methods defined for conversion to number")

    def __abs__(self):
        """Performs Absolute Value."""
        check_abs = self.getmethod("__abs__")
        if check_abs:
            return self.domethod(check_abs)
        if self < 0:
            return -self
        else:
            return self

    def __cmp__(self, other):
        """Performs Comparison."""
        check_cmp = self.getmethod("__cmp__")
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
            check_eq = self.getmethod("__eq__")
            if check_eq:
                return self.domethod(check_eq, other)
            check_ne = self.getmethod("__ne__")
            if check_ne:
                return not self.domethod(check_ne, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
            check_gt = self.getmethod("__gt__")
            if check_gt:
                check_lt = self.getmethod("__lt__")
                if check_lt:
                    return not self.domethod(check_gt, other) and not self.domethod(check_lt, other)
            check_ge = self.getmethod("__ge__")
            if check_ge:
                check_le = self.getmethod("__le__")
                if check_le:
                    return self.domethod(check_ge, other) and self.domethod(check_le, other)
            if isinstance(other, instancecalc):
                return classcalc.__eq__(self, other)
            else:
                return False

    def __ne__(self, other):
        """Performs Not Equal."""
        if not hasnum(other):
            return True
        else:
            check_ne = self.getmethod("__ne__")
            if check_ne:
                return self.domethod(check_ne, other)
            check_eq = self.getmethod("__eq__")
            if check_eq:
                return not self.domethod(check_eq, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) == 0.0
            check_gt = self.getmethod("__gt__")
            if check_gt:
                check_lt = self.getmethod("__lt__")
                if check_lt:
                    return not self.domethod(check_gt, other) and not self.domethod(check_lt, other)
            check_ge = self.getmethod("__ge__")
            if check_ge:
                check_le = self.getmethod("__le__")
                if check_le:
                    return not (self.domethod(check_ge, other) and self.domethod(check_le, other))
            if isinstance(other, instancecalc):
                return not classcalc.__eq__(self, other)
            else:
                return True

    def __gt__(self, other):
        """Performs Greater Than."""
        if not hasnum(other):
            return False
        else:
            check_gt = self.getmethod("__gt__")
            if check_gt:
                return self.domethod(check_gt, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) > 0.0
            check_le = self.getmethod("__le__")
            if check_le:
                return not self.domethod(check_le, other)
            check_ge = self.getmethod("__ge__")
            if check_ge:
                check_eq = self.getmethod("__eq__")
                if check_eq:
                    return self.domethod(check_ge, other) and not self.domethod(check_eq, other)
            raise ExecutionError("TypeError", "Insufficient methods defined for greater than")

    def __lt__(self, other):
        """Performs Less Than."""
        if not hasnum(other):
            return False
        else:
            check_lt = self.getmethod("__lt__")
            if check_lt:
                return self.domethod(check_lt, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) < 0.0
            check_ge = self.getmethod("__ge__")
            if check_ge:
                return not self.domethod(check_ge, other)
            check_le = self.getmethod("__le__")
            if check_le:
                check_eq = self.getmethod("__eq__")
                if check_eq:
                    return self.domethod(check_le, other) and not self.domethod(check_eq, other)
            raise ExecutionError("TypeError", "Insufficient methods defined for less than")

    def __ge__(self, other):
        """Performs Greater Than Or Equal."""
        if not hasnum(other):
            return False
        else:
            check_ge = self.getmethod("__ge__")
            if check_ge:
                return self.domethod(check_ge, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) >= 0.0
            check_lt = self.getmethod("__lt__")
            if check_lt:
                return not self.domethod(check_lt, other)
            check_gt = self.getmethod("__gt__")
            if check_gt:
                check_eq = self.getmethod("__eq__")
                if check_eq:
                    return self.domethod(check_gt, other) or self.domethod(check_eq, other)
            raise ExecutionError("TypeError", "Insufficient methods defined for greater than or equal")

    def __le__(self, other):
        """Performs Less Than Or Equal."""
        if not hasnum(other):
            return False
        else:
            check_le = self.getmethod("__le__")
            if check_le:
                return self.domethod(check_le, other)
            check_cmp = self.getmethod("__cmp__")
            if check_cmp:
                return self.domethod(check_cmp, other) <= 0.0
            check_gt = self.getmethod("__gt__")
            if check_gt:
                return not self.domethod(check_gt, other)
            check_lt = self.getmethod("__lt__")
            if check_lt:
                check_eq = self.getmethod("__eq__")
                if check_eq:
                    return self.domethod(check_lt, other) or self.domethod(check_eq, other)
            raise ExecutionError("TypeError", "Insufficient methods defined for less than or equal")

    def __str__(self):
        """Retrieves A String."""
        check_str = self.getmethod("__str__")
        if check_str:
            return e.prepare(self.domethod(check_str), True, False)
        else:
            return self.getrepr(True)

    def __len__(self):
        """Retrieves The Length."""
        check_len = self.getmethod("__len__")
        if check_len:
            return self.domethod(check_len)
        check_cont = self.getmethod("__matrix__")
        if check_cont:
            return len(self.domethod(check_cont))
        raise ExecutionError("ClassError", "Insufficient methods defined for len")

    def __bool__(self):
        """Converts To A Boolean."""
        check_bool = self.getmethod("__bool__")
        if check_bool:
            return bool(self.domethod(check_bool))
        check_num = self.getmethod("__num__")
        if check_num:
            return bool(self.domethod(check_num))
        check_len = self.getmethod("__len__")
        if check_len:
            return bool(self.domethod(check_len))
        check_cont = self.getmethod("__matrix__")
        if check_cont:
            return bool(self.domethod(check_cont))
        return True

    def typecalc(self):
        """Finds The Type Of The Instance."""
        item = self.getmethod("__type__")
        if item:
            return self.domethod(item)
        else:
            return rawstrcalc(self.evaltype)

    def op_repeat(self, other):
        """Performs **."""
        item = self.getmethod("__rep__")
        if item:
            return self.domethod(item, other)
        else:
            return NotImplemented

    def rop_repeat(self, other):
        """Performs Reverse **."""
        item = self.getmethod("__rrep__")
        if item:
            return self.domethod(item, other)
        else:
            return NotImplemented

    def op_join(self, params):
        """Performs ++."""
        item = self.getmethod("__join__")
        if item:
            return self.domethod(item, params)
        else:
            return NotImplemented

    def rop_join(self, params):
        """Performs Reverse ++."""
        item = self.getmethod("__rjoin__")
        if item:
            return self.domethod(item, params)
        else:
            return NotImplemented

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if indebug or maxrecursion <= 0:
            return e.speedyprep(self, False, bottom, indebug, maxrecursion)
        elif not bottom:
            return str(self)
        elif not top:
            return classcalc.getrepr(self, top, bottom, indebug, maxrecursion)+" ( )"
        else:
            check_repr = self.getmethod("__repr__")
            if check_repr:
                return e.prepare(self.domethod(check_repr), top, False, indebug, maxrecursion)
            else:
                return classcalc.getrepr(self, top, bottom, indebug, maxrecursion)+" ( )"

    def include(self):
        """Returns A Class For Inclusion."""
        item = self.getmethod("__include__")
        if item:
            return self.domethod(item)
        else:
            raise ExecutionError("TypeError", "Insufficient methods defined for include")

    def inside_enter(self, args):
        """Enters The Inside."""
        item = self.getmethod("__enter__")
        if item:
            return self.domethod(item, args)
        else:
            raise ExecutionError("TypeError", "Insufficient methods defined for inside")

    def inside_exit(self, args):
        """Exits The Inside."""
        item = self.getmethod("__exit__")
        if item:
            return self.domethod(item, args)
        elif len(args) == 1:
            return args[0]
        elif len(args) == 2 and isnull(args[0]):
            return args[1]
        else:
            return rowmatrixlist(args)

    def merge(self, other):
        """Merges Two Classes."""
        self.add(other.getvars())
        if isinstance(other, instancecalc):
            self.variables[self.parentvar].extend(other.getparent())

class atom(evalobject):
    """Implements Atoms."""
    evaltype = "_"

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("atom", )

    def copy(self):
        """Makes Another Atom."""
        return atom()

    @rabbit
    def calc(self):
        """Converts To Nothing."""
        return matrix(0)

    @rabbit
    def __eq__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    @rabbit
    def __ne__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    @rabbit
    def __gt__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    @rabbit
    def __lt__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    @rabbit
    def __ge__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    @rabbit
    def __le__(self, other):
        """Always Is True For Evaluator Objects."""
        if hasnum(other):
            return True
        else:
            return False

    def __iadd__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __radd__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __isub__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __rsub__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __imul__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __rmul__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __idiv__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __rdiv__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __ipow__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __rpow__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __imod__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __rmod__(self, other):
        """Always Returns self."""
        return self

    @rabbit
    def __str__(self):
        """Gets A Representation."""
        return "_"

class rollfunc(strfunc):
    """Implements A Random Number Generator Object."""
    memoize = False
    variables = ["__times__"]

    def __init__(self, stop, key=None, name=None, counter=None):
        """Creates The Random Number Generator."""
        self.gen = random(key)
        if counter is not None:
            self.gen.counter = int(counter)
        self.stop = getnum(stop)
        self.funcstr = str(self.stop)
        if name:
            self.name = str(name)
        else:
            self.name = e.unusedarg()

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("rollfunc", self.stop, self.gen.key, self.name, self.gen.counter)

    def copy(self):
        """Copies The Random Number Generator."""
        return rollfunc(self.stop, self.gen.key, self.name, self.gen.counter)

    @rabbit
    def calc(self, m=1.0):
        """Generates A Random Number."""
        e.setreturned()
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

    @rabbit
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

    def __init__(self, key, value):
        """Creates The Key-Value Pair."""
        self.k = key
        self.v = value

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("pair", itemstate(self.k), itemstate(self.v))

    def copy(self):
        """Copies The Key-Value Pair."""
        return pair(getcopy(self.k), getcopy(self.v))

    def call(self, variables):
        """Retrieves A Value."""
        e.overflow = variables[1:]
        if not variables:
            return self
        elif self.k == variables[0]:
            return self.v
        else:
            raise ExecutionError("KeyError", "Could not find key "+e.prepare(variables[0])+" in "+e.prepare(self))

    @rabbit
    def items(self):
        """Gets A List Containing The Key And The Value."""
        return [self.k, self.v]

    def remove(self, item):
        """Removes An Item."""
        raise TypeError("Pairs don't support subtraction")

    def __iadd__(self, item):
        """Extends With An Item."""
        if isinstance(item, dictionary):
            out = getcopy(item)
            out.store(self.k, self.v)
            return out
        elif isinstance(item, pair):
            out = {
                self.k : self.v,
                item.k : item.v
                }
            return dictionary(out)
        else:
            raise TypeError("Pairs only support addition by other pairs")

    def __imul__(self, item):
        """Extends With An Item."""
        self += item
        return self

    @rabbit
    def __eq__(self, other):
        """Performs Equality."""
        if isinstance(other, pair) and not isinstance(other, dictionary):
            return self.k == other.k and self.v == other.v
        else:
            return False

class dictionary(pair):
    """A Key-Value Dictionary."""
    evaltype = "dict"

    def __init__(self, items=None):
        """Creates The Dictionary."""
        if items is None:
            self.a = {}
        else:
            self.a = items.copy()

    def copy(self):
        """Copies The Dictionary."""
        return dictionary(self.a)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("dictionary", getstates(self.a))

    def store(self, key, value):
        """Stores An Item."""
        self.a[key] = value

    @rabbit
    def items(self):
        """Gets Items."""
        return list(self.a.items())

    def call(self, variables):
        """Retrieves A Value."""
        e.overflow = variables[1:]
        if not variables:
            return self
        elif variables[0] in self.a:
            return self.a[variables[0]]
        else:
            raise ExecutionError("KeyError", "Could not find key "+e.prepare(variables[0])+" in "+e.prepare(self))

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

    @rabbit
    def __eq__(self, other):
        """Performs Equality."""
        if isinstance(other, dictionary):
            return self.a == other.a
        else:
            return False

    @rabbit
    def __len__(self):
        """Finds A Length."""
        return len(self.a)

    @rabbit
    def __contains__(self, other):
        """Performs in."""
        return other in self.a

    @rabbit
    def tomatrix(self):
        """Converts To A Matrix."""
        items = list(self.a.items())
        out = matrix(len(items), 2)
        for x in xrange(0, len(items)):
            out.store(x, 0, items[x][0])
            out.store(x, 1, items[x][1])
        return out

    def __delitem__(self, key):
        """Deletes An Item."""
        del self.a[key]

    @rabbit
    def __cmp__(self, other):
        """Performs Comparison."""
        if isinstance(other, dictionary):
            return cmp(self.a, other.a)
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    @rabbit
    def __gt__(self, other):
        """Determines If Proper Subset."""
        if isinstance(other, dictionary):
            if len(self.a) > len(other.a):
                return self >= other
            else:
                return False
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    @rabbit
    def __ge__(self, other):
        """Determines If Subset."""
        if isinstance(other, dictionary):
            for item in other.a:
                if not item in self.a:
                    return False
            return True
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    @rabbit
    def __lt__(self, other):
        """Wraps Greater Than."""
        if isinstance(other, dictionary):
            return other > self
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

    @rabbit
    def __le__(self, other):
        """Wraps Greater Than Or Equal."""
        if isinstance(other, dictionary):
            return other >= self
        else:
            raise ExecutionError("TypeError", "Dictionaries can only be compared with other dictionaries")

class bracket(evalobject):
    """A To-Be-Calculated Row."""
    def __init__(self, items):
        """Constructs The Row."""
        self.items = items

    @rabbit
    def calc(self):
        """Calculates The Row."""
        out = []
        for item in self.items:
            item = basicformat(item)
            if item:
                out.append(e.calc(item))
        return rowmatrixlist(out)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("bracket", self.items)

class brace(bracket):
    """A To-Be-Calculated Dictionary."""

    @rabbit
    def calc(self):
        """Calculates The Dictionary."""
        out = {}
        for item in self.items:
            item = basicformat(item)
            if item:
                value = e.calc(item)
                if isinstance(value, dictionary):
                    out.update(value.a)
                elif isinstance(value, pair):
                    out[value.k] = value.v
                else:
                    raise ExecutionError("ValueError", "Dictionary got non-pair item "+e.prepare(value, False, True, True))
        return dictionary(out)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("brace", self.items)

class evalwrap(evalobject):
    """A Wrapper For Converting An Arbitrary Python Object Into A Rabbit Object."""
    check = 2
    evaltype = "Meta.wrap"
    notmatrix = True

    def __init__(self, inputobj, reference=None, safemethods=None):
        """Constructs The Wrapper."""
        if reference is None or istext(reference):
            self.ref = reference
        else:
            self.ref = reference()
        if safemethods is None:
            self.safe = []
        else:
            self.safe = safemethods
        self.obj = inputobj

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        if self.ref is None:
            raise ExecutionError("WrapperError", "Cannot get the state of a temporary wrapper object")
        else:
            return ("find", self.ref)

    def copy(self):
        """Copies The Wrapper."""
        return evalwrap(self.obj, self.ref, self.safe)

    def convert(self, item):
        """Converts An Item."""
        return e.topython(item)

    def argproc(self, variables):
        """Converts Variables."""
        args, kwargs = [], {}
        for var in variables:
            item = self.convert(var)
            if isinstance(item, pair):
                kwargs[self.convert(item.k)] = self.convert(item.v)
            else:
                args.append(item)
        return args, kwargs

    def prepare(self, output, ref=None):
        """Prepares The Output Of A Python Call."""
        return e.frompython(output, ref)

    def getref(self):
        """Gets The Reference."""
        if self.ref is None:
            raise ExecutionError("WrapperError", "Cannot do operations on an unreferenced wrapper")
        else:
            return "("+self.ref+")"

    def checksafe(self, name):
        """Sets Returned If name Isn't Safe."""
        if self.safe is not True and (self.safe is False or name not in self.safe):
            e.setreturned()

    def call(self, variables):
        """Calls The Function."""
        self.checksafe("__call__")
        def _ref():
            return self.getref()+"(("+strlist(variables, "),(", lambda x: e.prepare(x, False, True))+"))"
        args, kwargs = self.argproc(variables)
        return self.prepare(self.obj(*args, **kwargs), _ref)

    def isfunc(self):
        """Determines Whether Or Not The Object Is A Function."""
        return hasattr(self.obj, "__call__")

    def ismatrix(self):
        """Determines Whether Or Not The Object Is A Matrix."""
        return hasattr(self.obj, "__iter__")

    def getrepr(self, top, bottom, indebug, maxrecursion):
        """Gets A Representation."""
        if indebug or maxrecursion <= 0:
            return self.ref
        elif not bottom:
            return str(self)
        elif not top:
            return self.ref
        else:
            return repr(self)

    def __repr__(self):
        """Gets A Representation."""
        self.checksafe("__repr__")
        return repr(self.obj)

    def __str__(self):
        """Gets A String."""
        self.checksafe("__str__")
        return str(self.obj)

    def hasitemcall(self):
        """Determines Whether Or Not The Object Has An Item Call."""
        return hasattr(self.obj, "__getitem__")

    def itemcall(self, variables):
        """Gets An Item."""
        if hasattr(self, "__getitem__"):
            self.checksafe("__getitem__")
            args, kwargs = self.argproc(variables)
            if kwargs or len(args) > 1:
                args = slice(*args, **kwargs)
            def _ref():
                return self.getref()+":("+strlist(variables, "):(", lambda x: e.prepare(x, False, True))+")"
            return self.prepare(self.obj[args[0]], _ref)
        else:
            return self.call(variables)

    def getmethod(self, key):
        """Gets A Method."""
        if hasattr(self.obj, key):
            self.checksafe(key)
            return self.prepare(getattr(self.obj, key), self.getref()+"."+key)
        else:
            return None

    def __bool__(self):
        """Converts To A Boolean."""
        self.checksafe("__bool__")
        return bool(self.obj)

    def __int__(self):
        """Converts To An Integer."""
        self.checksafe("__int__")
        return int(self.obj)

    def __float__(self):
        """Converts To A Float."""
        self.checksafe("__float__")
        return old_float(self.obj)

    def __index__(self):
        """Gets An Index."""
        if hasattr(self.obj, "__index__"):
            self.checksafe("__index__")
            return self.obj.__index__()
        else:
            return int(self)

    def __len__(self):
        """Gets A Length."""
        self.checksafe("__len__")
        return len(self.obj)

    def __complex__(self):
        """Gets A Complex Number."""
        self.checksafe("__complex__")
        return complex(self.obj)

    def __eq__(self, other):
        """Performs ==."""
        self.checksafe("__eq__")
        return self.obj == self.convert(other)

    def __ne__(self, other):
        """Performs !=."""
        self.checksafe("__ne__")
        return self.obj != self.convert(other)

    def __lt__(self, other):
        """Performs <."""
        self.checksafe("__lt__")
        return self.obj < self.convert(other)

    def __gt__(self, other):
        """Performs >."""
        self.checksafe("__gt__")
        return self.obj > self.convert(other)

    def __le__(self, other):
        """Performs <=."""
        self.checksafe("__le__")
        return self.obj <= self.convert(other)

    def __ge__(self, other):
        """Performs >=."""
        self.checksafe("__ge__")
        return self.obj >= self.convert(other)

    def __add__(self, other):
        """Performs Addition."""
        self.checksafe("__add__")
        def _ref():
            return self.getref()+"+("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj + self.convert(other), _ref)

    def __radd__(self, other):
        """Performs Reverse Addition."""
        self.checksafe("__radd__")
        def _ref():
            return "("+e.prepare(other, False, True)+")+"+self.getref()
        return self.prepare(self.convert(other) + self.obj, _ref)

    def __sub__(self, other):
        """Performs Subtraction."""
        self.checksafe("__sub__")
        def _ref():
            return self.getref()+"-("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj - self.convert(other), _ref)

    def __rsub__(self, other):
        """Performs Reverse Subtraction."""
        self.checksafe("__rsub__")
        def _ref():
            return "("+e.prepare(other, False, True)+")-"+self.getref()
        return self.prepare(self.convert(other) - self.obj, _ref)

    def __mul__(self, other):
        """Performs Multiplication."""
        self.checksafe("__mul__")
        def _ref():
            return self.getref()+"*("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj * self.convert(other), _ref)

    def __rmul__(self, other):
        """Performs Reverse Multiplication."""
        self.checksafe("__rmul__")
        def _ref():
            return "("+e.prepare(other, False, True)+")*"+self.getref()
        return self.prepare(self.convert(other) * self.obj, _ref)

    def __div__(self, other):
        """Performs Division."""
        self.checksafe("__div__")
        def _ref():
            return self.getref()+"/("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj / self.convert(other), _ref)

    def __rdiv__(self, other):
        """Performs Reverse Division."""
        self.checksafe("__rdiv__")
        def _ref():
            return "("+e.prepare(other, False, True)+")/"+self.getref()
        return self.prepare(self.convert(other) / self.obj, _ref)

    def __floordiv__(self, other):
        """Performs Floor Division."""
        self.checksafe("__floordiv__")
        def _ref():
            return self.getref()+"//("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj // self.convert(other), _ref)

    def __rfloordiv__(self, other):
        """Performs Reverse Floor Division."""
        self.checksafe("__rfloordiv__")
        def _ref():
            return "("+e.prepare(other, False, True)+")//"+self.getref()
        return self.prepare(self.convert(other) // self.obj, _ref)

    def __mod__(self, other):
        """Performs Modulus."""
        self.checksafe("__mod__")
        def _ref():
            return self.getref()+"%("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj % self.convert(other), _ref)

    def __rmod__(self, other):
        """Performs Reverse Modulus."""
        self.checksafe("__rmod__")
        def _ref():
            return "("+e.prepare(other, False, True)+")%"+self.getref()
        return self.prepare(self.convert(other) % self.obj, _ref)

    def __pow__(self, other):
        """Performs Exponentiation."""
        self.checksafe("__pow__")
        def _ref():
            return self.getref()+"^("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj ** self.convert(other), _ref)

    def __rpow__(self, other):
        """Performs Reverse Exponentiation."""
        self.checksafe("__rpow__")
        def _ref():
            return "("+e.prepare(other, False, True)+")^"+self.getref()
        return self.prepare(self.convert(other) ** self.obj, _ref)

    def __lshift__(self, other):
        """Performs Left Shift."""
        self.checksafe("__lshift__")
        def _ref():
            return self.getref()+" lshift ("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj << self.convert(other), _ref)

    def __rlshift__(self, other):
        """Performs Reverse Left Shift."""
        self.checksafe("__rlshift__")
        def _ref():
            return "("+e.prepare(other, False, True)+") lshift "+self.getref()
        return self.prepare(self.convert(other) << self.obj, _ref)

    def __rshift__(self, other):
        """Performs Right Shift."""
        self.checksafe("__rshift__")
        def _ref():
            return self.getref()+" rshift ("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj >> self.convert(other), _ref)

    def __rrshift__(self, other):
        """Performs Reverse Right Shift."""
        self.checksafe("__rrshift__")
        def _ref():
            return "("+e.prepare(other, False, True)+") rshift "+self.getref()
        return self.prepare(self.convert(other) >> self.obj, _ref)

    def __or__(self, other):
        """Performs Bitwise Or."""
        self.checksafe("__or__")
        def _ref():
            return self.getref()+" bitor ("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj | self.convert(other), _ref)

    def __ror__(self, other):
        """Performs Reverse Bitwise Or."""
        self.checksafe("__ror__")
        def _ref():
            return "("+e.prepare(other, False, True)+") bitor "+self.getref()
        return self.prepare(self.convert(other) | self.obj, _ref)

    def __and__(self, other):
        """Performs Bitwise And."""
        self.checksafe("__and__")
        def _ref():
            return self.getref()+" bitand ("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj & self.convert(other), _ref)

    def __rand__(self, other):
        """Performs Reverse Bitwise And."""
        self.checksafe("__rand__")
        def _ref():
            return "("+e.prepare(other, False, True)+") bitand "+self.getref()
        return self.prepare(self.convert(other) & self.obj, _ref)

    def __xor__(self, other):
        """Performs Bitwise Xor."""
        self.checksafe("__xor__")
        def _ref():
            return self.getref()+" bitxor ("+e.prepare(other, False, True)+")"
        return self.prepare(self.obj ^ self.convert(other), _ref)

    def __rxor__(self, other):
        """Performs Reverse Bitwise Xor."""
        self.checksafe("__rxor__")
        def _ref():
            return "("+e.prepare(other, False, True)+") bitxor "+self.getref()
        return self.prepare(self.convert(other) ^ self.obj, _ref)

    def __neg__(self):
        """Performs Unary Negation."""
        self.checksafe("__neg__")
        return self.prepare(-self.obj, "-"+self.getref()+"")

    def __pos__(self):
        """Performs Unary Positive."""
        self.checksafe("__pos__")
        return self.prepare(+self.obj, "+"+self.getref()+"")

    def __invert__(self):
        """Performs Bitwise Inverse."""
        self.checksafe("__invert__")
        return self.prepare(~self.obj, "bitnot:"+self.getref())

    def __abs__(self):
        """Performs Absolute Value."""
        self.checksafe("__abs__")
        return self.prepare(abs(self.obj), "abs:"+self.getref())

    def __bin__(self):
        """Gets A Binary Representation."""
        self.checksafe("__bin__")
        return self.prepare(bin(self.obj), "bin:"+self.getref())

    def __oct__(self):
        """Gets An Octal Representation."""
        self.checksafe("__oct__")
        return self.prepare(oct(self.obj), "oct:"+self.getref())

    def __hex__(self):
        """Gets A Hex Representation."""
        self.checksafe("__hex__")
        return self.prepare(hex(self.obj), "hex:"+self.getref())

    def __round__(self, place):
        """Performs Round."""
        self.checksafe("__round__")
        def _ref():
            return "round:"+self.getref()+":("+e.prepare(place, False, True)+")"
        return self.prepare(round(self.obj, place), _ref)

    def __divmod__(self, other):
        """Performs divmod."""
        self.checksafe("__divmod__")
        def _ref():
            return self.getref()+" divmod ("+e.prepare(other, False, True)+")"
        return self.prepare(divmod(self.obj, other), _ref)

    def __rdivmod__(self, other):
        """Performs Reverse divmod."""
        self.checksafe("__rdivmod__")
        def _ref():
            return "("+e.prepare(other, False, True)+") divmod "+self.getref()
        return self.prepare(divmod(other, self.obj), _ref)

    def __contains__(self, item):
        """Performs in."""
        self.checksafe("__contains__")
        def _ref():
            return "("+e.prepare(item, False, True)+") in "+self.getref()
        return item in self.obj

    def inside_enter(self, args):
        """Enters The Inside."""
        if len(args) > 1:
            raise ExecutionError("ArgumentError", "Excess arguments "+strlist(args[1:], ", ", lambda x: e.prepare(x, False, True)))
        elif hasattr(self.obj, "__enter__"):
            self.checksafe("__enter__")
            out = self.prepare(self.obj.__enter__())
            if args:
                return e.getcall(args[0])([out])
            else:
                return out
        else:
            raise ExecutionError("WrapperError", "Object has no __enter__ method")

    def inside_exit(self, args):
        """Exits The Inside."""
        if hasattr(self.obj, "__exit__"):
            self.checksafe("__exit__")
            self.obj.__exit__(None, None, None)
        if len(args) == 1:
            return args[0]
        elif len(args) == 2 and isnull(args[0]):
            return args[1]
        else:
            return rowmatrixlist(args)

    def __hash__(self):
        """Returns A Hash."""
        self.checksafe("__hash__")
        return hash(self.obj)

    def tomatrix(self):
        """Converts To A Matrix."""
        self.checksafe("__iter__")
        out = []
        for item in self.obj:
            out.append(item)
        return self.prepare(out)
