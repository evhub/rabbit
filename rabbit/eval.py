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

from .prelude import *
import operator

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

class Evaluate(BaseException):
    """A Stack-Killer Evaluation Exception."""
    def __init__(self, arg, funcs):
        """Creates The Evaluation."""
        self.arg = arg
        self.funcs = funcs

def _and(x, y):
    """Performs and."""
    return x and y

def _or(x, y):
    """Performs or."""
    return x or y

def _xor(x, y):
    """Performs xor."""
    return (not y and x) or (not x and y)

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

    ---     Toggles pure blocks.
    =       Sets variable names.
    ::      Calls a meta-function.
    $       Seperates with clauses (read as 'with' or 'where').
    ,       Seperates list elements.
    ->      Creates a key-value pair.
    ;       Seperates conditionals (read as 'else').
    @       Checks a conditional (read as 'at' or 'if').
    |       Performs logical or.
    &       Performs logical and.
    ?!      Performs logical unary operations.
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
    .       Denotes methods.
    normal  Evaluates numbers."""
    constructors = {
        "atom": lambda self, args: atom(
            ),
        "reciprocal": lambda self, args: reciprocal(
            self.deitem(args[0])
            ),
        "negative": lambda self, args: negative(
            self.deitem(args[0])
            ),
        "fraction": lambda self, args: fraction(
            self.deitem(args[0]),
            self.deitem(args[1])
            ),
        "pair": lambda self, args: pair(
            self.deitem(args[0]),
            self.deitem(args[1])
            ),
        "dictionary": lambda self, args: dictionary(
            self.devariables(args[0])
            ),
        "data": lambda self, args: data(
            args[0],
            args[1]
            ),
        "multidata": lambda self, args: multidata(
            args[0],
            args[1]
            ),
        "rollfunc": lambda self, args: rollfunc(
            args[0],
            args[1],
            args[2],
            args[3]
            ),
        "matrix": matrixconstructor,
        "strfunc": lambda self, args: strfunc(
            args[0],
            args[1],
            self.devariables(args[2]),
            args[3],
            args[4],
            args[5],
            args[6],
            args[7],
            self.devariables(args[8]),
            args[9],
            False
            ),
        "codestr": lambda self, args: codestr(
            args[0]
            ),
        "strcalc": lambda self, args: rawstrcalc(
            args[0]
            ),
        "derivfunc": lambda self, args: derivfunc(
            args[0],
            args[1],
            self.devariables(args[2]),
            args[3],
            args[4],
            args[5],
            args[6],
            args[7],
            self.devariables(args[8]),
            args[9],
            False,
            n=args[10],
            accuracy=args[11],
            scaledown=args[12]
            ),
        "integfunc": lambda self, args: integfunc(
            args[0],
            args[1],
            self.devariables(args[2]),
            args[3],
            args[4],
            args[5],
            args[6],
            args[7],
            self.devariables(args[8]),
            args[9],
            False,
            accuracy=args[10]
            ),
        "usefunc": lambda self, args: usefunc(
            args[0],
            args[1],
            args[2],
            args[3],
            args[4],
            args[5],
            args[6],
            args[7],
            self.devariables(args[8]),
            self.delist(args[9]),
            args[10]
            ),
        "classcalc": lambda self, args: classcalc(
            self.devariables(args[0]),
            selfvar=args[1],
            restricted=args[2]
            ),
        "namespace": lambda self, args: namespace(
            self.devariables(args[0]),
            selfvar=args[1],
            restricted=args[2]
            ),
        "instancecalc": lambda self, args: instancecalc(
            self.devariables(args[0]),
            top=False,
            selfvar=args[1],
            parentvar=args[2],
            restricted=args[3]
            ),
        "brace": lambda self, args: brace(
            args[0]
            ),
        "bracket": lambda self, args: bracket(
            args[0]
            ),
        "wrap": lambda self, args: evalwrap(
            args[0]
            )
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
    calcops = ["$", "::"]
    multiargops = bools + callops + "+-@~|&;,$" + "".join(strgroupers.keys()) + "".join(groupers.keys()) + "".join(aliases.keys())
    reserved = multiargops + stringchars + "".join(strgroupers.values()) + "".join(groupers.values()) + parenchar + formatchars
    purechar = "-"
    digits = string.digits
    withvar = "__where__"
    errorvar = "__error__"
    fatalvar = "fatal"
    namevar = "name"
    messagevar = "message"
    replacer = re.compile("(?<![\s"+parenchar+"])\s+(?![\s"+parenchar+"])")
    recursion = 0
    redef = False
    useclass = None
    returned = False
    spawned = False
    calculated = None
    using = None
    pure = False
    clean = False
    all_clean = False
    tailing = False
    infix = True

    def __init__(self, variables=None, processor=None, color=None, speedy=False, maxrecursion=10):
        """Initializes The Evaluator."""
        set_e(self)
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
        """Makes A New Essentially Identically-Configured Evaluator."""
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
            self.precalc_brack,
            self.precalc_cmd
            ]
        self.calc_funcs = [
            self.calc_pure,
            self.calc_set,
            self.calc_cmd,
            self.calc_with,
            self.calc_list,
            self.calc_pair,
            self.calc_pieces,
            self.calc_condo,
            self.calc_or,
            self.calc_and,
            self.calc_unary,
            self.calc_eq,
            self.calc_eval,
            self.eval_loop,
            self.eval_lambda,
            self.eval_remove,
            self.eval_join,
            self.eval_lambda,
            self.eval_repeat,
            self.eval_lambda,
            self.eval_add,
            self.eval_lambda,
            self.eval_mod,
            self.eval_intdiv,
            self.eval_mul,
            self.eval_call
            ]
        self.sets = [
            self.set_def,
            self.set_normal
            ]
        self.calls = [
            (self.call_parenvar, True),
            (self.call_var, True),
            (self.call_lambda, True),
            (self.call_neg, True),
            (self.call_reciproc, True),
            (self.call_colon, True),
            (self.call_paren, False),
            (self.call_exp, True),
            (self.call_comp, True),
            (self.call_lambdacoeff, True),
            (self.call_method, True),
            (self.call_normal, True)
            ]
        self.funcs = evalfuncs()

    def fresh(self):
        """Resets The Variables To Their Defaults."""
        self.parens = []
        self.variables = {
            "Warning":classcalc({
                self.errorvar: True,
                self.fatalvar: False
                }),
            "Error":classcalc({
                self.errorvar: True,
                self.fatalvar: True
                }),
            "pure":funcfloat(self.funcs.purecall, "pure", reqargs=1),
            "env":funcfloat(self.funcs.envcall, "env"),
            "call":funcfloat(self.funcs.callcall, "call", reqargs=1),
            "retrieve":funcfloat(self.funcs.itemcallcall, "retrieve", reqargs=1),
            "copy":funcfloat(self.funcs.copycall, "copy", reqargs=1),
            "type":funcfloat(self.funcs.typecall, "type"),
            "str":funcfloat(self.funcs.strcall, "str"),
            "repr":funcfloat(self.funcs.reprcall, "repr"),
            "code":funcfloat(self.funcs.codecall, "code"),
            "calc":funcfloat(self.funcs.docalc, "calc", reqargs=1),
            "do":funcfloat(self.funcs.nonecalc, "do", reqargs=1),
            "fold":funcfloat(self.funcs.foldcall, "fold", reqargs=2),
            "map":funcfloat(self.funcs.mapcall, "map", reqargs=2),
            "filter":funcfloat(self.funcs.filtercall, "filter", reqargs=2),
            "for":funcfloat(self.funcs.forcall, "for", reqargs=2),
            "while":funcfloat(self.funcs.whilecall, "while", reqargs=1),
            "zip":funcfloat(self.funcs.zipcall, "zip", reqargs=1),
            "zipwith":funcfloat(self.funcs.zipwithcall, "zipwith", reqargs=2),
            "prepend":funcfloat(self.funcs.conscall, "prepend", reqargs=2),
            "append":funcfloat(self.funcs.appendcall, "append", reqargs=2),
            "row":funcfloat(self.funcs.rowcall, "row"),
            "list":funcfloat(self.funcs.listcall, "list"),
            "matrix":funcfloat(self.funcs.matrixcall, "matrix"),
            "sum":funcfloat(self.funcs.sumcall, "sum", reqargs=1),
            "prod":funcfloat(self.funcs.prodcall, "prod", reqargs=1),
            "min":funcfloat(self.funcs.mincall, "min", reqargs=1),
            "max":funcfloat(self.funcs.maxcall, "max", reqargs=1),
            "join":funcfloat(self.funcs.joincall, "join", reqargs=2),
            "connect":funcfloat(self.funcs.connectcall, "connect", reqargs=1),
            "merge":funcfloat(self.funcs.mergecall, "merge", reqargs=1),
            "sort":funcfloat(self.funcs.sortcall, "sort", reqargs=1),
            "rev":funcfloat(self.funcs.reversecall, "rev", reqargs=1),
            "round":funcfloat(self.funcs.roundcall, "round", reqargs=1),
            "num":funcfloat(self.funcs.numcall, "num"),
            "int":funcfloat(self.funcs.intcall, "int"),
            "base":funcfloat(self.funcs.basecall, "base", reqargs=2),
            "bin":funcfloat(self.funcs.bincall, "bin", reqargs=1),
            "oct":funcfloat(self.funcs.octcall, "oct", reqargs=1),
            "hex":funcfloat(self.funcs.hexcall, "hex", reqargs=1),
            "pair":funcfloat(self.funcs.paircall, "pair"),
            "dict":funcfloat(self.funcs.dictcall, "dict"),
            "eval":funcfloat(self.funcs.evalcall, "eval", reqargs=1),
            "find":funcfloat(self.funcs.findcall, "find", reqargs=2),
            "split":funcfloat(self.funcs.splitcall, "split", reqargs=1),
            "replace":funcfloat(self.funcs.replacecall, "replace", reqargs=1),
            "in":funcfloat(self.funcs.containscall, "in", reqargs=2),
            "range":funcfloat(self.funcs.rangecall, "range", reqargs=1),
            "len":funcfloat(self.funcs.lencall, "len", reqargs=1),
            "size":funcfloat(self.funcs.sizecall, "size", reqargs=1),
            "abs":funcfloat(self.funcs.abscall, "abs", reqargs=1),
            "from":funcfloat(self.funcs.instanceofcall, "from", reqargs=2),
            "iserr":funcfloat(self.funcs.iserrcall, "iserr", reqargs=1),
            "class":funcfloat(self.funcs.classcall, "class"),
            "object":funcfloat(self.funcs.instancecall, "object"),
            "func":funcfloat(self.funcs.functioncall, "func"),
            "namespace":funcfloat(self.funcs.namespacecall, "namespace"),
            "try":funcfloat(self.funcs.trycall, "try"),
            "raise":funcfloat(self.funcs.raisecall, "raise"),
            "except":funcfloat(self.funcs.exceptcall, "except"),
            "read":funcfloat(self.funcs.readcall, "read", reqargs=1),
            "write":funcfloat(self.funcs.writecall, "write", reqargs=1),
            "is":funcfloat(self.funcs.iseqcall, "is", reqargs=2),
            "include":funcfloat(self.funcs.includecall, "include", reqargs=1),
            "def":funcfloat(self.funcs.defcall, "def", reqargs=1),
            "require":funcfloat(self.funcs.requirecall, "require", reqargs=1),
            "assert":funcfloat(self.funcs.assertcall, "assert", reqargs=1),
            "import":funcfloat(self.funcs.importcall, "import", reqargs=1),
            "bitnot":funcfloat(self.funcs.bitnotcall, "bitnot", reqargs=1),
            "bitor":funcfloat(self.funcs.bitorcall, "bitor", reqargs=2),
            "bitand":funcfloat(self.funcs.bitandcall, "bitand", reqargs=2),
            "bitxor":funcfloat(self.funcs.bitxorcall, "bitxor", reqargs=2),
            "rshift":funcfloat(self.funcs.rshiftcall, "rshift", reqargs=2),
            "lshift":funcfloat(self.funcs.lshiftcall, "lshift", reqargs=2),
            "union":funcfloat(self.funcs.unioncall, "union", reqargs=2),
            "intersect":funcfloat(self.funcs.intersectcall, "intersect", reqargs=2),
            "inside":funcfloat(self.funcs.insidecall, "inside", reqargs=1),
            "python":funcfloat(self.funcs.pythonevalcall, "python", reqargs=1),
            "input":funcfloat(self.funcs.inputcall, "input"),
            "any":funcfloat(self.funcs.anycall, "any"),
            "all":funcfloat(self.funcs.allcall, "all"),
            "open":funcfloat(self.funcs.opencall, "open", reqargs=1),
            "chr":funcfloat(self.funcs.chrcall, "chr", reqargs=1),
            "ord":funcfloat(self.funcs.ordcall, "ord", reqargs=1),
            "bool":usefunc(bool, "bool", ["x"]),
            "pow":usefunc(pow, "pow", ["y", "x", "m"], reqargs=2),
            "hash":usefunc(hash, "hash", ["x"]),
            "ascii":funcfloat(self.funcs.asciicall, "ascii", reqargs=1),
            "Rand":classcalc({
                "die":funcfloat(self.funcs.randcall, "die", reqargs=1),
                "gen":evalwrap(random, "gen")
                }, name="Rand"),
            "Meta":classcalc({
                "var":funcfloat(self.funcs.getvarcall, "var", reqargs=1),
                "val":funcfloat(self.funcs.getvalcall, "val", reqargs=1),
                "use":funcfloat(self.funcs.usecall, "use"),
                "using":funcfloat(self.funcs.usingcall, "using"),
                "alias":funcfloat(self.funcs.aliascall, "alias", reqargs=1),
                "aliases":funcfloat(self.funcs.aliasescall, "aliases"),
                "paren":funcfloat(self.funcs.getparenvarcall, "paren"),
                "parens":funcfloat(self.funcs.getparenscall, "parens"),
                "unused":funcfloat(self.funcs.unusedcall, "unused"),
                "serialize":funcfloat(self.funcs.getstatecall, "serialize"),
                "deserialize":funcfloat(self.funcs.fromstatecall, "deserialize"),
                "wrap":funcfloat(self.funcs.wrapcall, "wrap", reqargs=1),
                "purify":funcfloat(self.funcs.purifycall, "purify", reqargs=2),
                "run":funcfloat(self.funcs.runcall, "run", reqargs=1),
                "global":funcfloat(self.funcs.globalcall, "global", reqargs=1),
                "del":funcfloat(self.funcs.delcall, "del", reqargs=1),
                "to":funcfloat(self.funcs.tocall, "to", reqargs=1),
                "exec":funcfloat(self.funcs.cmdcall, "exec", reqargs=1),
                "pipe":funcfloat(self.funcs.pipecall, "pipe"),
                "caller":funcfloat(self.funcs.getcallcall, "caller", reqargs=1),
                "retriever":funcfloat(self.funcs.getitemcallcall, "retriever", reqargs=1),
                "get":funcfloat(self.funcs.getattrcall, "get", reqargs=2),
                "has":funcfloat(self.funcs.hasattrcall, "has", reqargs=2),
                "memoize":funcfloat(self.funcs.memoizecall, "memoize"),
                "super":funcfloat(self.funcs.supercall, "super", reqargs=1),
                "effect":usefunc(self.setreturned, "effect")
                }, name="Meta"),
            "Math":classcalc({
                "divmod":funcfloat(self.funcs.divmodcall, "divmod", reqargs=2),
                "frac":funcfloat(self.funcs.fractioncall, "frac"),
                "simp":funcfloat(self.funcs.simpcall, "simp", reqargs=1),
                "det":funcfloat(self.funcs.detcall, "det", reqargs=1),
                "dim":funcfloat(self.funcs.dimcall, "dim", reqargs=1),
                "floor":usefunc(math.floor, "floor", ["x"]),
                "ceil":usefunc(math.ceil, "ceil", ["x"]),
                "log":usefunc(math.log10, "log", ["x"]),
                "ln":usefunc(math.log, "ln", ["x"]),
                "sqrt":usefunc(isqrt, "sqrt", ["x"]),
                "tan":usefunc(math.tan, "tan", ["x"]),
                "sin":usefunc(math.sin, "sin", ["x"]),
                "cos":usefunc(math.cos, "cos", ["x"]),
                "atan":usefunc(math.atan, "atan", ["x"]),
                "asin":usefunc(math.asin, "asin", ["x"]),
                "acos":usefunc(math.acos, "acos", ["x"]),
                "rad":usefunc(math.degrees, "rad", ["x"]),
                "deg":usefunc(math.radians, "deg", ["x"]),
                "fact":usefunc(factorial, "fact", ["x"]),
                "gcd":usefunc(gcd, "gcd", ["x", "y"]),
                "lcm":usefunc(lcm, "lcm", ["x", "y"]),
                "perm":usefunc(perm, "perm", ["n", "k"]),
                "comb":usefunc(comb, "comb", ["n", "k"]),
                "real":funcfloat(self.funcs.realcall, "real"),
                "imag":funcfloat(self.funcs.imagcall, "imag"),
                "complex":usefunc(complex, "complex", ["re", "im"]),
                "e":math.e,
                "pi":math.pi,
                "E":usefunc(E10, "E", ["x"]),
                "D":funcfloat(self.funcs.derivcall, "D", reqargs=1),
                "S":funcfloat(self.funcs.integcall, "S", reqargs=1),
                "i":complex(0.0, 1.0)
                }, name="Math"),
            "Stats":classcalc({
                "data":funcfloat(self.funcs.datacall, "data"),
                "gamma":usefunc(gamma, "gamma", ["x"]),
                "normdist":usefunc(normdist, "normdist", ["x", "mean", "stdev"], reqargs=1),
                "binomP":usefunc(binomP, "binomP", ["n", "p", "x"]),
                "poissonP":usefunc(poissonP, "poissonP", ["lambda", "x"]),
                "hypgeoP":usefunc(hypgeoP, "hypgeoP", ["x", "n", "K", "N"]),
                "tdist":usefunc(tdist, "tdist", ["x", "df"]),
                "teq":usefunc(teq, "teq", ["df"]),
                "chisqdist":usefunc(chisqdist, "chisqdist", ["x", "df"]),
                "chisqeq":usefunc(chisqeq, "chisqeq", ["df"]),
                "Fdist":usefunc(Fdist, "Fdist", ["x", "dfT", "dfE"]),
                "Feq":usefunc(Feq, "Feq", ["dfT", "dfE"]),
                "normP":usefunc(normP, "normP", ["x", "y", "mean", "stdev"], reqargs=2),
                "tP":usefunc(tP, "tP", ["x", "y", "df"]),
                "chisqP":usefunc(chisqP, "chisqP", ["x", "df"]),
                "FP":usefunc(FP, "FP", ["x", "dfT", "dfE"])
                }, name="Stats"),
            "Ops":classcalc({
                "and":usefunc(_and, "and", ["x", "y"]),
                "or":usefunc(_or, "or", ["x", "y"]),
                "xor":usefunc(_xor, "xor", ["x", "y"]),
                "not":usefunc(operator.not_, "not", ["x"]),
                "add":usefunc(operator.add, "add", ["x", "y"]),
                "sub":usefunc(operator.sub, "sub", ["x", "y"]),
                "mul":usefunc(operator.mul, "mul", ["x", "y"]),
                "div":usefunc(operator.truediv, "div", ["x", "y"]),
                "mod":usefunc(operator.mod, "mod", ["x", "y"]),
                "floordiv":usefunc(operator.floordiv, "floordiv", ["x", "y"]),
                "eq":usefunc(operator.eq, "eq", ["x", "y"]),
                "ne":usefunc(operator.ne, "ne", ["x", "y"]),
                "lt":usefunc(operator.lt, "lt", ["x", "y"]),
                "le":usefunc(operator.le, "le", ["x", "y"]),
                "gt":usefunc(operator.gt, "gt", ["x", "y"]),
                "ge":usefunc(operator.ge, "ge", ["x", "y"])
                }, name="Ops"),
            "null":matrix(0),
            "true":True,
            "false":False,
            "_":atom(),
            funcfloat.allargs : matrix(0)
            }
        self.variables.update({
            "prop":strfunc("class\xab__value__(^self,getter:getter)=getter()\xbb()", ["getter"], name="prop"),
            "Unicode":classcalc({
                "__include__" : strfunc("""self.includes$self.aliases~~Meta.alias""", ["self"], name="__include__"),
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
                "includes" : classcalc({
                    "\xf8" : "null",
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
                    "\u23E8" : "Math.E",
                    "\u2400" : rawstrcalc("\x00"),
                    "\u2401" : rawstrcalc("\x01"),
                    "\u2402" : rawstrcalc("\x02"),
                    "\u2403" : rawstrcalc("\x03"),
                    "\u2404" : rawstrcalc("\x04"),
                    "\u2405" : rawstrcalc("\x05"),
                    "\u2406" : rawstrcalc("\x06"),
                    "\u2407" : rawstrcalc("\x07"),
                    "\u2408" : rawstrcalc("\x08"),
                    "\u2409" : rawstrcalc("\x09"),
                    "\u240a" : rawstrcalc("\n"),
                    "\u240b" : rawstrcalc("\x0b"),
                    "\u240c" : rawstrcalc("\x0c"),
                    "\u240d" : rawstrcalc("\r"),
                    "\u240e" : rawstrcalc("\x0e"),
                    "\u240f" : rawstrcalc("\x0f"),
                    "\u2410" : rawstrcalc("\x10"),
                    "\u2411" : rawstrcalc("\x11"),
                    "\u2412" : rawstrcalc("\x12"),
                    "\u2413" : rawstrcalc("\x13"),
                    "\u2414" : rawstrcalc("\x14"),
                    "\u2415" : rawstrcalc("\x15"),
                    "\u2416" : rawstrcalc("\x16"),
                    "\u2417" : rawstrcalc("\x17"),
                    "\u2418" : rawstrcalc("\x18"),
                    "\u2419" : rawstrcalc("\x19"),
                    "\u241a" : rawstrcalc("\x1a"),
                    "\u241b" : rawstrcalc("\x1b"),
                    "\u241c" : rawstrcalc("\x1c"),
                    "\u241d" : rawstrcalc("\x1d"),
                    "\u241e" : rawstrcalc("\x1e"),
                    "\u241f" : rawstrcalc("\x1f"),
                    "\u2420" : rawstrcalc(" "),
                    "\u2421" : rawstrcalc("\x21"),
                    "\u2209" : strfunc("!\u2208(__)", name="\u2209", overflow=False),
                    "\u220b" : strfunc("\u2208(rev(__))", name="\u220b", overflow=False),
                    "\u220c" : strfunc("!\u220b(__)", name="\u220c", overflow=False),
                    "\u221b" : strfunc("x^(1/3)", ["x"], name="\u221b", lexical=False),
                    "\u221c" : strfunc("Math.sqrt(Math.sqrt(x))", ["x"], name="\u221c"),
                    "\u222c" : strfunc("Math.S((Math.S((f,)++args),)++args)", ["f", "args"], reqargs=1, name="\u222c"),
                    "\u222d" : strfunc("Math.S((Math.S((Math.S((f,)++args),)++args),)++args)", ["f", "args"], reqargs=1, name="\u222d")
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
        if self.validvar(name):
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

    def getitemcall(self, func):
        """Gets The Item-Callable Part Of A Function."""
        if hasitemcall(func):
            return func.itemcall
        else:
            raise AttributeError("Function has no itemcall method")

    def forshow(self, arg):
        """Prepares An Item For Showing."""
        if not istext(arg):
            return self.prepare(arg, True, True, 2)
        else:
            return str(arg)

    def converterr(self, err):
        """Converts A Caught Error Into An Error Instance."""
        if len(err) == 3 or (len(err) == 4 and err[3] is None):
            out = instancecalc({
                self.errorvar : True,
                self.fatalvar : err[2]
                })
            out.store(self.namevar, rawstrcalc(err[0]))
            out.store(self.messagevar, rawstrcalc(err[1]))
            return out
        elif len(err) == 4:
            return err[3]
        else:
            raise SyntaxError("Invalid error signature of "+repr(err))

    def speedyprep(self, item, top=False, bottom=False, indebug=False, maxrecursion=0):
        """Speedily Prepares The Output Of An Evaluation."""
        out = "class \xab"+"\n"*top+" "
        if not indebug and bottom and not top:
            out += 'raise("LoopError", "Maximum recursion depth exceeded in object preparation")'
        elif istext(item):
            out += item
        else:
            out += "__type__ := `"+self.evaltypestr(item)+"`"
        out += "\n"*top+" \xbb"
        return out

    def prepare(self, item, top=False, bottom=True, indebug=False, maxrecursion=None):
        """Prepares The Output Of An Evaluation."""
        if maxrecursion is None:
            maxrecursion = self.maxrecursion
        if istext(item):
            out = str(item)
        elif item is None:
            out = "null"
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
                    out += self.prepare(x, False, bottom, indebug, maxrecursion)+", "
                if len(item) > 0:
                    out = out[:-1]
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
                        out += self.prepare(x, False, bottom, indebug, maxrecursion)+", "
                    if len(y) > 0:
                        out = out[:-2]
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
                out += " "+self.prepare(pair(k,v), False, bottom, indebug, maxrecursion)+","
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
                    out += "\n "
            out += "}"
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
            if not bottom or self.validvar(a) or a == "()":
                out += a
            else:
                out += "("+a+")"
            if isinstance(item, pair):
                out += " -> "
            else:
                out += "/"
            b = self.prepare(part_b, False, bottom, indebug, maxrecursion)
            if not bottom or self.validvar(b) or a == "()":
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
            out += "\\"+"^"*(not item.didsnapshot())+"%"*(item.memoize)+strlist(variables,",")
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
            if not bottom or self.validvar(test) or test == "()":
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

    def splitdedent(self, inputstring, splitfunc=lambda x: x.splitlines(), top=True):
        """Splits And Unsplits By Dedents."""
        inputstring = str(inputstring)
        split = fullsplit(inputstring, self.indentchar, self.dedentchar, 1, False, iswhite, True)
        if len(split) > 1 or (split and istext(split[0])):
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
            if top > 0:
                out = self.splitdedent(new, splitfunc, False)
            else:
                out = [new]
        else:
            raise SyntaxError("Error in evaluating indentation len("+repr(split[0])+")>1")
        return out

    def iseq(self, a, b):
        """Determines Whether Two Evaluator Objects Are Really Equal."""
        return itemstate(a) == itemstate(b)

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

    def calc(self, inputstring, info="", top=False):
        """Performs Top-Level Calculation."""
        inputstring = str(inputstring)
        calculated, self.calculated = self.calculated, matrix(0)
        self.process(inputstring, info, self.setcalculated, top)
        out, self.calculated = self.calculated, calculated
        return out

    def process(self, inputstring, info="", command=None, top=None):
        """Performs Top-Level Evaluation."""
        inputstring = str(inputstring)
        calc_top = None
        if top is None:
            top = command is not None
        elif top < 0:
            calc_top = top
            top = False
        if calc_top is None:
            calc_top = top
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
            self.proc_calc(inputstring, calc_top, command)
        finally:
            if top:
                if not self.spawned:
                    self.processor.addcommand(inputstring)
                self.spawned = self.spawned or spawned
                self.tailing = tailing
            self.clean_end(cleaned)
            self.recursion -= 1

    def do_pre(self, item, top=-1):
        """Does The Pre-Processing."""
        for func in self.preprocs:
            item = func(item, top)
        for func in self.precalcs:
            item = func(item)
        return item

    def proc_calc(self, original, top, command):
        """Gets The Value Of An Expression."""
        if top < -1:
            calc_top = False
        else:
            calc_top = top
        item = self.do_pre(original, calc_top)
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
            try:
                out = self.calc_proc(inputlist[x], calc_top)
                self.printdebug(self.prepare(out, False, True, True)+" <<= "+inputlist[x])
            finally:
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
            try:
                out = self.getcall(self.using)([codestr(inputstring)])
                self.printdebug(self.prepare(out, False, True, True)+" <:: "+original)
            finally:
                self.recursion -= 1
            return out
        else:
            expression = self.remformat(inputstring)
            return self.calc_next(expression, self.calc_funcs, True)

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
                value = self.do_pre(item[1])
                if value:
                    command += self.lambdamarker+self.wrap(value)+self.lambdamarker
                else:
                    command += self.lambdamarker*2
            elif item[0] in self.rawstringchars:
                command += self.wrap(rawstrcalc(item[1]))
            elif item[0] in self.stringchars + "".join(self.strgroupers.keys()) + "".join(self.strgroupers.values()):
                command += self.wrap(strcalc(item[1]))
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
            openstr, closestr = self.indentchar, self.dedentchar
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
                    for x in xrange(0, len(lines)):
                        check = leading(lines[x])
                        if x:
                            if check > current:
                                levels.append(current)
                                current = check
                                lines[x-1] = lines[x-1]+openstr
                            elif check in levels:
                                point = levels.index(check)+1
                                closers = closestr*(len(levels[point:])+1)
                                newline = ""
                                for c in lines[x-1]:
                                    if c in self.groupers.values():
                                        newline += closers
                                        closers = ""
                                    newline += c
                                lines[x-1] = newline+closers
                                levels = levels[:point]
                                current = levels.pop()
                            elif current != check:
                                raise ExecutionError("IndentationError", "Illegal dedent to unused indentation level in line "+lines[x]+" (#"+str(x)+")")
                            new.append(lines[x-1])
                        else:
                            current = check
                    closers = closestr*(len(levels)-1)
                    newline = ""
                    for c in lines[-1]:
                        if c in self.groupers.values():
                            newline += closers
                            closers = ""
                        newline += c
                    new.append(newline+closers)
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
                command += self.wrap(codestr(""))
            elif len(x) == 1:
                command += self.wrap(codestr(x[0]))
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
                command += self.wrap(brace(self.splitdedent(original, lambda x: x.split(","))))
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
                command += self.wrap(bracket(self.splitdedent(original, lambda x: x.split(","))))
            else:
                raise SyntaxError("Error in evaluating brackets len("+repr(x)+")>1")
        return command

    def precalc_cmd(self, inputstring):
        """Evaluates Statements."""
        inputlist = carefulsplit(inputstring, "::", counters={self.indentchar:self.dedentchar})
        out = [basicformat(inputlist[0])]
        for x in xrange(1, len(inputlist)):
            if ";;" in inputlist[x]:
                a,b = inputlist[x].split(";;", 1)
                new = self.wrap(basicformat(a))+" ;; "+basicformat(b)
            else:
                new = self.wrap(basicformat(inputlist[x]))
            out.append(new)
        return " :: ".join(out)

    def calc_next(self, arg, funcs, top=False):
        """Calls The Next Function."""
        while True:
            if istext(arg):
                arg = basicformat(arg)
            if not arg:
                raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
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
                try:
                    if funcs:
                        out = func(arg, funcs)
                    else:
                        out = func(arg)
                finally:
                    self.clean_end(cleaned)
                return out

    def unclean(self, all_clean=False):
        """Sets clean."""
        self.clean = False
        if all_clean is not None:
            self.all_clean = all_clean

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
        if len(args) > 0:
            func = basicformat(func)
            original = []
            for arg in args:
                original.append(self.namefind(basicformat(arg)))
            displayer = func+" :: "+strlist(original, " :: ")
            self.printdebug("::> "+displayer)
            self.recursion += 1
            try:
                if func:
                    cleaned = self.clean_begin()
                    item = self.funcfind(func)
                    params = []
                    for x in xrange(0, len(original)):
                        if x != len(original)-1 or original[x]:
                            params.append(codestr(original[x]))
                    self.clean_end(cleaned)
                    out = self.call_colon_set(item, params)
                else:
                    out = codestr(strlist(original, " :: "))
                self.printdebug(self.prepare(out, False, True, True)+" <:: "+displayer)
            finally:
                self.recursion -= 1
            return out
        else:
            return self.calc_next(inputstring, calc_funcs)

    def calc_pure(self, expression, calc_funcs):
        """Toggles Pure On And Off."""
        if madeof(expression, self.purechar):
            if len(expression) < 3:
                raise ExecutionError("SyntaxError", "Pure toggles must be at least three characters")
            elif self.pure > 1:
                raise ExecutionError("PureError", "A pure toggle was attempted inside of a pure statement")
            else:
                self.pure = not self.pure
                return self.pure
        else:
            return self.calc_next(expression, calc_funcs)

    def calc_with(self, expression, calc_funcs):
        """Evaluates With Clauses."""
        inputlist = expression.split("$")
        if len(inputlist) > 1:
            cleaned = self.clean_begin()
            inputlist.reverse()
            item = inputlist.pop()
            withclass = classcalc(selfvar=self.withvar)
            for x in inputlist:
                inputstring = basicformat(x)
                if x:
                    withclass.process(x)
                else:
                    raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
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
                    sides[0] = basicformat(sides[0][:-1])
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
        if not self.readytofunc(sides[0], allowed="."):
            raise ExecutionError("SyntaxError", "Could not set to invalid variable name "+sides[0])
        else:
            classlist = []
            delfrom = None
            if self.useclass:
                if isinstance(self.useclass, tuple):
                    delfrom = self.variables[self.useclass[0]].doset
                else:
                    classlist = [self.useclass]
            method = False
            if "." in sides[0]:
                method = True
                classlist += sides[0].split(".")
                for x in xrange(0, len(classlist)-1):
                    if not self.validvar(classlist[x]):
                        raise ExecutionError("SyntaxError", "Could not set to invalid class name "+classlist[x])
                sides[0] = classlist.pop()
                if delfrom is not None and classlist[0] in delfrom:
                    del delfrom[classlist[0]]
                    delfrom = None
                useclass = self.funcfind(classlist[0])
                doset = [useclass, classlist[1]]
                if isinstance(useclass, classcalc):
                    for x in xrange(1, len(classlist)):
                        last = useclass
                        useclass = useclass.retrieve(classlist[x])
                        if not isinstance(useclass, classcalc):
                            raise ExecutionError("ClassError", "Could not set "+classlist[x]+" in "+self.prepare(last, False, True, True))
                else:
                    raise ExecutionError("VariableError", "Could not find class "+self.prepare(classlist[0], False, True, True))
            elif classlist:
                useclass = self.funcfind(classlist[0])
            else:
                useclass = None
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
                        elif self.redef:
                            self.setreturned()
                            self.variables[value[0]] = value[1]
                        elif self.variables[value[0]] is not value[1]:
                            raise ExecutionError("RedefinitionError", "The variable "+value[0]+" already exists")
                        if docalc:
                            out = value[1]
                        else:
                            out = strfloat(value[0], name=value[0])
                    else:
                        if method:
                            doset[0].doset[doset[1]] = None
                        if value[0] not in useclass.variables:
                            if not method:
                                useclass.store(value[0], value[1])
                            elif self.redef:
                                self.setreturned()
                                useclass.store(value[0], value[1])
                            else:
                                raise ExecutionError("RedefinitionError", "Cannot add attribute "+value[0])
                        elif useclass.variables[value[0]] is not value[1]:
                            if self.redef:
                                self.setreturned()
                                useclass.store(value[0], value[1])
                            else:
                                raise ExecutionError("RedefinitionError", "Cannot redefine attribute "+value[0])
                        if docalc:
                            out = value[1]
                        else:
                            out = strfunc(useclass.selfvar+".("+value[0]+")", [], {useclass.selfvar:useclass}, value[0])
                    if delfrom is not None and value[0] in delfrom:
                        del delfrom[value[0]]
                    return out

    def readytofunc(self, expression, extra="", allowed=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        funcparts = expression.split(self.parenchar, 1)
        out = funcparts[0] != "" and (self.validvar(funcparts[0], extra, allowed)) and (len(funcparts) == 1 or funcparts[1].endswith(self.parenchar))
        if out and len(funcparts) != 1:
            return not self.insideouter(funcparts[1][:-1])
        else:
            return out

    def set_def(self, sides):
        """Creates Functions."""
        if self.parenchar in sides[0] and sides[0].endswith(self.parenchar):
            sides[0] = sides[0].split(self.parenchar, 1)
            sides[0][0] = basicformat(sides[0][0])
            sides[0][1] = self.namefind(self.parenchar+sides[0][1])
            return (sides[0][0], self.eval_set(sides[0][1], sides[1], sides[0][0]))

    def set_normal(self, sides):
        """Performs =."""
        if self.validvar(sides[0]):
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
                inputlist[x] = basicformat(inputlist[x])
                if inputlist[x]:
                    out.append(self.calc_next(inputlist[x], calc_funcs))
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
                if item:
                    itemlist.append(self.calc_next(item, calc_funcs))
                else:
                    itemlist.append(matrix(0))
            out = itemlist[-1]
            for x in reversed(xrange(0, len(itemlist)-1)):
                out = pair(itemlist[x], out)
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
                        raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
                    else:
                        if istext(inputlist[x-1]):
                            inputlist[x-1] = self.calc_next(inputlist[x-1], calc_funcs)
                        args.append(inputlist[x-1])
                    if x == len(inputlist)-1:
                        raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
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
                            if hasgt:
                                raise ExecutionError("SyntaxError", "Illegal double greater than")
                            else:
                                hasgt = True
                        elif c == "<":
                            if haslt:
                                raise ExecutionError("SyntaxError", "Illegal double less than")
                            else:
                                haslt = True
                        elif c == "\u2260":
                            if hasne:
                                raise ExecutionError("SyntaxError", "Illegal double not equals")
                            else:
                                hasne = True
                        elif c == "!":
                            if inv:
                                raise ExecutionError("SyntaxError", "Illegal double negation")
                            else:
                                inv = True
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
                        return False
            return True

    def calc_eval(self, expression, calc_funcs):
        """Evaluates An Expression."""
        self.unclean(None)
        self.printdebug("==> "+expression)
        self.recursion += 1
        try:
            out = self.eval_check(self.calc_next(expression, calc_funcs), True)
            self.printdebug(self.prepare(out, False, True, True)+" <== "+expression)
        finally:
            self.recursion -= 1
        return out

    def eval_loop(self, expression, eval_funcs):
        """Performs List Comprehension."""
        complist = expression.split("~")
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
            return self.eval_loop_set(lists, item)

    def eval_loop_set(self, lists, func):
        """Performs Recursive Comprehension."""
        original = getcopy(func)
        if hascall(original):
            func = self.getcall(original)
        else:
            raise ExecutionError("ValueError", "Can only loop with a function")
        new_lists = []
        out_type = "list"
        for value, argnum in reversed(lists):
            value = getcopy(value)
            if hasmatrix(value):
                value = getmatrix(value)
                if isinstance(value, strcalc):
                    out_type = "str"
                elif out_type == "list" and not value.onlydiag():
                    out_type = "row"
                value = value.getitems()
            else:
                value = [value]
            new_lists.append((value, argnum))
        lists = new_lists
        out = []
        while lists:
            params = []
            new_lists = []
            for units, argnum in lists:
                params += units[:argnum]
                units = units[argnum:]
                if units:
                    new_lists.append((units, argnum))
            if params:
                overflow, self.overflow = self.overflow, []
                value = func(params)
                if self.overflow:
                    raise ExecutionError("ArgumentError", "Excess arguments of "+strlist(self.overflow, ", ", lambda x: self.prepare(x, False, True, True))+" to "+self.prepare(original, False, True, True))
                elif not isnull(value):
                    out.append(value)
                self._overflow = overflow
            else:
                break
            lists = new_lists
        if out_type == "list":
            return diagmatrixlist(out)
        elif out_type == "row":
            return rowmatrixlist(out)
        elif out_type == "str":
            return rawstrcalc(strlist(out, "", lambda x: self.prepare(x, True, False)))
        else:
            raise SyntaxError("Invalid eval_loop lists out_type of "+str(out_type))

    def eval_lambda(self, expression, eval_funcs=None):
        """Evaluates Lambdas."""
        if expression.startswith(self.lambdamarker):
            out = expression[1:].split(self.lambdamarker, 1)
            out[0] = self.namefind(out[0])
            if len(out) == 1:
                return strfloat(out[0])
            elif not out[0]:
                return strfunc(out[1])
            else:
                return self.eval_set(out[0], out[1])
        elif eval_funcs is None:
            raise SyntaxError("Invalid eval_lambda call")
        else:
            return self.calc_next(expression, eval_funcs)

    def eval_set(self, original, funcstr, name=None):
        """Performs Setting."""
        temp = self.outersplit(self.namefind(basicformat(original)), ",", top=False)
        params = []
        personals = {}
        allargs = None
        inopt = 0
        reqargs = None
        lexical = True
        memoize = False
        done = False
        while done == False:
            if lexical and temp[0].startswith("^"):
                temp[0] = temp[0][1:]
                lexical = False
            elif not memoize and temp[0].startswith("%"):
                temp[0] = temp[0][1:]
                memoize = True
            else:
                done = True
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
                        raise ExecutionError("ArgumentError", "Catch-all argument must come last")
                elif x.startswith("-"):
                    x = x[1:]
                    inopt = 2
                    if reqargs is None:
                        reqargs = len(params)
                elif x.startswith("+"):
                    if inopt:
                        raise ExecutionError("ArgumentError", "Cannot have required args after optional args")
                    else:
                        x = x[1:]
                else:
                    special = False
                equal_test = x.split("=", 1)
                colon_test = x.split(":", 1)
                if len(equal_test) > 1 and equal_test[0] and self.validvar(equal_test[0]):
                    inopt = 3
                    if reqargs is None:
                        reqargs = len(params)
                    equal_test[0] = basicformat(equal_test[0])
                    personals[equal_test[0]] = self.calc(equal_test[1], " <\\=")
                    x = equal_test[0]
                elif len(colon_test) > 1 and colon_test[0] and self.validvar(colon_test[0]):
                    if not special:
                        doparam = False
                    colon_test[0] = basicformat(colon_test[0])
                    personals[colon_test[0]] = self.calc(colon_test[1], " <\\:")
                    x = colon_test[0]
                elif inopt == 1:
                    raise ExecutionError("ArgumentError", "Cannot have normal args after optional args")
                elif not x or not self.validvar(x):
                    raise ExecutionError("VariableError", "Could not set to invalid variable "+x)
                else:
                    x = basicformat(x)
                if doallargs:
                    allargs = x
                if doparam:
                    params.append(x)
                if inopt > 1:
                    inopt = 1
        return strfunc(funcstr, params, personals, name, allargs=allargs, reqargs=reqargs, memoize=memoize, lexical=lexical)

    def eval_join(self, expression, eval_funcs):
        """Performs Concatenation."""
        inputlist = expression.split("++")
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
                for i in xrange(0, len(items)):
                    x = items[i]
                    if i and hasattr(x, "rop_join"):
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
                    out = rawstrcalc("")
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
                    return dictionary(out)
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

    def eval_remove(self, expression, eval_funcs):
        """Performs Removal."""
        inputlist = expression.split("--")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            item = self.calc_next(inputlist[0], eval_funcs)
            params = []
            for x in xrange(1, len(inputlist)):
                params.append(self.calc_next(inputlist[x], eval_funcs))
            item = getcopy(item)
            test = NotImplemented
            if hasattr(item, "op_remove"):
                try:
                    test = item.op_remove(params)
                except NotImplementedError:
                    test = NotImplemented
            if test is NotImplemented:
                for param in params:
                    if hasattr(param, "rop_remove"):
                        try:
                            temp = param.rop_remove(item)
                        except NotImplementedError:
                            temp = NotImplemented
                        if temp is not NotImplemented:
                            params.remove(param)
                            item = getcopy(temp)
            if test is not NotImplemented:
                item = test
            elif isinstance(item, classcalc):
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

    def eval_repeat(self, expression, eval_funcs):
        """Evaluates Repeats."""
        inputlist = expression.split("**")
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

    def eval_add(self, expression, eval_funcs):
        """Evaluates The Addition Part Of An Expression."""
        inputlist = splitinplace(expression.split("+"), "-", self.callops)
        if not inputlist:
            raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
        elif len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                item = self.calc_next(inputlist[x], eval_funcs)
                if isinstance(item, negative):
                    value = item + value
                else:
                    value = value + item
            return value

    def eval_mod(self, expression, eval_funcs):
        """Evaluates The Modulus Part Of An Expression."""
        inputlist = expression.split("%")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                value = value % self.calc_next(inputlist[x], eval_funcs)
            return value

    def eval_intdiv(self, expression, eval_funcs):
        """Evaluates The Floor Division Part Of An Expression."""
        inputlist = expression.split("//")
        if len(inputlist) == 1:
            return self.calc_next(inputlist[0], eval_funcs)
        else:
            self.unclean()
            value = self.calc_next(inputlist[0], eval_funcs)
            for x in xrange(1, len(inputlist)):
                value = value // self.calc_next(inputlist[x], eval_funcs)
            return value

    def eval_mul(self, expression, eval_funcs):
        """Evaluates The Multiplication Part Of An Expression."""
        original = expression.split("*")
        if "" in original:
            raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
        else:
            inputlist = splitinplace(original, "/")
            if not inputlist:
                raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
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

    def eval_call(self, original, top=True):
        """Evaluates A Variable."""
        inputstring = basicformat(original)
        self.printdebug("=> "+inputstring)
        if inputstring:
            self.recursion += 1
            cleaned = self.clean_begin(None, None)
            try:
                for func, ifbottom in self.calls:
                    if ifbottom or top:
                        out = func(inputstring)
                        if out is not None:
                            break
                self.printdebug(self.prepare(out, False, True, True)+" <= "+inputstring)
            finally:
                self.clean_end(cleaned)
                self.recursion -= 1
            return out
        else:
            raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")

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
                if isinstance(value, (bool, complex)):
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
        return hasnum(item) or islist(item)

    def call_var(self, inputstring):
        """Checks If Variable."""
        if inputstring in self.variables:
            self.unclean()
            item, key = self.getfind(inputstring, True)
            if istext(item):
                value = self.calc(str(item), " | var")
            elif item is None:
                value = matrix(0)
            elif self.convertable(item):
                value = item
            else:
                raise ExecutionError("ValueError", "Unconvertable variable value of "+repr(item))
            if isprop(value):
                value = self.deprop(value)
            else:
                self.variables[key] = value
            return value

    def call_parenvar(self, inputstring):
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
                elif item is None:
                    value = matrix(0)
                elif self.convertable(item):
                    value = item
                else:
                    raise ExecutionError("ValueError", "Unconvertable variable value of "+repr(item))
                return value

    def deprop(self, value):
        """Evaluates Property Objects."""
        while isprop(value):
            value = self.getcall(value)(None)
        return value

    def call_lambda(self, inputstring):
        """Wraps Lambda Evaluation."""
        if inputstring.startswith(self.lambdamarker):
            return self.eval_lambda(inputstring)

    def call_neg(self, inputstring):
        """Evaluates Unary -."""
        if inputstring.startswith("-"):
            self.unclean()
            inputstring = basicformat(inputstring[1:])
            if inputstring:
                return negative(self.eval_call(inputstring))
            else:
                return -1

    def call_reciproc(self, inputstring):
        """Evaluates /."""
        if inputstring.startswith("/"):
            self.unclean()
            inputstring = basicformat(inputstring[1:])
            if inputstring:
                return reciprocal(self.eval_call(inputstring))
            else:
                raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")

    def call_exp(self, inputstring):
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
                elif x == 0 or x == len(inputlist)-1:
                    raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")
                else:
                    level += 1
            return value

    def call_colon(self, inputstring):
        """Evaluates Colons."""
        if ":" in inputstring:
            cleaned = self.clean_begin()
            inputlist = inputstring.split(":")
            if inputlist[0]:
                item = self.funcfind(inputlist[0])
                params = []
                for x in xrange(1, len(inputlist)):
                    if inputlist[x]:
                        params.append(getcopy(self.eval_check(self.eval_call(inputlist[x]), True)))
                self.clean_end(cleaned)
                return self.call_colon_set(item, params)
            else:
                raise ExecutionError("SyntaxError", "Null must be enclosed in parentheses")

    def call_colon_set(self, item, params):
        """Performs Colon Function Calls."""
        overflow, self.overflow = self.overflow, []
        if isnull(item):
            if params:
                raise ExecutionError("NullError", "Null cannot be called")
            else:
                value = item
        elif hasitemcall(item):
            value = self.getitemcall(item)(params)
        elif ismatrix(item):
            value = self.getitemcall(getmatrix(item))(params)
        elif isfunc(item):
            value = self.getcall(item)(params)
        elif len(params) == 0:
            value = item
        else:
            raise ExecutionError("ArgumentError", "Excess arguments of "+strlist(params, ", ", lambda x: self.prepare(x, False, True, True))+" to "+self.prepare(item, False, True, True))
        while len(self.overflow) > 0:
            temp = self.overflow[:]
            self.overflow = []
            value = self.call_colon_set(value, temp)
        self._overflow = overflow
        return value

    def unusedarg(self):
        """Returns An Unused Arg."""
        out = "'"
        while "__"+out+"__" in self.variables:
            out += "'"
        return "__"+out+"__"

    def call_paren(self, original):
        """Evaluates Parentheses."""
        inputstring = (self.parenchar*2).join(switchsplit(self.replacer.sub(self.parenchar*2, original), self.digits, notstring=self.reserved))
        if self.parenchar in inputstring:
            self.printdebug("(|) "+inputstring) 
            templist = inputstring.split(self.parenchar)
            checkops = delspace(self.callops, self.subparenops)
            inputlist = [[]]
            feed = inputlist[0]
            last = False
            for x in xrange(0, len(templist)):
                templist[x] = basicformat(templist[x])
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
            try:
                values = []
                cleaned = self.clean_begin()
                for i in xrange(0, len(inputlist)):
                    l = inputlist[i]
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
                        item = strfunc(autoarg+l[0], [autoarg], overflow=False).call([values.pop()])
                    else:
                        item = self.eval_call(l[0], False)
                    args = []
                    for x in xrange(1, len(l)):
                        if l[x]:
                            args.append(self.eval_call(l[x], False))
                    if i == len(inputlist)-1 and not values:
                        self.clean_end(cleaned)
                    item = self.call_paren_do(item, args)
                    if values and isfunc(item) and self.infix:
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
            finally:
                self.recursion -= 1
            return value

    def call_paren_do(self, item, arglist):
        """Does Parentheses Calling."""
        while arglist:
            infixed = False
            while not isfunc(item):
                if arglist:
                    arg = arglist.pop(0)
                    if isfunc(arg) and self.infix:
                        cleaned = self.clean_begin()
                        if arglist:
                            arg = self.call_paren_do(arg, [arglist.pop(0)])
                        item = self.call_paren_do(arg, [item])
                        self.clean_end(cleaned)
                        infixed = True
                    elif not isnull(arg):
                        item = item * arg
                else:
                    return item
            if not arglist:
                if infixed:
                    args = None
                else:
                    args = []
            elif isinstance(arglist[0], matrix) and arglist[0].onlydiag():
                args = arglist.pop(0).getdiag()
                if isinstance(item, (strfunc, usefunc)) and item.overflow and len(args) > len(item.variables):
                    args = args[:len(item.variables)-1] + [diagmatrixlist(args[len(item.variables)-1:])]
            else:
                args = [arglist.pop(0)]
            if args is not None:
                overflow, self.overflow = self.overflow, []
                item = self.getcall(getcopy(item))(getcopy(args))
                if self.overflow:
                    raise ExecutionError("ArgumentError", "Excess arguments of "+strlist(self.overflow, ", ", lambda x: self.prepare(x, False, True, True))+" to "+self.prepare(item, False, True, True))
                self._overflow = overflow
        return item

    def call_comp(self, inputstring):
        """Performs Function Composition."""
        if ".." in inputstring:
            self.unclean()
            funclist = []
            for item in inputstring.split(".."):
                funclist.append(self.wrap(self.eval_call(item)))
            return strfunc(strlist(funclist, "(")+"("*bool(funclist)+strfunc.allargs+")"*len(funclist), overflow=False)

    def call_lambdacoeff(self, inputstring):
        """Evaluates Lambda Coefficients."""
        parts = inputstring.split(self.lambdamarker, 1)
        if len(parts) > 1:
            return self.eval_call(parts[0]+self.wrap(self.eval_lambda(self.lambdamarker+parts[1])))

    def call_method(self, inputstring):
        """Returns Method Instances."""
        if "." in inputstring:
            itemlist = inputstring.split(".")
            isfloat = len(itemlist) < 3
            for item in itemlist:
                isfloat = isfloat and (not item or madeof(item, self.digits))
            if not isfloat:
                self.unclean()
                itemlist[0] = self.funcfind(itemlist[0])
                out = itemlist[0]
                for x in xrange(1, len(itemlist)):
                    out = self.getmethod(out, itemlist[x])
                return out

    def getmethod(self, item, methodname, check=False):
        """Gets A Method."""
        new = None
        key = self.namefind(methodname)
        if hasattr(item, "getmethod"):
            new = item.getmethod(key)
        elif hasattr(item, key):
            test = getattr(item, key)
            if hasnum(test):
                new = test
            elif hasattr(test, "__doc__"):
                docstring = basicformat(test.__doc__)
                if docstring.startswith("(|") and "|)" in docstring:
                    rabstring = docstring[2:].split("|)")[0]
                    if ":" in rabstring:
                        rabcheck, rabstring = rabstring.split(":", 1)
                        rabcheck = superformat(rabcheck)
                        if rabcheck == "rabbit":
                            if check:
                                return True
                            rabstring = basicformat(rabstring)
                            inputstring = self.prepare(item, False, True)+".("+key+")"
                            if not rabstring:
                                new = evalwrap(self, test, inputstring)
                            elif rabstring.startswith("="):
                                rabarg = eval(basicformat(rabstring[1:]))
                                new = evalwrap(test, inputstring, rabarg)
                            elif ":" in rabstring:
                                name, rabargs = basicformat(rabstring).split(":", 1)
                                name = basicformat(name)
                                if not name:
                                    new = eval(rabargs)
                                else:
                                    if rabargs:
                                        args, kwargs = eval(rabargs)
                                    else:
                                        args, kwargs = [], {}
                                    if name == "usefunc":
                                        new = usefunc(test, *args, **kwargs)
                                    elif name == "funcfloat":
                                        new = funcfloat(test, *args, **kwargs)
                                    elif name == "unifunc":
                                        new = unifunc(test, *args, **kwargs)
                                    elif name == "evalwrap":
                                        new = evalwrap(test, *args, **kwargs)
                                    else:
                                        raise ExecutionError("ValueError", "Invalid Rabbit wrapper of "+name)
                            else:
                                raise ExecutionError("ValueError", "Invalid Rabbit wrapping of "+rabstring)
        if check:
            return new is not None
        elif new is None:
            raise ExecutionError("AttributeError", "Cannot get method "+key+" from "+self.prepare(item, False, True, True))
        else:
            return new

    def call_normal(self, inputstring):
        """Returns Argument."""
        return self.eval_check(inputstring)

    def getparen(self, num):
        """Gets A Parenthesis."""
        test = self.parens[num]
        if istext(test):
            return basicformat(test)
        elif isinstance(test, bracket):
            return test.calc()
        else:
            return test

    def namefind(self, varname, follow=False):
        """Finds A Name."""
        varname = basicformat(varname)
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
            item = basicformat(item)
            original = item
            self.printdebug("> "+self.prepare(original, False, True, True))
            self.recursion += 1
            try:
                if item in self.variables:
                    item = self.variables[item]
                else:
                    item = self.calc(item, " >")
                self.printdebug(self.prepare(item, False, True, True)+" < "+self.prepare(original, False, True, True))
            finally:
                self.recursion -= 1
        return item

    def find(self, *args, **kwargs):
        """Wraps getfind."""
        out, _ = self.getfind(*args, **kwargs)
        return out

    def getfind(self, key, follow=False):
        """Finds A String."""
        out = key
        old = None
        while not self.iseq(old, out):
            old = out
            out, key = self.finding(key, follow)
        return out, key

    def finding(self, key, follow=False):
        """Performs String Finding."""
        out = key
        if istext(key):
            out = self.namefind(key, follow)
            if istext(out) and out in self.variables and (follow or istext(self.variables[out])):
                key, out = out, self.variables[key]
        return out, key

    def condense(self):
        """Simplifies Variable Hierarchies."""
        for x in self.variables:
            self.variables[x] = self.find(x, True)

    def validvar(self, varname, extra="", allowed=""):
        """Determines If A Variable Name Is Valid."""
        if not varname or madeof(varname, self.digits):
            return False
        else:
            reserved = self.reserved+extra
            for x in varname:
                if x in reserved and x not in allowed:
                    return False
            return True

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
            return "null"
        elif hasattr(item, "evaltype"):
            if istext(item.evaltype):
                return item.evaltype
            else:
                return item.evaltype()
        elif isinstance(item, complex):
            return "complex"
        elif isinstance(item, bool):
            return "bool"
        elif isint(item):
            return "int"
        elif isnum(item):
            return "num"
        else:
            return namestr(item)

    def typecalc(self, item):
        """Finds A Type."""
        if hasattr(item, "typecalc"):
            return item.typecalc()
        else:
            return rawstrcalc(self.evaltypestr(item))

    def getvars(self):
        """Gets Variables Absent selfvar."""
        out = self.variables.copy()
        if self.useclass:
            del out[self.useclass]
        if classcalc.selfvar in out:
            del out[classcalc.selfvar]
        return out

    def frompython(self, item, *args, **kwargs):
        """Converts A Python Object To A Rabbit Object."""
        if item is None:
            out = atom()
        elif istext(item):
            out = rawstrcalc(item)
        elif isinstance(item, tuple):
            out = diagmatrixlist(map(self.frompython, item), clean=False)
        elif islist(item):
            out = rowmatrixlist(map(self.frompython, item), clean=False)
        elif isinstance(item, dict):
            out = {}
            for k,v in item.items():
                out[self.frompython(k)] = self.frompython(v)
            out = dictionary(out)
        elif hasnum(item):
            out = item
        else:
            out = evalwrap(item, *args, **kwargs)
        return out

    def topython(self, item):
        """Converts A Rabbit Object To A Python Object."""
        if isinstance(item, self.tempobjects):
            out = self.topython(item.calc())
        elif isinstance(item, atom):
            out = None
        elif isinstance(item, strcalc):
            out = str(item)
        elif isinstance(item, matrix):
            out = map(self.topython, item.getitems())
            if item.onlydiag():
                out = tuple(out)
            else:
                out = list(out)
        elif isinstance(item, dictionary):
            out = {}
            for k,v in item.a:
                out[self.topython(k)] = self.topython(v)
        elif isinstance(item, evalwrap):
            out = item.obj
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

    def findfile(self, original):
        """Does A file."""
        filename = os.path.relpath(os.path.normcase(original))
        tests = [filename, filename+".rab"]
        for dirpath in sys.path:
            for filepath in tests:
                test = os.path.abspath(os.path.join(dirpath, filepath))
                if os.path.isfile(test):
                    return test
        raise ExecutionError("IOError", "Could not find file "+str(original))
