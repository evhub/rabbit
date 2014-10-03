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

from .carrot.file import *
from .fraction import *
from .data import *

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

class evalfuncs(object):
    """Implements Evaluator Functions."""
    typefuncs = {
        }

    def usecall(self, variables):
        """Uses A Default Statement."""
        e.setreturned()
        if not variables:
            e.using = None
        else:
            e.overflow = variables[1:]
            e.using = variables[0]
        return matrix(0)

    def delcall(self, variables):
        """Deletes A Variable."""
        e.setreturned()
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to del")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                original = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            if original in e.variables:
                out = e.variables[original]
                del e.variables[original]
            elif "." in original:
                test = original.split(".")
                item = test.pop()
                useclass = e.find(test[0], True)
                if isinstance(useclass, classcalc):
                    last = useclass
                    for x in xrange(1, len(test)):
                        useclass = usecla(test[x])
                        if not isinstance(useclass, classcalc):
                            raise ExecutionError("ClassError", "Could not delete "+test[x]+" in "+e.prepare(last, False, True, True))
                else:
                    raise ExecutionError("VariableError", "Could not find class "+test[0])
                out = useclass.retrieve(item)
                useclass.remove(item)
            else:
                raise ExecutionError("VariableError", "Could not find "+original)
            return out

    def iseqcall(self, variables):
        """Determines Whether All Arguments Are Equal."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to is")
        else:
            out = True
            for x in xrange(0, len(variables)-1):
                out = out and e.iseq(variables[x], variables[x+1])
            return out

    def includecall(self, variables):
        """Includes A Class In The Global Namespace."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to include")
        else:
            e.setreturned()
            out = []
            for arg in variables:
                last = None
                while isinstance(arg, instancecalc):
                    if last is None or not e.iseq(last, arg):
                        last = arg
                        arg = arg.include()
                    else:
                        raise ExecutionError("LoopError", "Illegal infinite recursive loop in __include__")
                if isinstance(arg, classcalc):
                    out.append(classcalc(e.setvars(arg.getvars(True))))
                else:
                    raise ExecutionError("ValueError", "Can only include a class")
            if len(out) == 1:
                return out[0]
            else:
                return diagmatrixlist(out)

    def usingcall(self, variables):
        """Retrieves The Current Function Being Used."""
        e.setreturned()
        e.overflow = variables
        if e.using is None:
            return matrix(0)
        else:
            return e.using

    def envcall(self, variables):
        """Retrieves A Class Of The Global Environment."""
        e.setreturned()
        e.overflow = variables
        return classcalc(e.getvars())

    def trycall(self, variables):
        """Catches Errors."""
        result, err = catch(self.docalc, variables, " | try")
        if err:
            return rowmatrixlist([matrix(0), e.converterr(err)])
        else:
            return rowmatrixlist([result, matrix(0)])

    def raisecall(self, variables):
        """Raises An Error."""
        if not variables:
            raise ExecutionError("Error", "An error occured")
        elif len(variables) == 1:
            if isinstance(variables[0], instancecalc) and self.iserrcall(variables):
                name = variables[0].getmethod(e.namevar)
                if name:
                    name = e.prepare(name, False, False)
                else:
                    name = "Error"
                message = variables[0].getmethod(e.messagevar)
                if message:
                    message = e.prepare(message, False, False)
                else:
                    message = "An error occured"
                fatal = variables[0].getmethod(e.fatalvar)
                if fatal:
                    fatal = bool(fatal)
                else:
                    fatal = False
                raise ExecutionError(name, message, fatal, variables[0])
            elif isinstance(variables[0], evalwrap):
                raise variables[0].obj
            else:
                raise ExecutionError("Error", e.prepare(variables[0], False, False))
        else:
            raise ExecutionError(e.prepare(variables[0], False, False), strlist(variables[1:], "; ", lambda x: e.prepare(x, False, False)))

    def exceptcall(self, variables):
        """Excepts Errors."""
        if not variables:
            return rowmatrixlist([matrix(0), False])
        elif isinstance(variables[0], matrix) and variables[0].y == 1 and variables[0].x == 2:
            items = variables[0].items()
            if self.iserrcall([items[1]]):
                for check in variables[1:]:
                    if items[1] == check or items[1].getmethod(e.namevar) == check:
                        return rowmatrixlist([items[0], True])
                return self.raisecall([items[1]])
            else:
                return rowmatrixlist([items[0], False])
        else:
            raise ExecutionError("ValueError", "Can only except the result of a try")

    def instanceofcall(self, variables):
        """Determines Whether Something Is An Instance Of Something Else."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to from")
        else:
            if isinstance(variables[0], evalwrap):
                for x in xrange(1, len(variables)):
                    if isinstance(variables[x], evalwrap):
                        other = variables[x].obj
                    else:
                        other = variables[x]
                    if not isinstance(other, variables[0].obj):
                        return False
            elif isinstance(variables[0], classcalc):
                for x in xrange(1, len(variables)):
                    if not (isinstance(variables[x], instancecalc) and variables[x].isfrom(variables[0])):
                        return False
            else:
                check = e.typecalc(variables[0])
                for x in xrange(1, len(variables)):
                    if check != e.typecalc(variables[x]):
                        return False
            return True

    def iserrcall(self, variables):
        """Determines Whether Something Is An Error."""
        if not variables:
            return False
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], instancecalc) and variables[0].getmethod(e.errorvar):
                return True
            else:
                return False

    def classcall(self, variables):
        """Converts To A Class."""
        e.overflow = variables[1:]
        if not variables:
            return classcalc()
        elif isinstance(variables[0], instancecalc):
            return variables[0].toclass()
        elif isinstance(variables[0], classcalc):
            return variables[0]
        elif isinstance(variables[0], strcalc):
            original = str(variables[0])
            out = classcalc()
            for cmd in e.splitdedent(original, lambda x: x.splitlines()):
                out.process(cmd)
            return out
        elif isinstance(variables[0], dictionary):
            outvars = {}
            for k,v in variables[0].a.items():
                if isinstance(k, strcalc):
                    outvars[str(k)] = v
                else:
                    raise ExecutionError("ValueError", "Class dictionaries must have strings as their keys")
            return classcalc(outvars)
        else:
            raise ExecutionError("ClassError", "Cannot convert "+e.prepare(variables[0], False, True, True)+" to class")

    def instancecall(self, variables):
        """Converts To An Instance."""
        e.overflow = variables[1:]
        if not variables:
            return e.getcall(classcalc())([])
        elif isinstance(variables[0], instancecalc):
            return variables[0]
        elif isinstance(variables[0], classcalc):
            return variables[0].toinstance()
        elif isinstance(variables[0] (strcalc, dictionary)):
            return self.instancecall([self.classcall([variables[0]])])
        else:
            raise ExecutionError("ClassError", "Cannot convert "+e.prepare(variables[0], False, True, True)+" to instance")

    def namespacecall(self, variables):
        """Converts To A Namespace."""
        e.overflow = variables[1:]
        if not variables:
            return namespace()
        elif isinstance(variables[0], namespace):
            return variables[0]
        elif isinstance(variables[0], classcalc):
            return namespace(variables[0].getvars(True))
        elif isinstance(variables[0], (strcalc, dictionary)):
            return self.namespacecall([self.classcall([variables[0]])])
        else:
            raise ExecutionError("ClassError", "Cannot convert "+e.prepare(variables[0], False, True, True)+" to namespace")

    def getvalcall(self, variables):
        """Calculates A Variable Without Changing It."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to val")
        else:
            e.setreturned()
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                original = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            if original in e.variables:
                return e.funcfind(original)
            else:
                raise ExecutionError("KeyError", "Could not find "+original+" in variables")

    def getparenscall(self, variables):
        """Retreives The Number Of Parentheses."""
        e.setreturned()
        e.overflow = variables
        return float(len(e.parens))

    def getparenvarcall(self, variables):
        """Gets The Value Of A Paren."""
        e.setreturned()
        if not variables:
            variables = [-1]
        e.overflow = variables[1:]
        if not isint(variables[0]):
            raise ExecutionError("ValueError", "Only integers can be indexes")
        elif variables[0] < 0:
            variables[0] += len(e.parens)
        if 0 < variables[0] and variables[0] < len(e.parens):
            return codestr(e.prepare(e.getparen(variables[0]), False, True))
        else:
            raise ExecutionError("KeyError", "Could not find "+e.parenchar+str(variables[0])+e.parenchar+" in parens")

    def getvarcall(self, variables):
        """Gets The Value Of A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to var")
        else:
            e.setreturned()
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                original = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            if original in e.variables:
                return rawstrcalc(e.prepare(e.variables[original], False, True))
            else:
                raise ExecutionError("KeyError", "Could not find "+original+" in variables")

    def copycall(self, variables):
        """Makes Copies Of Items."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to copy")
        else:
            e.overflow = variables[1:]
            return getcopy(variables[0])

    def rowcall(self, variables):
        """Constructs A Matrix Row."""
        if not variables:
            return rowmatrixlist([])
        elif len(variables) == 1:
            if isinstance(variables[0], matrix):
                if variables[0].onlyrow():
                    return variables[0]
                elif variables[0].onlydiag():
                    return rowmatrixlist(variables[0].getitems())
                else:
                    return rowmatrixlist(variables[0].rows())
            elif hasmatrix(variables[0]):
                return self.rowcall([getmatrix(variables[0])])
            else:
                return matrix(1,1, variables[0])
        else:
            return rowmatrixlist(variables)

    def listcall(self, variables):
        """Constructs A Matrix List."""
        if not variables:
            return matrix(0)
        elif len(variables) == 1:
            if isinstance(variables[0], matrix):
                if variables[0].onlydiag():
                    return variables[0]
                elif variables[0].onlyrow():
                    return diagmatrixlist(variables[0].items())
                else:
                    return diagmatrixlist(variables[0].rows())
            elif hasmatrix(variables[0]):
                return self.listcall([getmatrix(variables[0])])
            else:
                return matrix(1,1, variables[0], fake=True)
        else:
            return diagmatrixlist(variables)

    def matrixcall(self, variables):
        """Constructs A Matrix."""
        if not variables:
            return rowmatrixlist([])
        elif len(variables) == 1:
            return getmatrix(variables[0])
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
            value = 1
            for v in variables:
                value *= v
            return value

    def dimcall(self, variables):
        """Returns The Dimensions Of The Matrix."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to dim")
        else:
            e.overflow = variables[1:]
            return diagmatrixlist(list(getmatrix(variables[0]).dimensions()))

    def anycall(self, variables):
        """Wraps any."""
        if not variables:
            return False
        elif len(variables) == 1 and ismatrix(variables[0]):
            return any(getmatrix(variables[0]).getitems())
        else:
            return any(variables)

    def allcall(self, variables):
        """Wraps all."""
        if not variables:
            return True
        elif len(variables) == 1 and ismatrix(variables[0]):
            return all(getmatrix(variables[0]).getitems())
        else:
            return all(variables)

    def sumcall(self, variables):
        """Finds A Sum."""
        if not variables:
            return 0
        else:
            value = variables[0]
            for x in xrange(1, len(variables)):
                if ismatrix(variables[x]):
                    value += self.sumcall(getmatrix(variables[x]).getitems())
                else:
                    value += variables[x]
            return value

    def prodcall(self, variables):
        """Finds A Product."""
        if not variables:
            return 1
        else:
            value = variables[0]
            for x in xrange(1, len(variables)):
                if ismatrix(variables[x]):
                    value *= self.prodcall(getmatrix(variables[x]).getitems())
                else:
                    value *= variables[x]
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
                out = variables[0].new(0, fake=False)
                for i in xrange(0, len(variables)):
                    for row in variables[i].a:
                        out.newrow(list(row))
                return out
            else:
                out = []
                for i in variables:
                    if ismatrix(i):
                        out += getmatrix(i).items()
                    else:
                        out.append(i)
                return rowmatrixlist(out)

    def findcall(self, variables):
        """Finds Equivalencies."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to find")
        else:
            variables[1] = getmatrix(variables[1])
            if variables[1].onlydiag():
                for x in xrange(0, variables[1].lendiag()):
                    if variables[1].retrieve(x) == variables[0]:
                        return x
            else:
                for x,y in variables[1].coords():
                    if variables[1].retrieve(x,y) == variables[0]:
                        return diagmatrixlist([x,y])
            return matrix(0)

    def mergecall(self, variables):
        """Merges Variables."""
        return diagmatrixlist(merge(variables))

    def sizecall(self, variables):
        """Finds A Size."""
        return totlen(diagmatrixlist(variables))

    def lencall(self, variables):
        """Finds A Length."""
        tot = 0
        for x in variables:
            if hasattr(x, "getlen"):
                tot += x.getlen()
            else:
                try:
                    test = len(x)
                except:
                    tot += 1
                else:
                    tot += test
        return tot

    def rangecall(self, variables):
        """Constructs A Range."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to range")
        elif len(variables) == 1:
            return rangematrix(0, variables[0])
        elif len(variables) == 2:
            return rangematrix(variables[0], variables[1])
        else:
            return rangematrix(variables[0], variables[1], variables[2])

    def roundcall(self, variables):
        """Performs round."""
        if not variables:
            return 0.0
        elif len(variables) == 1:
            return round(variables[0])
        else:
            return round(variables[0], variables[1])

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
            e.overflow = variables[2:]
            num = e.prepare(variables[1], False, False)
            return int(num, variables[0])

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
            e.overflow = variables[1:]
            return rawstrcalc(self.reprstrip(func(variables[0])))

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
                                temp += e.prepare(y, True, False)
                            new.append(rawstrcalc(temp))
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
                if isinstance(variables[x], dictionary):
                    for k,v in variables[x].a.items():
                        pairs[k] = v
                elif isinstance(variables[x], pair):
                    pairs[variables[x].k] = variables[x].v
                else:
                    raise ExecutionError("ValueError", "Can only replace pairs")
            if isinstance(variables[0], strcalc):
                out = self.replacecall([getmatrix(variables[0]), dictionary(pairs)])
                if isinstance(out, matrix) and out.onlydiag():
                    new = ""
                    for x in out.getitems():
                        new += e.prepare(x, True, False)
                    return rawstrcalc(new)
                else:
                    return out
            elif ismatrix(variables[0]):
                variables[0] = getmatrix(variables[0])
                if variables[0].onlydiag():
                    for x in xrange(0, variables[0].lendiag()):
                        temp = variables[0].retrieve(x)
                        if temp in pairs:
                            variables[0].store(x,x, pairs[temp])
                else:
                    for y,x in variables[0].coords():
                        temp = variables[0].retrieve(y,x)
                        if temp in pairs:
                            variables[0].store(y,x, pairs[temp])
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
                return rowmatrixlist(out)
        else:
            return self.sortcall([diagmatrixlist(variables)])

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
            return self.reversecall([diagmatrixlist(variables)])

    def containscall(self, variables):
        """Performs in."""
        if variables:
            if hasattr(variables[0], "__contains__"):
                for x in xrange(1, len(variables)):
                    if variables[x] in variables[0]:
                        return True
            else:
                for x in xrange(1, len(variables)):
                    if variables[x] == variables[0]:
                        return True
        return False

    def typecall(self, variables):
        """Finds Types."""
        if len(variables) == 0:
            return e.typecalc(matrix(0))
        elif len(variables) == 1:
            return e.typecalc(variables[0])
        else:
            out = []
            for x in variables:
                out.append(e.typecalc(x))
            return diagmatrixlist(out)

    def tocall(self, variables, varstrings="xyzwpqrabchjklmABFGHJKMOTUVWXY"):
        """Returns A Converter Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to to")
        elif len(variables) == 1:
            if isinstance(variables[0], (strcalc, funcfloat)):
                variables[0] = self.typestr(variables[0])
                if variables[0] in e.variables and isinstance(e.variables[variables[0]], funcfloat):
                    return e.variables[variables[0]]
                elif variables[0] in e.variables and (istext(variables[0]) or isnum(variables[0]) or isinstance(e.variables[variables[0]], bool) or (iseval(value) and not hascall(value))):
                    return strfloat(variables[0], [])
                else:
                    return strfunc(variables[0]+":"+varstrings[0], [varstrings[0]])
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
                return strfunc(out, args)
            else:
                raise ExecutionError("TypeError", "Unable to create a converter for "+repr(variables[0]))
        else:
            return self.tocall([diagmatrixlist(variables)])

    def typestr(self, item):
        """Processes A Type Identifier."""
        item = e.prepare(item, False, False)
        if item in self.typefuncs:
            return self.typefuncs[item]
        else:
            return "("+item+")"

    def codecall(self, variables):
        """Converts To Code."""
        if not variables:
            return codestr("")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                return codestr(str(variables[0]))
            else:
                return codestr(e.prepare(variables[0], False, True))

    def strcall(self, variables):
        """Finds A String."""
        out = []
        for x in variables:
            out.append(e.prepare(x, True, False))
        return rawstrcalc("".join(out))

    def reprcall(self, variables):
        """Finds A Representation."""
        if len(variables) != 1:
            variables = [diagmatrixlist(variables)]
        return rawstrcalc(e.prepare(variables[0], True, True))

    def joincall(self, variables):
        """Joins Variables By A Delimiter."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to join")
        else:
            delim = variables[0]
            if isinstance(delim, strcalc):
                tostring = True
            else:
                tostring = False
            out = []
            for x in xrange(1, len(variables)):
                item = variables[x]
                if ismatrix(item):
                    item = self.joincall([delim]+getmatrix(item).getitems())
                if not isinstance(item, strcalc):
                    tostring = False
                out += [item, delim]
            out.pop()
            if tostring:
                return rawstrcalc("".join(map(str, out)))
            elif len(out) == 1:
                return out[0]
            else:
                return diagmatrixlist(out)

    def abscall(self, variables):
        """Performs abs."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to abs")
        else:
            e.overflow = variables[1:]
            return abs(variables[0])

    def datacall(self, variables):
        """Performs data."""
        if not variables:
            return data()
        elif len(variables) == 1:
            if isinstance(variables[0], data):
                return variables[0]
            else:
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

    def docalc(self, variables, info=" | calc"):
        """Performs calc."""
        out = []
        for x in variables:
            if isinstance(x, codestr):
                out.append(e.calc(str(x), info, -2))
            elif isinstance(x, strcalc):
                out.append(e.calc(str(x), info, -1))
            else:
                raise ExecutionError("ValueError", "Can't calc non-string values")
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def nonecalc(self, variables):
        """Performs calc And Returns null."""
        for x in variables:
            if isinstance(x, codestr):
                e.process(str(x), " | do", top=-2)
            elif isinstance(x, strcalc):
                e.process(str(x), " | do", top=-1)
            else:
                raise ExecutionError("ValueError", "Can't calc non-string values")
        return matrix(0)

    def cmdcall(self, variables):
        """Performs exec."""
        e.setreturned()
        for item in variables:
            if isinstance(item, strcalc):
                e.processor.evaltext(str(item), False)
            else:
                raise ExecutionError("ValueError", "Can't exec non-string values")
        return matrix(0)

    def foldcall(self, variables):
        """Folds A Function Over A Matrix."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to fold")
        else:
            e.overflow = variables[2:]
            func = e.getcall(variables[0])
            items = getmatrix(variables[1]).getitems()
            if not items:
                return matrix(0)
            elif len(items) == 1:
                return func(items)
            else:
                acc = items[0]
                for x in xrange(1, len(items)):
                    acc = func([acc, items[x]])
                return acc

    def mapcall(self, variables):
        """Maps A Function Over A Matrix."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to map")
        else:
            e.overflow = variables[2:]
            func = e.getcall(variables[0])
            cont = getmatrix(variables[1])
            cont.code(lambda x: func([x]))
            return cont

    def filtercall(self, variables):
        """Filters A Function Over A Matrix."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to filter")
        else:
            e.overflow = variables[2:]
            func = e.getcall(variables[0])
            cont = getmatrix(variables[1])
            out = []
            for item in cont.getitems():
                if func([item]):
                    out.append(item)
            if cont.onlydiag():
                return diagmatrixlist(out)
            else:
                return rowmatrixlist(out)

    def forcall(self, variables):
        """Calls A Function Over A Matrix."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to for")
        else:
            e.overflow = variables[2:]
            func = e.getcall(variables[1])
            for item in getmatrix(variables[0]).getitems():
                func(item)
            return matrix(0)

    def whilecall(self, variables):
        """Calls A Function While True."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to while")
        else:
            e.overflow = variables[1:]
            func = e.getcall(variables[0])
            while func([]):
                pass
            return matrix(0)

    def zipcall(self, variables):
        """Zips Matrices."""
        if not variables:
            return matrix(0)
        else:
            conts = []
            for item in variables:
                conts.append(getmatrix(item).getitems())
            out = []
            while True:
                do = True
                new = []
                for cont in conts:
                    if cont:
                        new.append(cont.pop(0))
                    else:
                        do = False
                        break
                if do:
                    out.append(new)
                else:
                    break
            return matrixlist(out)

    def zipwithcall(self, variables):
        """Zips Matrices With A Function."""
        if not variables:
            return matrix(0)
        else:
            func = e.getcall(variables[0])
            conts = []
            for x in xrange(1, len(variables)):
                conts.append(getmatrix(variables[x]).getitems())
            out = []
            while True:
                do = True
                new = []
                for cont in conts:
                    if cont:
                        new.append(cont.pop(0))
                    else:
                        do = False
                        break
                if do:
                    out.append(func(new))
                else:
                    break
            return diagmatrixlist(out)

    def derivcall(self, variables):
        """Returns The nth Derivative Of A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to D")
        else:
            n = 1
            varname = e.varname
            accuracy = 0.0001
            scaledown = 1.25
            func = variables[0]
            if len(variables) > 1:
                n = int(variables[1])
            if len(variables) > 2:
                if isinstance(variables[2], strcalc):
                    varname = str(variables[2])
                else:
                    raise ExecutionError("ValueError", "Variable names must be strings")
            if len(variables) > 3:
                accuracy = float(variables[3])
            if len(variables) > 4:
                scaledown = float(variables[4])
                e.overflow = variables[5:]
            if isinstance(func, strfunc):
                if len(func.variables):
                    varname = func.variables.pop(0)
                return derivfunc(func.funcstr,
                                 personals=func.personals,
                                 name=func.name,
                                 overflow=func.overflow,
                                 allargs=func.allargs,
                                 reqargs=func.reqargs,
                                 memoize=func.memoize,
                                 memo=func.memo,
                                 method=func.method,
                                 variables=func.variables,
                                 n=n,
                                 accuracy=accuracy,
                                 scaledown=scaledown,
                                 varname=varname)
            elif isinstance(func, funcfloat):
                return derivfuncfloat(func, n, accuracy, scaledown)
            else:
                return derivfunc(e.prepare(func, False, True), n=n, accuracy=accuracy, scaledown=scaledown, varname=varname)

    def integcall(self, variables):
        """Returns The Integral Of A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to S")
        else:
            varname = e.varname
            accuracy = 0.0001
            func = variables[0]
            if len(variables) > 1:
                if isinstance(variables[1], strcalc):
                    varname = str(variables[1])
                else:
                    raise ExecutionError("ValueError", "Variable names must be strings")
            if len(variables) > 2:
                accuracy = float(variables[2])
                e.overflow = variables[3:]
            if isinstance(func, strfunc):
                if len(func.variables):
                    varname = func.variables.pop(0)
                return integfunc(func.funcstr,
                                 personals=func.personals,
                                 name=func.name,
                                 overflow=func.overflow,
                                 allargs=func.allargs,
                                 reqargs=func.reqargs,
                                 memoize=func.memoize,
                                 memo=func.memo,
                                 method=func.method,
                                 variables=func.variables,
                                 accuracy=accuracy,
                                 varname=varname)
            elif isinstance(func, funcfloat):
                return integfuncfloat(func, accuracy)
            else:
                return integfunc(e.prepare(func, False, True), accuracy=accuracy, varname=varname)

    def randcall(self, variables):
        """Returns A Random Number Generator Object."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to die")
        else:
            e.setreturned()
            key = None
            if len(variables) > 1:
                key = e.prepare(variables[1], True, False)
                e.overflow = variables[2:]
            return rollfunc(variables[0], key)

    def writecall(self, variables):
        """Writes To A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to write")
        else:
            e.setreturned()
            e.overflow = variables[2:]
            if isinstance(variables[0], strcalc):
                name = str(variables[0])
            else:
                raise ExecutionError("ValueError", "File names must be strings")
            if len(variables) == 1:
                writer = ""
            else:
                writer = e.prepare(variables[1], False, False)
            with openfile(name, "wb") as f:
                writefile(f, writer)
            return matrix(0)

    def readcall(self, variables):
        """Reads From A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to read")
        else:
            e.setreturned()
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                name = str(variables[0])
            else:
                raise ExecutionError("ValueError", "File names must be strings")
            with openfile(name) as f:
                return rawstrcalc(readfile(f))

    def purecall(self, variables):
        """Ensures Purity."""
        pure, e.pure = e.pure, 2
        try:
            out = self.docalc(variables)
        finally:
            e.pure = pure
        return out

    def defcall(self, variables):
        """Defines A Variable."""
        redef, e.redef = e.redef, True
        try:
            out = self.docalc(variables)
        finally:
            e.redef = redef
        return out

    def globalcall(self, variables):
        """Defines A Global Variable."""
        e.useclass = (e.useclass,)
        try:
            out = self.docalc(variables)
        finally:
            e.useclass = e.useclass[0]
        return out

    def aliascall(self, variables):
        """Makes Aliases."""
        e.overflow = variables[2:]
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to alias")
        elif len(variables) == 1:
            e.setreturned()
            if isinstance(variables[0], strcalc):
                key = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Aliases must be strings")
            if key in e.aliases:
                out = rawstrcalc(e.aliases[key])
                del e.aliases[key]
            else:
                out = matrix(0)
            return out
        else:
            e.setreturned()
            if isinstance(variables[0], strcalc):
                key = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Aliases must be strings")
            if isinstance(variables[1], strcalc):
                value = str(variables[1])
            else:
                raise ExecutionError("ValueError", "Aliases must be strings")
            e.aliases[key] = value
            return diagmatrixlist([rawstrcalc(key), rawstrcalc(value)])

    def aliasescall(self, variables):
        """Gets Aliases."""
        e.overflow = variables
        return e.frompython(e.aliases)

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

    def divmodcall(self, variables):
        """Wraps divmod."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to lshift")
        else:
            e.overflow = variables[2:]
            q,r = divmod(variables[0], variables[1])
            return diagmatrixlist([q,r])

    def callcall(self, variables):
        """Calls A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to call")
        elif hascall(variables[0]):
            return e.getcall(variables[0])(variables[1:])
        else:
            raise ExecutionError("ArgumentError", "Uncallable object "+e.prepare(variables[0], False, True, True))

    def itemcallcall(self, variables):
        """Item Calls A Function."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to retrieve")
        elif hasitemcall(variables[0]):
            return variables[0].itemcall(variables[1:])
        else:
            raise ExecutionError("ArgumentError", "Un-item-callable object "+e.prepare(variables[0], False, True, True))

    def paircall(self, variables):
        """Creates A Pair."""
        if not variables:
            return pair(matrix(0), matrix(0))
        elif len(variables) > 1:
            e.overflow = variables[2:]
            return pair(variables[0], variables[1])
        elif isinstance(variables[0], dictionary):
            if not variables[0].a:
                return pair(matrix(0), matrix(0))
            elif len(variables[0].a) == 1:
                k = variables[0].keys()[0]
                return pair(key, variables[0].a[key])
            else:
                raise ExecutionError("ValueError", "Only dictionaries of length <= 1 can be converted to pairs")
        elif isinstance(variables[0], pair):
            return variables[0]
        else:
            return pair(variables[0], matrix(0))

    def dictcall(self, variables):
        """Creates A Dictionary."""
        if not variables:
            return dictionary()
        elif len(variables) == 1:
            if isinstance(variables[0], dictionary):
                return variables[0]
            elif isinstance(variables[0], pair):
                return dictionary({variables[0].k:variables[0].v})
            elif isinstance(variables[0], classcalc):
                return e.frompython(variables[0].getvars())
            else:
                raise TypeError("Received non-dictionary object "+e.prepare(variables[0], False, True, True))
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
            raise ExecutionError("ArgumentError", "Not enough arguments to intersect")
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
        else:
            e.setreturned()
            for arg in variables:
                if isinstance(arg, strcalc):
                    original = str(arg)
                else:
                    raise ExecutionError("ValueError", "Can't run non-string valueS")
                if not e.processor.evalfile(original, False):
                    raise ExecutionError("IOError", "Failed to execute file "+str(original))
                else:
                    e.processor.dumpdebug(True)
            return matrix(0)

    def requirecall(self, variables):
        """Performs require."""
        e.setreturned()
        old_e = e
        try:
            new_e = old_e.new()
            new_e.processor.e = new_e
            new_e.processor.fresh(None)
            out = classcalc()
            params = out.begin()
            new_e.funcs.runcall(variables)
            out.end(params)
        finally:
            set_e(old_e)
            old_e.processor.e = old_e
        return out

    def evalcall(self, variables):
        """Performs eval."""
        out = []
        old_e = e
        try:
            new_e = old_e.new()
            new_e.processor.e = new_e
            new_e.processor.fresh(None)
            for x in variables:
                if isinstance(x, codestr):
                    item = new_e.calc(str(x), " | eval", -2)
                elif isinstance(x, strcalc):
                    item = new_e.calc(str(x), " | eval", -1)
                else:
                    raise ExecutionError("ValueError", "Can't eval non-string values")
                out.append(item)
        finally:
            set_e(old_e)
            old_e.processor.e = old_e
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def assertcall(self, variables):
        """Checks For Errors By Asserting That Something Is True."""
        out = []
        for x in variables:
            if isinstance(x, codestr):
                test = e.calc(str(x), " | assertion", -2)
            elif isinstance(x, strcalc):
                test = e.calc(str(x), " | assertion", -1)
            else:
                raise ExecutionError("ValueError", "Can't calc non-string values")
            if test:
                out.append(test)
            else:
                raise ExecutionError("AssertionError", "Assertion failed that "+str(x)+" (Result = "+e.prepare(test, False, True, True)+")")
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def importcall(self, variables):
        """Performs import."""
        if not variables:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        else:
            e.setreturned()
            out = []
            for item in variables:
                if isinstance(variables[0], strcalc):
                    name = str(variables[0])
                else:
                    raise ExecutionError("ValueError", "Module names must be strings")
                impbaseclass = doimport(name)
                funcname = "import:`"+name+"`"
                if hasattr(impbaseclass, "__rabbit__"):
                    impclass = impbaseclass.__rabbit__(e)
                    if impclass is None:
                        value = matrix(0)
                    elif iseval(impclass):
                        value = impclass
                    elif "`" in name:
                        raise ExecutionError("ValueError", "Cannot install files with a backtick in them")
                    elif hascall(impclass):
                        value = funcfloat(e.getcall(impclass), funcstr=funcname)
                    elif hasattr(impclass, "precall"):
                        value = usefunc(impclass.precall, funcstr=funcname)
                    elif hasattr(impclass, "unicall"):
                        value = unifunc(impclass.unicall, funcstr=funcname)
                    else:
                        value = evalwrap(impclass, funcname)
                elif "`" in name:
                    raise ExecutionError("ValueError", "Cannot import files with a backtick in them")
                else:
                    value = evalwrap(impbaseclass, funcname)
                out.append(value)
            if len(out) == 1:
                return out[0]
            else:
                return diagmatrixlist(out)

    def insidecall(self, variables):
        """Performs inside."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to inside")
        else:
            inside = variables[0]
            args = []
            if len(variables) > 1:
                args = variables[2:]
                if hasattr(variables[1], "inside_exit"):
                    outside = variables[1].inside_exit
                else:
                    outside = e.getcall(variables[1])
            elif hasattr(inside, "inside_exit"):
                outside = inside.inside_exit
            else:
                outside = None
            if hasattr(inside, "inside_enter"):
                inside = inside.inside_enter
            else:
                inside = e.getcall(inside)
            def _outside(variables):
                arg = inside(args)
                out = None
                try:
                    out = self.docalc(variables)
                finally:
                    if outside is not None:
                        if out is None:
                            return outside([arg])
                        else:
                            return outside([arg, out])
                    elif not isnull(arg):
                        if out is None:
                            return e.getcall(arg)([])
                        else:
                            return e.getcall(arg)([out])
                    else:
                        return out
            return funcfloat(_outside, "inside:("+strlist(variables, "):(", lambda x: e.prepare(x, False, True))+")", reqargs=1)

    def unusedcall(self, variables):
        """Gets Unused Variables."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to unused")
        else:
            e.setreturned()
            e.overflow = variables[1:]
            if isinstance(variables[0], classcalc):
                out = {}
                for k,v in variables[0].getvars(True).items():
                    if istext(v):
                        out[k] = v
                return classcalc(out)
            else:
                raise TypeError("Only classes can have their variables analyzed")

    def wrapcall(self, variables):
        """Wraps An Object."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to wrap")
        else:
            e.setreturned()
            ref = "Meta.wrap:("+e.prepare(variables[0], False, True)+")"
            if len(variables) > 1:
                ref += ":("+e.prepare(variables[1], False, True)+")"
                safe = []
                for item in getmatrix(variables[1]).getitems():
                    if isinstance(item, strcalc):
                        out.append(str(item))
                    else:
                        raise ExecutionError("ValueError", "Method names must be strings")
                e.overflow = variables[2:]
            else:
                safe = None
            if not isinstance(variables[0], evalwrap):
                return evalwrap(variables[0], ref, safe)
            elif safe is None:
                return variables[0]
            else:
                e.setreturned()
                return evalwrap(variables[0].obj, ref, safe)

    def purifycall(self, variables):
        """Purifies A Wrapper Method."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to purify")
        else:
            e.setreturned()
            e.overflow = variables[2:]
            if isinstance(variables[1], strcalc):
                names = [str(variables[1])]
            elif isinstance(variables[1], matrix):
                names = []
                for item in variables[1].getitems():
                    if isinstance(item, strcalc):
                        names.append(str(item))
                    else:
                        raise ExecutionError("ValueError", "Variable names must be strings")
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            if isinstance(variables[0], evalwrap):
                for name in names:
                    if name in variables[0].safe:
                        raise ExecutionError("ValueError", "The variable "+name+" is already pure")
                    else:
                        variables[0].safe.append(name)
                return variables[0]
            else:
                raise ExecutionError("ValueError", "Can only purify wraps")

    def functioncall(self, variables):
        """Converts To A Function."""
        if not variables:
            return strfunc("")
        elif not isinstance(variables[0], strcalc):
            e.overflow = variables[1:]
            if isfunc(variables[0]):
                return variables[0]
            else:
                raise ExecutionError("ValueError", "Could not convert to function "+e.prepare(variables[0], False, True))
        elif len(variables) == 1:
            return strfloat(str(variables[0]))
        elif isinstance(variables[1], strcalc):
            e.overflow = variables[2:]
            return e.eval_set(str(variables[0]), str(variables[1]))
        else:
            raise ExecutionError("ValueError", "Variable lists must be strings")

    def memoizecall(self, variables):
        """Memoizes Functions."""
        out = self.functioncall(variables)
        out.memoize = True
        return out

    def getstatecall(self, variables):
        """Gets A State."""
        if not variables:
            item = matrix(0)
        elif len(variables) == 1:
            item = variables[0]
        else:
            item = diagmatrixlist(variables)
        return e.frompython(itemstate(item))

    def fromstatecall(self, variables):
        """Converts From A State."""
        if not variables:
            item = matrix(0)
        elif len(variables) == 1:
            item = variables[0]
        else:
            item = diagmatrixlist(variables)
        return e.deitem(e.topython(item))

    def pipecall(self, variables):
        """Wraps A Python Global."""
        e.setreturned()
        if not variables:
            return e.frompython(globals(), "wrap()")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                key = str(variables[0])
                search = globals()
                if key in search:
                    def _ref():
                        return "wrap:`"+key+"`"
                    return e.frompython(search[key], _ref)
                else:
                    raise ExecutionError("AttributError", "Python has no variable "+key)
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")

    def pythonevalcall(self, variables):
        """Wraps Python eval."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to python")
        else:
            out = []
            for item in variables:
                if isinstance(item, strcalc):
                    inputstring = basicformat(item)
                else:
                    raise ExecutionError("ValueError", "Can only eval strings")
                out.append(e.frompython(compute(inputstring, builtins=True)))
            if len(out) == 1:
                return out[0]
            else:
                return diagmatrixlist(out)

    def getcallcall(self, variables):
        """Wraps getcall."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to caller")
        else:
            e.overflow = variables[1:]
            return funcfloat(e.getcall(variables[0]), funcstr="Meta.caller:("+e.prepare(variables[0], False, True)+")")

    def getitemcallcall(self, variables):
        """Wraps getcall."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to retriever")
        else:
            e.overflow = variables[1:]
            return funcfloat(e.getitemcall(variables[0]), funcstr="Meta.retriever:("+e.prepare(variables[0], False, True)+")")

    def inputcall(self, variables):
        """Wraps raw_input."""
        if variables:
            e.setreturned()
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                return rawstrcalc(raw_input(str(variables[0])))
            else:
                raise ExecutionError("ValueError", "Prompts must be strings")
        else:
            return rawstrcalc(raw_input())

    def getattrcall(self, variables):
        """Gets An Attribute."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to get")
        else:
            e.overflow = variables[2:]
            if isinstance(variables[1], strcalc):
                name = str(variables[1])
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            return e.getmethod(variables[0], name)

    def hasattrcall(self, variables):
        """Checks An Attribute."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to has")
        else:
            e.overflow = variables[2:]
            if isinstance(variables[1], strcalc):
                name = str(variables[1])
            else:
                raise ExecutionError("ValueError", "Variable names must be strings")
            return e.getmethod(variables[0], name, True)

    def opencall(self, variables):
        """Opens A File."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to open")
        else:
            e.setreturned()
            if isinstance(variables[0], strcalc):
                name = str(variables[0])
            else:
                raise ExecutionError("ValueError", "File names must be strings")
            ref = "open:`name`"
            if len(variables) > 1:
                e.overflow = variables[2:]
                if isinstance(variables[1], strcalc):
                    opentype = str(variables[1])
                else:
                    raise ExecutionError("ValueError", "Open types must be strings")
                ref += ":`"+opentype+"`"
                return evalwrap(openfile(name, opentype), ref)
            else:
                return evalwrap(openfile(name), ref)

    def chrcall(self, variables):
        """Wraps unichr."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to chr")
        else:
            e.overflow = variables[1:]
            return rawstrcalc(chr(variables[0]))

    def ordcall(self, variables):
        """Wraps ord."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to ord")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                inputstring = str(variables[0])
            else:
                raise ExecutionError("ValueError", "Only strings can be characters")
            return ord(inputstring)

    def supercall(self, variables):
        """Wraps type."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to super")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], evalwrap):
                return evalwrap(type(variables[0].obj), "Meta.super:("+variables[0].ref+")")
            else:
                raise ExecutionError("ValueError", "Can only get the super of a wrap")

    def conscall(self, variables):
        """Performs cons."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to prepend")
        else:
            e.overflow = variables[2:]
            cont = getmatrix(variables[1])
            if cont.onlydiag():
                return diagmatrixlist([variables[0]]+cont.getdiag())
            else:
                return rowmatrixlist([variables[0]]+cont.items())

    def appendcall(self, variables):
        """Performs append."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to prepend")
        else:
            e.overflow = variables[2:]
            cont = getmatrix(variables[1])
            if cont.onlydiag():
                return diagmatrixlist(cont.getdiag()+[variables[0]])
            else:
                return rowmatrixlist(cont.items()+[variables[0]])

    def asciicall(self, variables):
        """Wraps ascii."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to ascii")
        else:
            e.overflow = variables[1:]
            if isinstance(variables[0], strcalc):
                return rawstrcalc(variables[0].getascii())
            else:
                raise ExecutionError("ValueError", "Can only use ascii on strings")
