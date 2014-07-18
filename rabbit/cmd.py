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

from __future__ import with_statement, absolute_import, print_function, unicode_literals

from .carrot.app import *
from .eval import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class mathbase(safebase):
    """A Base Class For PythonPlus Evaluators."""
    multiargops = "=:*+-%/^@~\\|&;<>.,([{$!?\u2260\u2264\u2265"
    statements = ["debug", "run", "assert", "do", "show", "del", "def", "make"]
    messages = []
    commands = []
    ans = [matrix(0)]
    returned = 1
    useclass = None
    redef = False
    doshow = True
    top = False
    errorlog = False

    def __init__(self, name="Evaluator", message="Enter A Rabbit Command:", height=None, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.debug = bool(debug)
        if message:
            message = str(message)
            self.messages.append(message)
        if height is None:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name), int(height))
        self.show = self.appshow
        self.populator()
        self.printdebug(": ON")
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def setdebug(self, state):
        """Sets The Debugging State."""
        state = bool(state)
        self.e.debug = True
        if state:
            self.printdebug(": ON")
        else:
            self.printdebug(": OFF")
        self.debug = state
        self.e.debug = self.debug

    def printdebug(self, message):
        """Prints Debug Output."""
        self.e.printdebug(message)

    def adderror(self, error, detail, variables=None):
        """Adds An Error To The Log."""
        self.printdebug("<!> "+str(error)+": "+str(detail))
        if variables is not None:
            self.e.recursion += 1
            for k,v in variables.items():
                self.printdebug(str(k)+" = "+str(v))
            self.e.recursion -= 1
        self.dumpdebug()

    def dumpdebug(self, top=False):
        """Dumps Debug Output."""
        if not top:
            self.show(strlist(self.e.debuglog, "\n"), True)
            self.errorlog = True
        self.e.debuglog = []

    def appshow(self, arg, message=False):
        """Displays Something."""
        arg = self.e.forshow(arg)
        if message:
            self.app.display(arg)
            for line in arg.split("\n"):
                self.messages.append(line)
        else:
            self.app.display(arg)

    def popshow(self, arg, message=None):
        """Displays Something In A Popup."""
        popup("Info", self.e.forshow(arg), "Output")

    def calc(self, expression):
        """Evaluates An Expression."""
        if self.debug:
            self.e.info = 1
        else:
            self.e.info = " <<| Traceback"
        return self.e.calc(expression)

    def test(self, expression):
        """Tests An Expression."""
        return self.e.test(expression)

    def printcall(self, variables, func=None):
        """Performs print."""
        self.returned = 1
        if variables is None or len(variables) == 0:
            out = self.e.prepare(matrix(0), True, False)
        else:
            out = []
            for x in variables:
                out.append(self.e.prepare(x, True, False))
            out = " ".join(out)
        if func is None:
            self.show(out)
        else:
            func(out)
        return rawstrcalc(out, self.e)

    def showcall(self, variables):
        """Performs show."""
        return self.printcall(variables, func=lambda x: popup("Info", x, "Output"))

    def anscall(self, variables):
        """Performs ans."""
        if variables is None or len(variables) == 0:
            return self.ans[-1]
        else:
            self.e.overflow = variables[1:]
            return self.ans[getint(variables[0])]

    def grabcall(self, variables):
        """Performs grab."""
        if variables is None or len(variables) == 0:
            out = self.app.get().split("\n")[-1]
            if out in self.messages:
                return rawstrcalc(out, self.e)
            else:
                return strfloat(out, self.e)
        else:
            self.e.overflow = variables[1:]
            out = self.app.getlines()[getint(variables[0])]
            if out in self.messages:
                return rawstrcalc(out, self.e)
            else:
                return strfloat(out, self.e)

    def installcall(self, variables):
        """Performs x = import."""
        if variables is None or len(variables) == 0:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        elif len(variables) == 1:
            inputstring = self.e.prepare(variables[0], False, False)
            name = delspace(delspace(inputstring), self.e.reserved)
            try:
                impclass = dirimport(inputstring).interface
            except IOError:
                raise ExecutionError("IOError", "Could not find for install file "+inputstring)
            else:
                if iseval(impclass):
                    return impclass(self)
                elif hascall(impclass):
                    return funcfloat(impclass(self).call, self.e, name)
                else:
                    try:
                        impclass.precall
                    except AttributeError:
                        try:
                            impclass.unicall
                        except AttributeError:
                            return impclass(self)
                        else:
                            return unifunc(impclass(self).unicall, self.e, name)
                    else:
                        return usefunc(impclass(self).precall, self.e, name)
        else:
            out = []
            for x in variables:
                out.append(self.installcall([x]))
            return diagmatrixlist(out)

    def savecall(self, variables):
        """Performs save."""
        if variables is None or len(variables) == 0:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], False, False)
            try:
                writefile(getfile(original, "wb"), strlist(self.commands, "\n"))
            except IOError:
                raise ExecutionError("IOError", "Could not find for save file "+original)
        else:
            for x in variables:
                self.savecall([x])
        return matrix(0)

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_help,
            self.cmd_debug,
            self.cmd_clear,
            self.cmd_run,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_del,
            self.cmd_make,
            self.cmd_def,
            self.cmd_set,
            self.cmd_normal
            ]
        self.set_cmds = [
            self.set_def,
            self.set_normal
            ]
        self.e = evaluator(processor=self)
        self.fresh(True)
        self.genhelp()

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "save":funcfloat(self.savecall, self.e, "save"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab")
            })

    def genhelp(self):
        """Generates The helpstring."""
        self.helpstring = "Commands:"
        for cmd in self.cmds:
            self.helpstring += "\n    "+namestr(cmd).split("_")[-1]

    def initialize(self, args=()):
        """Runs Any Files Fed To The Constructor."""
        if istext(args):
            self.evalfile(args)
        else:
            for x in args:
                self.initialize(x)

    def reset(self):
        """Resets Top Variables."""
        self.dumpdebug(True)
        self.e.recursion = 0

    def handler(self, event=None):
        """Handles A Return Event."""
        self.reset()
        original = self.box.output()
        cmd = carefulsplit(original, "#", '"`', {"\u201c":"\u201d"})[0]
        if delspace(cmd) == "":
            if len(self.box.commands) > 1:
                self.process(self.box.commands[-2], True)
        else:
            self.box.add(original)
            self.process(cmd, True)

    def evalfile(self, name):
        """Runs A File."""
        try:
            tempfile = openfile(name, "rb")
        except IOError:
            return False
        else:
            self.evaltext(readfile(tempfile))
            tempfile.close()
            return True

    def evaltext(self, inputstring):
        """Runs Text."""
        cmdlist = inputstring.splitlines()
        x = 0
        while x < len(cmdlist):
            self.reset()
            cmdlist[x] = carefulsplit(cmdlist[x], "#", '"`', {"\u201c":"\u201d"})[0]
            while x < len(cmdlist)-1 and (delspace(cmdlist[x+1]) == "" or iswhite(cmdlist[x+1][0])):
                cmdlist[x] += "\n"+carefulsplit(cmdlist.pop(x+1), "#", '"`', {"\u201c":"\u201d"})[0]
            self.process(cmdlist[x], True)
            x += 1

    def process(self, inputstring, top=False):
        """Processes A Command."""
        inputstring = basicformat(inputstring)
        self.returned = 1
        if inputstring != "":
            if top:
                self.saferun(self.doproc, inputstring)
            else:
                self.doproc(inputstring)

    def doproc(self, inputstring):
        """Does The Processing."""
        inputstring = str(inputstring)
        for func in self.pre_cmds:
            if func(inputstring) is not None:
                return True

    def pre_cmd(self, inputstring):
        """Evaluates Commands."""
        for original in carefulsplit(inputstring, ";;", '"`', {"\u201c":"\u201d"}, {"{":"}"}):
            if delspace(original) != "":
                original = basicformat(original)
                for func in self.cmds:
                    if func(original) is not None:
                        name = namestr(func).split("_")[-1]
                        if name != "run":
                            self.commands.append(original)
                        self.printdebug("|: "+name)
                        break
        return True

    def cmd_help(self, inputstring):
        """Performs help."""
        if superformat(inputstring).startswith("help"):
            inputstring = inputstring[4:]
            if inputstring == "":
                self.show(self.helpstring, True)
            elif inputstring[0] == " ":
                self.show(self.findhelp(basicformat(inputstring)), True)
            else:
                return None
            return True

    def cmd_debug(self, original):
        """Controls Debugging."""
        if superformat(original).startswith("debug"):
            original = basicformat(original[5:])
            if original == "":
                self.setdebug(not self.debug)
            elif original[0] == " ":
                if formatisyes(original):
                    self.setdebug(True)
                elif formatisno(original):
                    self.setdebug(False)
                else:
                    raise ExecutionError("StatementError", "Unrecognized debug state of "+original)
            else:
                return None
            return True

    def cmd_clear(self, original):
        """Performs clear."""
        if superformat(original) == "clear":
            self.app.clear()
            return True

    def cmd_run(self, original):
        """Performs run."""
        if superformat(original).startswith("run "):
            original = basicformat(original[4:])
            if not self.evalfile(original):
                raise ExecutionError("IOError", "Could not find file "+str(original))
            else:
                return True

    def cmd_assert(self, original):
        """Checks For Errors By Asserting That Something Is True."""
        if superformat(original).startswith("assert "):
            original = basicformat(original[7:])
            if not self.e.test(original):
                raise AssertionError("Assertion failed that "+original)
            return True

    def cmd_do(self, original):
        """Evaluates Functions Silently."""
        if superformat(original).startswith("do "):
            test = self.calc(original[3:])
            if test is not None and not isnull(test):
                self.ans.append(test)
            return True

    def cmd_del(self, original):
        """Deletes A Variable."""
        if superformat(original).startswith("del "):
            original = basicformat(original[4:])
            if original in self.e.variables:
                del self.e.variables[original]
            elif "." in original:
                test = original.split(".")
                item = test.pop()
                useclass = self.e.find(test[0], True, False)
                if isinstance(useclass, classcalc):
                    last = useclass
                    for x in xrange(1, len(test)):
                        useclass = useclass.retrieve(test[x])
                        if not isinstance(useclass, classcalc):
                            raise ExecutionError("ClassError", "Could not delete "+test[x]+" in "+self.e.prepare(last, False, True, True))
                else:
                    raise ExecutionError("VariableError", "Could not find class "+test[0])
                useclass.remove(item)
            else:
                raise ExecutionError("VariableError", "Could not find "+original)
            self.printdebug("< "+original+" >")
            return True

    def cmd_make(self, original):
        """Sets A Variable."""
        if superformat(original).startswith("make "):
            test = self.cmd_set(original[5:])
            if test:
                return test
            else:
                raise ExecutionError("DefinitionError", "No definition was done in the statement "+original)

    def cmd_def(self, original):
        """Defines A Variable."""
        if superformat(original).startswith("def "):
            self.redef = True
            test = self.cmd_set(original[4:])
            self.redef = False
            if test:
                return test
            else:
                raise ExecutionError("DefinitionError", "No definition was done in the statement "+original)

    def cmd_set(self, original):
        """Evaluates Definition Commands."""
        if "=" in original:
            sides = original.split("=", 1)
            sides[0] = basicformat(sides[0])
            sides[1] = basicformat(sides[1])
            docalc = False
            if sides[0].endswith(":"):
                sides[0] = sides[0][:-1]
                docalc = True
            sides[0] = carefulsplit(sides[0], ",", '"`', {"\u201c":"\u201d"}, {"(":")", "{":"}", "[":"]"})
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
                        if not self.cmd_set_do([sides[0][x], self.e.wrap(toset)], docalc):
                            raise ExecutionError("VariableError", "Could not multi-set to invalid variable "+sides[0][x])
                    return True
            else:
                sides[0] = sides[0][0]
                return self.cmd_set_do(sides, docalc)
                
    def cmd_set_do(self, sides, docalc):
        """Performs The Definition Command."""
        sides[0] = sides[0].split("(", 1)
        if len(sides[0]) > 1:
            sides[0] = delspace(sides[0][0])+"("+sides[0][1]
        else:
            sides[0] = delspace(sides[0][0])
        if self.readytofunc(sides[0], allowed="."):
            useclass = None
            if self.useclass:
                classlist = [self.useclass]
            else:
                classlist = []
            if "." in sides[0]:
                classlist += sides[0].split(".")
                for x in xrange(0, len(classlist)-1):
                    if self.e.isreserved(classlist[x]):
                        return False
                sides[0] = classlist.pop()
                useclass = self.e.find(classlist[0], True, False)
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
                                raise ExecutionError("ClassError", "Could not set "+classlist[x]+" in "+self.e.prepare(last, False, True, True))
                elif classlist[0] in self.e.variables and istext(self.e.variables[classlist[0]]) and len(classlist) == 1:
                    sides[1] = "( "+self.e.variables[classlist[0]]+" )"+" + { "+sides[0]+" :"*docalc+" "*(not docalc)+"= "+sides[1]+" }"
                    sides[0] = classlist[0]
                    useclass = None
                    classlist = []
                    docalc = False
                else:
                    raise ExecutionError("VariableError", "Could not find class "+self.e.prepare(classlist[0], False, True, True))
            elif self.useclass:
                useclass = self.e.funcfind(self.useclass)
            sides[1] = basicformat(sides[1])
            for func in self.set_cmds:
                value = func(sides)
                if value is not None:
                    if not isinstance(value, tuple):
                        value = sides[0], value
                    self.printdebug(": "+strlist(classlist, ".")+"."*bool(classlist)+value[0]+" "+":"*docalc+"= "+self.e.prepare(value[1], False, True, True))
                    if useclass is None:
                        if not self.redef and value[0] in self.e.variables:
                            raise ExecutionError("RedefinitionError", "The variable "+value[0]+" already exists")
                        else:
                            if docalc:
                                self.e.variables[value[0]] = self.trycalc(value[1])
                            else:
                                self.e.variables[value[0]] = value[1]
                    else:
                        if not self.redef and value[0] in useclass.variables:
                            raise ExecutionError("RedefinitionError", "The attribute "+value[0]+" already exists")
                        else:
                            if docalc:
                                useclass.store(value[0], self.trycalc(value[1]))
                            else:
                                useclass.store(value[0], value[1])
                    return True

    def readytofunc(self, expression, extra="", allowed=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        funcparts = expression.split("(", 1)
        top = True
        if len(funcparts) == 1 and self.e.parenchar in funcparts[0]:
                funcparts = funcparts[0].split(self.e.parenchar, 1)
                top = False
        out = funcparts[0] != "" and (not self.e.isreserved(funcparts[0], extra, allowed)) and (len(funcparts) == 1 or funcparts[1].endswith(")"*top or self.e.parenchar))
        if out and len(funcparts) != 1:
            return not isinside(funcparts[1][:-1], '"`', {"\u201c":"\u201d"}, {"(":")", "{":"}", "[":"]"})
        else:
            return out

    def set_def(self, sides):
        """Creates Functions."""
        top = None
        if "(" in sides[0] and sides[0].endswith(")"):
            top = True
        elif self.e.parenchar in sides[0] and sides[0].endswith(self.e.parenchar):
            top = False
        if top is not None:
            if top:
                sides[0] = sides[0][:-1].split("(", 1)
            else:
                sides[0] = sides[0].split(self.e.parenchar, 1)
                sides[0][1] = self.e.namefind(self.e.parenchar+sides[0][1])
            params, personals, allargs, reqargs = self.e.eval_set(sides[0][1].split(","))
            return (sides[0][0], strfunc(sides[1], self.e, params, personals, allargs=allargs, reqargs=reqargs))

    def set_normal(self, sides):
        """Performs =."""
        if not self.e.isreserved(sides[0]):
            return sides[1]

    def cmd_normal(self, original):
        """Evaluates Functions."""
        self.returned = 0
        test = self.calc(original)
        if test is not None:
            self.ans.append(test)
            if self.doshow and self.returned == 0:
                self.show(self.e.prepare(self.ans[-1], True, True))
            return True

    def trycalc(self, inputobject):
        """Attempts To Calculate A Variable."""
        if istext(inputobject):
            return self.calc(inputobject)
        else:
            return inputobject

    def call(self, item, value, varname="x"):
        """Evaluates An Item With A Value."""
        out = self.e.call(item, value, varname)
        if out is None:
            raise ExecutionError("NoneError", "Nothing to call")
        else:
            return out

    def getstates(self, variables):
        """Compiles Variables."""
        out = {}
        for k,v in variables.items():
            try:
                v.getstate
            except AttributeError:
                value = v
            else:
                value = v.getstate()
            out[k] = value
        return out

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
                value = rollfunc(args[0], self.e, args[1], args[2], args[3])
            elif name == "matrix":
                value = matrix(args[1], args[2], converter=args[3], fake=args[4])
                for y in xrange(0, len(args[0])):
                    for x in xrange(0, len(args[0][y])):
                        value.store(y,x, self.deitem(args[0][y][x]))
            elif name == "strfunc":
                value = strfunc(args[0], self.e, args[1], self.devariables(args[2]), args[3], args[4], args[5])
            elif name == "strcalc":
                value = rawstrcalc(args[0], self.e)
            elif name == "derivfunc":
                value = derivfunc(args[0], args[1], args[2], args[3], self.e, args[4], args[5], args[6])
            elif name == "integfunc":
                value = integfunc(args[0], args[1], self.e, args[2], args[3], args[4])
            elif name == "usefunc":
                value = usefunc(args[0], self.e, args[1], args[2], args[3], args[4], args[5])
            elif name == "classcalc":
                value = classcalc(self.e, self.devariables(args[0]))
            elif name == "instancecalc":
                value = instancecalc(self.e, self.devariables(args[0]), self.devariables(args[1]))
            elif name == "find":
                tofind = str(args[0])
                if tofind in self.e.variables:
                    value = self.e.variables[tofind]
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

if __name__ == "__main__":
    mathbase().start()
