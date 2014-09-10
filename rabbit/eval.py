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

class Evaluate(BaseException):
    """A Stack-Killer Evaluation Exception."""
    def __init__(self, arg, funcs):
        """Creates The Evaluation."""
        self.arg = arg
        self.funcs = funcs

def matrixconstructor(self, args):
    """Reconstructs A Matrix."""
    value = matrix(args[1], args[2], converter=args[3], fake=args[4])
    for y in xrange(0, len(args[0])):
        for x in xrange(0, len(args[0][y])):
            value.store(y,x, self.deitem(args[0][y][x]))
    return value

class evaluator(object):
    """Evaluates Equations And Expressions.

Global Operator Precedence List:
    "       Opens and closes strings.
    `       Opens and closes raw strings.
    ()      Opens and closes parentheses.
    \xab\xbb      Opens and closes code blocks.
    {}      Opens and closes dictionaries.
    []      Opens and closes matrix rows.

    ;;      Separates top-level commands.

    $       Seperates with clauses (read as 'with' or 'where').
    ::      Calls a meta-function.

    ,       Seperates list elements.
    ->      Creates a key-value pair.
    ;       Seperates conditionals (read as 'else').
    @       Checks a conditional (read as 'at' or 'if').
    ?!      Performs logical unary operations.
    |       Performs logical or.
    &       Performs logical and.
    >?!=<   Performs equality or inequality checks.

    ~       Applies a list to a function for looping.
    \\       Creates a lambda.
    --      Performs removal.
    ++      Performs concatenation.
    **      Performs repeat.
    +-      Performs addition and subtraction.
    %       Performs modulo.
    //      Performs floor division.
    */      Performs multiplication and division.

    \u03bb       Denotes a lambda.
    -       Denotes negatives.
    /       Denotes reciprocals.
    ^       Performs exponentiation.
    :       Performs function calls.
    \xa7       Denotes parentheses.
    ..      Performs function composition.
    .       Denotes methods and functions of functions.
    normal  Evaluates numbers."""
    constructors = {
        "atom": lambda self, args: atom(),
        "reciprocal": lambda self, args: reciprocal(self.deitem(args[0])),
        "negative": lambda self, args: negative(self.deitem(args[0])),
        "fraction": lambda self, args: fraction(self.deitem(args[0]), self.deitem(args[1])),
        "pair": lambda self, args: pair(self, self.deitem(args[0]), self.deitem(args[1])),
        "dictionary": lambda self, args: dictionary(self, self.devariables(args[0])),
        "data": lambda self, args: data(args[0], args[1]),
        "multidata": lambda self, args: multidata(args[0], args[1]),
        "rollfunc": lambda self, args: rollfunc(args[0], self, args[1], args[2], args[3]),
        "matrix": matrixconstructor,
        "strfunc": lambda self, args: strfunc(args[0], self, args[1], self.devariables(args[2]), args[3], args[4], args[5], args[6], args[7], self.devariables(args[8]), args[9]),
        "codestr": lambda self, args: codestr(args[0], self),
        "strcalc": lambda self, args: rawstrcalc(args[0], self),
        "derivfunc": lambda self, args: derivfunc(args[0], args[1], args[2], args[3], self, args[4], args[5], args[6], args[7], self.devariables(args[8])),
        "integfunc": lambda self, args: integfunc(args[0], args[1], self, args[2], args[3], args[4], self.devariables(args[5])),
        "usefunc": lambda self, args: usefunc(args[0], self, args[1], args[2], args[3], args[4], args[5], args[6], args[7], self.devariables(args[8])),
        "classcalc": lambda self, args: classcalc(self, self.devariables(args[0])),
        "namespace": lambda self, args: namespace(self, self.devariables(args[0])),
        "instancecalc": lambda self, args: instancecalc(self, self.devariables(args[0]), top=False),
        "makefunc": lambda self, args: makefunc(args[0], self, args[1], args[2], self.devariables(args[3])),
        "brace": lambda self, args: brace(self, args[0]),
        "bracket": lambda self, args: bracket(self, args[0])
        }
    testers = {
        }
    tempobjects = negative, reciprocal
    varname = "x"
    directchar = "\xb6"
    indentchar = "\u2021"
    dedentchar = "\u2020"
    formatchars = directchar + indentchar + dedentchar
    parenchar = "\xa7"
    aliases = {
        "<<":"\xab",
        ">>":"\xbb",
        "\t":"    "
        }
    rawstringchars = "`"
    lambdachars = "\\"
    stringchars = rawstringchars + lambdachars + '"'
    strgroupers = {
        "\u201c":"\u201d"
        }
    groupers = {
        "(":")",
        "\xab":"\xbb",
        "{":"}",
        "[":"]"
        }
    unary = "!?"
    bools = unary + "<>=\u2260"
    lambdamarker = "\u03bb"
    subparenops = ".^"
    callops = subparenops + lambdamarker + "%/*:"
    calcops = "$"
    multiargops = bools + callops + "+-@~|&;," + calcops + "".join(strgroupers.keys()) + "".join(groupers.keys()) + "".join(aliases.keys())
    reserved = string.digits + multiargops + stringchars + "".join(strgroupers.values()) + "".join(groupers.values()) + parenchar + formatchars
    errorvar = "__error__"
    fatalvar = "fatal"
    namevar = "name"
    messagevar = "message"
    autoarg = "____"
    recursion = 0
    redef = False
    useclass = None
    returned = True
    spawned = True
    calculated = None
    using = None
    pure = False
    clean = False
    all_clean = False
    tailing = False

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
        self.setup()
        self.fresh()
        if variables is not None:
            self.makevars(variables)

    def new(self):
        """Makes A New Identically-Configured Evaluator."""
        return evaluator(None, self.processor, self.color, self.speedy, self.maxrecursion)

    @property
    def overflow(self):
        """Gets The Overflow."""
        return self._overflow

    @overflow.setter
    def overflow(self, inputlist):
        """Sets The Overflow."""
        if inputlist:
            self.unclean()
        self._overflow = inputlist

    def setup(self):
        """Performs Basic Setup."""
        self._overflow = []
        self.debuglog = []
        self.preprocs = [
            self.preproc_alias,
            self.preproc_string,
            self.preproc_format,
            self.preproc_indent
            ]
        self.precalcs = [
            self.precalc_paren,
            self.precalc_block,
            self.precalc_dict,
            self.precalc_brack
            ]
        self.calc_funcs = [
            self.calc_cmd,
            self.calc_format,
            self.calc_set,
            self.calc_with,
            self.calc_list,
            self.calc_pair,
            self.calc_pieces,
            self.calc_condo,
            self.calc_or,
            self.calc_and,
            self.calc_unary,
            self.calc_eq,
            self.calc_eval
            ]
        self.sets = [
            self.set_def,
            self.set_normal
            ]
        self.eval_splits = [
            ("~", True),
            (self.lambdamarker, False),
            ("--", True),
            ("++", True),
            ("**", True),
            ("+", True, ["-", self.callops, 2]),
            ("%", True),
            ("//", True),
            ("*", True, ["/"])
            ]
        self.eval_funcs = [
            self.eval_loop,
            self.eval_lambda,
            self.eval_remove,
            self.eval_join,
            self.eval_repeat,
            self.eval_add,
            self.eval_mod,
            self.eval_intdiv,
            self.eval_mul,
            self.eval_call
            ]
        self.calls = [
            self.call_parenvar,
            self.call_var,
            self.call_lambda,
            self.call_neg,
            self.call_reciproc,
            self.call_colon,
            self.call_paren,
            self.call_exp,
            self.call_comp,
            self.call_lambdacoeff,
            self.call_method,
            self.call_normal
            ]
        self.funcs = evalfuncs(self)

    def fresh(self):
        """Resets The Variables To Their Defaults."""
        self.parens = []
        self.variables = {
            "Warning":classcalc(self, {
                self.errorvar: 1.0,
                self.fatalvar: 0.0
                }),
            "Error":classcalc(self, {
                self.errorvar: 1.0,
                self.fatalvar: 1.0
                }),
            "pure":funcfloat(self.funcs.purecall, self, "pure", reqargs=1),
            "env":funcfloat(self.funcs.envcall, self, "env"),
            "call":funcfloat(self.funcs.callcall, self, "call", reqargs=1),
            "copy":funcfloat(self.funcs.copycall, self, "copy", reqargs=1),
            "type":funcfloat(self.funcs.typecall, self, "type"),
            "to":funcfloat(self.funcs.tocall, self, "to", reqargs=1),
            "str":funcfloat(self.funcs.strcall, self, "str"),
            "repr":funcfloat(self.funcs.reprcall, self, "repr"),
            "code":funcfloat(self.funcs.codecall, self, "code"),
            "calc":funcfloat(self.funcs.docalc, self, "calc", reqargs=1),
            "exec":funcfloat(self.funcs.cmdcall, self, "exec", reqargs=1),
            "fold":funcfloat(self.funcs.foldcall, self, "fold", reqargs=1),
            "row":funcfloat(rowmatrixlist, self, "row"),
            "list":funcfloat(self.funcs.listcall, self, "list", reqargs=1),
            "matrix":funcfloat(self.funcs.matrixcall, self, "matrix", reqargs=1),
            "cont":funcfloat(self.funcs.getmatrixcall, self, "cont", reqargs=1),
            "sum":funcfloat(self.funcs.sumcall, self, "sum", reqargs=1),
            "prod":funcfloat(self.funcs.prodcall, self, "prod", reqargs=1),
            "min":funcfloat(self.funcs.mincall, self, "min", reqargs=1),
            "max":funcfloat(self.funcs.maxcall, self, "max", reqargs=1),
            "join":funcfloat(self.funcs.joincall, self, "join", reqargs=2),
            "connect":funcfloat(self.funcs.connectcall, self, "connect", reqargs=1),
            "merge":funcfloat(self.funcs.mergecall, self, "merge", reqargs=1),
            "sort":funcfloat(self.funcs.sortcall, self, "sort", reqargs=1),
            "rev":funcfloat(self.funcs.reversecall, self, "rev", reqargs=1),
            "round":funcfloat(self.funcs.roundcall, self, "round", reqargs=1),
            "num":funcfloat(self.funcs.numcall, self, "num"),
            "int":funcfloat(self.funcs.intcall, self, "int"),
            "base":funcfloat(self.funcs.basecall, self, "base", reqargs=2),
            "bin":funcfloat(self.funcs.bincall, self, "bin", reqargs=1),
            "oct":funcfloat(self.funcs.octcall, self, "oct", reqargs=1),
            "hex":funcfloat(self.funcs.hexcall, self, "hex", reqargs=1),
            "pair":funcfloat(self.funcs.paircall, self, "pair"),
            "dict":funcfloat(self.funcs.dictcall, self, "dict"),
            "eval":funcfloat(self.funcs.evalcall, self, "eval", reqargs=1),
            "find":funcfloat(self.funcs.findcall, self, "find", reqargs=2),
            "split":funcfloat(self.funcs.splitcall, self, "split", reqargs=1),
            "replace":funcfloat(self.funcs.replacecall, self, "replace", reqargs=1),
            "in":funcfloat(self.funcs.containscall, self, "in", reqargs=2),
            "range":funcfloat(self.funcs.rangecall, self, "range", reqargs=1),
            "len":funcfloat(self.funcs.lencall, self, "len", reqargs=1),
            "size":funcfloat(self.funcs.sizecall, self, "size", reqargs=1),
            "abs":funcfloat(self.funcs.abscall, self, "abs", reqargs=1),
            "from":funcfloat(self.funcs.instanceofcall, self, "from", reqargs=2),
            "iserr":funcfloat(self.funcs.iserrcall, self, "iserr", reqargs=1),
            "class":funcfloat(self.funcs.classcall, self, "class"),
            "namespace":funcfloat(self.funcs.namespacecall, self, "namespace"),
            "try":funcfloat(self.funcs.trycall, self, "try"),
            "raise":funcfloat(self.funcs.raisecall, self, "raise"),
            "except":funcfloat(self.funcs.exceptcall, self, "except"),
            "read":funcfloat(self.funcs.readcall, self, "read", reqargs=1),
            "write":funcfloat(self.funcs.writecall, self, "write", reqargs=1),
            "is":funcfloat(self.funcs.iseqcall, self, "is", reqargs=2),
            "include":funcfloat(self.funcs.includecall, self, "include", reqargs=1),
            "del":funcfloat(self.funcs.delcall, self, "del", reqargs=1),
            "def":funcfloat(self.funcs.defcall, self, "def", reqargs=1),
            "global":funcfloat(self.funcs.globalcall, self, "global", reqargs=1),
            "effect":usefunc(self.setreturned, self, "effect"),
            "run":funcfloat(self.funcs.runcall, self, "run", reqargs=1),
            "require":funcfloat(self.funcs.requirecall, self, "require", reqargs=1),
            "assert":funcfloat(self.funcs.assertcall, self, "assert"),
            "install":funcfloat(self.funcs.installcall, self, "install", reqargs=1),
            "bitnot":funcfloat(self.funcs.bitnotcall, self, "bitnot", reqargs=1),
            "bitor":funcfloat(self.funcs.bitorcall, self, "bitor", reqargs=2),
            "bitand":funcfloat(self.funcs.bitandcall, self, "bitand", reqargs=2),
            "bitxor":funcfloat(self.funcs.bitxorcall, self, "bitxor", reqargs=2),
            "rshift":funcfloat(self.funcs.rshiftcall, self, "rshift", reqargs=2),
            "lshift":funcfloat(self.funcs.lshiftcall, self, "lshift", reqargs=2),
            "union":funcfloat(self.funcs.unioncall, self, "union", reqargs=2),
            "intersect":funcfloat(self.funcs.intersectcall, self, "intersect", reqargs=2),
            "rand":funcfloat(self.funcs.randcall, self, "rand", reqargs=1),
            "Meta":classcalc(self, {
                "var":funcfloat(self.funcs.getvarcall, self, "var", reqargs=1),
                "val":funcfloat(self.funcs.getvalcall, self, "val", reqargs=1),
                "use":funcfloat(self.funcs.usecall, self, "use"),
                "using":funcfloat(self.funcs.usingcall, self, "using"),
                "alias":funcfloat(self.funcs.aliascall, self, "alias", reqargs=1),
                "aliases":funcfloat(self.funcs.aliasescall, self, "aliases"),
                "paren":funcfloat(self.funcs.getparenvarcall, self, "paren"),
                "parens":funcfloat(self.funcs.getparenscall, self, "parens")
                }, name="Meta"),
            "Math":classcalc(self, {
                "pow":usefunc(pow, self, "pow", ["y", "x", "m"]),
                "data":funcfloat(self.funcs.datacall, self, "data"),
                "frac":funcfloat(self.funcs.fractioncall, self, "frac"),
                "simp":funcfloat(self.funcs.simpcall, self, "simp"),
                "det":funcfloat(self.funcs.detcall, self, "det", reqargs=1),
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
                "rad":usefunc(math.degrees, self, "rad", ["x"]),
                "deg":usefunc(math.radians, self, "deg", ["x"]),
                "fact":usefunc(factorial, self, "fact", ["x"]),
                "gcd":usefunc(gcd, self, "gcd", ["x", "y"]),
                "lcm":usefunc(lcm, self, "lcm", ["x", "y"]),
                "perm":usefunc(perm, self, "perm", ["n", "k"]),
                "comb":usefunc(comb, self, "comb", ["n", "k"]),
                "real":funcfloat(self.funcs.realcall, self, "real"),
                "imag":funcfloat(self.funcs.imagcall, self, "imag"),
                "e":math.e,
                "pi":math.pi,
                "E":usefunc(E10, self, "E", ["x"]),
                "D":funcfloat(self.funcs.derivcall, self, "D", reqargs=1),
                "S":funcfloat(self.funcs.integcall, self, "S", reqargs=1),
                "i":complex(0.0, 1.0)
                }, name="Math"),
            "Stats":classcalc(self, {
                "gamma":usefunc(gamma, self, "gamma", ["x"]),
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
                }, name="Stats"),
            "none":matrix(0),
            "true":1.0,
            "false":0.0,
            "_":atom(),
            funcfloat.allargs : matrix(0)
            }
        self.variables.update({
            "prop":strfunc("class\xab__value__(self,getter:getter)=getter()\xbb()", self, ["getter"], name="prop"),
            "inside":strfunc("\\__,begin:begin,end:end\\(out$end()$out=calc(__)$begin())", self, ["begin", "end"], name="inside"),
            "Unicode":classcalc(self, {
                "__include__" : strfunc("""self.includes$self.aliases~~Meta.alias""", self, ["self"], name="__include__"),
                "aliases" : self.frompython({
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
                    "\u2044":"/",
                    "\u2237":"::",
                    "\u2192":"->",
                    "\u2254":":=",
                    "\u225f":"?="
                    }),
                "includes" : classcalc(self, {
                    "\xf8" : "none",
                    "\u221e" : "inf",
                    "\u2211" : "sum",
                    "\u03c0" : "Math.pi",
                    "\u221a" : "Math.sqrt",
                    "\u222b" : "Math.S",
                    "\u0393" : "Stats.gamma",
                    "\u220f" : "prod",
                    "\u2208" : "in",
                    "\u230a" : "min",
                    "\u2308" : "max",
                    "\xb0" : "Math.deg",
                    "\u22d8" : "lshift",
                    "\u22d9" : "rshift",
                    "\u22c3" : "union",
                    "\u22c2" : "intersect",
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
                    "\u2421" : rawstrcalc("\x21", self),
                    "\u2209" : strfunc("!\u2208(__)", self, name="\u2209", overflow=False),
                    "\u220b" : strfunc("\u2208(rev(__))", self, name="\u220b", overflow=False),
                    "\u220c" : strfunc("!\u220b(__)", self, name="\u220c", overflow=False),
                    "\u221b" : strfunc("x^(1/3)", self, ["x"], name="\u221b"),
                    "\u221c" : strfunc("Math.sqrt(Math.sqrt(x))", self, ["x"], name="\u221c"),
                    "\u222c" : strfunc("Math.S((Math.S((f,)++args),)++args)", self, ["f", "args"], reqargs=1, name="\u222c"),
                    "\u222d" : strfunc("Math.S((\u222c((f,)++args),)++args)", self, ["f", "args"], reqargs=1, name="\u222d")
                    })
                }, name="Unicode").call([])
            })

    def setreturned(self, value=True):
        """Sets returned."""
        value = bool(value)
        if value and self.pure:
            raise ExecutionError("PureError", "A pure statement attempted to produce a side effect")
        self.returned = value

    def setspawned(self, value=True):
        """Sets spawned."""
        value = bool(value)
        if value:
            self.setreturned()
        self.spawned = value

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

    def getcall(self, item):
        """Gets The Callable Part Of An Item."""
        return getcall(item, self)

    def forshow(self, arg):
        """Prepares An Item For Showing."""
        if not istext(arg):
            return self.prepare(arg, True, True, 2)
        else:
            return str(arg)

    def speedyprep(self, item, top=False, bottom=False, indebug=False, maxrecursion=0):
        """Speedily Prepares The Output Of An Evaluation."""
        out = "class \xab"+"\n"*top
        if not indebug and bottom and not top:
            out += 'raise("RuntimeError", "Maximum recursion depth exceeded in object preparation")'
        else:
            out += " __type__ "
            if istext(item):
                out += "= "+str(item)
            else:
                out += ":= `"+self.evaltypestr(item)+"`"
        out += "\n"*top+" \xbb"
        return out

    def prepare(self, item, top=False, bottom=True, indebug=False, maxrecursion=None):
        """Prepares The Output Of An Evaluation."""
        if maxrecursion is None:
            maxrecursion = self.maxrecursion
        if istext(item):
            out = str(item)
        elif item is None:
            out = "none"
        elif isinstance(item, bool):
            if item:
                out = "true"
            else:
                out = "false"
        elif isinstance(item, complex):
            out = ""
            if item.real != 0:
                out += self.prepare(item.real, False, bottom, indebug, maxrecursion)+"+"
            if item.imag == 1:
                out += "i"
            else:
                out += self.prepare(item.imag, False, bottom, indebug, maxrecursion)+"*i"
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
        elif self.speedy and indebug:
            out = self.speedyprep(item, top, bottom, True, maxrecursion)
        elif isinstance(item, (data, multidata)):
            if bottom:
                out = "data:(" + self.prepare(getmatrix(item), False, True, indebug, maxrecursion) + ")"
            else:
                out = self.prepare(getmatrix(item), top, bottom, indebug, maxrecursion)
        elif isinstance(item, matrix):
            if item.y == 0:
                out = "()"
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
        elif isinstance(item, dictionary):
            out = "{"
            if top:
                out += "\n"
            for k,v in item.a.items():
                out += " "+self.prepare(pair(self,k,v), False, bottom, indebug, maxrecursion)+","
                if top:
                    out += "\n"
                else:
                    out += " "
            if not item.a:
                if top:
                    out = out[:-1]
            else:
                out = out[:-2]
                if top:
                    out += "\n"
            out += " }"
        elif isinstance(item, negative):
            out = "-"+self.prepare(item.n, top, bottom, indebug, maxrecursion)
        elif isinstance(item, reciprocal):
            out = "/"+self.prepare(item.d, top, bottom, indebug, maxrecursion)
        elif isinstance(item, (fraction, pair)):
            if isinstance(item, pair):
                part_a = item.k
            else:
                part_a = item.n
            if isinstance(item, pair):
                part_b = item.v
            else:
                part_b = item.d
            out = ""
            a = self.prepare(part_a, False, bottom, indebug, maxrecursion)
            if not bottom or madeof(a, string.digits) or not self.isreserved(a):
                out += a
            else:
                out += "("+a+")"
            if isinstance(item, pair):
                out += " -> "
            else:
                out += "/"
            b = self.prepare(part_b, False, bottom, indebug, maxrecursion)
            if not bottom or madeof(b, string.digits) or not self.isreserved(b):
                out += b
            else:
                out += "("+b+")"
        elif bottom and isinstance(item, rollfunc):
            out = "rand:"+self.prepare(item.stop, False, bottom, indebug, maxrecursion)
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
                out = out[:-1]
            out += "\\"
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
                out = "\\\\"+str(item)
        elif hasattr(item, "getrepr"):
            out = item.getrepr(top, bottom, indebug, maxrecursion-1)
        elif getcheck(item) >= 1:
            out = str(item)
        elif indebug:
            if indebug > 1:
                out = str(item)
            else:
                out = repr(item)
        else:
            raise ExecutionError("DisplayError", "Unable to display "+repr(item))
        return str(out)

    def insideouter(self, inputstring, groupers=None):
        """Determines If Inside A String Or Grouper."""
        if groupers is None:
            groupers = self.groupers
        return isinside(inputstring, self.stringchars, self.strgroupers, groupers)

    def outersplit(self, inputstring, splitstring, groupers=None, top=True):
        """Splits By Something Not In A String Or Grouper."""
        if groupers is None:
            groupers = self.groupers
        if top:
            return carefulsplit(inputstring, splitstring, self.stringchars, self.strgroupers, groupers)
        else:
            return carefulsplit(inputstring, splitstring, closers=groupers)

    def remcomment(self, inputstring, commentstring="#"):
        """Removes A Comment."""
        return basicformat(self.outersplit(inputstring, commentstring, {})[0], leading=False)

    def setcalculated(self, result):
        """Sets calculated."""
        self.calculated = result

    def remformat(self, inputstring):
        """Removes All Formatting."""
        return delspace(inputstring, self.formatchars)

    def splitdedent(self, inputstring, splitfunc=lambda x: x.split("\n"), top=True):
        """Splits And Unsplits By Dedents."""
        inputstring = str(inputstring)
        split = fullsplit(inputstring, self.indentchar, self.dedentchar, 1, not top, iswhite, True)
        if not top or len(split) > 1 or (split and istext(split[0])):
            out = []
            join = False
            for item in split:
                new = None
                new_join, join = join, False
                if istext(item):
                    new = splitfunc(item)
                elif len(item) == 1:
                    while not istext(new):
                        if istext(item[0]):
                            new = item[0]
                        elif len(item[0]) == 1:
                            new = item[0][0]
                        else:
                            raise SyntaxError("Error in evaluating indentation len("+repr(item[0])+")>1")
                    join = True
                elif item:
                    raise SyntaxError("Error in evaluating indentation len("+repr(item)+")>1")
                else:
                    join = True
                if new is not None:
                    if new_join:
                        if istext(new):
                            out[-1] += new
                        elif new:
                            out[-1] += new[0]
                            out += new[1:]
                    elif not istext(new):
                        out += new
                    elif out:
                        out[-1] += new
                    else:
                        out.append(new)
        elif not split or not split[0]:
            out = [""]
        elif len(split[0]) == 1:
            item = split[0]
            new = None
            while not istext(new):
                if istext(item[0]):
                    new = item[0]
                elif len(item[0]) == 1:
                    new = item[0][0]
                else:
                    raise SyntaxError("Error in evaluating indentation len("+repr(item[0])+")>1")
            out = self.splitdedent(new, splitfunc, False)
        else:
            raise SyntaxError("Error in evaluating indentation len("+repr(split[0])+")>1")
        return out

    def iseq(self, a, b):
        """Determines Whether Two Evaluator Objects Are Really Equal."""
        return type(a) is type(b) and itemstate(a) == itemstate(b)

    def wrap(self, item):
        """Wraps An Item In Parentheses."""
        for x in xrange(0, len(self.parens)):
            if self.iseq(self.parens[x], item):
                return self.parenchar+str(x)+self.parenchar
        indexstr = self.parenchar+str(len(self.parens))+self.parenchar
        self.parens.append(item)
        return indexstr

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

    def calc(self, inputstring, info=""):
        """Performs Top-Level Calculation."""
        inputstring = str(inputstring)
        calculated, self.calculated = self.calculated, matrix(0)
        self.process(inputstring, info, self.setcalculated, False)
        out, self.calculated = self.calculated, calculated
        return out

    def process(self, inputstring, info="", command=None, top=None):
        """Performs Top-Level Evaluation."""
        inputstring = str(inputstring)
        if top is None:
            top = command is not None
        else:
            top = top
        if info is None:
            info = " <<"+"-"*(70-len(inputstring)-2*self.recursion)
        else:
            info = str(info)
        if top:
            self.printdebug(">>> "+inputstring+info)
            self.recursion += 1
            spawned = self.spawned
            self.setspawned(False)
            tailing, self.tailing = self.tailing, False
            cleaned = self.clean_begin(True, True)
        else:
            self.printdebug(":>> "+inputstring+info)
            self.recursion += 1
            cleaned = self.clean_begin(None, None)
        try:
            self.proc_calc(inputstring, top, command)
        finally:
            if top:
                if not self.spawned:
                    self.processor.addcommand(inputstring)
                self.setspawned(self.spawned or spawned)
                self.tailing = tailing
            self.clean_end(cleaned)
            self.recursion -= 1

    def do_pre(self, item, top):
        """Does The Pre-Processing."""
        for func in self.preprocs:
            item = func(item, top)
        for func in self.precalcs:
            item = func(item)
        return item

    def proc_calc(self, original, top, command):
        """Gets The Value Of An Expression."""
        item = self.do_pre(original, top)
        self.printdebug("| "+str(item))
        if top:
            splitfunc = lambda x: splitany(x, [";;", "\n"])
        else:
            splitfunc = lambda x: x.split(";;")
        inputlist = []
        for original in self.splitdedent(item, splitfunc):
            original = basicformat(original)
            if not iswhite(original):
                inputlist.append(original)
        cleaned = self.clean_begin()
        for x in xrange(0, len(inputlist)):
            if x == len(inputlist)-1:
                self.clean_end(cleaned)
            self.printdebug("=>> "+inputlist[x])
            self.recursion += 1
            out = self.calc_proc(inputlist[x], top)
            self.printdebug(self.prepare(out, False, True, True)+" <<= "+inputlist[x])
            self.recursion -= 1
            if command is not None:
                command(out)

    def calc_proc(self, inputstring, top=True):
        """Calculates Use Functions."""
        if top and self.using:
            func = self.prepare(self.using, False, True, True)
            original = func+" :: "+inputstring
            self.printdebug("::> "+original)
            self.recursion += 1
            out = self.getcall(self.using)([codestr(inputstring, self)])
            self.printdebug(self.prepare(out, False, True, True)+" <:: "+original)
            self.recursion -= 1
            return out
        else:
            return self.calc_next(inputstring, self.calc_funcs, True)

    def preproc_alias(self, inputstring, top=True):
        """Applies Aliases."""
        if top:
            out = replaceall(inputstring, self.aliases, self.stringchars, self.strgroupers)
        else:
            out = inputstring
        return out

    def preproc_string(self, expression, top=None):
        """Evaluates The String Part Of An Expression."""
        toplist = eithersplit(expression, self.stringchars, self.strgroupers)
        command = ""
        for item in toplist:
            if istext(item):
                command += item
            elif item[0] in self.lambdachars:
                value = self.do_pre(item[1], True)
                if value:
                    command += self.lambdamarker+self.wrap(value)+self.lambdamarker
                else:
                    command += self.lambdamarker*2
            elif item[0] in self.rawstringchars:
                command += self.wrap(rawstrcalc(item[1], self))
            elif item[0] in self.stringchars + "".join(self.strgroupers.keys()) + "".join(self.strgroupers.values()):
                command += self.wrap(strcalc(item[1], self))
        return command

    def preproc_format(self, inputstring, top=None):
        """Performs Pre-Formatting."""
        out = []
        for line in inputstring.splitlines():
            out.append(self.remcomment(line))
        return "\n".join(out)

    def preproc_indent(self, inputstring, top=True):
        """Evaluates Indentation."""
        if top:
            inputlist = inputstring.split(self.directchar)
            out = []
            for x in xrange(0, len(inputlist)):
                if x%2 == 0:
                    lines = []
                    for line in inputlist[x].splitlines():
                        if not iswhite(line):
                            lines.append(line)
                    if not lines:
                        lines.append("")
                    new = []
                    levels = []
                    openstr, closestr = self.indentchar, self.dedentchar
                    for x in xrange(0, len(lines)):
                        check = leading(lines[x])
                        if levels:
                            if check > levels[-1]:
                                levels.append(check)
                                lines[x-1] = lines[x-1]+openstr
                            elif check in levels:
                                point = levels.index(check)+1
                                closers = closestr*(len(levels[point:]))
                                newline = ""
                                for c in lines[x-1]:
                                    if c in self.groupers.values():
                                        newline += closers+c
                                        closers = ""
                                    else:
                                        newline += c
                                lines[x-1] = newline+closers
                                levels = levels[:point]
                            else:
                                raise ExecutionError("IndentationError", "Illegal dedent to unused indentation level in line "+lines[x]+" (#"+str(x)+")")
                            new.append(lines[x-1])
                        else:
                            levels.append(check)
                    new.append(lines[-1]+closestr*(len(levels)-1))
                    out.append("\n".join(new))
                else:
                    out.append(inputlist[x])
            return "".join(out)
        else:
            return inputstring

    def precalc_paren(self, expression):
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

    def precalc_block(self, expression):
        """Creates A Code Block."""
        blocklist = fullsplit(expression, "\xab", "\xbb", 1)
        command = ""
        for x in blocklist:
            if istext(x):
                command += x
            elif not x:
                command += self.wrap(codestr("", self))
            elif len(x) == 1:
                command += self.wrap(codestr(x[0], self))
            else:
                raise SyntaxError("Error in evaluating block len("+repr(x)+")>1")
        return command

    def precalc_dict(self, expression):
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
                command += self.wrap(brace(self, self.splitdedent(original, lambda x: x.split(","))))
            else:
                raise SyntaxError("Error in evaluating braces len("+repr(x)+")>1")
        return command

    def precalc_brack(self, expression):
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
                command += self.wrap(bracket(self, self.splitdedent(original, lambda x: x.split(","))))
            else:
                raise SyntaxError("Error in evaluating brackets len("+repr(x)+")>1")
        return command

    def calc_next(self, arg, funcs, top=False):
        """Calls The Next Function."""
        while True:
            funcs = funcs[:]
            if top:
                func = funcs.pop(0)
                if funcs:
                    cleaned = self.clean_begin(True, None)
                    try:
                        return func(arg, funcs)
                    except Evaluate as params:
                        arg = params.arg
                        funcs = params.funcs
                    finally:
                        self.clean_end(cleaned)
                else:
                    cleaned = self.clean_begin(None, None)
                    out = func(arg)
                    self.clean_end(cleaned)
                    return out
            elif self.clean:
                raise Evaluate(arg, funcs)
            else:
                func = funcs.pop(0)
                cleaned = self.clean_begin(None, None)
                if funcs:
                    out = func(arg, funcs)
                else:
                    out = func(arg)
                self.clean_end(cleaned)
                return out

    def unclean(self):
        """Sets clean."""
        self.clean = False
        self.all_clean = False

    def clean_begin(self, new_clean=False, new_all_clean=False):
        """Starts A Clean Block."""
        if new_clean is None:
            new_clean = self.clean
        if new_all_clean is None:
            new_all_clean = self.all_clean
        clean, self.clean = self.clean, new_clean
        all_clean, self.all_clean = self.all_clean, new_all_clean
        return clean, all_clean

    def clean_end(self, cleaned, all_clean_check=False, clean_check=False):
        """Ends A Clean Block."""
        clean, all_clean = cleaned
        if all_clean_check:
            all_clean = all_clean and self.all_clean
        if clean_check:
            clean = clean and self.clean
        self.clean = clean
        self.all_clean = all_clean

    def calc_cmd(self, inputstring, calc_funcs):
        """Evaluates Statements."""
        inputlist = self.splitdedent(inputstring, lambda x: x.split("::"))
        func, args = inputlist[0], inputlist[1:]
        func = basicformat(func)
        if len(args) > 0:
            original = func+" :: "+strlist(args, " :: ")
            self.printdebug("::> "+original)
            self.recursion += 1
            if func:
                cleaned = self.clean_begin()
                item = self.funcfind(func)
                params = []
                for x in xrange(0, len(args)):
                    arg = basicformat(args[x])
                    if x != len(args)-1 or arg:
                        params.append(codestr(arg, self))
                self.clean_end(cleaned)
                out = self.call_colon_set(item, params)
            else:
                out = codestr(strlist(args, "::"), self)
            self.printdebug(self.prepare(out, False, True, True)+" <:: "+original)
            self.recursion -= 1
            return out
        else:
            return self.calc_next(inputstring, calc_funcs)

    def calc_format(self, expression, calc_funcs):
        """Removes Unwanted Characters."""
        return self.calc_next(delspace(self.remformat(expression)), calc_funcs)

    def calc_with(self, expression, calc_funcs):
        """Evaluates With Clauses."""
        inputlist = expression.split("$")
        if len(inputlist) > 1:
            cleaned = self.clean_begin()
            inputlist.reverse()
            item = inputlist.pop()
            withclass = classcalc(self)
            for x in inputlist:
                withclass.process(x)
            self.clean_end(cleaned)
            return withclass.calc(item)
        else:
            return self.calc_next(expression, calc_funcs)

    def calc_set(self, original, calc_funcs):
        """Evaluates Definition Commands."""
        sides = original.split("=", 1)
        if len(sides) > 1:
            sides[0] = basicformat(sides[0])
            sides[1] = basicformat(sides[1])
            if not containsany(sides[0], self.calcops) and not endswithany(sides[0], self.bools) and not startswithany(sides[1], self.bools):
                self.unclean()
                docalc = False
                if sides[0].endswith(":"):
                    sides[0] = sides[0][:-1]
                    docalc = True
                sides[0] = sides[0].split(",")
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
                        raise ExecutionError("SyntaxError", "Could not set to invalid variable list "+strlist(sides[0], ","))
                else:
                    sides[0] = sides[0][0]
                    return self.calc_set_do(sides, docalc)
        return self.calc_next(original, calc_funcs)
                
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
            redef = self.redef
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
                                sides[1] = "( "+useclass+" )"+" ++ class\xab "+sides[0]+" "+":"*docalc+"= "+sides[1]+" \xbb"
                                sides[0] = classlist[x]
                                useclass = last
                                classlist = classlist[:x]
                                docalc = False
                                break
                            else:
                                raise ExecutionError("ClassError", "Could not set "+classlist[x]+" in "+self.prepare(last, False, True, True))
                elif classlist[0] in self.variables and istext(self.variables[classlist[0]]) and len(classlist) == 1:
                    sides[1] = "( "+self.variables[classlist[0]]+" ) ++ class\xab "+sides[0]+" "+":"*docalc+"= "+sides[1]+" \xbb"
                    sides[0] = classlist[0]
                    useclass = None
                    classlist = []
                    docalc = False
                else:
                    raise ExecutionError("VariableError", "Could not find class "+self.prepare(classlist[0], False, True, True))
            elif self.useclass:
                useclass = self.funcfind(self.useclass)
                redef = True
            sides[1] = basicformat(sides[1])
            for func in self.sets:
                value = func(sides)
                if value is not None:
                    if not isinstance(value, tuple):
                        value = sides[0], value
                    if docalc:
                        value = value[0], self.trycalc(value[1])
                    self.printdebug(": "+strlist(classlist, ".")+"."*bool(classlist)+value[0]+" "+":"*docalc+"= "+self.prepare(value[1], False, True, True))
                    if useclass is None:
                        if value[0] not in self.variables:
                            self.variables[value[0]] = value[1]
                        elif redef:
                            self.setreturned()
                            self.variables[value[0]] = value[1]
                        elif self.variables[value[0]] is not value[1]:
                            raise ExecutionError("RedefinitionError", "The variable "+value[0]+" already exists")
                        if docalc:
                            out = value[1]
                        else:
                            out = strfloat(value[0], self, name=value[0])
                    else:
                        if value[0] not in useclass.variables or useclass.variables[value[0]] is not value[1]:
                            if redef:
                                self.setreturned()
                                useclass.store(value[0], value[1])
                            else:
                                raise ExecutionError("RedefinitionError", "Cannot redefine attribute "+value[0])
                        if docalc:
                            out = value[1]
                        else:
                            out = strfunc(useclass.selfvar+"."+value[0], self, [], {useclass.selfvar:useclass}, value[0])
                    if delfrom is not None and value[0] in delfrom:
                        del delfrom[value[0]]
                    return out

    def readytofunc(self, expression, extra="", allowed=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        funcparts = expression.split(self.parenchar, 1)
        out = funcparts[0] != "" and (not self.isreserved(funcparts[0], extra, allowed)) and (len(funcparts) == 1 or funcparts[1].endswith(self.parenchar))
        if out and len(funcparts) != 1:
            return not self.insideouter(funcparts[1][:-1])
        else:
            return out

    def set_def(self, sides):
        """Creates Functions."""
        if self.parenchar in sides[0] and sides[0].endswith(self.parenchar):
            sides[0] = sides[0].split(self.parenchar, 1)
            sides[0][1] = self.namefind(self.parenchar+sides[0][1])
            params, personals, allargs, reqargs = self.eval_set(self.outersplit(sides[0][1], ",", top=False))
            return (sides[0][0], strfunc(sides[1], self, params, personals, allargs=allargs, reqargs=reqargs))

    def set_normal(self, sides):
        """Performs =."""
        if not self.isreserved(sides[0]):
            return sides[1]

    def calc_list(self, inputstring, calc_funcs):
        """Evaluates Matrices."""
        inputlist = inputstring.split(",")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            self.unclean()
            out = []
            for x in xrange(0, len(inputlist)):
                item = self.calc_next(inputlist[x], calc_funcs)
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

    def calc_pair(self, expression, calc_funcs):
        """Evaluates Key-Value Pairs."""
        inputlist = expression.split("->")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            self.unclean()
            itemlist = []
            for item in inputlist:
                itemlist.append(self.calc_next(item, calc_funcs))
            out = itemlist[-1]
            for x in reversed(xrange(0, len(itemlist)-1)):
                out = pair(self, itemlist[x], out)
            return out

    def calc_pieces(self, expression, calc_funcs):
        """Evaluates Piecewise Expressions."""
        inputlist = expression.split(";")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            cleaned = self.clean_begin()
            for x in xrange(0, len(inputlist)):
                if x == len(inputlist)-1:
                    self.clean_end(cleaned)
                    return self.calc_next(inputlist[x], calc_funcs)
                else:
                    test = self.calc_next(inputlist[x], calc_funcs)
                    if not isnull(test):
                        return test

    def calc_condo(self, item, calc_funcs):
        """Evaluates Conditions."""
        item = item.rsplit("@", 1)
        if len(item) == 1:
            return self.calc_next(item[0], calc_funcs)
        else:
            cleaned = self.clean_begin()
            check = bool(self.calc_next(item[1], calc_funcs))
            self.clean_end(cleaned)
            if check:
                return self.calc_next(item[0], [self.calc_condo]+calc_funcs)
            else:
                return matrix(0)

    def calc_or(self, inputstring, calc_funcs):
        """Evaluates The Or Part Of A Boolean Expression."""
        inputlist = inputstring.split("|")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], calc_funcs)
            for x in xrange(1, len(inputlist)):
                if value:
                    break
                value = value or self.calc_next(inputlist[x], calc_funcs)
            return value

    def calc_and(self, inputstring, calc_funcs):
        """Evaluates The And Part Of A Boolean Expression."""
        inputlist = inputstring.split("&")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], calc_funcs)
            for x in xrange(1, len(inputlist)):
                if not value:
                    break
                value = value and self.calc_next(inputlist[x], calc_funcs)
            return value

    def calc_unary(self, inputstring, calc_funcs):
        """Evaluates The Unary Part Of A Boolean Expression."""
        if inputstring.startswith("!"):
            self.unclean()
            return not self.calc_next(inputstring[1:], [self.calc_unary]+calc_funcs)
        elif inputstring.startswith("?"):
            self.unclean()
            return bool(self.calc_next(inputstring[1:], [self.calc_unary]+calc_funcs))
        else:
            return self.calc_next(inputstring, calc_funcs)

    def calc_eq(self, inputstring, calc_funcs):
        """Evaluates The Equation Part Of A Boolean Expression."""
        inputlist = switchsplit(inputstring, self.bools)
        if len(inputlist) == 0:
            return matrix(0)
        elif len(inputlist) == 1 and not madeof(inputlist[0], self.bools):
            return self.calc_next(inputlist[0], calc_funcs)
        else:
            self.unclean()
            for x in xrange(0, len(inputlist)):
                if istext(inputlist[x]) and madeof(inputlist[x], self.bools):
                    args = []
                    if x == 0:
                        args.append(matrix(0))
                    else:
                        if istext(inputlist[x-1]):
                            inputlist[x-1] = self.calc_next(inputlist[x-1], calc_funcs)
                        args.append(inputlist[x-1])
                    if x == len(inputlist)-1:
                        args.append(matrix(0))
                    else:
                        if istext(inputlist[x+1]):
                            inputlist[x+1] = self.calc_next(inputlist[x+1], calc_funcs)
                        args.append(inputlist[x+1])
                    out = False
                    haseq = False
                    hasgt = False
                    haslt = False
                    hasne = False
                    inv = False
                    found = {}
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
                        elif c in self.testers:
                            found[c] = testers[c]
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
                    for test in found.values():
                        out = out or test(args[0], args[1])
                    if inv:
                        out = not out
                    if not out:
                        return 0.0
            return 1.0

    def calc_eval(self, expression):
        """Evaluates An Expression."""
        top, ops = self.eval_split(expression)
        value = reassemble(top, ops)
        self.printdebug("==> "+value)
        self.recursion += 1
        out = self.eval_check(self.calc_next(top, self.eval_funcs, True), True)
        self.printdebug(self.prepare(out, False, True, True)+" <== "+value)
        self.recursion -= 1
        return out

    def eval_split(self, expression):
        """Splits An Expression By eval_splits."""
        params = self.eval_splits[0]
        if len(params) == 2:
            (op, split), args = params, None
        elif len(params) == 3:
            op, split, args = params
        else:
            raise SyntaxError("Invalid eval_split "+repr(params))
        if split:
            top = expression.split(op)
        else:
            top = [expression]
        if args is not None:
            top = splitinplace(top, *args)
        ops = [op]
        if not split and top[0].startswith(op):
            return top, ops
        else:
            return self.eval_split_do(top, ops, self.eval_splits[1:])

    def eval_split_do(self, top, ops, eval_splits):
        """Performs Splitting."""
        if eval_splits:
            params = eval_splits.pop(0)
            if len(params) == 2:
                (op, split), args = params, None
            elif len(params) == 3:
                op, split, args = params
            else:
                raise SyntaxError("Invalid eval_split "+repr(params))
            ops.append(op)
            for x in xrange(0, len(top)):
                if split:
                    top[x] = top[x].split(op)
                else:
                    top[x] = [top[x]]
                if args is not None:
                    top[x] = splitinplace(top[x], *args)
                if split or not top[x][0].startswith(op):
                    top[x], ops = self.eval_split_do(top[x], ops, eval_splits[:])
        return top, ops

    def eval_loop(self, complist, eval_funcs):
        """Performs List Comprehension."""
        if len(complist) == 1:
            return self.calc_next(complist[0], eval_funcs)
        else:
            self.unclean()
            item = self.calc_next(complist.pop(), eval_funcs)
            lists = []
            argnum = 1
            for x in reversed(xrange(0, len(complist))):
                if not delist(complist[x]):
                    argnum += 1
                else:
                    lists.append((self.calc_next(complist[x], eval_funcs), argnum))
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
            for x in xrange(0, len(units)//argnum):
                for y in xrange(0, argnum):
                    args.append(units[argnum*x+y])
                if len(lists) == 0:
                    if isfunc(func):
                        item = self.getcall(func)(args)
                    else:
                        item = func
                else:
                    item = self.eval_loop_set(lists[:], args, func)
                for y in xrange(0, argnum):
                    args.remove(units[argnum*x+y])
                new.append(item)
            if fromstring:
                outstr = ""
                for item in new:
                    if not isnull(item):
                        outstr += self.prepare(item, True, False)
                out = rawstrcalc(outstr, self)
            elif value.onlydiag():
                out = diagmatrixlist(new)
            else:
                out = rowmatrixlist(new)
            return out
        else:
            args.append(value)
            if len(lists) == 0:
                if isfunc(func):
                    out = self.getcall(func)(args)
                else:
                    out = func
            else:
                out = self.eval_loop_set(lists, args, func)
            args.remove(value)
            return out

    def eval_lambda(self, inputlist, eval_funcs=None):
        """Evaluates Lambdas."""
        if islist(inputlist[0]):
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            inputstring = inputlist[0]
            out = inputstring[1:].split(self.lambdamarker, 1)
            out[0] = self.namefind(out[0])
            if len(out) == 1:
                return strfloat(out[0], self, check=False)
            elif not out[0]:
                return strfloat(out[1], self, check=False)
            else:
                params, personals, allargs, reqargs = self.eval_set(self.outersplit(self.namefind(out[0]), ",", top=False))
                return strfloat(out[1], self, params, personals, check=False, allargs=allargs, reqargs=reqargs)

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
                    x = x[1:]
                    inopt = True
                    if reqargs is None:
                        reqargs = len(params)
                elif inopt:
                    raise ExecutionError("ArgumentError", "Cannot have required args after optional args")
                elif x.startswith("+"):
                    x = x[1:]
                else:
                    special = False
                equal_test = x.split("=", 1)
                colon_test = x.split(":", 1)
                if len(equal_test) > 1 and equal_test[0] and not self.isreserved(equal_test[0]):
                    inopt = True
                    if reqargs is None:
                        reqargs = len(params)
                    equal_test[0] = delspace(equal_test[0])
                    personals[equal_test[0]] = self.calc(equal_test[1], " <\\=")
                    x = equal_test[0]
                elif len(colon_test) > 1 and colon_test[0] and not self.isreserved(colon_test[0]):
                    if not special:
                        doparam = False
                    colon_test[0] = delspace(colon_test[0])
                    personals[colon_test[0]] = self.calc(colon_test[1], " <\\:")
                    x = colon_test[0]
                elif not x or self.isreserved(x):
                    raise ExecutionError("VariableError", "Could not set to invalid variable "+x)
                else:
                    x = delspace(x)
                if doallargs:
                    allargs = x
                if doparam:
                    params.append(x)
        return params, personals, allargs, reqargs

    def eval_join(self, inputlist, eval_funcs):
        """Performs Concatenation."""
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            items = []
            for item in inputlist:
                item = self.calc_next(item, eval_funcs)
                if not isnull(item):
                    items.append(item)
            if len(items) == 0:
                return matrix(0)
            elif len(items) == 1:
                return items[0]
            else:
                if hasattr(items[0], "op_join"):
                    try:
                        test = items[0].op_join(items[1:])
                    except NotImplementedError:
                        test = NotImplemented
                    if test is not NotImplemented:
                        return test
                dostr = 0
                dolist = 0
                dobrack = 0
                dodata = 0
                domultidata = 0
                domatrix = 0
                doclass = 0
                dodict = 0
                rowlen = None
                tot = len(items)
                for x in items:
                    if hasattr(x, "rop_join"):
                        params = items[:]
                        params.remove(x)
                        try:
                            test = x.rop_join(params)
                        except NotImplementedError:
                            test = NotImplemented
                        if test is not NotImplemented:
                            return test
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
                    elif isinstance(x, pair):
                        dodict += 1
                    else:
                        tot -= 1
                if dostr > 0:
                    out = rawstrcalc("", self)
                    for x in items:
                        out += x
                    return out
                elif dodict == len(items):
                    out = {}
                    for x in items:
                        if isinstance(x, dictionary):
                            out.update(x.a)
                        else:
                            out[x.k] = x.v
                    return dictionary(self, out)
                elif doclass == len(items):
                    out = items[0].copy()
                    for x in xrange(1, len(items)):
                        out.extend(items[x])
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
                elif domatrix == len(items):
                    out = []
                    for x in items:
                        out += x.a
                    return matrixlist(out, float)
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
                elif domultidata == len(items):
                    out = []
                    for x in items:
                        if isinstance(x, matrix):
                            for l in x.a:
                                out.append((l[0], l[1]))
                        else:
                            out += x.items()
                    return multidata(out)
                else:
                    raise ExecutionError("TypeError", "Could not concatenate items "+strlist(items, ", ", lambda x: self.prepare(x, False, True, True)))

    def eval_remove(self, inputlist, eval_funcs):
        """Performs Removal."""
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            item = self.calc_next(inputlist[0], eval_funcs)
            params = []
            for x in xrange(1, len(inputlist)):
                params.append(self.calc_next(inputlist[x], eval_funcs))
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
            elif isinstance(item, dictionary):
                for arg in params:
                    if isinstance(arg, dictionary):
                        for k,v in arg.a.items():
                            if k in item.a and item.a[k] == v:
                                del item.a[k]
                    elif isinstance(arg, pair):
                        if arg.k in item.a and (isnull(arg.v) or item.a[arg.k] == arg.v):
                            del item.a[arg.k]
                        elif isnull(arg.k):
                            temp = flip(item.a)
                            if arg.v in temp:
                                del temp[arg.v]
                                item.a = flip(temp)
                    else:
                        raise ExecutionError("TypeError", "Can only remove pairs and dictionaries from dictionaries")
            else:
                raise ExecutionError("TypeError", "Could not remove from item "+self.prepare(item, False, True, True))
            return item

    def eval_repeat(self, inputlist, eval_funcs):
        """Evaluates Repeats."""
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            out = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                done = False
                num = self.calc_next(inputlist[x], eval_funcs)
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

    def eval_add(self, inputlist, eval_funcs):
        """Evaluates The Addition Part Of An Expression."""
        if not inputlist:
            return matrix(0)
        elif len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                item = self.calc_next(inputlist[x], eval_funcs)
                if isnull(value):
                    value = item
                elif isinstance(item, negative):
                    value = item + value
                else:
                    value = value + item
            return value

    def eval_mod(self, inputlist, eval_funcs):
        """Evaluates The Modulus Part Of An Expression."""
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                value = value % self.calc_next(inputlist[x], eval_funcs)
            return value

    def eval_intdiv(self, inputlist, eval_funcs):
        """Evaluates The Floor Division Part Of An Expression."""
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                value = value // self.calc_next(inputlist[x], eval_funcs)
            return value

    def eval_mul(self, inputlist, eval_funcs):
        """Evaluates The Multiplication Part Of An Expression."""
        if not inputlist:
            return matrix(0)
        elif len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                item = self.calc_next(inputlist[x], eval_funcs)
                if isinstance(item, reciprocal):
                    value = item * value
                else:
                    value = value * item
            return value

    def eval_call(self, inputstring, top=True):
        """Evaluates A Variable."""
        self.printdebug("=> "+inputstring)
        self.recursion += 1
        for func in self.calls:
            out = func(inputstring, top)
            if out is not None:
                break
        self.printdebug(self.prepare(out, False, True, True)+" <= "+inputstring)
        self.recursion -= 1
        return out

    def eval_check(self, value, top=False):
        """Checks A Value."""
        if value is None:
            return matrix(0)
        elif top and isinstance(value, self.tempobjects):
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
                return self.eval_check(float(value), top)
            else:
                raise ExecutionError("VariableError", "Unable to process "+str(value))

    def convertable(self, item):
        """Determines If An Item Can Be Converted By eval_check."""
        return hasnum(item) or islist(item) or isinstance(item, bool) or item is None

    def call_var(self, inputstring, top=None):
        """Checks If Variable."""
        if inputstring in self.variables:
            self.unclean()
            item, key = self.getfind(inputstring, True)
            if istext(item):
                value = self.calc(str(item), " | var")
            elif self.convertable(item):
                value = item
            else:
                raise ValueError("Unconvertable variable value of "+repr(item))
            if isprop(value):
                value = self.deprop(value)
                store = False
            if not self.isreserved(key):
                self.variables[key] = value
            return value

    def call_parenvar(self, inputstring, top=None):
        """Checks If Parentheses."""
        if inputstring.startswith(self.parenchar) and inputstring.endswith(self.parenchar):
            item = self.namefind(inputstring, True)
            if item is not inputstring:
                if istext(item):
                    item = str(item)
                    if self.tailing and self.all_clean:
                        raise TailRecursion(item, self.variables.copy())
                    else:
                        value = self.calc(item, " | parenvar")
                elif self.convertable(item):
                    value = item
                else:
                    raise ValueError("Unconvertable variable value of "+repr(item))
                return value

    def deprop(self, value):
        """Evaluates Property Objects."""
        while isprop(value):
            value = self.getcall(value)(None)
        return value

    def call_lambda(self, inputstring, top=None):
        """Wraps Lambda Evaluation."""
        if inputstring.startswith(self.lambdamarker):
            return self.eval_lambda([inputstring])

    def call_neg(self, inputstring, top=None):
        """Evaluates Unary -."""
        if inputstring.startswith("-"):
            self.unclean()
            item = self.eval_call(inputstring[1:])
            if isnull(item):
                return -1.0
            else:
                return negative(item)

    def call_reciproc(self, inputstring, top=None):
        """Evaluates /."""
        if inputstring.startswith("/"):
            self.unclean()
            item = self.eval_call(inputstring[1:])
            if isnull(item):
                return item
            else:
                return reciprocal(item)

    def call_exp(self, inputstring, top=None):
        """Evaluates The Exponential Part Of An Expression."""
        if "^" in inputstring:
            self.unclean()
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
                        raise ExecutionError("NoneError", "Cannot exponentiate nothing")
                    else:
                        level += 1
            return value

    def call_colon(self, inputstring, top=None):
        """Evaluates Colons."""
        if ":" in inputstring:
            cleaned = self.clean_begin()
            inputlist = inputstring.split(":")
            item = self.funcfind(inputlist[0])
            params = []
            for x in xrange(1, len(inputlist)):
                if inputlist[x]:
                    params.append(getcopy(self.eval_call(inputlist[x])))
            self.clean_end(cleaned)
            return self.call_colon_set(item, params)

    def call_colon_set(self, item, params):
        """Performs Colon Function Calls."""
        overflow, self.overflow = self.overflow, []
        docalc = False
        if isnull(item):
            if params:
                raise ExecutionError("NoneError", "Nothing cannot be called")
            else:
                return item
        elif hasattr(item, "itemcall") and item.itemcall is not None:
            value = item.itemcall(params)
        elif ismatrix(item):
            item = getmatrix(item)
            if not params:
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
            self._overflow = params[2:]
        elif isfunc(item):
            value = self.getcall(item)(params)
        elif len(params) == 0:
            value = item
        else:
            raise ExecutionError("ArgumentError", "Excess argument"+"s"*(len(params) > 1)+" of "+strlist(params, ", ", lambda x: self.prepare(x, False, True, True))+" to "+self.prepare(item, False, True, True))
        while docalc or len(self.overflow) > 0:
            docalc = False
            temp = self.overflow[:]
            self.overflow = []
            value = self.call_colon_set(value, temp)
        self._overflow = overflow
        return value

    def unusedarg(self):
        """Returns An Unused Arg."""
        out = self.autoarg
        while out in self.variables:
            out = "_"+out
        return out

    def call_paren(self, inputstring, top=True):
        """Evaluates Parentheses."""
        if top:
            inputstring = (self.parenchar*2).join(switchsplit(inputstring, string.digits, notstring=self.reserved))
            if self.parenchar in inputstring:
                self.unclean()
                self.printdebug("(|) "+inputstring) 
                templist = inputstring.split(self.parenchar)
                checkops = delspace(self.callops, self.subparenops)
                inputlist = [[]]
                feed = inputlist[0]
                last = False
                for x in xrange(0, len(templist)):
                    if x%2 == 1:
                        if templist[x]:
                            last = True
                            if feed and feed[-1] and feed[-1][-1] in checkops:
                                feed[-1] += self.parenchar+templist[x]+self.parenchar
                            else:
                                feed.append(self.parenchar+templist[x]+self.parenchar)
                            last = True
                        else:
                            last = False
                    elif templist[x]:
                        if feed and ((templist[x] and templist[x][0] in checkops) or (feed[-1] and feed[-1][-1] in checkops)):
                            feed[-1] += templist[x]
                        else:
                            if last:
                                inputlist.append([])
                                feed = inputlist[-1]
                            feed.append(templist[x])
                temp = "("+strlist(inputlist, ") * (", lambda l: strlist(l, " : "))+")"
                self.printdebug("(>) "+temp)
                self.recursion += 1
                values = []
                for l in inputlist:
                    x = 0
                    while x < len(l):
                        if endswithany(l[x], self.subparenops) and x+1 < len(l):
                            l[x] += l.pop(x+1)
                        if startswithany(l[x], self.subparenops) and x > 0:
                            l[x-1] += l.pop(x)
                            x -= 1
                        x += 1
                    if not l:
                        item = matrix(0)
                    elif len(values) > 0 and startswithany(l[0], self.subparenops):
                        autoarg = self.unusedarg()
                        item = strfunc(autoarg+l[0], self, [autoarg], overflow=False).call([values.pop()])
                    else:
                        item = self.eval_call(l[0], False)
                    args = []
                    for x in xrange(1, len(l)):
                        args.append(self.eval_call(l[x], False))
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
            overflow, self.overflow = self.overflow, []
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
                item = self.getcall(item)(args)
            else:
                item = self.getcall(item)([arg])
            if self.overflow:
                out, self.overflow = self.overflow, overflow
                raise ExecutionError("ArgumentError", "Excess argument"+"s"*(len(out) > 1)+" of "+strlist(out, ", ", lambda x: self.prepare(x, False, True, True)))
            else:
                x += 1
            self._overflow = overflow
        return item

    def call_comp(self, inputstring, top=None):
        """Performs Function Composition."""
        if ".." in inputstring:
            self.unclean()
            funclist = []
            for item in inputstring.split(".."):
                func = self.eval_call(item)
                if not isnull(func):
                    funclist.append(self.wrap(func))
            return strfunc(strlist(funclist, "(")+"("*bool(funclist)+strfunc.allargs+")"*len(funclist), self, overflow=False)

    def call_lambdacoeff(self, inputstring, top=None):
        """Evaluates Lambda Coefficients."""
        parts = inputstring.split(self.lambdamarker, 1)
        if len(parts) > 1:
            return self.eval_call(parts[0]+self.wrap(self.eval_lambda([self.lambdamarker+parts[1]])))

    def call_method(self, inputstring, top=None):
        """Returns Method Instances."""
        if "." in inputstring:
            itemlist = inputstring.split(".")
            isfloat = len(itemlist) < 3
            for item in itemlist:
                isfloat = isfloat and (not item or madeof(item, string.digits))
            if not isfloat:
                self.unclean()
                itemlist[0] = self.funcfind(itemlist[0])
                out = itemlist[0]
                for x in xrange(1, len(itemlist)):
                    key = itemlist[x]
                    if hasattr(out, "getmethod"):
                        new = out.getmethod(key)
                    elif isnull(out):
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
                                #TODO: This is where whatever test is should be wrapped regardless in a special full-conversion wrapper
                        else:
                            raise ExecutionError("AttributeError", "Cannot get method "+key+" from "+self.prepare(out, False, True, True))
                    out = new
                return out

    def call_normal(self, inputstring, top=None):
        """Returns Argument."""
        return self.eval_check(inputstring)

    def getparen(self, num):
        """Gets A Parenthesis."""
        test = self.parens[num]
        if isinstance(test, bracket):
            return test.calc()
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
            out = self.getcall(item)(varproc(value))
        elif hasnum(item):
            return item
        else:
            oldvars = self.setvars({varname: value})
            try:
                out = self.getcall(item)(None)
            finally:
                self.setvars(oldvars)
        return self.call(out, value, varname)

    def evaltypestr(self, item):
        if isnull(item):
            return "none"
        elif hasattr(item, "evaltype"):
            if istext(item.evaltype):
                return item.evaltype
            else:
                return item.evaltype()
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
        elif isinstance(item, tuple):
            out = diagmatrixlist(map(self.frompython, item))
        elif islist(item):
            out = rowmatrixlist(map(self.frompython, item))
        elif isinstance(item, dict):
            out = {}
            for k,v in item.items():
                out[self.frompython(k)] = self.frompython(v)
            out = dictionary(self, out)
        elif isfunc(item):
            out = item
        else:
            raise TypeError("Cannot convert non-evaluatour result type "+typestr(item))
        return out

    def topython(self, item):
        """Converts A Rabbit Object To A Python Object."""
        if isnull(item):
            out = None
        elif isinstance(item, strcalc):
            out = str(item)
        elif isinstance(item, matrix):
            out = map(topython, item.getitems())
            if item.onlydiag():
                out = tuple(out)
            else:
                out = list(out)
        elif isinstance(item, dictionary):
            out = {}
            for k,v in item.a:
                out[self.topython(k)] = self.topython(v)
        else:
            out = item
        return out

    def deitem(self, item):
        """Decompiles An Item."""
        if isinstance(item, tuple):
            name = str(item[0])
            args = item[1:]
            if name in self.constructors:
                value = self.constructors[name](self, args)
            elif name == "find":
                value = self.calc(args[0])
            else:
                raise ExecutionError("UnpicklingError", "Rabbit could not unpickle "+name)
        else:
            value = item
        return value

    def devariables(self, variables):
        """Decompiles Variables."""
        out = {}
        for k,v in variables.items():
            out[self.deitem(k)] = self.deitem(v)
        return out

    def delist(self, inputlist):
        """Decompiles A List."""
        out = []
        for x in inputlist:
            out.append(self.deitem(x))
        return out

class evalfuncs(object):
    """Implements Evaluator Functions."""
    typefuncs = {
        "number": "num",
        "list": "cont",
        "row": "cont",
        "matrix": "cont",
        "multidata": "data",
        "fraction": "frac",
        "string": "str",
        "dictionary": "dict"
        }

    def __init__(self, e):
        """Initializes The Functions."""
        self.e = e

    def usecall(self, variables):
        """Uses A Default Statement."""
        if not variables:
            self.e.setreturned()
            self.e.using = None
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
            self.e.using = variables[0]
        return matrix(0)

    def delcall(self, variables):
        """Deletes A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to del")
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
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
            return out

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
            self.e.setreturned()
            last = None
            while isinstance(variables[0], instancecalc):
                if last is None or not self.iseq(last, variables[0]):
                    last = variables[0]
                    variables[0] = variables[0].include()
                else:
                    raise ExecutionError("RuntimeError", "Illegal infinite recursive loop in __include__")
            if isinstance(variables[0], classcalc):
                oldvars = self.e.setvars(variables[0].getvars(True))
                return classcalc(self.e, oldvars)
            else:
                raise ValueError("Can only include a class")
        else:
            out = []
            for arg in variables:
                out.append(self.includecall([arg]))
            return diagmatrixlist(out)

    def usingcall(self, variables):
        """Retrieves The Current Function Being Used."""
        self.e.setreturned()
        self.e.overflow = variables
        if self.e.using is None:
            return matrix(0)
        else:
            return self.e.using

    def envcall(self, variables):
        """Retrieves A Class Of The Global Environment."""
        self.e.setreturned()
        self.e.overflow = variables
        return classcalc(self.e, self.e.getvars())

    def trycall(self, variables):
        """Catches Errors."""
        if not variables:
            return matrix(0)
        else:
            self.e.overflow = variables[1:]
            original = self.e.prepare(variables[0], True, False)
            result, err = catch(self.e.calc, original)
            if err:
                out = instancecalc(self.e, {
                    classcalc.selfvar : None,
                    self.e.errorvar : 1.0,
                    self.e.fatalvar : float(err[2])
                    })
                out.store(self.e.namevar, strcalc(err[0], self.e))
                out.store(self.e.messagevar, strcalc(err[1], self.e))
                if len(err) > 3:
                    for k,v in err[3].items():
                        out.variables[k] = v
                return rowmatrixlist([matrix(0), out])
            else:
                return rowmatrixlist([result, matrix(0)])

    def raisecall(self, variables):
        """Raises An Error."""
        if not variables:
            raise ExecutionError("Error", "An error occured")
        elif len(variables) == 1:
            if isinstance(variables[0], instancecalc) and self.iserrcall(variables):
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
                extras = variables[0].getvars(True)
                del extras[self.e.errorvar]
                if self.e.namevar in extras:
                    del extras[self.e.namevar]
                if self.e.messagevar in extras:
                    del extras[self.e.messagevar]
                if self.e.fatalvar in extras:
                    del extras[self.e.fatalvar]
                extras[variables[0].parentvar] = variables[0].getparent()
                raise ExecutionError(name, message, fatal, extras)
            else:
                raise ExecutionError("Error", self.e.prepare(variables[0], False, False))
        else:
            raise ExecutionError(self.e.prepare(variables[0], False, False), strlist(variables[1:], "; ", lambda x: self.e.prepare(x, False, False)))

    def exceptcall(self, variables):
        """Excepts Errors."""
        if not variables:
            return rowmatrixlist([matrix(0), 0.0])
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
        self.e.overflow = variables[1:]
        if not variables:
            return classcalc(self.e)
        elif isinstance(variables[0], instancecalc):
            return variables[0].toclass()
        elif isinstance(variables[0], classcalc):
            return variables[0]
        elif isinstance(variables[0], strcalc):
            original = self.e.prepare(variables[0], True, False)
            out = classcalc(self.e)
            for cmd in self.e.splitdedent(original, lambda x: x.splitlines()):
                out.process(cmd)
            return out
        else:
            raise ExecutionError("ClassError", "Cannot convert "+self.e.prepare(variables[0], False, True, True)+" to class")

    def namespacecall(self, variables):
        """Converts To A Namespace."""
        self.e.overflow = variables[1:]
        if not variables:
            return namespace(self.e)
        elif isinstance(variables[0], namespace):
            return variables[0]
        elif isinstance(variables[0], classcalc):
            return namespace(variables[0].e, variables[0].getvars(True))
        else:
            raise ExecutionError("ClassError", "Cannot convert "+self.e.prepare(variables[0], False, True, True)+" to namespace")

    def getvalcall(self, variables):
        """Calculates A Variable Without Changing It."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to val")
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
            original = self.e.prepare(variables[0], False, False)
            if original in self.e.variables:
                return self.e.funcfind(original)
            else:
                return matrix(0)

    def getparenscall(self, variables):
        """Retreives The Number Of Parentheses."""
        self.e.setreturned()
        self.e.overflow = variables
        return float(len(self.e.parens))

    def getparenvarcall(self, variables):
        """Gets The Value Of A Paren."""
        if not variables:
            variables = [-1]
        self.e.overflow = variables[1:]
        self.e.setreturned()
        original = getint(variables[0])
        if original < 0:
            original += len(self.e.parens)
        if 0 < original and original < len(self.e.parens):
            return rawstrcalc(self.e.prepare(self.e.getparen(original), True, True), self.e)
        else:
            return matrix(0)

    def getvarcall(self, variables):
        """Gets The Value Of A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to var")
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
            original = self.e.prepare(variables[0], False, False)
            if original in self.e.variables:
                return rawstrcalc(self.e.prepare(self.e.variables[original], True, True), self.e)
            else:
                return matrix(0)

    def copycall(self, variables):
        """Makes Copies Of Items."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to copy")
        else:
            self.e.overflow = variables[1:]
            if iseval(variables[0]):
                return variables[0].copy()
            else:
                return variables[0]

    def getmatrixcall(self, variables):
        """Converts To Matrices."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to cont")
        elif len(variables) == 1:
            return getmatrix(variables[0])
        else:
            return diagmatrixlist(variables)

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
            if ismatrix(x):
                value += self.sumcall(getmatrix(x).items())
            else:
                value += x
        return value

    def prodcall(self, variables):
        """Finds A Product."""
        value = 1.0
        for x in variables:
            if ismatrix(x):
                value *= self.prodcall(getmatrix(x).getitems())
            else:
                value *= x
        return value

    def maxcall(self, variables):
        """Performs max."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to max")
        elif len(variables) == 1:
            return max(getmatrix(variables[0]).getitems())
        else:
            return max(variables)

    def mincall(self, variables):
        """Performs min."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to min")
        elif len(variables) == 1:
            return min(getmatrix(variables[0]).getitems())
        else:
            return min(variables)

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
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to find")
        else:
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
            return rangematrix(0.0, getnum(variables[0]))
        elif len(variables) == 2:
            return rangematrix(getnum(variables[0]), getnum(variables[1]))
        else:
            return rangematrix(getnum(variables[0]), getnum(variables[1]), getnum(variables[2]))

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
            return func(0.0)
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
        return self.numcall(variables, func=lambda x: makeint(x))

    def basecall(self, variables):
        """Peforms base."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to base")
        else:
            self.e.overflow = variables[2:]
            base = getnum(variables[0])
            num = self.e.prepare(variables[1], False, False)
            return int(num, base)

    def reprstrip(self, inputrepr):
        """Strips A Python Base Representation."""
        while inputrepr and inputrepr[0] in "0box":
            inputrepr = inputrepr[1:]
        return inputrepr

    def bincall(self, variables, func=bin):
        """Performs bin."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to bin")
        else:
            self.e.overflow = variables[1:]
            return rawstrcalc(self.reprstrip(func(getnum(variables[0]))), self.e)

    def octcall(self, variables):
        """Performs oct."""
        return self.bincall(variables, oct)

    def hexcall(self, variables):
        """Performs hex."""
        return self.bincall(variables, hex)

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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to split")
        else:
            items = variables[1:]
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
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to replace")
        else:
            pairs = {}
            for x in xrange(1, len(variables)):
                if x%2 == 1:
                    temp = variables[x]
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
            variables[0] = getmatrix(variables[0])
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
        """Performs in."""
        if variables:
            if hasmatrix(variables[0]):
                for x in xrange(1, len(variables)):
                    if variables[x] in variables[0]:
                        return 1.0
            else:
                for x in xrange(1, len(variables)):
                    if variables[x] == variables[0]:
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
                raise ExecutionError("TypeError", "Unable to create a converter for "+repr(variables[0]))
        else:
            return self.tocall([diagmatrixlist(variables)])

    def typestr(self, item):
        """Processes A Type Identifier."""
        item = self.e.prepare(item, False, False)
        if item in self.typefuncs:
            return self.typefuncs[item]
        else:
            return item

    def codecall(self, variables):
        """Converts To Code."""
        if not variables:
            return codestr("", self.e)
        else:
            self.e.overflow = variables[1:]
            return codestr(self.e.prepare(variables[0], True, False), self.e)

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
            raise ExecutionError("ArgumentError", "Not enough arguments to join")
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
        if not variables:
            return data()
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

    def fractioncall(self, variables, dosimp=False):
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
            out = self.fractioncall([variables[0]])
            for x in xrange(1, len(variables)):
                out /= self.fractioncall([variables[x]])
        if dosimp or (isnum(out.n) and isnum(out.d)):
            out.simptens()
        return out

    def simpcall(self, variables):
        """Simplifies Fractions."""
        out = self.fractioncall(variables, True)
        out.simplify()
        return out

    def docalc(self, variables):
        """Performs calc."""
        out = []
        for x in variables:
            inputstring = self.e.prepare(x, False, False)
            out.append(self.e.calc(self.e.do_pre(inputstring, True), " | calc"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def evalcall(self, variables):
        """Performs eval."""
        out = []
        e = self.e.new()
        for x in variables:
            inputstring = e.prepare(x, False, False)
            out.append(e.calc(e.do_pre(inputstring, True), " | eval"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def cmdcall(self, variables):
        """Performs exec."""
        for item in variables:
            inputstring = self.e.prepare(item, False, False)
            self.e.processor.evaltext(inputstring)
        return matrix(0)

    def foldcall(self, variables, func=None, overflow=True):
        """Folds A Function Over A Matrix."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to fold")
        elif len(variables) == 1:
            return self.e.getcall(self.e.funcfind(variables[0]))(self.e.variables)
        else:
            func = func or self.e.getcall(self.e.funcfind(variables[0]))
            item = variables[1]
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
            self.e.setreturned()
            stop = getnum(variables[0])
            key = None
            if len(variables) > 1:
                key = self.e.prepare(variables[1], True, False)
                self.e.overflow = variables[2:]
            return rollfunc(stop, self.e, key)

    def writecall(self, variables):
        """Writes To A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to write")
        else:
            self.e.overflow = variables[2:]
            self.e.setreturned()
            name = self.e.prepare(variables[0], False, False)
            if len(variables) == 1:
                writer = ""
            else:
                writer = self.e.prepare(variables[1], False, False)
            with openfile(name, "wb") as f:
                writefile(f, writer)
            return matrix(0)

    def readcall(self, variables):
        """Reads From A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to read")
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
            name = self.e.prepare(variables[0], False, False)
            with openfile(name) as f:
                return rawstrcalc(readfile(f), self.e)

    def purecall(self, variables):
        """Ensures Purity."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to pure")
        else:
            self.e.overflow = variables[1:]
            original = self.e.prepare(variables[0], True, False)
            pure, self.e.pure = self.e.pure, True
            try:
                out = self.e.calc(original, " | pure")
            finally:
                self.e.pure = pure
            return out

    def defcall(self, variables):
        """Defines A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to def")
        else:
            self.e.overflow = variables[1:]
            original = self.e.prepare(variables[0], True, False)
            redef, self.e.redef = self.e.redef, True
            try:
                out = self.e.calc(original, " | def")
            finally:
                self.e.redef = redef
            return out

    def globalcall(self, variables):
        """Defines A Global Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to global")
        else:
            self.e.overflow = variables[1:]
            original = self.e.prepare(variables[0], True, False)
            useclass, self.e.useclass = self.e.useclass, False
            try:
                out = self.e.calc(original, " | global")
            finally:
                self.e.useclass = useclass
            return out

    def aliascall(self, variables):
        """Makes Aliases."""
        self.e.overflow = variables[2:]
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to alias")
        elif len(variables) == 1:
            self.e.setreturned()
            key = self.e.prepare(variables[0], True, False)
            if key in self.e.aliases:
                out = rawstrcalc(self.e.aliases[key], self.e)
                del self.e.aliases[key]
            else:
                out = matrix(0)
            return out
        else:
            self.e.setreturned()
            key = self.e.prepare(variables[0], True, False)
            value = self.e.prepare(variables[1], True, False)
            self.e.aliases[key] = value
            return diagmatrixlist([rawstrcalc(key, self.e), rawstrcalc(value, self.e)])

    def aliasescall(self, variables):
        """Gets Aliases."""
        self.e.overflow = variables
        out = dictionary(self.e)
        for k,v in self.e.aliases.items():
            out.store(rawstrcalc(k, self.e), rawstrcalc(v, self.e))
        return out

    def bitnotcall(self, variables):
        """Wraps ~."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to bitnot")
        elif len(variables) == 1:
            return ~variables[0]
        else:
            out = []
            for arg in variables:
                out.append(~arg)
            return diagmatrixlist(out)

    def bitorcall(self, variables):
        """Wraps |."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to bitor")
        else:
            out = variables[0]
            for x in xrange(1, len(variables)):
                out = out | variables[x]
            return out

    def bitandcall(self, variables):
        """Wraps &."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to bitand")
        else:
            out = variables[0]
            for x in xrange(1, len(variables)):
                out = out & variables[x]
            return out

    def bitxorcall(self, variables):
        """Wraps ^."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to bitxor")
        else:
            out = variables[0]
            for x in xrange(1, len(variables)):
                out = out ^ variables[x]
            return out

    def rshiftcall(self, variables):
        """Wraps >>."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to rshift")
        else:
            out = variables[-1]
            for x in xrange(0, len(variables)-1):
                out = out >> variables[x]
            return out

    def lshiftcall(self, variables):
        """Wraps <<."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to lshift")
        else:
            out = variables[-1]
            for x in xrange(0, len(variables)-1):
                out = out << variables[x]
            return out

    def callcall(self, variables):
        """Calls A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to call")
        elif len(variables) == 1:
            return collapse(variables[0])
        else:
            return self.e.getcall(variables[0])(variables[1:])

    def paircall(self, variables):
        """Creates A Pair."""
        if not variables:
            return pair(self.e, matrix(0), matrix(0))
        elif len(variables) == 1:
            return pair(self.e, variables[0], matrix(0))
        else:
            self.e.overflow = variables[2:]
            return pair(self.e, variables[0], variables[1])

    def dictcall(self, variables):
        """Creates A Dictionary."""
        if not variables:
            return dictionary(self.e)
        elif len(variables) == 1:
            if isinstance(variables[0], dictionary):
                return variables[0]
            else:
                raise TypeError("Received non-dictionary object "+self.e.prepare(variables[0], False, True, True))
        else:
            out = []
            for arg in variables:
                out.append(self.dictcall([arg]))
            return diagmatrixlist(out)

    def unioncall(self, variables):
        """Performs union."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to union")
        elif len(variables) == 2:
            a,b = getmatrix(variables[0]), getmatrix(variables[1])
            out = list(set(a.getitems()) | set(b.getitems()))
            if a.onlyrow():
                return rowmatrixlist(out)
            else:
                return diagmatrixlist(out)
        else:
            out = variables[0]
            for x in xrange(1, len(variables)):
                out = self.unioncall([out, variables[x]])
            return out

    def intersectcall(self, variables):
        """Performs intersect."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to union")
        elif len(variables) == 2:
            a,b = getmatrix(variables[0]), getmatrix(variables[1])
            out = list(set(a.getitems()) & set(b.getitems()))
            if a.onlyrow():
                return rowmatrixlist(out)
            else:
                return diagmatrixlist(out)
        else:
            out = variables[0]
            for x in xrange(1, len(variables)):
                out = self.intersectcall([out, variables[x]])
            return out

    def runcall(self, variables):
        """Performs run."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to run")
        elif len(variables) == 1:
            self.e.setreturned()
            original = os.path.normcase(self.e.prepare(variables[0], False, False))
            while not os.path.isfile(original):
                if "." not in original:
                    original += ".rab"
                else:
                    raise ExecutionError("IOError", "Could not find file "+str(original))
            if not self.e.processor.evalfile(original):
                raise ExecutionError("IOError", "Failed to execute file "+str(original))
            else:
                self.e.processor.dumpdebug(True)
        else:
            for arg in variables:
                self.runcall([arg])
        return matrix(0)

    def requirecall(self, variables):
        """Performs require."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to require")
        elif len(variables) == 1:
            self.e.setreturned()
            out = classcalc(self.e)
            params = out.begin()
            self.runcall(variables)
            out.end(params)
            return out
        else:
            out = []
            for arg in variables:
                out.append(self.requirecall([arg]))
            return diagmatrixlist(out)

    def assertcall(self, variables):
        """Checks For Errors By Asserting That Something Is True."""
        if not variables:
            raise ExecutionError("NoneError", "Assertion failed that none")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                out = self.e.calc(original, " | assert")
            else:
                original = self.e.prepare(variables[0], True, True, True)
                out = variables[0]
        else:
            for arg in variables:
                self.assertcall([arg])
            out = 1.0
        test = bool(out)
        if test:
            return out
        else:
            raise ExecutionError("AssertionError", "Assertion failed that "+original, {"Result":out})

    def installcall(self, variables):
        """Performs install."""
        if not variables:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        elif len(variables) == 1:
            self.setreturned()
            name = self.prepare(variables[0], False, False)
            try:
                impbaseclass = dirimport(inputstring)
            except IOError:
                raise ExecutionError("IOError", "Could not find for install file "+name)
            else:
                if hasattr(impbaseclass, "__rabbit__"):
                    impclass = impbaseclass.__rabbit__
                    funcname = "install`"+name+"`"
                    if impclass is None:
                        return matrix(0)
                    elif iseval(impclass):
                        return impclass(self)
                    elif "`" in name:
                        raise ValueError("Cannot install files with a backtick in them")
                    elif hascall(impclass):
                        return funcfloat(getcall(impclass(self)), self, funcname)
                    else:
                        try:
                            impclass.precall
                        except AttributeError:
                            try:
                                impclass.unicall
                            except AttributeError:
                                return impclass(self)
                            else:
                                return unifunc(impclass(self).unicall, self, funcname)
                        else:
                            return usefunc(impclass(self).precall, self, funcname)
                else:
                    raise ExecutionError("ImportError", "Found no __rabbit__ variable in file "+name)
        else:
            out = []
            for x in variables:
                out.append(self.installcall([x]))
            return diagmatrixlist(out)
