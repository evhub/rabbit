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

from .data import *
from .fraction import *
from .carrot.file import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class evaluator(object):
    """Evaluates Equations And Expressions.

Global Operator Precedence List:
    ;;      Separates top-level commands.
    ::      Calls a meta-function.

    "       Opens and closes strings.
    `       Opens and closes raw strings.
    {}      Opens and closes classes.
    []      Opens and closes matrix rows.
    ()      Opens and closes parentheses.

    $       Seperates with clauses (read as 'with' or 'where').
    ;       Seperates conditionals (read as 'else').
    @       Checks a conditional (read as 'at' or 'if').

    |       Performs logical 'or'.
    &       Performs logical 'and'.
    >?!=<   Performs equality or inequality checks.

    ~       Applies a list to a function for looping.
    \\       Creates a lambda.
    ++      Performs concatenation.
    --      Performs removal.
    **      Performs repeat.
    ,       Seperates list elements.
    +-      Performs addition and subtraction.
    %       Performs modulo.
    */      Performs multiplication and division.

    \\       Denotes a lambda.
    -       Denotes negatives.
    /       Denotes reciprocals.
    ^       Performs exponentiation.
    :       Performs function calls.
    \xa7       Denotes parentheses.
    ..      Performs function composition.
    .       Denotes methods and functions of functions.
    normal  Evaluates numbers."""
    varname = "x"
    parenchar = "\xa7"
    aliases = {
        "\t":"    ",
        "\xac":"!",
        "\xf7":"/",
        "\xd7":"*",
        "\u2219":"*",
        "\u22c5":"*",
        "\u2264":"<=",
        "\u2265":">=",
        "\u2227":"&",
        "\u2228":"|",
        "\u22c0":"&",
        "\u22c1":"|",
        "\u2212":"-",
        "\u2215":"/",
        "\u2044":"/"
        }
    groupers = {
        "(":")",
        "{":"}",
        "[":"]"
        }
    unary = "!?"
    bools = unary + "<>=\u2260"
    callops = "%/*^:\\"
    multiargops = bools + callops + "+-@~|&;.,$\u201c" + "".join(groupers.keys()) + "".join(aliases.keys())
    reserved = string.digits + multiargops + '")]}`\u201d' + "".join(groupers.values()) + parenchar
    errorvar = "__error__"
    fatalvar = "__fatal__"
    namevar = "name"
    messagevar = "message"
    debuglog = []
    recursion = 0
    overflow = []
    laxnull = True
    redef = False
    useclass = None
    returned = True
    spawned = True
    calculated = None

    def __init__(self, variables=None, processor=None, color=None, speedy=False, maxrecursion=10):
        """Initializes The Evaluator."""
        self.processor = processor
        try:
            self.processor.debug
        except AttributeError:
            self.debug = False
        else:
            self.debug = self.processor.debug
        self.speedy = bool(speedy)
        self.maxrecursion = int(maxrecursion)
        self.color = color
        self.funcs = evalfuncs(self)
        self.fresh()
        if variables is not None:
            self.makevars(variables)
        self.tops = [
            self.top_string,
            self.top_paren,
            self.top_class,
            self.top_brack
            ]
        self.pre_calcs = [
            self.pre_with,
            self.pre_set
            ]
        self.set_calcs = [
            self.set_def,
            self.set_normal
            ]
        self.calls = [
            self.call_var,
            self.call_parenvar,
            self.call_none,
            self.call_lambda,
            self.call_neg,
            self.call_reciproc,
            self.call_exp,
            self.call_colon,
            self.call_paren,
            self.call_comp,
            self.call_lambdacoeff,
            self.call_method,
            self.call_normal
            ]

    def new(self):
        """Makes A New Identically-Configured Evaluator."""
        return evaluator(None, self.processor, self.color, self.speedy, self.maxrecursion)

    def fresh(self):
        """Resets The Variables To Their Defaults."""
        self.parens = []
        self.variables = {
            "warning":classcalc(self, {
                self.errorvar: 1.0,
                self.fatalvar: 0.0
                }),
            "error":classcalc(self, {
                self.errorvar: 1.0,
                self.fatalvar: 1.0
                }),
            "env":funcfloat(self.funcs.envcall, self, "env"),
            "copy":funcfloat(self.funcs.copycall, self, "copy"),
            "type":funcfloat(self.funcs.typecall, self, "type"),
            "to":funcfloat(self.funcs.tocall, self, "to"),
            "str":funcfloat(self.funcs.strcall, self, "str"),
            "repr":funcfloat(self.funcs.reprcall, self, "repr"),
            "code":funcfloat(self.funcs.codecall, self, "code"),
            "calc":funcfloat(self.funcs.docalc, self, "calc"),
            "proc":funcfloat(self.funcs.cmdcall, self, "proc"),
            "fold":funcfloat(self.funcs.foldcall, self, "fold"),
            "row":funcfloat(rowmatrixlist, self, "row"),
            "list":funcfloat(self.funcs.listcall, self, "list"),
            "matrix":funcfloat(self.funcs.matrixcall, self, "matrix"),
            "cont":funcfloat(self.funcs.getmatrixcall, self, "cont"),
            "sum":funcfloat(self.funcs.sumcall, self, "sum"),
            "prod":funcfloat(self.funcs.prodcall, self, "prod"),
            "join":funcfloat(self.funcs.joincall, self, "join"),
            "connect":funcfloat(self.funcs.connectcall, self, "connect"),
            "merge":funcfloat(self.funcs.mergecall, self, "merge"),
            "sort":funcfloat(self.funcs.sortcall, self, "sort"),
            "rev":funcfloat(self.funcs.reversecall, self, "rev"),
            "round":funcfloat(self.funcs.roundcall, self, "round"),
            "num":funcfloat(self.funcs.numcall, self, "num"),
            "int":funcfloat(self.funcs.intcall, self, "int"),
            "eval":funcfloat(self.funcs.evalcall, self, "eval"),
            "find":funcfloat(self.funcs.findcall, self, "find"),
            "split":funcfloat(self.funcs.splitcall, self, "split"),
            "replace":funcfloat(self.funcs.replacecall, self, "replace"),
            "in":funcfloat(self.funcs.containscall, self, "in"),
            "range":funcfloat(self.funcs.rangecall, self, "range"),
            "len":funcfloat(self.funcs.lencall, self, "len"),
            "size":funcfloat(self.funcs.sizecall, self, "size"),
            "abs":funcfloat(self.funcs.abscall, self, "abs"),
            "d":funcfloat(self.funcs.randcall, self, "d"),
            "from":funcfloat(self.funcs.instanceofcall, self, "from"),
            "iserr":funcfloat(self.funcs.iserrcall, self, "iserr"),
            "class":funcfloat(self.funcs.classcall, self, "class"),
            "var":funcfloat(self.funcs.getvarcall, self, "var"),
            "val":funcfloat(self.funcs.getvalcall, self, "val"),
            "paren":funcfloat(self.funcs.getparenvarcall, self, "paren"),
            "parens":funcfloat(self.funcs.getparenscall, self, "parens"),
            "raise":funcfloat(self.funcs.raisecall, self, "raise"),
            "except":funcfloat(self.funcs.exceptcall, self, "except"),
            "real":funcfloat(self.funcs.realcall, self, "real"),
            "imag":funcfloat(self.funcs.imagcall, self, "imag"),
            "read":funcfloat(self.funcs.readcall, self, "read"),
            "write":funcfloat(self.funcs.writecall, self, "write"),
            "is":funcfloat(self.funcs.iseqcall, self, "is", reqargs=2),
            "include":funcfloat(self.funcs.includecall, self, "include"),
            "del":funcfloat(self.funcs.delcall, self, "del"),
            "def":funcfloat(self.funcs.defcall, self, "def"),
            "global":funcfloat(self.funcs.globalcall, self, "global"),
            "alias":funcfloat(self.funcs.aliascall, self, "alias"),
            "effect":usefunc(self.setreturned, self, "effect"),
            "pow":usefunc(pow, self, "pow", ["y", "x", "m"]),
            "E":usefunc(E10, self, "E", ["x"]),
            "D":funcfloat(self.funcs.derivcall, self, "D"),
            "S":funcfloat(self.funcs.integcall, self, "S"),
            "data":funcfloat(self.funcs.datacall, self, "data"),
            "frac":funcfloat(self.funcs.fractcall, self, "frac"),
            "simp":funcfloat(self.funcs.simpcall, self, "simp"),
            "det":funcfloat(self.funcs.detcall, self, "det"),
            "math":classcalc(self, {
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
                "gamma":usefunc(gamma, self, "gamma", ["x"]),
                "gcd":usefunc(gcd, self, "gcd", ["x", "y"]),
                "lcm":usefunc(lcm, self, "lcm", ["x", "y"]),
                "perm":usefunc(perm, self, "perm", ["n", "k"]),
                "comb":usefunc(comb, self, "comb", ["n", "k"]),
                "succ":usefunc(succ, self, "'", ["x"]),
                "e":math.e,
                "pi":math.pi
                }),
            "stats":classcalc(self, {
                "normdist":usefunc(normdist, self, "normdist", ["x", "mean", "stdev"]),
                "binomP":usefunc(binomP, self, "binomP", ["n", "p", "x"]),
                "poissonP":usefunc(poissonP, self, "poissonP", ["lambda", "x"]),
                "hypgeoP":usefunc(hypgeoP, self, "hypgeoP", ["x", "n", "K", "N"]),
                "tdist":usefunc(tdist, self, "tdist", ["x", "df"]),
                "teq":usefunc(teq, self, "teq", ["df"], evalinclude="e"),
                "chisqdist":usefunc(chisqdist, self, "chisqdist", ["x", "df"]),
                "chisqeq":usefunc(chisqeq, self, "chisqeq", ["df"], evalinclude="e"),
                "Fdist":usefunc(Fdist, self, "Fdist", ["x", "dfT", "dfE"]),
                "Feq":usefunc(Feq, self, "Feq", ["dfT", "dfE"], evalinclude="e"),
                "normP":usefunc(normP, self, "normP", ["x", "y", "mean", "stdev"]),
                "tP":usefunc(tP, self, "tP", ["x", "y", "df"], evalinclude="e"),
                "chisqP":usefunc(chisqP, self, "chisqP", ["x", "df"], evalinclude="e"),
                "FP":usefunc(FP, self, "FP", ["x", "dfT", "dfE"], evalinclude="e")
                }),
            "i":complex(0.0, 1.0),
            "none":matrix(0),
            "empty":rowmatrixlist([matrix(0)]),
            "true":1.0,
            "false":0.0,
            "_":atom(),
            funcfloat.allargs : matrix(0),
            "\xf8" : "none",
            "\u221e" : "inf",
            "\u2211" : "sum",
            "\u03c0" : "math.pi",
            "\u221a" : "math.sqrt",
            "\u222b" : "math.S",
            "\u0393" : "math.gamma",
            "\u220f" : "math.prod",
            "\u2208" : "in",
            "\u230a" : "min",
            "\u2308" : "max",
            "\xb0" : "math.rad",
            "\xbd" : 0.5,
            "\xbc" : 0.25,
            "\xbe" : 0.75,
            "\u2400" : rawstrcalc("\x00", self),
            "\u2401" : rawstrcalc("\x01", self),
            "\u2402" : rawstrcalc("\x02", self),
            "\u2403" : rawstrcalc("\x03", self),
            "\u2404" : rawstrcalc("\x04", self),
            "\u2405" : rawstrcalc("\x05", self),
            "\u2406" : rawstrcalc("\x06", self),
            "\u2407" : rawstrcalc("\x07", self),
            "\u2408" : rawstrcalc("\x08", self),
            "\u2409" : rawstrcalc("\x09", self),
            "\u240a" : rawstrcalc("\n", self),
            "\u240b" : rawstrcalc("\x0b", self),
            "\u240c" : rawstrcalc("\x0c", self),
            "\u240d" : rawstrcalc("\r", self),
            "\u240e" : rawstrcalc("\x0e", self),
            "\u240f" : rawstrcalc("\x0f", self),
            "\u2410" : rawstrcalc("\x10", self),
            "\u2411" : rawstrcalc("\x11", self),
            "\u2412" : rawstrcalc("\x12", self),
            "\u2413" : rawstrcalc("\x13", self),
            "\u2414" : rawstrcalc("\x14", self),
            "\u2415" : rawstrcalc("\x15", self),
            "\u2416" : rawstrcalc("\x16", self),
            "\u2417" : rawstrcalc("\x17", self),
            "\u2418" : rawstrcalc("\x18", self),
            "\u2419" : rawstrcalc("\x19", self),
            "\u241a" : rawstrcalc("\x1a", self),
            "\u241b" : rawstrcalc("\x1b", self),
            "\u241c" : rawstrcalc("\x1c", self),
            "\u241d" : rawstrcalc("\x1d", self),
            "\u241e" : rawstrcalc("\x1e", self),
            "\u241f" : rawstrcalc("\x1f", self),
            "\u2420" : rawstrcalc(" ", self),
            "\u2421" : rawstrcalc("\x21", self)
            }
        self.variables.update({
            "\u2209" : strfunc("!\u2208(__)", self, name="\u2209", overflow=False),
            "\u220b" : strfunc("\u2208(rev(__))", self, name="\u220b", overflow=False),
            "\u220c" : strfunc("!\u220b(__)", self, name="\u220c", overflow=False),
            "\u221b" : strfunc("x^(1/3)", self, ["x"], name="\u221b"),
            "\u221c" : strfunc("math.sqrt(math.sqrt(x))", self, ["x"], name="\u221c"),
            "\u222c" : strfunc("math.S(math.S(f,++args),++args)", self, ["f", "args"], reqargs=1, name="\u222c"),
            "\u222d" : strfunc("math.S(math.S(math.S(f,++args),++args),++args)", self, ["f", "args"], reqargs=1, name="\u222d")
            })

    def setreturned(self, value=True):
        """Sets returned."""
        self.returned = bool(value)

    def setspawned(self, value=True):
        """Sets spawned."""
        self.spawned = bool(value)
        self.setreturned()

    def printdebug(self, message):
        """Prints Debug Output."""
        for line in str(message).splitlines():
            item = self.recursion*"  "+line
            if self.color in colors:
                item = addcolor(item, self.color)
            if self.debug:
                print(item)
            else:
                self.debuglog.append(item)

    def makevars(self, variables):
        """Forcibly Stores Variables."""
        self.variables.update(variables)

    def makeparens(self, parens):
        """Forcibly Stores Parens."""
        self.parens = parens

    def setvars(self, newvars):
        """Sets New Variables."""
        oldvars = {}
        for k in newvars:
            oldvars[k] = haskey(self.variables, k)
        for k,v in newvars.items():
            if not k is v:
                if v is None:
                    if k in self.variables:
                        del self.variables[k]
                else:
                    self.variables[k] = v
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

    def forshow(self, arg):
        """Prepares An Item For Showing."""
        if not istext(arg):
            return self.prepare(arg, True, True, 2)
        else:
            return str(arg)

    def speedyprep(self, item, top=False, bottom=False, indebug=False, maxrecursion=0):
        """Speedily Prepares The Output Of An Evaluation."""
        out = "{"+"\n"*top
        if not indebug and bottom and not top:
            out += 'raise("RuntimeError", "Maximum recursion depth exceeded in object preparation")'
        else:
            out += " __type__ "
            if istext(item):
                out += "= "+str(item)
            else:
                out += ":= `"+self.evaltypestr(item)+"`"
        out += "\n"*top+" }"
        return out

    def prepare(self, item, top=False, bottom=True, indebug=False, maxrecursion=None):
        """Prepares The Output Of An Evaluation."""
        if maxrecursion is None:
            maxrecursion = self.maxrecursion
        if istext(item):
            out = str(item)
        elif isinstance(item, atom):
            out = repr(item)
        elif isinstance(item, codestr):
            out = str(item)
            if bottom:
                out = "::"+out
        elif isinstance(item, strcalc):
            if bottom:
                out = repr(item)
            else:
                out = str(item)
        elif item is None:
            out = "none"
        elif isinstance(item, bool):
            out = self.prepare(float(item), False, bottom, indebug, maxrecursion)
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
        elif isinstance(item, complex):
            out = ""
            if item.real != 0:
                out += self.prepare(item.real, False, bottom, indebug, maxrecursion)+"+"
            if item.imag == 1:
                out += "i"
            else:
                out += self.prepare(item.imag, False, bottom, indebug, maxrecursion)+"*i"
        elif self.speedy and indebug:
            out = self.speedyprep(item, top, bottom, True, maxrecursion)
        elif isinstance(item, instancecalc):
            if maxrecursion <= 0:
                out = self.speedyprep(item, False, bottom, indebug, maxrecursion)
            elif indebug or bottom:
                out = item.getrepr(top, maxrecursion-1)
            else:
                out = str(item)
        elif isinstance(item, classcalc):
            out = item.getrepr(top, bottom, indebug, maxrecursion)
        elif isinstance(item, (data, multidata)):
            if bottom:
                out = "data:(" + self.prepare(getmatrix(item), False, True, indebug, maxrecursion) + ")"
            else:
                out = self.prepare(getmatrix(item), top, bottom, indebug, maxrecursion)
        elif isinstance(item, matrix):
            if item.y == 0:
                if self.laxnull:
                    out = "()"
                else:
                    out = "none"
            elif item.onlydiag():
                out = "("
                for x in item.getdiag():
                    out += self.prepare(x, False, bottom, indebug, maxrecursion)+","
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
                        out += self.prepare(x, False, bottom, indebug, maxrecursion)+","
                    if len(y) > 0:
                        out = out[:-1]
                    out += "]:\n"
                out = out[:-2]
            else:
                out = "matrix:["
                for y in item.a:
                    for x in y:
                        out += self.prepare(x, False, bottom, indebug, maxrecursion)+","
                    out = out[:-1]+"]:["
                out = out[:-2]
        elif isinstance(item, (fraction, reciprocal)):
            out = ""
            a = self.prepare(item.n, False, bottom, indebug, maxrecursion)
            if not bottom or madeof(a, string.digits) or not self.isreserved(a):
                out += a
            else:
                out += "("+a+")"
            out += "/"
            b = self.prepare(item.d, False, bottom, indebug, maxrecursion)
            if not bottom or madeof(b, string.digits) or not self.isreserved(b):
                out += b
            else:
                out += "("+b+")"
        elif bottom and isinstance(item, rollfunc):
            out = "d:"+self.prepare(item.stop, False, bottom, indebug, maxrecursion)
        elif bottom and isinstance(item, strfunc):
            out = ""
            if isinstance(item, integbase):
                out += "S:"
            elif isinstance(item, derivbase):
                out += "D:"
            variables = item.getvars()
            personals = item.getpers()
            if item.method:
                personals[item.method] = item.method
            out += "\\"+strlist(variables,",")
            if len(variables) > 0:
                out += ","
            for x,y in personals.items():
                out += str(x)+":("
                if maxrecursion <= 0 and isinstance(y, classcalc):
                    out += self.speedyprep(y, False, bottom, indebug, maxrecursion)
                else:
                    out += self.prepare(y, False, True, indebug, maxrecursion-1)
                out += "),"
            if len(variables) > 0 or len(personals) > 0:
                out = out[:-1]+"\\"
            test = self.prepare(item.funcstr, False, True, indebug, maxrecursion)
            if self.isreserved(test, allowed=string.digits):
                out += "("+test+")"
            else:
                out += test
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
                out += self.prepare(item.other_func, False, bottom, indebug, maxrecursion)
                try:
                    item.n
                except AttributeError:
                    pass
                else:
                    if item.n != 1:
                        out += ":"+str(item.n)
            else:
                out = "\\"+str(item)
        elif isinstance(item, funcfloat) or getcheck(item) >= 1:
            out = str(item)
        elif indebug:
            if indebug > 1:
                out = str(item)
            else:
                try:
                    item.getrepr
                except AttributeError:
                    out = repr(item)
                else:
                    out = item.getrepr(top, maxrecursion-1)
        else:
            raise ExecutionError("DisplayError", "Unable to display "+repr(item))
        return str(out)

    def insideouter(self, inputstring, groupers=None):
        """Determines If Inside A String Or Grouper."""
        if groupers is None:
            groupers = self.groupers
        return isinside(inputstring, '"`', {"\u201c":"\u201d"}, groupers)

    def outersplit(self, inputstring, splitstring, groupers=None):
        """Splits By Something Not In A String Or Grouper."""
        if groupers is None:
            groupers = self.groupers
        return carefulsplit(inputstring, splitstring, '"`', {"\u201c":"\u201d"}, groupers)

    def remcomment(self, inputstring, commentstring="#"):
        """Removes A Comment."""
        return self.outersplit(inputstring, commentstring, {})[0]

    def setcalculated(self, result):
        """Sets calculated."""
        self.calculated = result

    def calc(self, inputstring, info=""):
        """Performs Top-Level Calculation."""
        calculated, self.calculated = self.calculated, matrix(0)
        self.process(inputstring, info, self.setcalculated, False)
        out, self.calculated = self.calculated, calculated
        return out

    def process(self, inputstring, info="", command=None, top=None):
        """Performs Top-Level Evaluation."""
        inputstring = self.remcomment(replaceall(str(inputstring), self.aliases, '"`', {"\u201c":"\u201d"}))
        if top is None:
            top = command is not None
        else:
            top = top
        for original in self.outersplit(inputstring, ";;"):
            original = basicformat(original)
            if not iswhite(original):
                out = self.proc_top(original, info, top)
                if command is not None:
                    command(out)

    def proc_top(self, inputstring, info="", top=False):
        """Gets The Value Of An Expression."""
        if info is None:
            info = " <<"+"-"*(70-len(inputstring)-2*self.recursion)
        self.printdebug(">>> "+inputstring+str(info))
        self.recursion += 1
        out = self.proc_cmd(inputstring, top)
        self.printdebug(self.prepare(out, False, True, True)+" <<< "+inputstring)
        self.recursion -= 1
        return out

    def proc_cmd(self, inputstring, top=False):
        """Evaluates Statements."""
        if top:
            spawned = self.spawned
            self.setspawned(False)
        inputlist = self.outersplit(inputstring, "::")
        func, args = inputlist[0], inputlist[1:]
        func = basicformat(func)
        if len(args) == 0:
            out = self.proc_calc(func)
        else:
            original = func+" :: "+strlist(args, " :: ")
            self.printdebug("::> "+original)
            self.recursion += 1
            if func:
                item = self.funcfind(func)
                params = []
                for x in xrange(0, len(args)):
                    arg = basicformat(args[x])
                    if x != len(args)-1 or arg:
                        params.append(codestr(arg, self))
                out = self.call_colon_set(item, params)
            else:
                out = codestr(strlist(args, "::"), self)
            self.printdebug(self.prepare(out, False, True, True)+" <:: "+original)
            self.recursion -= 1
        if top:
            if not self.spawned:
                self.processor.addcommand(inputstring)
            self.setspawned(self.spawned or spawned)
        return out

    def trycalc(self, inputobject):
        """Attempts To Calculate A Variable."""
        if istext(inputobject):
            return self.calc(inputobject)
        else:
            return inputobject

    def getitem(self, variable):
        """Gets The Calculated Value Of A Variable."""
        if variable in self.variables:
            self.variables[variable] = self.trycalc(self.variables[variable])
            return self.variables[variable]
        else:
            return matrix(0)

    def calcitem(self, variable):
        """Ensures That A Variable Exists."""
        self.variables[variable] = self.getitem(variable)

    def proc_calc(self, inputstring):
        """Performs Full Evaluation On An Expression."""
        self.printdebug("=>> "+inputstring)
        self.recursion += 1
        out = self.calc_top(inputstring)
        self.printdebug(self.prepare(out, False, True, True)+" <<= "+inputstring)
        self.recursion -= 1
        return out

    def calc_top(self, value):
        """Begins Calculation."""
        for func in self.tops:
            value = func(value)
        self.printdebug("| "+self.prepare(value, False, True, True))
        return self.calc_pre(value)

    def iseq(self, a, b):
        """Determines Whether Two Evaluator Objects Are Really Equal."""
        return type(a) is type(b) and self.itemstate(a) == self.itemstate(b)

    def wrap(self, item):
        """Wraps An Item In Parentheses."""
        for x in xrange(0, len(self.parens)):
            if self.iseq(self.parens[x], item):
                return self.parenchar+str(x)+self.parenchar
        indexstr = self.parenchar+str(len(self.parens))+self.parenchar
        self.parens.append(item)
        return indexstr

    def top_string(self, expression):
        """Evaluates The String Part Of An Expression."""
        strlist = eithersplit(expression, '"`', {"\u201c":"\u201d"})
        command = ""
        for item in strlist:
            if istext(item):
                command += item
            elif item[0] in ['"', "\u201c", "\u201d"]:
                command += self.wrap(strcalc(item[1], self))
            elif item[0] == "`":
                command += self.wrap(rawstrcalc(item[1], self))
        return command

    def top_paren(self, expression):
        """Evaluates The Parenthetical Part Of An Expression."""
        parenlist = fullsplit(expression, "(", ")", 1)
        command = ""
        for x in parenlist:
            if istext(x):
                command += x
            elif len(x) <= 1:
                if len(x) < 1:
                    command += self.wrap("")
                else:
                    command += self.wrap(x[0])
            else:
                raise SyntaxError("Error in evaluating parentheses len("+repr(x)+")>1")
        return command

    def top_class(self, expression):
        """Evaluates The Curly Brackets In An Expression."""
        curlylist = fullsplit(expression, "{", "}", 1)
        command = ""
        for x in curlylist:
            if istext(x):
                command += x
            elif len(x) <= 1:
                if len(x) < 1:
                    original = ""
                else:
                    original = x[0]
                lines = []
                for line in original.splitlines():
                    if not iswhite(line):
                        lines.append(line)
                cmds = []
                last = ""
                for x in xrange(0, len(lines)):
                    if x == 0:
                        num = leading(lines[x])
                        last = lines[x]
                    else:
                        check = leading(lines[x])
                        if check > num:
                            last += "\n"+lines[x]
                        elif check == num:
                            cmds.append(last)
                            last = lines[x]
                        else:
                            raise ExecutionError("IndentationError", "Unexpected dedent in line "+lines[x])
                if last:
                    cmds.append(last)
                command += self.wrap(curry(self.top_class_do, cmds))
            else:
                raise SyntaxError("Error in evaluating curly braces len("+repr(x)+")>1")
        return command

    def top_class_do(self, cmds):
        """Calculates A Class."""
        out = classcalc(self)
        for cmd in cmds:
            out.process(cmd)
        return out

    def top_brack(self, expression):
        """Evaluates The Brackets In An Expression."""
        bracklist = fullsplit(expression, "[", "]", 1)
        command = ""
        for x in bracklist:
            if istext(x):
                command += x
            elif len(x) <= 1:
                if len(x) < 1:
                    original = ""
                else:
                    original = x[0]
                command += self.wrap(curry(self.top_brack_do, original))
            else:
                raise SyntaxError("Error in evaluating brackets len("+repr(x)+")>1")
        return command

    def top_brack_do(self, original):
        """Calculates A Bracket."""
        out = self.calc(original)
        if isinstance(out, matrix) and out.onlydiag():
            out = out.getdiag()
        else:
            out = [out]
        return rowmatrixlist(out)

    def calc_pre(self, expression):
        """Performs Pre-Format Evaluation."""
        for func in self.pre_calcs:
            test = func(expression)
            if test is not None:
                return test
        return self.calc_post(expression)

    def pre_with(self, expression):
        """Evaluates With Clauses."""
        inputlist = expression.split("$")
        if len(inputlist) > 1:
            inputlist.reverse()
            item = inputlist.pop()
            withclass = classcalc(self)
            for x in inputlist:
                withclass.process(x)
            return withclass.calc(item)

    def pre_set(self, inputstring):
        """Evaluates Setting."""
        test = self.calc_set(inputstring)
        if test is not None:
            return test

    def calc_set(self, original):
        """Evaluates Definition Commands."""
        sides = original.split("=", 1)
        if len(sides) > 1:
            sides[0] = basicformat(sides[0])
            sides[1] = basicformat(sides[1])
            if not endswithany(sides[0], self.bools) and not startswithany(sides[1], self.bools):
                docalc = False
                if sides[0].endswith(":"):
                    sides[0] = sides[0][:-1]
                    docalc = True
                sides[0] = self.outersplit(sides[0], ",")
                if len(sides[0]) > 1:
                    test = True
                    for x in sides[0]:
                        test = test and self.readytofunc(x)
                    if test:
                        sides[1] = self.calc(sides[1])
                        func = diagmatrixlist
                        if isinstance(sides[1], matrix):
                            if sides[1].onlydiag():
                                sides[1] = sides[1].getitems()
                            else:
                                sides[1] = sides[1].items()
                                func = rowmatrixlist
                        elif isinstance(sides[1], strcalc):
                            sides[1] = sides[1].tomatrix().getitems()
                            func = None
                        else:
                            sides[1] = [sides[1]]
                        out = []
                        for x in xrange(0, len(sides[0])):
                            if x == len(sides[0])-1:
                                toset = sides[1][x:]
                            else:
                                toset = sides[1][x:x+1]
                            if len(toset) == 0:
                                toset = matrix(0)
                            elif len(toset) == 1:
                                toset = toset[0]
                            elif func is not None:
                                toset = func(toset)
                            else:
                                itemlist = toset
                                toset = itemlist.pop(0)
                                for item in itemlist:
                                    toset += item
                            out.append(toset)
                            if not self.calc_set_do([sides[0][x], self.wrap(toset)], docalc):
                                raise ExecutionError("VariableError", "Could not multi-set to invalid variable "+sides[0][x])
                        return diagmatrixlist(out)
                    else:
                        raise ExecutionError("SyntaxError", "Could not set to invalid variable "+strlist(sides[0], ","))
                else:
                    sides[0] = sides[0][0]
                    return self.calc_set_do(sides, docalc)
                
    def calc_set_do(self, sides, docalc):
        """Performs The Definition Command."""
        sides[0] = sides[0].split("(", 1)
        if len(sides[0]) > 1:
            sides[0] = delspace(sides[0][0])+"("+sides[0][1]
        else:
            sides[0] = delspace(sides[0][0])
        if not self.readytofunc(sides[0], allowed="."):
            raise ExecutionError("SyntaxError", "Could not set to invalid variable name "+sides[0])
        else:
            useclass = None
            if self.useclass:
                classlist = [self.useclass]
            else:
                classlist = []
            delfrom = None
            if self.useclass is False and classcalc.selfvar in self.variables and isinstance(self.variables[classcalc.selfvar], classcalc):
                delfrom = self.variables[classcalc.selfvar].doset
            if "." in sides[0]:
                classlist += sides[0].split(".")
                for x in xrange(0, len(classlist)-1):
                    if self.isreserved(classlist[x]):
                        raise ExecutionError("SyntaxError", "Could not set to invalid class name "+classlist[x])
                sides[0] = classlist.pop()
                if delfrom is not None and classlist[0] in delfrom:
                    del delfrom[classlist[0]]
                    delfrom = None
                useclass = self.find(classlist[0], True)
                if isinstance(useclass, classcalc):
                    for x in xrange(1, len(classlist)):
                        last = useclass
                        useclass = useclass.retrieve(classlist[x])
                        if not isinstance(useclass, classcalc):
                            if istext(useclass) and len(classlist) == x+1:
                                sides[1] = "( "+useclass+" )"+" + { "+sides[0]+" :"*docalc+" "*(not docalc)+"= "+sides[1]+" }"
                                sides[0] = classlist[x]
                                useclass = last
                                classlist = classlist[:x]
                                docalc = False
                                break
                            else:
                                raise ExecutionError("ClassError", "Could not set "+classlist[x]+" in "+self.prepare(last, False, True, True))
                elif classlist[0] in self.variables and istext(self.variables[classlist[0]]) and len(classlist) == 1:
                    sides[1] = "( "+self.variables[classlist[0]]+" )"+" + { "+sides[0]+" :"*docalc+" "*(not docalc)+"= "+sides[1]+" }"
                    sides[0] = classlist[0]
                    useclass = None
                    classlist = []
                    docalc = False
                else:
                    raise ExecutionError("VariableError", "Could not find class "+self.prepare(classlist[0], False, True, True))
            elif self.useclass:
                useclass = self.funcfind(self.useclass)
            sides[1] = basicformat(sides[1])
            for func in self.set_calcs:
                value = func(sides)
                if value is not None:
                    if not isinstance(value, tuple):
                        value = sides[0], value
                    self.printdebug(": "+strlist(classlist, ".")+"."*bool(classlist)+value[0]+" "+":"*docalc+"= "+self.prepare(value[1], False, True, True))
                    if useclass is None:
                        if not self.redef and value[0] in self.variables:
                            raise ExecutionError("RedefinitionError", "The variable "+value[0]+" already exists")
                        else:
                            if docalc:
                                out = self.trycalc(value[1])
                                self.variables[value[0]] = out
                            else:
                                self.variables[value[0]] = value[1]
                                out = strfloat(value[0], self, name=value[0])
                    else:
                        if not self.redef and value[0] in useclass.variables:
                            raise ExecutionError("RedefinitionError", "The attribute "+value[0]+" already exists")
                        else:
                            if docalc:
                                out = self.trycalc(value[1])
                                useclass.store(value[0], out)
                            else:
                                useclass.store(value[0], value[1])
                                out = strfunc(useclass.selfvar+"."+value[0], self, [], {useclass.selfvar:useclass}, value[0], overflow=False)
                    if delfrom is not None and value[0] in delfrom:
                        del delfrom[value[0]]
                    return out

    def readytofunc(self, expression, extra="", allowed=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        funcparts = expression.split("(", 1)
        top = True
        if len(funcparts) == 1 and self.parenchar in funcparts[0]:
                funcparts = funcparts[0].split(self.parenchar, 1)
                top = False
        out = funcparts[0] != "" and (not self.isreserved(funcparts[0], extra, allowed)) and (len(funcparts) == 1 or funcparts[1].endswith(")"*top or self.parenchar))
        if out and len(funcparts) != 1:
            return not self.insideouter(funcparts[1][:-1])
        else:
            return out

    def set_def(self, sides):
        """Creates Functions."""
        top = None
        if "(" in sides[0] and sides[0].endswith(")"):
            top = True
        elif self.parenchar in sides[0] and sides[0].endswith(self.parenchar):
            top = False
        if top is not None:
            if top:
                sides[0] = sides[0][:-1].split("(", 1)
            else:
                sides[0] = sides[0].split(self.parenchar, 1)
                sides[0][1] = self.namefind(self.parenchar+sides[0][1])
            params, personals, allargs, reqargs = self.eval_set(self.outersplit(sides[0][1], ","))
            return (sides[0][0], strfunc(sides[1], self, params, personals, allargs=allargs, reqargs=reqargs))

    def set_normal(self, sides):
        """Performs =."""
        if not self.isreserved(sides[0]):
            return sides[1]

    def calc_post(self, expression):
        """Formats Expressions."""
        return self.calc_pieces(delspace(expression))

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
        value = reassemble(top, ["|", "&"])
        self.printdebug("==> "+value)
        self.recursion += 1
        out = self.bool_or(top)
        self.printdebug(self.prepare(out, False, True, True)+" <== "+value)
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

    def bool_eq(self, inputstring):
        """Evaluates The Equation Part Of A Boolean Expression."""
        inputlist = switchsplit(inputstring, self.bools)
        if len(inputlist) == 0:
            return matrix(0)
        elif len(inputlist) == 1 and not madeof(inputlist[0], self.bools):
            return self.calc_eval(inputlist[0])
        else:
            for x in xrange(0, len(inputlist)):
                if istext(inputlist[x]) and madeof(inputlist[x], self.bools):
                    args = []
                    if x == 0:
                        args.append(matrix(0))
                    else:
                        if istext(inputlist[x-1]):
                            inputlist[x-1] = self.calc_eval(inputlist[x-1])
                        args.append(inputlist[x-1])
                    if x == len(inputlist)-1:
                        args.append(matrix(0))
                    else:
                        if istext(inputlist[x+1]):
                            inputlist[x+1] = self.calc_eval(inputlist[x+1])
                        args.append(inputlist[x+1])
                    out = False
                    haseq = False
                    hasgt = False
                    haslt = False
                    hasne = False
                    inv = False
                    for c in inputlist[x]:
                        if c == "=":
                            haseq = True
                        elif c == ">":
                            hasgt = True
                        elif c == "<":
                            haslt = True
                        elif c == "\u2260":
                            hasne = True
                        elif c == "!":
                            inv = not inv
                    if haseq and hasne:
                        out = args[0] != args[1] or args[0] == args[1]
                    elif haseq and hasgt and haslt:
                        out = args[0] >= args[1] or args[0] <= args[1]
                    elif (hasgt and haslt) or hasne:
                        out = args[0] != args[1]
                    elif hasgt and haseq:
                        out = args[0] >= args[1]
                    elif haslt and haseq:
                        out = args[0] <= args[1]
                    elif hasgt:
                        out = args[0] > args[1]
                    elif haslt:
                        out = args[0] < args[1]
                    else:
                        out = args[0] == args[1]
                    if inv:
                        out = not out
                    if not out:
                        return False
            return True

    def calc_eval(self, expression):
        """Evaluates An Expression."""
        top = expression.split("~")
        for a in xrange(0, len(top)):
            top[a] = [top[a]]
            if not top[a][0].startswith("\\"):
                top[a][0] = top[a][0].split("++")
                for c in xrange(0, len(top[a][0])):
                    top[a][0][c] = top[a][0][c].split("--")
                    for d in xrange(0, len(top[a][0][c])):
                        top[a][0][c][d] = top[a][0][c][d].split("**")
                        for e in xrange(0, len(top[a][0][c][d])):
                            top[a][0][c][d][e] = top[a][0][c][d][e].split(",")
                            for f in xrange(0, len(top[a][0][c][d][e])):
                                top[a][0][c][d][e][f] = splitinplace(top[a][0][c][d][e][f].split("+"), "-", self.callops, 2)
                                for g in xrange(0, len(top[a][0][c][d][e][f])):
                                    top[a][0][c][d][e][f][g] = top[a][0][c][d][e][f][g].split("%")
                                    for h in xrange(0, len(top[a][0][c][d][e][f][g])):
                                        top[a][0][c][d][e][f][g][h] = splitinplace(top[a][0][c][d][e][f][g][h].split("*"), "/")
        value = reassemble(top, ["~", "\\", "++", "--", "**", ",", "+", "%", "*"])
        self.printdebug("=> "+value)
        self.recursion += 1
        out = self.eval_check(self.eval_loop(top), True)
        self.printdebug(self.prepare(out, False, True, True)+" <= "+value)
        self.recursion -= 1
        return out

    def eval_loop(self, complist):
        """Performs List Comprehension."""
        if len(complist) == 1:
            return self.eval_lambda(complist[0])
        else:
            item = self.eval_lambda(complist.pop())
            lists = []
            argnum = 1
            for x in reversed(xrange(0, len(complist))):
                if not delist(complist[x]):
                    argnum += 1
                else:
                    lists.append((self.eval_lambda(complist[x]), argnum))
                    argnum = 1
            if argnum > 1:
                lists.append((matrix(0), argnum))
            return self.eval_loop_set(lists, [], item)

    def eval_loop_set(self, lists, args, func):
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
                    item = self.eval_loop_set(lists[:], args, func)
                for y in xrange(0, argnum):
                    args.remove(units[argnum*x+y])
                if not isnull(item):
                    new.append(item)
            if fromstring:
                out = rawstrcalc(strlist(new, "", converter=lambda x: self.prepare(x, True, False)), self)
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
                out = self.eval_loop_set(lists, args, func)
            args.remove(value)
            return out

    def eval_lambda(self, inputlist):
        """Evaluates Lambdas."""
        if islist(inputlist[0]):
            return self.eval_join(inputlist[0])
        else:
            inputstring = inputlist[0]
            out = inputstring[1:].split("\\", 1)
            if len(out) == 1:
                test = self.find(out[0], True)
                if isinstance(test, funcfloat):
                    return test
                elif hascall(test):
                    return test.call(None)
                else:
                    while out[0].startswith(self.parenchar) and out[0].endswith(self.parenchar) and out[0] in self.variables and (istext(self.variables[out[0]]) or isinstance(self.variables[out[0]], strcalc)):
                        if isinstance(self.variables[out[0]], strcalc):
                            out[0] = repr(self.variables[out[0]])
                        else:
                            out[0] = str(self.variables[out[0]])
                return strfloat(out[0], self, check=False)
            elif out[0] == "":
                return strfloat(out[1], self, check=False)
            else:
                params, personals, allargs, reqargs = self.eval_set(self.outersplit(self.namefind(out[0]), ","))
                if out[1].startswith("\\"):
                    return strfloat(out[1][1:], self, params, personals, check=False, allargs=allargs, reqargs=reqargs)
                else:
                    while out[1].startswith(self.parenchar) and out[1].endswith(self.parenchar) and out[1] in self.variables and (istext(self.variables[out[1]]) or isinstance(self.variables[out[1]], strcalc)):
                        if isinstance(self.variables[out[1]], strcalc):
                            out[1] = repr(self.variables[out[1]])
                        else:
                            out[1] = str(self.variables[out[1]])
                    return strfloat(out[1], self, params, personals, allargs=allargs, reqargs=reqargs)

    def eval_set(self, temp):
        """Performs Setting."""
        params = []
        personals = {}
        allargs = None
        inopt = None
        reqargs = None
        for i in xrange(0, len(temp)):
            x = basicformat(temp[i])
            if x:
                doparam = True
                doallargs = False
                special = True
                if x.startswith("*"):
                    if i == len(temp)-1:
                        x = x[1:]
                        doallargs = True
                    else:
                        raise ExecutionError("ArgumentError", "Catch all argument must come last")
                elif x.startswith("-"):
                    inopt = True
                    if reqargs is None:
                        reqargs = len(params)
                    x = x[1:]
                elif inopt:
                    raise ExecutionError("ArgumentError", "Cannot have required args after optional args")
                elif x.startswith("+"):
                    x = x[1:]
                else:
                    special = False
                if ":" in x:
                    if not special:
                        doparam = False
                    x = x.split(":", 1)
                    x[0] = delspace(x[0])
                    if not x[0] or self.isreserved(x[0]):
                        raise ExecutionError("VariableError", "Could not set to invalid personal "+x[0])
                    else:
                        personals[x[0]] = self.calc(x[1], " <\\")
                    x = x[0]
                else:
                    x = delspace(x)
                if doallargs:
                    if not x or self.isreserved(x):
                        raise ExecutionError("VariableError", "Could not set to invalid allargs "+x)
                    else:
                        allargs = x
                if doparam:
                    if not x or self.isreserved(x):
                        raise ExecutionError("VariableError", "Could not set to invalid variable "+x)
                    else:
                        params.append(x)
        return params, personals, allargs, reqargs

    def eval_join(self, inputlist):
        """Performs Concatenation."""
        items = []
        for item in inputlist:
            item = self.eval_remove(item)
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
            doclass = 0
            rowlen = None
            tot = len(items)
            for x in items:
                if isinstance(x, strcalc):
                    dostr += 1
                elif isinstance(x, matrix):
                    dodata += 1
                    if rowlen is None:
                        rowlen = x.x
                    if x.x == rowlen:
                        domatrix += 1
                        if rowlen == 2:
                            domultidata += 1
                    if x.onlydiag():
                        dolist += 1
                    elif x.onlyrow():
                        dobrack += 1
                elif isinstance(x, multidata):
                    domultidata += 1
                elif isinstance(x, data):
                    dodata += 1
                elif isinstance(x, classcalc):
                    doclass += 1
                else:
                    domatrix -= 1
                    domultidata -= 1
                    tot -= 1
            if dostr > 0:
                out = rawstrcalc("", self)
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
            elif doclass == len(items):
                out = items[0].copy()
                for x in xrange(1, len(items)):
                    out.extend(items[x])
                return out
            else:
                raise ExecutionError("TypeError", "Could not concatenate items "+repr(items))

    def eval_remove(self, inputlist):
        """Performs Removal."""
        item = self.eval_repeat(inputlist[0])
        if len(inputlist) > 1:
            params = []
            for x in xrange(1, len(inputlist)):
                params.append(self.eval_repeat(inputlist[x]))
            item = getcopy(item)
            if isinstance(item, classcalc):
                item.calcall()
                while len(params) > 0:
                    arg = params.pop(0)
                    if isinstance(arg, strcalc):
                        arg = str(arg)
                        if arg in item.variables:
                            item.remove(arg)
                    elif isinstance(arg, classcalc):
                        arg.calcall()
                        for k,v in arg.getvars().items():
                            if k in item.variables and item.variables[k] == v:
                                item.remove(k)
                    elif hasmatrix(arg):
                        params.extend(getmatrix(arg).getitems())
                    else:
                        raise ExecutionError("TypeError", "Could not remove from class item "+self.prepare(arg, False, True, True))
            elif isinstance(item, matrix):
                if item.onlyrow() or item.onlydiag():
                    if item.onlydiag():
                        row = False
                    else:
                        row = True
                    items = item.getitems()
                    for arg in params:
                        if arg in items:
                            items.remove(arg)
                    if row:
                        item = rowmatrixlist(items)
                    else:
                        item = diagmatrixlist(items)
                else:
                    for arg in params:
                        if isinstance(arg, matrix):
                            for row in arg.a:
                                if row in item.a:
                                    item.a.remove(row)
                                    item.y -= 1
                        else:
                            raise ExecutionError("TypeError", "Can only remove matrices from matrices")
            elif isinstance(item, strcalc):
                for arg in params:
                    arg = self.prepare(arg, True, False)
                    pos = item.calcstr.find(arg)
                    if pos >= 0:
                        item.calcstr = item.calcstr[:pos]+item.calcstr[pos+len(arg):]
            elif isinstance(item, multidata):
                for arg in params:
                    if isinstance(arg, matrix):
                        arg = arg.getitems()
                        if len(arg) == 2:
                            if arg[0] in item.x.units:
                                index = item.x.units.index(arg[0])
                                if item.y.units[index] == arg[1]:
                                    item.x.units.pop(index)
                                    item.y.units.pop(index)
                        else:
                            raise ExecutionError("TypeError", "Can only remove matrix pairs from multidata")
                    elif arg in item.x.units:
                        item.y.units.pop(item.x.units.index(arg))
                        item.x.units.remove(arg)
            elif isinstance(item, data):
                for arg in params:
                    if arg in item.units:
                        item.units.remove(arg)
            else:
                raise ExecutionError("TypeError", "Could not remove from item "+self.prepare(item, False, True, True))
        return item

    def eval_repeat(self, inputlist):
        """Evaluates Repeats."""
        if len(inputlist) == 1:
            return self.eval_list(inputlist[0])
        else:
            out = self.eval_list(inputlist[0])
            for x in xrange(1, len(inputlist)):
                done = False
                num = self.eval_list(inputlist[x])
                if hasattr(out, "op_repeat"):
                    try:
                        test = out.op_repeat(num)
                    except NotImplementedError:
                        test = NotImplemented
                    if test is not NotImplemented:
                        out = test
                        done = True
                if not done and hasattr(num, "rop_repeat"):
                    try:
                        test = num.rop_repeat(out)
                    except NotImplementedError:
                        test = NotImplemented
                    if test is not NotImplemented:
                        out = test
                        done = True
                if isinstance(out, matrix) and (out.onlyrow() or out.onlydiag()):
                    if out.onlydiag():
                        row = False
                    else:
                        row = True
                    out = out.getitems()
                if not done:
                    num = getint(num)
                    if islist(out):
                        if num < 0:
                            out = out[::-1] * (-num)
                        else:
                            out = out * num
                        done = True
                    else:
                        out = [out] * abs(num)
                        row = False
                        done = True
            if islist(out):
                if row:
                    return rowmatrixlist(out)
                else:
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
                    value = value + item
            return value

    def eval_mod(self, inputlist):
        """Evaluates The Modulus Part Of An Expression."""
        value = self.eval_mul(inputlist[0])
        for x in xrange(1, len(inputlist)):
            value = value % self.eval_mul(inputlist[x])
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
                    value = value * item
            return value

    def eval_call(self, inputstring):
        """Evaluates A Variable."""
        self.printdebug("-> "+inputstring)
        self.recursion += 1
        for func in self.calls:
            value = func(inputstring)
            if value is not None:
                break
        out = self.eval_check(value)
        self.printdebug(self.prepare(out, False, True, True)+" <- "+inputstring+" | "+namestr(func).split("_")[-1])
        self.recursion -= 1
        return out

    def eval_check(self, value, top=False):
        """Checks A Value."""
        if value is None:
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
            elif hasreal(value) is not None:
                return self.eval_check(float(value))
            else:
                raise ExecutionError("VariableError", "Unable to process "+str(value))

    def convertable(self, item):
        """Determines If An Item Can Be Converted By eval_check."""
        return hasnum(item) or islist(item) or isinstance(item, bool) or item is None

    def call_var(self, inputstring):
        """Checks If Variable."""
        if inputstring in self.variables:
            item, key = self.getfind(inputstring, True)
            if istext(item):
                value = self.calc(str(item), " | var")
            elif self.convertable(item):
                value = item
            else:
                value = getcall(item)(None)
            if not self.isreserved(key):
                self.variables[key] = value
            return value

    def call_parenvar(self, inputstring):
        """Checks If Parentheses."""
        if inputstring.startswith(self.parenchar) and inputstring.endswith(self.parenchar):
            item = self.namefind(inputstring, True)
            if item is not inputstring:
                if istext(item):
                    value = self.calc(str(item), " | parenvar")
                elif self.convertable(item):
                    value = item
                else:
                    value = getcall(item)(None)
                return value

    def call_none(self, inputstring):
        """Evaluates A Null."""
        if inputstring == "":
            if self.laxnull:
                return matrix(0)
            else:
                raise ExecutionError("NoneError", "Cannot evaluate the empty string")

    def call_lambda(self, inputstring):
        """Wraps Lambda Evaluation."""
        if inputstring.startswith("\\"):
            return self.eval_lambda([inputstring])

    def call_neg(self, inputstring):
        """Evaluates Unary -."""
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
            level = 1
            for x in reversed(xrange(0, len(inputlist))):
                item = inputlist[x]
                if item:
                    value = knuth(self.eval_call(item), value, level)
                    level = 1
                else:
                    if x == 0 or x == len(inputlist)-1:
                        value = knuth(self.eval_call(""), value, level)
                        level = 1
                    else:
                        level += 1
            return value

    def call_colon(self, inputstring):
        """Evaluates Colons."""
        if ":" in inputstring:
            inputlist = inputstring.split(":")
            if inputlist[0]:
                params = []
                for x in xrange(1, len(inputlist)):
                    if inputlist[x]:
                        params.append(getcopy(self.eval_call(inputlist[x])))
                item = self.funcfind(inputlist[0])
                return self.call_colon_set(item, params)
            else:
                result, err = catch(self.eval_call, strlist(inputlist[1:], ":"))
                if err:
                    out = classcalc(self, {
                        self.errorvar : 1.0,
                        self.fatalvar : float(err[2])
                        }).toinstance()
                    out.store(self.namevar, strcalc(err[0], self))
                    out.store(self.messagevar, strcalc(err[1], self))
                    if len(err) > 3:
                        for k,v in err[3].items():
                            out.store(k, v)
                    return rowmatrixlist([matrix(0), out])
                else:
                    return rowmatrixlist([result, matrix(0)])

    def call_colon_set(self, item, params):
        """Performs Colon Function Calls."""
        self.overflow = []
        docalc = False
        if isnull(item):
            if len(params) == 0:
                return item
            else:
                raise ExecutionError("NoneError", "Nothing cannot be called")
        elif isinstance(item, strcalc) and not isinstance(item, codestr):
            item = item.calcstr
            if len(params) == 0:
                value = rawstrcalc(item[-1], self)
            elif len(params) == 1:
                value = rawstrcalc(item[int(params[0])], self)
            else:
                value = rawstrcalc(item[int(params[0]):int(params[1])], self)
                self.overflow = params[2:]
        elif isinstance(item, classcalc) and not isinstance(item, instancecalc):
            if len(params) == 0:
                value = item.toinstance()
            else:
                self.overflow = params[1:]
                value = item.calc(self.prepare(params[0], False, False))
        elif isinstance(item, multidata):
            if len(params) == 0:
                value = item.x.units[0]
            else:
                self.overflow = params[1:]
                if params[0] in item.x.units:
                    value = item.y.units[item.x.units.index(params[0])]
                else:
                    value = matrix(0)
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
        elif len(params) == 0:
            value = item
        else:
            raise ExecutionError("ArgumentError", "Excess argument"+"s"*(len(params) > 1)+" of "+strlist(params, ", ", lambda x: self.prepare(x, False, True, True))+" to "+self.prepare(item, False, True, True))
        while docalc or len(self.overflow) > 0:
            docalc = False
            temp = self.overflow[:]
            self.overflow = []
            value = self.call_colon_set(value, temp)
        return value

    def call_paren(self, inputstring):
        """Evaluates Parentheses."""
        inputstring = strlist(switchsplit(inputstring, string.digits, notstring=self.reserved), self.parenchar*2)        
        if self.parenchar in inputstring:
            self.printdebug("(|) "+inputstring) 
            templist = inputstring.split(self.parenchar)
            inputlist = [[]]
            feed = inputlist[0]
            last = False
            for x in xrange(0, len(templist)):
                if x%2 == 1:
                    if templist[x]:
                        feed.append(self.parenchar+templist[x]+self.parenchar)
                        last = True
                    else:
                        last = False
                elif templist[x]:
                    if last:
                        inputlist.append([])
                        feed = inputlist[-1]
                    feed.append(templist[x])
            temp = "("+strlist(inputlist, ") * (", lambda l: strlist(l, " : "))+")"
            self.printdebug("(>) "+temp)
            self.recursion += 1
            values = []
            for l in inputlist:
                item = matrix(0)
                if l[0].startswith("."):
                    if len(values) > 0:
                        item = strfunc(strfunc.autoarg+l[0], self, [strfunc.autoarg], overflow=False).call([values.pop()])
                    else:
                        raise ExecutionError("NoneError", "Nothing does not have methods")
                else:
                    item = self.eval_call(l[0])
                args = []
                for x in xrange(1, len(l)):
                    args.append(self.eval_call(l[x]))
                item = self.call_paren_do(item, args)
                if values and isinstance(item, funcfloat) and item.infix:
                    values.append(self.call_paren_do(item, [values.pop()]))
                else:
                    values.append(item)
            if len(values) == 0:
                value = matrix(0)
            else:
                value = values[0]
                for x in xrange(1, len(values)):
                    value = value * values[x]
            self.printdebug(self.prepare(value, False, True, True)+" (<) "+temp)
            self.recursion -= 1
            return value

    def call_paren_do(self, item, arglist):
        """Does Parentheses Calling."""
        x = 0
        while x < len(arglist):
            self.overflow = []
            arg = getcopy(arglist[x])
            if not isfunc(item):
                if isinstance(arg, funcfloat) and arg.infix:
                    if x+1 < len(arglist):
                        arg = self.call_paren_do(arg, [arglist.pop(x+1)])
                    item = self.call_paren_do(arg, [item])
                elif not isnull(arg):
                    item = item * arg
            elif isinstance(arg, matrix) and arg.onlydiag():
                args = arg.getdiag()
                if isinstance(item, (strfunc, usefunc)) and item.overflow and len(args) > len(item.variables):
                    args = args[:len(item.variables)-1] + [diagmatrixlist(args[len(item.variables)-1:])]
                item = getcall(item)(args)
            else:
                item = getcall(item)([arg])
            if self.overflow:
                out = self.overflow
                self.overflow = []
                raise ExecutionError("ArgumentError", "Excess argument"+"s"*(len(out) > 1)+" of "+strlist(out, ", ", lambda x: self.prepare(x, False, True, True)))
            else:
                x += 1
        return item

    def call_comp(self, inputstring):
        """Performs Function Composition."""
        if ".." in inputstring:
            funclist = inputstring.split("..")
            return strfunc(strlist(funclist, "(")+"("+strfunc.allargs+")"*len(funclist), self, overflow=False)

    def call_lambdacoeff(self, inputstring):
        """Evaluates Lambda Coefficients."""
        parts = inputstring.split("\\", 1)
        if len(parts) > 1:
            return self.eval_call(parts[0]+self.wrap(self.eval_lambda(["\\"+parts[1]])))

    def call_method(self, inputstring):
        """Returns Method Instances."""
        if "." in inputstring:
            itemlist = inputstring.split(".")
            isfloat = len(itemlist) < 3
            for item in itemlist:
                isfloat = isfloat and (not item or madeof(item, string.digits))
            if not isfloat:
                itemlist[0] = self.funcfind(itemlist[0])
                out = itemlist[0]
                for x in xrange(1, len(itemlist)):
                    key = itemlist[x]
                    if hasattr(out, "getmethod"):
                        new = out.getmethod(key)
                    elif self.laxnull and isnull(out):
                        raise ExecutionError("NoneError", "Nothing does not have methods")
                    else:
                        if hasattr(out, key):
                            new = None
                            test = getattr(out, key)
                            if hasnum(test):
                                new = test
                            elif hasattr(test, "__doc__"):
                                docstring = basicformat(test.__doc__)
                                if docstring.startswith("[|") and "|]" in docstring:
                                    rabstring = superformat(docstring[2:].split("|]")[0])
                                    if ":" in rabstring:
                                        rabcheck, rabstring = rabstring.split(":", 1)
                                        if basicformat(rabcheck) == "rabbit":
                                            name, rabargs = basicformat(rabstring).split(":", 1)
                                            name = delspace(name)
                                            if not name:
                                                new = eval(rabargs)
                                            else:
                                                if rabargs:
                                                    args, kwargs = eval(rabargs)
                                                else:
                                                    args, kwargs = [], {}
                                                if name == "usefunc":
                                                    new = usefunc(test, self, *args, **kwargs)
                                                elif name == "funcfloat":
                                                    args, kwargs = rabargs
                                                    new = funcfloat(test, self, *args, **kwargs)
                                                elif name == "unifunc":
                                                    args, kwargs = rabargs
                                                    new = unifunc(test, self, *args, **kwargs)
                                                elif name == "makefunc":
                                                    args, kwargs = rabargs
                                                    new = makefunc(test, self, *args, **kwargs)
                                                else:
                                                    raise ValueError("Invalid Rabbit wrapper of "+name)
                            if new is None:
                                raise ExecutionError("AttributeError", "Cannot get method "+key+" from "+self.prepare(out, False, True, True))
                                # This is where whatever test is should be wrapped regardless in a special full-conversion wrapper
                        else:
                            raise ExecutionError("AttributeError", "Cannot get method "+key+" from "+self.prepare(out, False, True, True))
                    out = new
                return out

    def call_normal(self, inputstring):
        """Returns Argument."""
        return inputstring

    def getparen(self, num):
        """Gets A Parenthesis."""
        test = self.parens[num]
        if typestr(test) == "function":
            return test()
        else:
            return test

    def namefind(self, varname, follow=False):
        """Finds A Name."""
        while varname.startswith(self.parenchar) and varname.endswith(self.parenchar):
            checknum = varname[1:-1]
            if checknum in self.variables:
                num = getint(self.funcfind(checknum))
            elif isreal(checknum) is not None:
                num = getint(checknum)
            else:
                break
            if num < 0:
                num += len(self.parens)
            if num < 0 or num >= len(self.parens):
                raise ExecutionError("VariableError", "Could not find parentheses "+self.parenchar+str(num)+self.parenchar)
            elif istext(self.parens[num]):
                varname = self.getparen(num)
            elif follow:
                return self.getparen(num)
            else:
                break
        return varname

    def funcfind(self, item):
        """Finds A Value."""
        while istext(item):
            original = item
            self.printdebug("> "+self.prepare(original, False, True, True))
            self.recursion += 1
            if item in self.variables:
                item = self.variables[item]
            else:
                item = self.calc(item, " >")
            self.printdebug(self.prepare(item, False, True, True)+" < "+self.prepare(original, False, True, True))
            self.recursion -= 1
        return item

    def find(self, *args, **kwargs):
        """Wraps getfind."""
        out, _ = self.getfind(*args, **kwargs)
        return out

    def getfind(self, key, follow=False):
        """Finds A String."""
        old = ""
        if istext(key):
            new = basicformat(key)
        else:
            new = key
        while not self.iseq(old, new):
            key = old
            old = new
            new = self.finding(old, follow)
        return new, key

    def finding(self, key, follow=False):
        """Performs String Finding."""
        if istext(key):
            out = self.namefind(key, follow)
        else:
            out = key
        if istext(out) and out in self.variables and (follow or istext(self.variables[out])):
            out = self.variables[out]
        return out

    def condense(self):
        """Simplifies Variable Hierarchies."""
        for x in self.variables:
            self.variables[x] = self.find(x, True)

    def isreserved(self, expression, extra="", allowed=""):
        """Determines If An Expression Contains Reserved Characters."""
        if not expression:
            return True
        else:
            reserved = self.reserved+extra
            for x in expression:
                if x in self.reserved and not x in allowed:
                    return True
            return False

    def call(self, item, value, varname=None):
        """Evaluates An Item With A Value."""
        if varname is None:
            varname = self.varname
        if istext(item):
            oldvars = self.setvars({varname: value})
            try:
                out = self.calc(item)
            finally:
                self.setvars(oldvars)
        elif isfunc(item):
            out = getcall(item)(varproc(value))
        elif hasnum(item):
            return item
        else:
            oldvars = self.setvars({varname: value})
            try:
                out = getcall(item)(None)
            finally:
                self.setvars(oldvars)
        return self.call(out, value, varname)

    def evaltypestr(self, item):
        """Finds A String For A Type."""
        if isinstance(item, instancecalc):
            return "instance"
        elif isinstance(item, classcalc):
            return "class"
        elif isinstance(item, data):
            return "data"
        elif isinstance(item, multidata):
            return "multidata"
        elif isnull(item):
            return "none"
        elif isinstance(item, matrix):
            if item.onlydiag():
                return "list"
            elif item.onlyrow():
                return "row"
            else:
                return "matrix"
        elif isinstance(item, (fraction, reciprocal)):
            return "fraction"
        elif isinstance(item, codestr):
            return "code"
        elif isinstance(item, strcalc):
            return "string"
        elif isinstance(item, funcfloat):
            return "function"
        elif isinstance(item, atom):
            return "atom"
        elif isinstance(item, complex):
            return "complex"
        elif isnum(item):
            return "number"
        else:
            return namestr(item)

    def typecalc(self, item):
        """Finds A Type."""
        if isinstance(item, instancecalc):
            return item.typecalc()
        else:
            return rawstrcalc(self.evaltypestr(item), self)

    def getvars(self):
        """Gets Variables Absent selfvar."""
        out = self.variables.copy()
        if classcalc.selfvar in out:
            del out[classcalc.selfvar]
        return out

    def frompython(self, item):
        """Converts A Python Object To A Rabbit Object."""
        if item is None:
            out = matrix(0)
        elif hasnum(item):
            out = item
        elif istext(item):
            out = strcalc(item, self)
        elif islist(item):
            out = diagmatrixlist(item, func=self.frompython)
        elif isfunc(item):
            out = item
        else:
            raise TypeError("Cannot convert non-evaluatour result type "+typestr(item))
        return out

    def liststate(self, inputlist):
        """Compiles A List."""
        return map(self.itemstate, inputlist)

    def getstates(self, variables):
        """Compiles Variables."""
        out = {}
        for k,v in variables.items():
            out[k] = self.itemstate(v)
        return out

    def itemstate(self, item):
        """Gets The State Of An Item."""
        if hasattr(item, "getstate"):
            return item.getstate()
        else:
            return item

    def deitem(self, item):
        """Decompiles An Item."""
        if isinstance(item, tuple):
            name = str(item[0])
            args = item[1:]
            if name == "atom":
                value = atom()
            elif name == "reciprocal":
                value = reciprocal(self.deitem(args[0]))
            elif name == "fraction":
                value = fraction(self.deitem(args[0]), self.deitem(args[1]))
            elif name == "data":
                value = data(args[0], args[1])
            elif name == "multidata":
                value = multidata(args[0], args[1])
            elif name == "rollfunc":
                value = rollfunc(args[0], self, args[1], args[2], args[3])
            elif name == "matrix":
                value = matrix(args[1], args[2], converter=args[3], fake=args[4])
                for y in xrange(0, len(args[0])):
                    for x in xrange(0, len(args[0][y])):
                        value.store(y,x, self.deitem(args[0][y][x]))
            elif name == "strfunc":
                value = strfunc(args[0], self, args[1], self.devariables(args[2]), args[3], args[4], args[5], args[6], args[7], self.devariables(args[8]), args[9])
            elif name == "codestr":
                value = codestr(args[0], self)
            elif name == "strcalc":
                value = rawstrcalc(args[0], self)
            elif name == "derivfunc":
                value = derivfunc(args[0], args[1], args[2], args[3], self, args[4], args[5], args[6], args[7], self.devariables(args[8]))
            elif name == "integfunc":
                value = integfunc(args[0], args[1], self, args[2], args[3], args[4], self.devariables(args[5]))
            elif name == "usefunc":
                value = usefunc(args[0], self, args[1], args[2], args[3], args[4], args[5], args[6], args[7], self.devariables(args[8]))
            elif name == "classcalc":
                value = classcalc(self, self.devariables(args[0]))
            elif name == "instancecalc":
                value = instancecalc(self, self.devariables(args[0]), self.devariables(args[1]))
            elif name == "makefunc":
                value = makefunc(args[0], self, args[1], args[2], self.devariables(args[3]))
            elif name == "find":
                tofind = str(args[0])
                if tofind in self.variables:
                    value = self.variables[tofind]
                else:
                    raise ExecutionError("UnpicklingError", "Rabbit could not find "+tofind)
            else:
                raise ExecutionError("UnpicklingError", "Rabbit could not unpickle "+name)
        else:
            value = item
        return value

    def devariables(self, variables):
        """Decompiles Variables."""
        out = {}
        for k,v in variables.items():
            out[k] = self.deitem(v)
        return out

    def delist(self, inputlist):
        """Decompiles A List."""
        out = []
        for x in inputlist:
            out.append(self.deitem(x))
        return out

class evalfuncs(object):
    """Implements Evaluator Functions."""
    def __init__(self, e):
        """Initializes The Functions."""
        self.e = e

    def delcall(self, variables):
        """Deletes A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to del")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], False, False)
            if original in self.e.variables:
                out = self.e.variables[original]
                del self.e.variables[original]
            elif "." in original:
                test = original.split(".")
                item = test.pop()
                useclass = self.e.find(test[0], True)
                if isinstance(useclass, classcalc):
                    last = useclass
                    for x in xrange(1, len(test)):
                        useclass = usecla(test[x])
                        if not isinstance(useclass, classcalc):
                            raise ExecutionError("ClassError", "Could not delete "+test[x]+" in "+self.e.prepare(last, False, True, True))
                else:
                    raise ExecutionError("VariableError", "Could not find class "+test[0])
                out = useclass.retrieve(item)
                useclass.remove(item)
            else:
                raise ExecutionError("VariableError", "Could not find "+original)
            self.e.setreturned()
            return out
        else:
            out = []
            for arg in variables:
                out.append(self.delcall([arg]))
            return diagmatrixlist(out)

    def iseqcall(self, variables):
        """Determins Whether All Arguments Are Equal."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to is")
        else:
            out = True
            last = variables[0]
            for x in xrange(1, len(variables)):
                out = out and iseq(last, variables[x])
            return out

    def includecall(self, variables):
        """Includes A Class In The Global Namespace."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to include")
        elif len(variables) == 1:
            if isinstance(variables[0], classcalc):
                oldvars = self.e.setvars(variables[0].getvars())
                self.e.setreturned()
                return classcalc(self.e, oldvars)
            else:
                raise ValueError("Can only include a class")
        else:
            out = []
            for arg in variables:
                out.append(self.includecall([arg]))
            return diagmatrixlist(out)

    def envcall(self, variables):
        """Retrieves A Class Of The Global Environment."""
        if variables:
            self.e.overflow = variables
        self.e.setreturned()
        return classcalc(self.e, self.e.getvars())

    def raisecall(self, variables):
        """Raises An Error."""
        if not variables:
            raise ExecutionError("Error", "An error occured")
        elif len(variables) == 1:
            if isinstance(variables[0], classcalc) and self.iserrcall(variables):
                name = variables[0].tryget(self.e.namevar)
                if name:
                    name = self.e.prepare(name, False, False)
                else:
                    name = "Error"
                message = variables[0].tryget(self.e.messagevar)
                if message:
                    message = self.e.prepare(message, False, False)
                else:
                    message = "An error occured"
                fatal = variables[0].tryget(self.e.fatalvar)
                if fatal:
                    fatal = bool(fatal)
                else:
                    fatal = False
                variables = variables[0].getvars()
                del variables[self.e.errorvar]
                if self.e.namevar in variables:
                    del variables[self.e.namevar]
                if self.e.messagevar in variables:
                    del variables[self.e.messagevar]
                if self.e.fatalvar in variables:
                    del variables[self.e.fatalvar]
                raise ExecutionError(name, message, fatal, variables)
            else:
                raise ExecutionError(self.e.prepare(variables[0], False, False), "An error occured")
        else:
            raise ExecutionError(self.e.prepare(variables[0], False, False), strlist(variables[1:], "; ", lambda x: self.e.prepare(x, False, False)))

    def exceptcall(self, variables):
        """Excepts Errors."""
        if not variables:
            return rowmatrixlist([0.0])
        elif isinstance(variables[0], matrix) and variables[0].y == 1 and variables[0].x == 2:
            items = variables[0].items()
            if self.iserrcall([items[1]]):
                for check in variables[1:]:
                    if items[1] == check or items[1].tryget(self.e.namevar) == check:
                        return rowmatrixlist([items[0], 1.0])
                return self.raisecall([items[1]])
            else:
                return rowmatrixlist([items[0], 0.0])
        else:
            raise ValueError("Can only except the result of a try")

    def instanceofcall(self, variables):
        """Determines Whether Something Is An Instance Of Something Else."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to from")
        else:
            if isinstance(variables[0], classcalc):
                for x in xrange(1, len(variables)):
                    if not (isinstance(variables[x], instancecalc) and variables[x].isfrom(variables[0])):
                        return 0.0
            else:
                check = self.e.typecalc(variables[0])
                for x in xrange(1, len(variables)):
                    if check != self.e.typecalc(variables[x]):
                        return 0.0
            return 1.0

    def iserrcall(self, variables):
        """Determines Whether Something Is An Error."""
        for item in variables:
            if not (isinstance(item, instancecalc) and item.tryget(self.e.errorvar)):
                return 0.0
        return 1.0

    def classcall(self, variables):
        """Converts To A Class."""
        if not variables:
            return classcalc(self.e)
        else:
            if isinstance(variables[0], instancecalc):
                self.e.overflow = variables[1:]
                return variables[0].toclass()
            elif isinstance(variables[0], classcalc):
                return variables[0]
            else:
                raise ExecutionError("ArgumentError", "Cannot convert non-class to class")

    def getvalcall(self, variables):
        """Calculates A Variable Without Changing It."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to val")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], False, False)
            self.e.setreturned()
            if original in self.e.variables:
                return self.e.funcfind(original)
            else:
                return matrix(0)
        else:
            out = []
            for x in variables:
                out.append(self.getvalcall([x]))
            return diagmatrixlist(out)

    def getparenscall(self, variables):
        """Retreives The Number Of Parentheses."""
        if variables:
            self.e.overflow = variables
        self.e.setreturned()
        return float(len(self.e.parens))

    def getparenvarcall(self, variables):
        """Gets The Value Of A Paren."""
        if not variables:
            variables = [-1]
        if len(variables) == 1:
            original = getint(variables[0])
            if original < 0:
                original += len(self.e.parens)
            self.e.setreturned()
            if 0 < original and original < self.e.parens:
                return rawstrcalc(self.e.prepare(self.e.getparen(original), True, True), self.e)
            else:
                return matrix(0)
        else:
            out = []
            for x in variables:
                out.append(self.getparenvarcall([x]))
            return diagmatrixlist(out)

    def getvarcall(self, variables):
        """Gets The Value Of A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to var")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], False, False)
            self.e.setreturned()
            if original in self.e.variables:
                return rawstrcalc(self.e.prepare(self.e.variables[original], True, True), self.e)
            else:
                return matrix(0)
        else:
            out = []
            for x in variables:
                out.append(self.getvarcall([x]))
            return diagmatrixlist(out)

    def copycall(self, variables):
        """Makes Copies Of Items."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to copy")
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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to cont")
        elif len(variables) == 1:
            return getmatrix(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.getmatrixcall([x]))
            return diagmatrixlist(out)

    def matrixcall(self, variables):
        """Constructs A Matrix."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to matrix")
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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to det")
        elif len(variables) == 1 and isinstance(variables[0], matrix):
            return variables[0].det()
        else:
            value = 1.0
            for v in variables:
                value *= v
            return value

    def listcall(self, variables):
        """Constructs A Matrix List."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to list")
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
        value = 1.0
        for x in variables:
            x = collapse(x)
            if ismatrix(x):
                value *= self.prodcall(getmatrix(x).getitems())
            else:
                value *= x
        return value

    def connectcall(self, variables):
        """Connects Variables."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to connect")
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
        if variables is not None and len(variables) >= 2:
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
        return diagmatrixlist(merge(variables))

    def sizecall(self, variables):
        """Finds A Size."""
        return totlen(diagmatrixlist(variables))

    def lencall(self, variables):
        """Finds A Length."""
        tot = 0.0
        for x in variables:
            try:
                x.getlen
            except AttributeError:
                try:
                    test = len(x)
                except:
                    tot += 1.0
                else:
                    tot += float(test)
            else:
                tot += float(x.getlen())
        return tot

    def rangecall(self, variables):
        """Constructs A Range."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to range")
        elif len(variables) == 1:
            return rangematrix(0.0, collapse(variables[0]))
        elif len(variables) == 2:
            return rangematrix(collapse(variables[0]), collapse(variables[1]))
        else:
            return rangematrix(collapse(variables[0]), collapse(variables[1]), collapse(variables[2]))

    def roundcall(self, variables):
        """Performs round."""
        if not variables:
            return 0.0
        elif len(variables) == 1:
            return round(getnum(variables[0]))
        else:
            return round(getnum(variables[0]), getint(variables[1]))

    def numcall(self, variables, new=True, func=makenum):
        """Performs float."""
        if not variables:
            return 0.0
        elif len(variables) == 1:
            try:
                variables[0].code
            except AttributeError:
                return func(variables[0])
            else:
                if new:
                    out = variables[0].copy()
                else:
                    out = variables[0]
                out.code(lambda x: func(x))
                return out
        else:
            return self.numcall([diagmatrixlist(variables)], False)

    def intcall(self, variables):
        """Performs int."""
        return self.numcall(variables, func=lambda x: float(makeint(x)))

    def realcall(self, variables):
        """Performs Re."""
        return self.numcall(variables, func=getnum)

    def imagcall(self, variables, new=True):
        """Performs Im."""
        if not variables:
            return complex(0.0, 1.0)
        elif len(variables) == 1:
            try:
                variables[0].code
            except AttributeError:
                return getimag(variables[0])
            else:
                if new:
                    out = variables[0].copy()
                else:
                    out = variables[0]
                out.code(lambda x: getimag(x))
                return out
        else:
            return self.imagcall([diagmatrixlist(variables)], False)

    def splitcall(self, variables):
        """Performs split."""
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
                        new.append(rawstrcalc(temp, self))
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
                return rawstrcalc(new, self)
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
        if not variables:
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
        if not variables:
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
            return self.reversecall([self.connectcall(variables)])

    def containscall(self, variables):
        """Performs contains."""
        if variables:
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

    def typecall(self, variables):
        """Finds Types."""
        if len(variables) == 0:
            return self.e.typecalc(matrix(0))
        elif len(variables) == 1:
            return self.e.typecalc(variables[0])
        else:
            out = []
            for x in variables:
                out.append(self.e.typecalc(x))
            return diagmatrixlist(out)

    def tocall(self, variables, varstrings="xyzwpqrabchjklmnABCFGHJKMNOQRTUVWXYZ"):
        """Returns A Converter Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to to")
        elif len(variables) == 1:
            if isinstance(variables[0], (strcalc, funcfloat)):
                variables[0] = self.typestr(variables[0])
                if variables[0] in self.e.variables and isinstance(self.e.variables[variables[0]], funcfloat):
                    return self.e.variables[variables[0]]
                elif variables[0] in self.e.variables and (istext(variables[0]) or isnum(variables[0]) or isinstance(self.e.variables[variables[0]], bool) or (iseval(value) and not hascall(value))):
                    return strfloat(variables[0], self.e, [])
                else:
                    return strfunc(variables[0]+":"+varstrings[0], self.e, [varstrings[0]])
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
                raise ExecutionError("ValueError", "Unable to create a converter for "+repr(variables[0]))
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

    def codecall(self, variables):
        """Converts To Code."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to code")
        elif len(variables) == 1:
            return codestr(self.e.prepare(variables[0], True, False), self.e)
        else:
            out = []
            for arg in variables:
                out.append(self.codecall([arg]))
            return diagmatrixlist(out)

    def strcall(self, variables):
        """Finds A String."""
        out = []
        for x in variables:
            out.append(self.e.prepare(x, True, False))
        return rawstrcalc(strlist(out, ""), self.e)

    def reprcall(self, variables):
        """Finds A Representation."""
        out = []
        for x in variables:
            out.append(self.e.prepare(x, False, True))
        return rawstrcalc(strlist(out, ""), self.e)

    def joincall(self, variables):
        """Joins Variables By A Delimiter."""
        if len(variables) < 2:
            return rawstrcalc("", self.e)
        else:
            delim = self.e.prepare(variables[0], True, False)
            out = ""
            for x in xrange(1, len(variables)):
                item = variables[x]
                if ismatrix(item):
                    out += self.joincall([delim]+getmatrix(item).getitems()).calcstr
                else:
                    out += self.e.prepare(item, True, False)
                out += delim
            return rawstrcalc(out[:-len(delim)], self.e)

    def abscall(self, variables):
        """Performs abs."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to abs")
        elif len(variables) == 1:
            return abs(variables[0])
        else:
            return self.abscall([diagmatrixlist(variables)])

    def datacall(self, variables):
        """Performs data."""
        if len(variables) == 1 and isinstance(variables[0], data):
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
        if not variables:
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
        out = self.fractcall(variables, True)
        out.simplify()
        return out

    def docalc(self, variables):
        """Performs calc."""
        out = []
        for x in variables:
            inputstring = self.e.prepare(x, False, False)
            out.append(self.e.calc(inputstring, " | calc"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def evalcall(self, variables):
        """Performs eval."""
        out = []
        e = self.e.new()
        for x in variables:
            inputstring = self.e.prepare(x, False, False)
            out.append(self.e.calc(inputstring, " | eval"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def cmdcall(self, variables):
        """Performs proc."""
        for item in variables:
            inputstring = self.e.prepare(item, False, False)
            self.e.processor.evaltext(inputstring)
        return matrix(0)

    def foldcall(self, variables, func=None, overflow=True):
        """Folds A Function Over A Matrix."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to fold")
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
                    if start is None:
                        start = items.pop(0)
                    for x in items:
                        start = func([start, x])
                    return start
            elif start is not None:
                return func([start, item])
            else:
                return item

    def derivcall(self, variables):
        """Returns The nth Derivative Of A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to D")
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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to S")
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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to d")
        else:
            stop = getnum(variables[0])
            key = None
            if len(variables) > 1:
                key = self.e.prepare(variables[1], True, False)
                self.e.overflow = variables[2:]
            self.e.setreturned()
            return rollfunc(stop, self.e, key)

    def writecall(self, variables):
        """Writes To A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to write")
        elif len(variables) == 2:
            name = self.e.prepare(variables[0], False, False)
            if len(variables) == 1:
                writer = ""
            else:
                writer = self.e.prepare(variables[1], False, False)
            self.e.setreturned()
            with openfile(name, "wb") as f:
                writefile(f, writer)
            return matrix(0)
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to write")

    def readcall(self, variables):
        """Reads From A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to read")
        elif len(variables) == 1:
            name = self.e.prepare(variables[0], False, False)
            self.e.setreturned()
            with openfile(name) as f:
                return rawstrcalc(readfile(f), self.e)
        else:
            out = []
            for x in variables:
                out.append(self.readcall([x]))
            return diagmatrixlist(out)

    def defcall(self, variables):
        """Defines A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to def")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], True, False)
            redef, self.e.redef = self.e.redef, True
            try:
                out = self.e.calc(original, " | def")
            finally:
                self.e.redef = redef
            self.e.setreturned()
            return out
        else:
            out = []
            for arg in variables:
                out.append(self.defcall([arg]))
            return diagmatrixlist(out)

    def globalcall(self, variables):
        """Defines A Global Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to def")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], True, False)
            useclass, self.e.useclass = self.e.useclass, False
            try:
                out = self.e.calc(original, " | global")
            finally:
                self.e.useclass = useclass
            self.e.setreturned()
            return out
        else:
            out = []
            for arg in variables:
                out.append(self.globalcall([arg]))
            return diagmatrixlist(out)

    def aliascall(self, variables):
        """Makes Aliases."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to alias")
        elif len(variables) == 1:
            key = self.e.prepare(variables[0], True, False)
            self.e.setreturned()
            if key in self.e.aliases:
                out = rawstrcalc(self.e.aliases[key], self.e)
                del self.e.aliases[key]
            else:
                out = matrix(0)
            return out
        elif len(variables) == 2:
            key = self.e.prepare(variables[0], True, False)
            value = self.e.prepare(variables[1], True, False)
            self.e.setreturned()
            self.e.aliases[key] = value
            return diagmatrixlist([rawstrcalc(key, self.e), rawstrcalc(value, self.e)])
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to alias")
