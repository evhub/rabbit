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

from .data import *
from .fraction import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class evaluator(object):
    """Evaluates Equations And Expressions.

Global Operator Precedence List:
    "       Opens and closes strings.
    {}      Opens and closes classes.
    []      Opens and closes matrix rows.
    ()      Opens and closes parentheses.

    $       Seperates with clauses (read as 'where').
    ;       Seperates conditionals (read as 'else').
    @       Checks a conditional (read as 'if' or 'at').

    |       Performs logical 'or'.
    &       Performs logical 'and'.
    >?!=<   Performs equality or inequality checks.

    ~       Applies a list to a function for looping.
    ..      Performs concatenation.
    **      Performs repeat.
    ,       Seperates list elements.
    +-      Performs addition and subtraction.
    %       Performs modulo.
    */      Performs multiplication and division.

    var     Evaluates variables.
    none    Evaluates empty expressions.
    -       Denotes negatives.
    /       Denotes reciprocals.
    ^       Performs exponentiation.
    \       Creates a lambda.
    :       Performs function calls.
    `       Denotes parentheses.
    .       Denotes methods and functions of functions.
    normal  Evaluates numbers."""
    reserved = string.digits+':;@~+-*^%/&|><!"=()[]{}\\,?`.$'
    varname = "x"
    defprefix = "'"
    lastname = "last"

    def __init__(self, variables=None, processor=None):
        """Initializes The Evaluator."""
        self.processor = processor
        try:
            self.processor.debug
        except AttributeError:
            self.debug = False
        else:
            self.debug = self.processor.debug
        if self.debug:
            self.info = ""
        self.recursion = 0
        self.overflow = []
        funcs = evalfuncs(self)
        self.variables = {
            "copy":funcfloat(funcs.copycall, self, "copy"),
            "type":funcfloat(funcs.typecall, self, "type"),
            "to":funcfloat(funcs.tocall, self, "to"),
            "str":funcfloat(funcs.strcall, self, "str"),
            "repr":funcfloat(funcs.reprcall, self, "repr"),
            "calc":funcfloat(funcs.docalc, self, "calc"),
            "fold":funcfloat(funcs.foldcall, self, "fold"),
            "D":funcfloat(funcs.derivcall, self, "D"),
            "S":funcfloat(funcs.integcall, self, "S"),
            "L":funcfloat(funcs.brackcall, self, "L"),
            "list":funcfloat(funcs.listcall, self, "list"),
            "matrix":funcfloat(funcs.matrixcall, self, "matrix"),
            "cont":funcfloat(funcs.getmatrixcall, self, "cont"),
            "det":funcfloat(funcs.detcall, self, "det"),
            "sum":funcfloat(funcs.sumcall, self, "sum"),
            "prod":funcfloat(funcs.prodcall, self, "prod"),
            "join":funcfloat(funcs.joincall, self, "join"),
            "merge":funcfloat(funcs.mergecall, self, "merge"),
            "sort":funcfloat(funcs.sortcall, self, "sort"),
            "rev":funcfloat(funcs.reversecall, self, "rev"),
            "round":funcfloat(funcs.roundcall, self, "round"),
            "num":funcfloat(funcs.numcall, self, "num"),
            "eval":funcfloat(funcs.collapsecall, self, "eval"),
            "find":funcfloat(funcs.findcall, self, "find"),
            "split":funcfloat(funcs.splitcall, self, "split"),
            "replace":funcfloat(funcs.replacecall, self, "replace"),
            "contains":funcfloat(funcs.containscall, self, "contains"),
            "range":funcfloat(funcs.rangecall, self, "range"),
            "len":funcfloat(funcs.lencall, self, "len"),
            "size":funcfloat(funcs.sizecall, self, "size"),
            "abs":funcfloat(funcs.abscall, self, "abs"),
            "data":funcfloat(funcs.datacall, self, "data"),
            "frac":funcfloat(funcs.fractcall, self, "frac"),
            "simp":funcfloat(funcs.simpcall, self, "simp"),
            "d":funcfloat(funcs.randcall, self, "d"),
            "floor":usefunc(math.floor, self, "floor", ["x"]),
            "ceil":usefunc(math.ceil, self, "ceil", ["x"]),
            "log":usefunc(math.log10, self, "log", ["x"]),
            "ln":usefunc(math.log, self, "ln", ["x"]),
            "sqrt":usefunc(isqrt, self, "sqrt", ["x"]),
            "tan":usefunc(math.tan, self, "tan", ["x"]),
            "sin":usefunc(math.sin, self, "sin", ["x"]),
            "cos":usefunc(math.cos, self, "cos", ["x"]),
            "atan":usefunc(math.atan, self, "atan", ["x"]),
            "asin":usefunc(math.asin, self, "asin", ["x"]),
            "acos":usefunc(math.acos, self, "acos", ["x"]),
            "deg":usefunc(math.degrees, self, "deg", ["x"]),
            "rad":usefunc(math.radians, self, "rad", ["x"]),
            "fact":usefunc(factorial, self, "fact", ["x"]),
            "normdist":usefunc(normdist, self, "normdist", ["x", "mean", "stdev"]),
            "binomP":usefunc(binomP, self, "binomP", ["n", "p", "x"]),
            "poissonP":usefunc(poissonP, self, "poissonP", ["lambda", "x"]),
            "hypgeoP":usefunc(hypgeoP, self, "hypgeoP", ["x", "n", "K", "N"]),
            "tdist":usefunc(tdist, self, "tdist", ["x", "df"]),
            "teq":usefunc(teq, self, "teq", ["df"], {"e":self}),
            "chisqdist":usefunc(chisqdist, self, "chisqdist", ["x", "df"]),
            "chisqeq":usefunc(chisqeq, self, "chisqeq", ["df"], {"e":self}),
            "Fdist":usefunc(Fdist, self, "Fdist", ["x", "dfT", "dfE"]),
            "Feq":usefunc(Feq, self, "Feq", ["dfT", "dfE"], {"e":self}),
            "normP":usefunc(normP, self, "normP", ["x", "y", "mean", "stdev"]),
            "tP":usefunc(tP, self, "tP", ["x", "y", "df"], {"e":self}),
            "chisqP":usefunc(chisqP, self, "chisqP", ["x", "df"], {"e":self}),
            "FP":usefunc(FP, self, "FP", ["x", "dfT", "dfE"], {"e":self}),
            "gamma":usefunc(gamma, self, "gamma", ["x"]),
            "gcd":usefunc(gcd, self, "gcd", ["x", "y"]),
            "lcm":usefunc(lcm, self, "lcm", ["x", "y"]),
            "perm":usefunc(perm, self, "perm", ["n", "k"]),
            "comb":usefunc(comb, self, "comb", ["n", "k"]),
            "i":complex(0.0, 1.0),
            "e":math.e,
            "pi":math.pi,
            "none":matrix(0),
            "true":1.0,
            "false":0.0,
            "D"+self.varname:"D",
            self.defprefix*2:matrix(0),
            self.defprefix+funcfloat.allargs:matrix(0),
            self.defprefix+self.varname:matrix(0),
            self.defprefix+self.lastname:matrix(0)
            }
        if variables != None:
            self.makevars(variables)
        self.calls = [
            self.call_var,
            self.call_none,
            self.call_neg,
            self.call_reciproc,
            self.call_exp,
            self.call_lambda,
            self.call_colon,
            self.call_paren,
            self.call_method,
            self.call_normal
            ]
        self.count = 0

    def makevars(self, variables):
        """Forcibly Stores Variables."""
        for k,v in variables.items():
            self.variables[k] = v

    def setvars(self, newvars):
        """Sets New Variables."""
        oldvars = {}
        for k in newvars:
            oldvars[k] = haskey(self.variables, k)
        for k,v in newvars.items():
            if k != v:
                if v == None:
                    if k in self.variables:
                        del self.variables[k]
                        if self.debug:
                            print(self.recursion*"  "+": < "+self.prepare(k, False, True, True)+" >")
                else:
                    self.variables[k] = v
                    if self.debug:
                        print(self.recursion*"  "+": "+self.prepare(k, False, True, True)+" = "+self.prepare(v, False, True, True))
        return oldvars

    def store(self, name, value):
        """Stores A Variable."""
        if not self.isreserved(name):
            self.variables[basicformat(name)] = value
            return True
        else:
            return False

    def retrieve(self, name):
        """Retrieves A Variable."""
        return self.variables[basicformat(name)]

    def prepare(self, item, top=False, bottom=True, indebug=False):
        """Prepares The Output Of An Evaluation."""
        if isinstance(item, classcalc):
            out = "{"
            if top:
                out += "\n"
            for k,v in item.variables.items():
                out += " "+k+" = "+self.prepare(v, False, bottom)+" ;;"
                if top:
                    out += "\n"
            if len(item.variables) > 0:
                out = out[:-1*(3+top)]
                if top:
                    out += "\n"
            elif top:
                out = out[:-1]
            out += " }"
        elif isinstance(item, (data, multidata)):
            if bottom:
                out = "data:(" + self.prepare(getmatrix(item), False, True) + ")"
            else:
                out = self.prepare(getmatrix(item), top, bottom)
        elif isinstance(item, matrix):
            if len(item) == 0:
                out = "()"
            elif item.onlydiag():
                out = "("
                for x in item.getdiag():
                    out += self.prepare(x, False, bottom)+","
                if len(item) > 1:
                    out = out[:-1]
                out += ")"
            elif top or item.onlyrow():
                out = ""
                if not item.onlyrow():
                    out += "matrix:\n"
                for y in item.a:
                    if not item.onlyrow():
                        out += " "
                    out += "["
                    for x in y:
                        out += self.prepare(x, False, bottom)+","
                    out = out[:-1]+"]:\n"
                out = out[:-2]
            else:
                out = "matrix:["
                for y in item.a:
                    for x in y:
                        out += self.prepare(x, False, bottom)+","
                    out = out[:-1]+"]:["
                out = out[:-2]
        elif isinstance(item, (fraction, reciprocal)):
            out = ""
            a = self.prepare(item.n, False, bottom)
            if not bottom or madeof(a, string.digits) or not self.isreserved(test):
                out += a
            else:
                out += "("+a+")"
            out += "/"
            b = self.prepare(item.d, False, bottom)
            if not bottom or madeof(b, string.digits) or not self.isreserved(test):
                out += b
            else:
                out += "("+b+")"
        elif isinstance(item, bool):
            out = self.prepare(float(item), False, bottom)
        elif isinstance(item, complex):
            out = ""
            if item.real != 0:
                out += self.prepare(item.real, False, bottom)+"+"
            if item.imag == 1:
                out += "i"
            else:
                out += self.prepare(item.imag, False, bottom)+"*i"
        elif isnum(item):
            out = repr(item)
            if "e" in out:
                out = out.replace("+", "").replace("e", "*10^")
                if out.startswith("1*"):
                    out = out[2:]
            elif out.endswith(".0"):
                out = out[:-2]
            elif out.endswith("L"):
                out = out[:-1]
        elif bottom and isinstance(item, rollfunc):
            out = "d:"+self.prepare(item.stop, False, bottom)
        elif bottom and isinstance(item, strfunc):
            out = ""
            if isinstance(item, integbase):
                out += "S:"
            elif isinstance(item, derivbase):
                out += "D:"
            variables = item.getvars()
            personals = item.getpers()
            if len(variables) == 1 and len(personals) == 0:
                out += "\\"+variables[0]
            elif len(variables) > 1 or len(personals) > 0:
                out += "\\("+strlist(variables,",")
                if len(variables) != 0:
                    out += ","
                for x,y in personals.items():
                    out += str(x)+":("+self.prepare(y, False, bottom)+"),"
                out = out[:-1]+")"
            out += "\\"
            test = self.prepare(item.funcstr, False, bottom)
            if madeof(test, string.digits) or not self.isreserved(test):
                out += test
            else:
                out += "("+test+")"
            try:
                item.n
            except AttributeError:
                pass
            else:
                if item.n != 1:
                    out += ":"+str(item.n)
        elif bottom and isinstance(item, funcfloat):
            if isinstance(item, derivbase):
                if isinstance(item, integbase):
                    out = "S:"
                else:
                    out = "D:"
                out += self.prepare(item.func, False, bottom)
                try:
                    item.n
                except AttributeError:
                    pass
                else:
                    if item.n != 1:
                        out += ":"+str(item.n)
            else:
                out = "\\"+str(item)
        elif bottom and isinstance(item, strcalc):
            out = repr(item)
        elif istext(item) or isinstance(item, (funcfloat, strcalc)) or getcheck(item) >= 1:
            out = str(item)
        elif indebug:
            out = repr(item)
        else:
            self.processor.adderror("DisplayError", "Unable to display "+repr(item))
            out = "()"
        return str(out)

    def test(self, equation):
        """Evaluates A Boolean Expression."""
        if self.debug:
            self.info = " | test"
        return bool(self.calc(equation))

    def calc(self, expression):
        """Performs Full Evaluation On An Expression."""
        inputstring = self.prepare(expression, False, True)
        if self.debug:
            if self.info == "*":
                self.info = " <<"+"-"*(70-len(inputstring)-2*self.recursion)
            print(self.recursion*"  "+">>> "+inputstring+self.info)
            self.info = ""
        self.recursion += 1
        out = self.calc_top(inputstring)
        if self.debug:
            print(self.recursion*"  "+self.prepare(out, False, True, True)+" <<< "+inputstring)
        self.recursion -= 1
        return out

    def calc_top(self, expression):
        """Begins Calculation."""
        value = self.calc_paren(fullsplit(
                    self.calc_brack(fullsplit(
                        self.calc_class(fullsplit(
                            delspace(self.calc_string(expression)),
                        "{", "}", 1)),
                    "[", "]")),
                "(", ")"))
        if self.debug:
            print(self.recursion*"  "+"| "+self.prepare(value, False, True, True))
        return self.calc_with(value)

    def wrap(self, item):
        """Wraps An Item In Parentheses."""
        indexstr = "`"+str(self.count)+"`"
        self.count += 1
        self.variables[indexstr] = item
        return indexstr

    def calc_string(self, expression):
        """Evaluates The String Part Of An Expression."""
        strlist = expression.split('"')
        command = ""
        for x in xrange(0, len(strlist)):
            if x%2 == 0:
                command += strlist[x]
            else:
                command += self.wrap(strcalc(strlist[x], self))
        return command

    def calc_class(self, curlylist):
        """Evaluates The Curly Brackets In An Expression."""
        command = ""
        for x in curlylist:
            if istext(x):
                command += x
            else:
                indexstr = "`"+str(self.count)+"`"
                self.count += 1
                command += indexstr
                self.variables[indexstr] = classcalc(self)
                self.variables[indexstr].process(strlist(x))
        return command

    def calc_brack(self, bracklist):
        """Evaluates The Brackets In An Expression."""
        command = ""
        for x in bracklist:
            if istext(x):
                command += x
            else:
                command += "(L("+ self.calc_brack(x) +"))"
        return command

    def calc_paren(self, parenlist):
        """Evaluates The Parenthetical Part Of An Expression."""
        command = ""
        for x in parenlist:
            if istext(x):
                command += x
            else:
                command += self.wrap(self.calc_paren(x))
        return command

    def calc_with(self, expression):
        """Evaluates With Clauses."""
        inputlist = expression.split("$")
        if len(inputlist) == 1:
            return self.calc_pieces(inputlist[0])
        else:
            inputlist.reverse()
            item = inputlist.pop()
            withclass = classcalc(self)
            for x in inputlist:
                withclass.process(x, methods=False)
            return withclass.calc(item)

    def calc_pieces(self, expression):
        """Evaluates Piecewise Expressions."""
        for item in expression.split(";"):
            test = self.calc_condo(item)
            if not isnull(test):
                return test
        return matrix(0)

    def calc_condo(self, item):
        """Evaluates Conditions."""
        item = item.rsplit("@", 1)
        if len(item) == 1:
            return self.calc_check(item[0])
        elif bool(self.calc_bool(item[1])):
            return self.calc_condo(item[0])
        else:
            return matrix(0)

    def calc_check(self, inputlist):
        """Handles Booleans."""
        value = self.calc_bool(inputlist)
        if isinstance(value, bool):
            return float(value)
        else:
            return value

    def calc_bool(self, equation):
        """Evaluates The Expression Part Of A Boolean Expression."""
        top = equation.split("|")
        for a in xrange(0, len(top)):
            top[a] = top[a].split("&")
        if self.debug:
            value = reassemble(top, ["|", "&"])
            print(self.recursion*"  "+"=>> "+value)
        self.recursion += 1
        out = self.bool_or(top)
        if self.debug:
            print(self.recursion*"  "+self.prepare(out, False, True, True)+" <<= "+value)
        self.recursion -= 1
        return out

    def bool_or(self, inputlist):
        """Evaluates The Or Part Of A Boolean Expression."""
        value = self.bool_and(inputlist[0])
        for x in xrange(1, len(inputlist)):
            if value:
                break
            value = value or self.bool_and(inputlist[x])
        return value

    def bool_and(self, inputlist):
        """Evaluates The And Part Of A Boolean Expression."""
        value = self.bool_unary(inputlist[0])
        for x in xrange(1, len(inputlist)):
            if not value:
                break
            value = value and self.bool_unary(inputlist[x])
        return value

    def bool_unary(self, inputstring):
        """Evaluates The Unary Part Of A Boolean Expression."""
        if inputstring.startswith("!"):
            return not self.bool_unary(inputstring[1:])
        elif inputstring.startswith("?"):
            return bool(self.bool_unary(inputstring[1:]))
        else:
            return self.bool_eq(inputstring)

    def bool_eq(self, inputstring, place=16, bools="<>=!?"):
        """Evaluates The Equation Part Of A Boolean Expression."""
        inputlist = switchsplit(inputstring, bools)
        if len(inputlist) == 0:
            return matrix(0)
        elif len(inputlist) == 1:
            return self.calc_eval(inputlist[0])
        else:
            for x in xrange(0, len(inputlist)):
                if madeof(inputlist[x], bools):
                    args = []
                    if x == 0:
                        args.append(matrix(0))
                    else:
                        args.append(self.calc_eval(inputlist[x-1]))
                    if x == len(inputlist)-1:
                        args.append(matrix(0))
                    else:
                        args.append(self.calc_eval(inputlist[x+1]))
                    if madeof(inputlist[x], "!") or madeof(inputlist[x], "?"):
                        out = args[0] == args[1]
                    else:
                        out = False
                        if "=" in inputlist[x]:
                            out = out or args[0] == args[1]
                        if ">" in inputlist[x]:
                            out = out or args[0] > args[1]
                        if "<" in inputlist[x]:
                            out = out or args[0] < args[1]
                    for i in inputlist[x]:
                        if i == "!":
                            out = not out
                    if not out:
                        return False
            return True

    def calc_eval(self, expression):
        """Evaluates An Expression."""
        top = expression.split("~")
        for a in xrange(0, len(top)):
            top[a] = top[a].split("..")
            for b in xrange(0, len(top[a])):
                top[a][b] = top[a][b].split("**")
                for c in xrange(0, len(top[a][b])):
                    top[a][b][c] = top[a][b][c].split(",")
                    for d in xrange(0, len(top[a][b][c])):
                        top[a][b][c][d] = splitinplace(top[a][b][c][d].split("+"), "-", "%/*^:", 2)
                        for e in xrange(0, len(top[a][b][c][d])):
                            top[a][b][c][d][e] = top[a][b][c][d][e].split("%")
                            for f in xrange(0, len(top[a][b][c][d][e])):
                                top[a][b][c][d][e][f] = splitinplace(top[a][b][c][d][e][f].split("*"), "/")
        if self.debug:
            value = reassemble(top, ["~", "..", "**", ",", "+", "%", "*"])
            print(self.recursion*"  "+"=> "+value)
        self.recursion += 1
        out = self.eval_check(self.eval_comp(top), True)
        if self.debug:
            print(self.recursion*"  "+self.prepare(out, False, True, True)+" <= "+value)
        self.recursion -= 1
        return out

    def eval_comp(self, complist):
        """Performs List Comprehension."""
        if len(complist) == 1:
            return self.eval_join(complist[0])
        else:
            item = self.eval_join(complist.pop())
            if isinstance(item, strfunc):
                item.personals[self.lastname] = matrix(0)
            lists = []
            argnum = 1
            for x in reversed(xrange(0, len(complist))):
                if not delist(complist[x]):
                    argnum += 1
                else:
                    lists.append((self.eval_join(complist[x]), argnum))
                    argnum = 1
            return self.eval_comp_set(lists, [], item)

    def eval_comp_set(self, lists, args, func):
        """Performs Recursive Comprehension."""
        value, argnum = lists.pop()
        if hasmatrix(value):
            fromstring = isinstance(value, strcalc)
            value = getmatrix(value)
            units = value.getitems()
            new = []
            for x in xrange(0, len(units)/argnum):
                for y in xrange(0, argnum):
                    args.append(units[argnum*x+y])
                if len(lists) == 0:
                    if isfunc(func):
                        item = getcall(func)(args)
                    else:
                        item = func
                else:
                    item = self.eval_comp_set(lists[:], args, func)
                for y in xrange(0, argnum):
                    args.remove(units[argnum*x+y])
                if not isnull(item):
                    new.append(item)
                    if isinstance(func, strfunc):
                        func.personals[self.lastname] = item
            if fromstring:
                out = strcalc(strlist(new, "", converter=lambda x: self.prepare(x, True, False)), self)
            elif value.onlydiag():
                out = diagmatrixlist(new)
            else:
                out = value.new()
                i = 0
                for y,x in out.coords():
                    out.store(y,x, new[i])
                    i += 1
            return out
        else:
            args.append(value)
            if len(lists) == 0:
                if isfunc(func):
                    out = getcall(func)(args)
                else:
                    out = func
            else:
                out = self.eval_comp_set(lists, args, func)
            args.remove(value)
            if isinstance(func, strfunc) and not isnull(out):
                func.personals[self.lastname] = out
            return out

    def eval_join(self, inputlist):
        """Performs Concatenation."""
        items = []
        for item in inputlist:
            item = self.eval_repeat(item)
            if not isnull(item):
                items.append(item)
        if len(items) == 0:
            return matrix(0)
        elif len(items) == 1:
            return items[0]
        else:
            dostr = 0
            dolist = 0
            dobrack = 0
            dodata = 0
            domultidata = 0
            domatrix = 0
            rowlen = None
            tot = len(items)
            for x in items:
                if isinstance(x, strcalc):
                    dostr += 1
                elif isinstance(x, matrix):
                    dodata += 1
                    if rowlen == None:
                        rowlen = x.x
                    if x.x == rowlen:
                        domatrix += 1
                        if rowlen == 2:
                            domultidata += 1
                    if len(x) == 1:
                        dolist += 1
                        dobrack += 1
                    elif x.onlydiag():
                        dolist += 1
                    elif x.onlyrow():
                        dobrack += 1
                elif isinstance(x, multidata):
                    domultidata += 1
                elif isinstance(x, data):
                    dodata += 1
                else:
                    domatrix -= 1
                    domultidata -= 1
                    tot -= 1
            if dostr > 0:
                out = strcalc("", self)
                for x in items:
                    out += x
                return out
            elif dolist == tot:
                out = []
                for x in items:
                    if isinstance(x, matrix):
                        out += x.getdiag()
                    else:
                        out.append(x)
                return diagmatrixlist(out)
            elif dobrack == tot:
                out = []
                for x in items:
                    if isinstance(x, matrix):
                        out += x[0]
                    else:
                        out.append(x)
                return rowmatrixlist(out)
            elif domatrix == tot:
                out = []
                for x in items:
                    out += x.a
                return matrixlist(out, float)
            elif domultidata == tot:
                out = []
                for x in items:
                    if isinstance(x, matrix):
                        for l in x.a:
                            out.append((l[0], l[1]))
                    else:
                        out += x.items()
                return multidata(out)
            elif dodata == tot:
                out = []
                for x in items:
                    if isinstance(x, data):
                        out += x.items()
                    elif isinstance(x, matrix):
                        out += x.getitems()
                    else:
                        out.append(x)
                return data(out)
            else:
                raise TypeError("Could not concatenate items "+repr(items))

    def eval_repeat(self, inputlist):
        """Evaluates Repeats."""
        if len(inputlist) == 1:
            return self.eval_list(inputlist[0])
        else:
            out = self.eval_list(inputlist[0])
            if isinstance(out, matrix) and out.onlydiag():
                out = out.getitems()
            for x in xrange(1, len(inputlist)):
                num = getint(self.eval_list(inputlist[x]))
                if islist(out):
                    if num < 0:
                        out = out[::-1]*(-num)
                    else:
                        out *= num
                else:
                    out = [out]*abs(num)
            if islist(out):
                return diagmatrixlist(out)
            else:
                return out

    def eval_list(self, inputlist):
        """Evaluates Matrices."""
        out = []
        for x in xrange(0, len(inputlist)):
            item = self.eval_add(inputlist[x])
            if not isnull(item):
                out.append(item)
        if len(out) == 0:
            return matrix(0)
        elif len(out) == 1:
            if len(inputlist) > 1:
                return matrix(1,1, out[0], fake=True)
            else:
                return out[0]
        else:
            return diagmatrixlist(out)

    def eval_add(self, inputlist):
        """Evaluates The Addition Part Of An Expression."""
        if len(inputlist) == 0:
            return matrix(0)
        else:
            value = self.eval_mod(inputlist[0])
            for x in xrange(1, len(inputlist)):
                item = self.eval_mod(inputlist[x])
                if isnull(value):
                    value = item
                elif not isnull(item):
                    value += item
            return value

    def eval_mod(self, inputlist):
        """Evaluates The Modulus Part Of An Expression."""
        value = self.eval_mul(inputlist[0])
        for x in xrange(1, len(inputlist)):
            value %= self.eval_mul(inputlist[x])
        return value

    def eval_mul(self, inputlist):
        """Evaluates The Multiplication Part Of An Expression."""
        if len(inputlist) == 0:
            return matrix(0)
        else:
            value = self.eval_call(inputlist[0])
            for x in xrange(1, len(inputlist)):
                item = self.eval_call(inputlist[x])
                if isnull(value):
                    value = item
                elif not isnull(item):
                    value *= item
            return value

    def eval_call(self, inputstring):
        """Evaluates A Variable."""
        if self.debug:
            print(self.recursion*"  "+"-> "+inputstring)
        self.recursion += 1
        for func in self.calls:
            value = func(inputstring)
            if value != None:
                break
        out = self.eval_check(value)
        if self.debug:
            print(self.recursion*"  "+self.prepare(out, False, True, True)+" <- "+inputstring+" | "+namestr(func).split("_")[-1])
        self.recursion -= 1
        return out

    def eval_check(self, value, top=False):
        """Checks A Value."""
        if value == None:
            return matrix(0)
        elif top and isinstance(value, reciprocal):
            return value.calc()
        elif islist(value):
            return domatrixlist(value)
        else:
            check = getcheck(value)
            if check > 0:
                return value
            elif check == 0:
                if isinstance(value, complex):
                    if value.imag == 0.0:
                        return float(value.real)
                    else:
                        return value
                elif value >= 0 or value <= 0:
                    return float(value)
                else:
                    return matrix(0)
            elif hasreal(value):
                return self.eval_check(float(value))
            else:
                self.processor.adderror("VariableError", "Unable to process "+str(value))
                return matrix(0)

    def call_var(self, inputstring):
        """Checks If Variable."""
        if inputstring in self.variables:
            if self.defprefix+inputstring in self.variables:
                self.variables[self.defprefix] = self.call_var(self.defprefix+inputstring)
            item = self.find(inputstring, True, False)
            if istext(item):
                if self.debug:
                    self.info = " | var"
                value = self.calc(str(item))
            elif hasnum(item) or islist(item):
                value = item
            else:
                value = getcall(item)(None)
            return value
        elif self.defprefix+inputstring in self.variables:
            return self.call_var(self.defprefix+inputstring)

    def call_none(self, inputstring):
        """Evaluates A Null."""
        if inputstring == "":
            return matrix(0)

    def call_neg(self, inputstring):
        """Evaluates -."""
        if inputstring.startswith("-"):
            item = self.eval_call(inputstring[1:])
            if isnull(item):
                return -1.0
            else:
                return -1.0*item

    def call_reciproc(self, inputstring):
        """Evaluates /."""
        if inputstring.startswith("/"):
            item = self.eval_call(inputstring[1:])
            if isnull(item):
                return item
            else:
                return reciprocal(item)

    def call_exp(self, inputstring):
        """Evaluates The Exponential Part Of An Expression."""
        if "^" in inputstring:
            inputlist = inputstring.split("^")
            value = 1.0
            for x in reversed(xrange(0, len(inputlist))):
                value = self.eval_call(inputlist[x])**value
            return value

    def call_lambda(self, inputstring):
        """Evaluates Lambdas."""
        if inputstring.startswith("\\"):
            out = inputstring[1:].split("\\", 1)
            if len(out) == 1:
                test = self.find(out[0], True, False)
                if isinstance(test, funcfloat):
                    return test
                elif hascall(test):
                    return test.call(None)
                else:
                    while out[0].startswith("`") and out[0].endswith("`") and out[0] in self.variables and (istext(self.variables[out[0]]) or isinstance(self.variables[out[0]], strcalc)):
                        if isinstance(self.variables[out[0]], strcalc):
                            out[0] = repr(self.variables[out[0]])
                        else:
                            out[0] = str(self.variables[out[0]])
                return strfloat(out[0], self, check=False)
            elif out[0] == "":
                return strfloat(out[1], self, check=False)
            else:
                temp = self.namefind(out[0]).split(",")
                params = []
                personals = {}
                for x in temp:
                    if ":" in x:
                        x = x.split(":", 1)
                        personals[x[0]] = self.find(x[1], True, False)
                    elif x != "":
                        params.append(x)
                if out[1].startswith("\\"):
                    return strfloat(out[1][1:], self, params, personals, check=False)
                else:
                    while out[1].startswith("`") and out[1].endswith("`") and out[1] in self.variables and (istext(self.variables[out[1]]) or isinstance(self.variables[out[1]], strcalc)):
                        if isinstance(self.variables[out[1]], strcalc):
                            out[1] = repr(self.variables[out[1]])
                        else:
                            out[1] = str(self.variables[out[1]])
                    return strfloat(out[1], self, params, personals)

    def call_colon(self, inputstring):
        """Evaluates Colons."""
        if ":" in inputstring:
            inputlist = inputstring.split(":")
            if inputlist[0] == "":
                for x in xrange(1, len(inputlist)):
                    self.processor.process(self.prepare(self.eval_call(inputlist[x]), False, False))
                try:
                    self.processor.ans
                except AttributeError:
                    return matrix(0)
                else:
                    return self.processor.ans[-1]
            else:
                params = []
                for x in xrange(1, len(inputlist)):
                    params.append(self.eval_call(inputlist[x]))
                item = self.funcfind(inputlist[0])
                return self.call_colon_set(item, params)

    def call_colon_set(self, item, params):
        """Performs Colon Function Calls."""
        self.overflow = []
        docalc = False
        if isinstance(item, strcalc):
            item = item.calcstr
            if len(params) == 0:
                value = strcalc(item[-1], self)
            elif len(params) == 1:
                value = strcalc(item[int(params[0])], self)
            else:
                value = strcalc(item[int(params[0]):int(params[1])], self)
                self.overflow = params[2:]
        elif hasmatrix(item):
            item = getmatrix(item)
            if len(params) == 0:
                value = item.retrieve(0)
            elif len(params) == 1:
                if isinstance(params[0], matrix):
                    value = item.retrieve(int(params[0].retrieve(0)), int(params[0].retrieve(1)))
                elif item.onlyrow():
                    value = item.retrieve(0, int(params[0]))
                else:
                    value = item.retrieve(int(params[0]))
            elif isinstance(params[0], matrix) and isinstance(params[1], matrix):
                if params[0].retrieve(0) < 0:
                    params[0].store(0,0, params[0].retrieve(0)+item.y+1.0)
                if params[0].retrieve(1) < 0:
                    params[0].store(1,1, params[0].retrieve(1)+item.x+1.0)
                if params[1].retrieve(0) < 0:
                    params[1].store(0,0, params[1].retrieve(0)+item.y+1.0)
                if params[1].retrieve(1) < 0:
                    params[1].store(1,1, params[1].retrieve(1)+item.x+1.0)
                if params[0].getdiag() == params[1].getdiag():
                    value = matrix(1,1, item.retrieve(int(params[0].retrieve(0)), int(params[0].retrieve(1))), fake=True)
                elif params[0].retrieve(0) == params[1].retrieve(0):
                    out = item[int(params[0].retrieve(0))][int(params[0].retrieve(1)):int(params[1].retrieve(1))+1]
                    value = diagmatrixlist(out)
                elif params[0].retrieve(1) == params[1].retrieve(1):
                    item.flip()
                    out = item[int(params[0].retrieve(1))][int(params[0].retrieve(0)):int(params[1].retrieve(0))+1]
                    value = diagmatrixlist(out)
                else:
                    out = []
                    if params[0].retrieve(0) <= params[1].retrieve(0):
                        ymin, ymax = int(params[0].retrieve(0)), int(params[1].retrieve(0))
                    else:
                        ymin, ymax = int(params[1].retrieve(0)), int(params[0].retrieve(0))
                    if params[0].retrieve(1) <= params[1].retrieve(1):
                        xmin, xmax = int(params[0].retrieve(1)), int(params[1].retrieve(1))
                    else:
                        xmin, xmax = int(params[1].retrieve(1)), int(params[0].retrieve(1))
                    for y in xrange(ymin, ymax+1):
                        out.append([])
                        for x in xrange(xmin, xmax+1):
                            out[-1].append(item.retrieve(y,x))
                    value = matrixlist(out, float)
            else:
                length = item.lendiag()
                params[0] = float(params[0])
                params[1] = float(params[1])
                if params[0] < 0:                
                    params[0] += length+1.0
                if params[1] < 0:
                    params[1] += length+1.0
                if params[0] == params[1]:
                    value = matrix(1,1, item.retrieve(int(params[1])), fake=True)
                elif params[0] < params[1]:
                    out = item.getdiag()[int(params[0]):int(params[1])]
                    value = diagmatrixlist(out)
                else:
                    out = item.getdiag()[int(params[1]):int(params[0])]
                    out.reverse()
                    value = diagmatrixlist(out)
            self.overflow = params[2:]
        elif isfunc(item):
            value = getcall(item)(params)
        else:
            value = item
        while docalc or len(self.overflow) > 0:
            docalc = False
            temp = self.overflow[:]
            self.overflow = []
            value = self.call_colon_set(value, temp)
        return value

    def call_paren(self, inputstring):
        """Evaluates Parentheses."""
        inputstring = strlist(switchsplit(inputstring, string.digits, [x for x in string.printable if not self.isreserved(x)]), "``")
        if "`" in inputstring:
            if self.debug:
                print(self.recursion*"  "+"(|) "+inputstring) 
            templist = inputstring.split("`")
            inputlist = []
            for x in xrange(0, len(templist)):
                if x%2 == 1:
                    if templist[x]:
                        name = "`"+templist[x]+"`"
                        if not name in self.variables:
                            num = int(self.eval_call(templist[x]))
                            if num < 0:
                                num += self.count
                            name = "`"+str(num)+"`"
                        if name in self.variables:
                            inputlist.append(name)
                        else:
                            self.processor.adderror("VariableError", "Could not find parentheses "+name)
                else:
                    inputlist.append(templist[x])
            values = []
            for x in xrange(0, len(inputlist)):
                if x%2 == 1:
                    inputlist[x] = self.eval_call(inputlist[x])
                    if inputlist[x] == None:
                        raise ValueError("Nothing was returned as a result of evaluating "+inputlist[x])
                    elif islist(values[-1]):
                        funcs = [values[-1][0]]
                        for x in xrange(1, len(values[-1])):
                            try:
                                funcs[-1].__dict__
                            except AttributeError:
                                funcs[-1] = self.eval_check(funcs[-1])
                            if values[-1][x] in vars(funcs[-1]):
                                funcs[-1] = vars(funcs[-1])[values[-1][x]]
                            elif values[-1][x] in vars(type(funcs[-1])):
                                arg = funcs[-1]
                                func = vars(type(arg))[values[-1][x]]
                                funcs[-1] = lambda *args: func(arg, *args)
                            else:
                                funcs.append(self.funcfind(values[-1][x]))
                        if istext(funcs[-1]):
                            values[-1] = strcalc(funcs[-1], self)
                            if not isnull(inputlist[x]):
                                values[-1] *= inputlist[x]
                        elif isnum(funcs[-1]) or isinstance(funcs[-1], strcalc):
                            values[-1] = funcs[-1]
                            if not isnull(inputlist[x]):
                                values[-1] *= inputlist[x]
                        elif islist(funcs[-1]):
                            values[-1] = diagmatrixlist(funcs[-1])
                            if not isnull(inputlist[x]):
                                values[-1] *= inputlist[x]
                        else:
                            if isinstance(inputlist[x], matrix):
                                args = inputlist[x].getitems()
                            else:
                                args = [inputlist[x]]
                            if self.debug:
                                print(self.recursion*"  "+"||> ("+strlist(args,",",converter=lambda x: self.prepare(x, False, True, True))+") > "+strlist(funcs," > ",converter=lambda x: self.prepare(x, False, True, True)))
                                self.recursion += 1
                            values[-1] = callfuncs(funcs, *args)
                            if self.debug:
                                print(self.recursion*"  "+self.prepare(values[-1])+" <||")
                                self.recursion -= 1
                            if istext(values[-1]):
                                values[-1] = strcalc(values[-1], self)
                    else:
                        values.append(inputlist[x])
                elif inputlist[x] == "-":
                    values.append(-1.0)
                elif "." in inputlist[x]:
                    itemlist = inputlist[x].split(".")
                    isfloat = len(itemlist) < 3
                    for item in itemlist:
                        isfloat = isfloat and (not item or madeof(item, string.digits))
                    if not isfloat:
                        itemlist[0] = self.funcfind(itemlist[0] or values.pop())
                        if not isinstance(itemlist[0], classcalc):
                            values.append(itemlist)
                        elif len(itemlist) == 2:
                            values.append(itemlist[0].retrieve(itemlist[1]))
                        else:
                            values.append(strfunc("inputclass."+strlist(itemlist[2:], "."), self, ["inputclass"]).call([itemlist[0].retrieve(itemlist[1])]))
                    else:
                        values.append(self.find(inputlist[x], True, False))
                else:
                    values.append(self.find(inputlist[x], True, False))
            values = clean(values)
            for x in xrange(0, len(values)):
                if istext(values[x]):
                    if self.debug:
                        self.info = " (<)"
                    values[x] = self.calc(values[x])
            if self.debug:
                temp = strlist(values," < ",converter=lambda x: self.prepare(x, False, True, True))
                print(self.recursion*"  "+"(>) "+temp)
                self.recursion += 1
            value = (len(values) != 0 and values[0]) or matrix(0)
            for x in xrange(1, len(values)):
                values[x] = values[x]
                if not isfunc(value):
                    value *= values[x]
                elif isinstance(values[x], matrix) and values[x].onlydiag():
                    args = values[x].getdiag()
                    if isinstance(value, (strfunc, usefunc)) and value.overflow and len(args) > len(value.variables):
                        args = args[:len(value.variables)-1] + [diagmatrixlist(args[len(value.variables)-1:])]
                    value = getcall(value)(args)
                else:
                    value = getcall(value)([values[x]])
            if self.debug:
                print(self.recursion*"  "+self.prepare(value)+" (<) "+temp)
                self.recursion -= 1
            return value

    def call_method(self, inputstring):
        """Returns Method Instances."""
        if "." in inputstring:
            itemlist = inputstring.split(".")
            isfloat = len(itemlist) < 3
            for item in itemlist:
                isfloat = isfloat and (not item or madeof(item, string.digits))
            if not isfloat:
                itemlist[0] = self.funcfind(itemlist[0])
                if isinstance(itemlist[0], classcalc):
                    if len(itemlist) == 2:
                        return itemlist[0].retrieve(itemlist[1])
                    else:
                        return strfunc("inputclass."+strlist(itemlist[2:], "."), self, ["inputclass"]).call([itemlist[0].retrieve(itemlist[1])])
                elif not isnull(itemlist[0]):
                    return strfunc("firstfunc."+strlist(itemlist[1:], ".")+"("+funcfloat.allargs+")", self, [funcfloat.allargs], {"firstfunc":itemlist[0]})

    def call_normal(self, inputstring):
        """Returns Argument."""
        return inputstring

    def namefind(self, varname):
        """Finds A Name."""
        while varname.startswith("`") and varname.endswith("`"):
            num = int(self.eval_call(varname[1:-1]))
            if num < 0:
                num += self.count
            varname = str(self.variables["`"+str(num)+"`"])
        return varname

    def funcfind(self, item):
        """Finds A Value."""
        while istext(item):
            original = item
            if self.debug:
                print(self.recursion*"  "+"> "+self.prepare(original, False, True, True))
            self.recursion += 1
            if item in self.variables:
                item = self.variables[item]
            else:
                if self.debug:
                    self.info = " >"
                item = self.calc(item)
            if self.debug:
                print(self.recursion*"  "+self.prepare(item, False, True, True)+" < "+self.prepare(original, False, True, True))
            self.recursion -= 1
        return item

    def find(self, key, follow=False, destroy=False):
        """Finds A String."""
        old = ""
        new = basicformat(key)
        while old != new:
            old = new
            new = self.finding(old, follow, destroy)
        return new

    def finding(self, key, follow=False, destroy=False):
        """Performs String Finding."""
        out = key
        if key in self.variables:
            if follow or istext(self.variables[key]) or (destroy and isinstance(self.variables[key], strcalc)):
                out = self.variables[key]
        if destroy and isinstance(out, strcalc):
            out = str(out)
        return out

    def condense(self):
        """Simplifies Variable Hierarchies."""
        for x in self.variables:
            self.variables[x] = self.find(x, True, False)

    def isreserved(self, expression, extra="", allowed=""):
        """Determines If An Expression Contains Reserved Characters."""
        if expression == "":
            return True
        for x in expression:
            if x in delspace(self.reserved, allowed)+extra:
                return True
        return False

    def call(self, item, value, varname=None):
        """Evaluates An Item With A Value."""
        if isnull(item):
            return None
        if varname == None:
            varname = self.varname
        if istext(item):
            old = self.variables[varname]
            self.variables[varname] = value
            out = self.calc(item)
            self.variables[varname] = old
        elif isfunc(item):
            out = getcall(item)(varproc(value))
        elif hasnum(item):
            return item
        else:
            old = self.variables[varname]
            self.variables[varname] = value
            out = getcall(item)(None)
            self.variables[varname] = old
        return self.call(out, value, varname)

class evalfuncs(object):
    """Implements Evaluator Functions."""
    def __init__(self, e):
        """Initializes The Functions."""
        self.e = e

    def brackcall(self, variables):
        """Evaluates Brackets."""
        if variables == None:
            return matrix(0)
        else:
            return rowmatrixlist(variables)

    def copycall(self, variables):
        """Makes Copies Of Items."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            if iseval(variables[0]):
                return variables[0].copy()
            else:
                return variables[0]
        else:
            out = []
            for x in variables:
                out.append(self.copycall([x]))
            return diagmatrixlist(out)

    def getmatrixcall(self, variables):
        """Converts To Matrices."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return getmatrix(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.getmatrixcall([x]))
            return diagmatrixlist(out)

    def matrixcall(self, variables):
        """Constructs A Matrix."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            tomatrix = []
            for x in variables:
                if isinstance(x, matrix):
                    tomatrix.append(x.getitems())
                elif hasnum(x):
                    tomatrix.append([x])
                else:
                    tomatrix.append(x)
            return matrixlist(tomatrix, float)

    def detcall(self, variables):
        """Returns The Determinant Of The Matrix."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1 and isinstance(variables[0], matrix):
            return variables[0].det()
        else:
            value = 1.0
            for v in variables:
                value *= v
            return value

    def listcall(self, variables):
        """Constructs A Matrix List."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            if isinstance(variables[0], matrix):
                if variables[0].onlyrow():
                    return diagmatrixlist(variables[0].items())
                else:
                    return variables[0]
            elif hasmatrix(variables[0]):
                return getmatrix(variables[0])
            else:
                return matrix(1,1, variables[0], fake=True)
        else:
            return diagmatrixlist(variables)

    def sumcall(self, variables):
        """Finds A Sum."""
        if variables == None:
            return matrix(0)
        else:
            value = 0.0
            for x in variables:
                x = collapse(x)
                if ismatrix(x):
                    value += self.sumcall(getmatrix(x).items())
                else:
                    value += x
            return value

    def prodcall(self, variables):
        """Finds A Product."""
        if variables == None:
            return matrix(0)
        else:
            value = 1.0
            for x in variables:
                x = collapse(x)
                if ismatrix(x):
                    value *= self.prodcall(getmatrix(x).getitems())
                else:
                    value *= x
            return value

    def joincall(self, variables):
        """Joins Variables."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            if isinstance(variables[0], matrix):
                keep = True
                for i in xrange(1, len(variables)):
                    if not (isinstance(variables[i], matrix) and (variables[i].x == variables[0].x or variables[i].getlen() == variables[0].x)):
                        keep = False
                        break
            else:
                keep = False
            if keep:
                for i in xrange(1, len(variables)):
                    if variables[i].onlydiag():
                        variables[0].newrow(variables[i].getitems())
                    else:
                        for row in variables[i].a:
                            variables[0].newrow(row)
                return variables[0]
            else:
                out = []
                for i in variables:
                    if ismatrix(i):
                        out += getmatrix(i).getitems()
                    else:
                        out.append(i)
                return diagmatrixlist(out)

    def findcall(self, variables):
        """Finds Equivalencies."""
        if variables != None and len(variables) >= 2:
            variables[1] = getmatrix(variables[1])
            if variables[1].onlydiag():
                for x in xrange(0, variables[1].lendiag()):
                    if variables[1].retrieve(x) == variables[0]:
                        return float(x)
            else:
                for x,y in variables[1].coords():
                    if variables[1].retrieve(x,y) == variables[0]:
                            return diagmatrixlist([float(x),float(y)])
        return matrix(0)

    def mergecall(self, variables):
        """Merges Variables."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            return diagmatrixlist(merge(variables))

    def sizecall(self, variables):
        """Finds A Size."""
        if variables == None:
            return matrix(0)
        else:
            return totlen(diagmatrixlist(variables))

    def lencall(self, variables):
        """Finds A Length."""
        if variables == None:
            return matrix(0)
        else:
            tot = 0.0
            for x in variables:
                if isinstance(x, matrix):
                    tot += x.getlen()
                elif isinstance(x, (strcalc, data, multidata)):
                    tot += len(x)
                else:
                    tot += 1.0
            return tot

    def rangecall(self, variables):
        """Constructs A Range."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return rangematrix(0.0, collapse(variables[0]))
        elif len(variables) == 2:
            return rangematrix(collapse(variables[0]), collapse(variables[1]))
        else:
            return rangematrix(collapse(variables[0]), collapse(variables[1]), collapse(variables[2]))

    def roundcall(self, variables):
        """Performs round."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 0:
            return 0.0
        elif len(variables) == 1:
            return round(getnum(variables[0]))
        else:
            return round(getnum(variables[0]), getint(variables[1]))

    def numcall(self, variables):
        """Performs float."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 0:
            return 0.0
        elif len(variables) == 1:
            if ismatrix(variables[0]):
                variables[0].code(lambda x: getnum(x))
                return variables[0]
            else:
                return getnum(variables[0])
        else:
            return self.numcall([diagmatrixlist(variables)])

    def splitcall(self, variables):
        """Performs split."""
        if variables == None:
            return matrix(0)
        else:
            variables[0] = collapse(variables[0])
            items = []
            for x in xrange(1, len(variables)):
                items.append(collapse(variables[x]))
            if isinstance(variables[0], strcalc):
                out = self.splitcall([getmatrix(variables[0])]+items)
                if isinstance(out, matrix) and out.onlydiag():
                    new = []
                    for x in out.getitems():
                        if isinstance(x, matrix) and x.onlydiag():
                            temp = ""
                            for y in x.getitems():
                                temp += self.e.prepare(y, True, False)
                            new.append(strcalc(temp, self))
                        else:
                            new.append(x)
                    return new
                else:
                    return out
            elif hasmatrix(variables[0]):
                out = [[]]
                for x in getmatrix(variables[0]).getitems():
                    if x in items:
                        out.append([])
                    else:
                        out[-1].append(x)
                return diagmatrixlist(out)
            elif variables[0] in items:
                return matrix(0)
            else:
                return variables[0]

    def replacecall(self, variables):
        """Performs replace."""
        if variables == None:
            return matrix(0)
        else:
            variables[0] = collapse(variables[0])
            pairs = {}
            for x in xrange(1, len(variables)):
                if x%2 == 1:
                    temp = collapse(variables[x])
                else:
                    pairs[temp] = variables[x]
            if isinstance(variables[0], strcalc):
                items = [getmatrix(variables[0])]
                for k,v in pairs.items():
                    items.append(k)
                    items.append(v)
                out = self.replacecall(items)
                if isinstance(out, matrix) and out.onlydiag():
                    new = ""
                    for x in out.getitems():
                        new += self.e.prepare(x, True, False)
                    return strcalc(new, self)
                else:
                    return out
            elif ismatrix(variables[0]):
                variables[0] = getmatrix(variables[0])
                keys = []
                values = []
                for k,v in pairs.items():
                    keys.append(k)
                    values.append(v)
                if variables[0].onlydiag():
                    for x in xrange(0, variables[0].lendiag()):
                        temp = variables[0].retrieve(x)
                        if temp in keys:
                            variables[0].store(x,x, values[keys.index(temp)])
                else:
                    for y,x in variables[0].coords():
                        temp = variables[0].retrieve(y,x)
                        if temp in keys:
                            variables[0].store(y,x, values[keys.index(temp)])
            else:
                while variables[0] in pairs:
                    variables[0] = pairs[variables[0]]
            return variables[0]

    def sortcall(self, variables):
        """Performs sort."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            if isinstance(variables[0], data):
                variables[0].sort()
                return variables[0]
            elif isinstance(variables[0], multidata):
                items = variables[0].items()
                items.sort()
                outx, outy = [], []
                for x,y in items:
                    outx.append(x)
                    outy.append(y)
                return multidata(outx, outy)
            elif not isinstance(variables[0], matrix):
                return matrix(1,1, variables[0], fake=True)
            elif variables[0].onlydiag():
                out = variables[0].getdiag()
                out.sort()
                return diagmatrixlist(out)
            else:
                out = variables[0].items()
                out.sort()
                return matrixitems(out)
        else:
            return self.sortcall([self.mergecall(variables)])

    def reversecall(self, variables):
        """Performs reverse."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            variables[0] = getmatrix(collapse(variables[0]))
            if variables[0].onlydiag():
                out = variables[0].getdiag()
                out.reverse()
                return diagmatrixlist(out)
            else:
                out = variables[0].items()
                out.reverse()
                return matrixitems(out, variables[0].y)
        else:
            return self.reversecall([self.joincall(variables)])

    def containscall(self, variables):
        """Performs contains."""
        if variables == None:
            return matrix(0)
        elif len(variables) > 1:
            variables[0] = collapse(variables[0])
            if isinstance(variables[0], (matrix, strcalc, data, multidata)):
                for x in xrange(1, len(variables)):
                    if collapse(variables[x]) in variables[0]:
                        return 1.0
            else:
                for x in xrange(1, len(variables)):
                    if collapse(variables[x]) == variables[0]:
                        return 1.0
        return 0.0

    def collapsecall(self, variables):
        """Collapses Float Strings."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            while isinstance(variables[0], funcfloat):
                variables[0] = collapse(variables[0])
            return variables[0]
        else:
            out = []
            for x in variables:
                out.append(collapsecall([x]))
            return diagmatrixlist(out)

    def typecall(self, variables):
        """Finds Types."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 0:
            return self.typecalc(matrix(0))
        elif len(variables) == 1:
            return self.typecalc(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.typecalc(x))
            return diagmatrixlist(out)

    def tocall(self, variables, varstrings="xyzwpqrabchjklmnABCFGHJKMNOQRTUVWXYZ"):
        """Returns A Converter Function."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            if isinstance(variables[0], (strcalc, funcfloat)):
                variables[0] = self.typestr(variables[0])
                if variables[0] in self.e.variables and isinstance(self.e.variables[variables[0]], funcfloat):
                    return self.e.variables[variables[0]]
                elif variables[0] in self.e.variables and (istext(variables[0]) or isnum(variables[0]) or isinstance(self.e.variables[variables[0]], bool) or (iseval(value) and not hascall(value))):
                    return strfloat(variables[0], self.e, [])
                else:
                    return strfloat(variables[0]+":x", self.e, ["x"])
            elif isinstance(variables[0], matrix):
                funcs = []
                for t in variables[0].getitems():
                    funcs.append(self.typestr(t))
                args = []
                for x in xrange(1, len(funcs)+1):
                    varstring = ""
                    while x > len(varstrings):
                        varstring += varstrings[x%len(varstrings)-1]
                        x /= len(varstrings)
                    varstring += varstrings[x-1]
                    args.append(varstring)
                out = ""
                for x in xrange(0, len(funcs)):
                    out += funcs[x]+":"+args[x]+","
                if len(out) > 0:
                    out = out[:-1]
                return strfloat(out, self.e, args)
            else:
                raise ValueError("Unable to create a converter for "+repr(variables[0]))
        else:
            return self.tocall([diagmatrixlist(variables)])

    def typestr(self, item):
        """Processes A Type Identifier."""
        item = self.e.prepare(item, False, False)
        if item == "number":
            item = "num"
        elif item in ["list", "row", "matrix"]:
            item = "cont"
        elif item == "multidata":
            item = "data"
        elif item == "fraction":
            item = "frac"
        elif item == "string":
            item = "str"
        return item

    def typecalc(self, item):
        """Finds A Type."""
        if isinstance(item, classcalc):
            return strcalc("class")
        elif isinstance(item, data):
            return strcalc("data")
        elif isinstance(item, multidata):
            return strcalc("multidata")
        elif isinstance(item, matrix):
            if len(item) == 0:
                return strcalc("none", self.e)
            elif item.onlydiag():
                return strcalc("list", self.e)
            elif item.onlyrow():
                return strcalc("row", self.e)
            else:
                return strcalc("matrix", self.e)
        elif isinstance(item, fraction):
            return strcalc("fraction", self.e)
        elif isinstance(item, strcalc):
            return strcalc("string", self.e)
        elif isinstance(item, funcfloat):
            return strcalc("function", self.e)
        elif isinstance(item, complex):
            return strcalc("complex", self.e)
        elif isnum(item):
            return strcalc("number", self.e)
        else:
            return strcalc(namestr(item), self.e)

    def strcall(self, variables):
        """Finds A String."""
        if variables == None:
            return matrix(0)
        else:
            out = ""
            for x in variables:
                if isinstance(x, strcalc):
                    out += str(x)
                elif ismatrix(x):
                    out += self.strcall(getmatrix(x).getitems())
                else:
                    out += self.e.prepare(x, True, False)
            return strcalc(out, self.e)

    def reprcall(self, variables):
        """Finds A Representation."""
        if variables == None:
            return matrix(0)
        else:
            out = ""
            for x in variables:
                if ismatrix(x):
                    out += self.reprcall(getmatrix(x).getitems())
                else:
                    out += self.e.prepare(x, False, True)
            return strcalc(out, self.e)

    def abscall(self, variables):
        """Performs abs."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 1:
            return abs(variables[0])
        else:
            return self.abscall([diagmatrixlist(variables)])

    def datacall(self, variables):
        """Performs data."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 1 and isinstance(variables[0], data):
            return variables[0]
        elif len(variables) == 1:
            return datamatrix(variables[0])
        elif len(variables) == 2 and isinstance(variables[0], data) and isinstance(variables[1], data):
            return multidata(variables[0], variables[1])
        elif len(variables) == 2 and ismatrix(variables[0]) and ismatrix(variables[1]):
            return multidata(getmatrix(variables[0]).getitems(), getmatrix(variables[1]).getitems())
        else:
            return self.datacall([diagmatrixlist(variables)])

    def fractcall(self, variables, dosimp=False):
        """Performs frac."""
        if variables == None:
            return matrix(0)
        elif len(variables) == 0:
            return fraction()
        elif len(variables) == 1:
            if isinstance(variables[0], fraction):
                out = variables[0]
            elif isnum(variables[0]):
                out = fractionfloat(variables[0])
            else:
                out = fraction(variables[0])
        else:
            out = self.fractcall([variables[0]])
            for x in xrange(1, len(variables)):
                out /= self.fractcall([variables[x]])
        if dosimp or (isnum(out.n) and isnum(out.d)):
            out.simptens()
        return out

    def simpcall(self, variables):
        """Simplifies Fractions."""
        if variables == None:
            return matrix(0)
        else:
            out = self.fractcall(variables, True)
            out.simplify()
        return out

    def docalc(self, variables):
        """Performs calc."""
        if variables == None:
            return matrix(0)
        else:
            out = []
            for x in variables:
                out.append(self.e.calc(self.e.prepare(x, False, False)))
            if len(out) == 1:
                return out[0]
            else:
                return diagmatrixlist(out)

    def foldcall(self, variables, func=None, overflow=True):
        """Folds A Function Over A Matrix."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        elif len(variables) == 1:
            return getcall(self.e.funcfind(variables[0]))(self.e.variables)
        else:
            func = func or getcall(self.e.funcfind(variables[0]))
            item = collapse(variables[1])
            if len(variables) >= 3:
                start = variables[2]
                if overflow:
                    self.e.overflow = variables[3:]
            else:
                start = None
            if isinstance(variables[0], strcalc):
                variables[0] = None
                variables[1] = item
                variables = variables[:3]
                return self.strcall([self.foldcall(variables, func, False)])
            elif hasmatrix(item):
                item = getmatrix(item)
                if len(item) == 0:
                    return matrix(0)
                else:
                    items = item.getitems()
                    if start == None:
                        start = items.pop(0)
                    for x in items:
                        start = func([start, x])
                    return start
            elif start != None:
                return func([start, item])
            else:
                return item

    def derivcall(self, variables):
        """Returns The nth Derivative Of A Function."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            n = 1
            varname = self.e.varname
            accuracy = 0.0001
            scaledown = 1.25
            func = variables[0]
            if len(variables) > 1:
                n = int(variables[1])
            if len(variables) > 2:
                varname = self.e.prepare(variables[2], False, False)
            if len(variables) > 3:
                accuracy = float(variables[3])
            if len(variables) > 4:
                scaledown = float(variables[4])
                self.e.overflow = variables[5:]
            if isinstance(func, strfunc):
                if len(func.variables) == 0:
                    return derivfunc(func.funcstr, n, accuracy, scaledown, self.e, varname, func.personals)
                else:
                    return derivfunc(func.funcstr, n, accuracy, scaledown, self.e, func.variables[0], func.personals)
            elif isinstance(func, funcfloat):
                return derivfuncfloat(func, n, accuracy, scaledown, self.e)
            else:
                return derivfunc(str(func), n, accuracy, scaledown, self.e, varname)

    def integcall(self, variables):
        """Returns The Integral Of A Function."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            varname = self.e.varname
            accuracy = 0.0001
            func = variables[0]
            if len(variables) > 1:
                varname = self.e.prepare(variables[1], False, False)
            if len(variables) > 2:
                accuracy = float(variables[2])
                self.e.overflow = variables[3:]
            if isinstance(func, strfunc):
                if len(func.variables) == 0:
                    return integfunc(func.funcstr, accuracy, self.e, varname, func.personals)
                else:
                    return integfunc(func.funcstr, accuracy, self.e, func.variables[0], func.personals)
            elif isinstance(func, funcfloat):
                return integfuncfloat(func, accuracy, self.e)
            else:
                return integfunc(str(func), accuracy, self.e, varname)

    def randcall(self, variables):
        """Returns A Random Number Generator Object."""
        if variables == None or len(variables) == 0:
            return matrix(0)
        else:
            stop = getnum(variables[0])
            key = None
            if len(variables) > 1:
                key = self.e.prepare(variables[1], True, False)
                self.e.overflow = variables[2:]
            return rollfunc(stop, self.e, key)
