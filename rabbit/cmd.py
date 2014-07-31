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
    """A Base Class For Rabbit Evaluators."""
    doshow = True
    errorlog = False
    info = None

    def startup(self):
        """Initializes Containers."""
        self.messages = []
        self.commands = []
        self.ans = [matrix(0)]

    def __init__(self, name="Evaluator", message="Enter A Rabbit Command:", height=None, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator."""
        self.debug = bool(debug)
        self.startup()
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
                self.printdebug(str(k)+" = "+self.e.prepare(v, True, True, True))
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

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.e = evaluator(processor=self)
        self.fresh(True)

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, self.e, "debug"),
            "run":funcfloat(self.runcall, self.e, "run"),
            "assert":funcfloat(self.assertcall, self.e, "assert"),
            "del":funcfloat(self.delcall, self.e, "del"),
            "make":funcfloat(self.makecall, self.e, "make"),
            "def":funcfloat(self.defcall, self.e, "def"),
            "save":funcfloat(self.savecall, self.e, "save"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab"),
            "clear":usefunc(self.clear, self.e, "clear", [])
            })

    def clear(self):
        """Clears The Console."""
        self.app.clear()
        self.e.setreturned()

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
        cmd = self.e.outersplit(original, "#", {})[0]
        if delspace(cmd) == "":
            if len(self.box.commands) > 1:
                self.process(self.box.commands[-2])
        else:
            self.box.add(original)
            self.process(cmd)

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
            cmdlist[x] = self.e.outersplit(cmdlist[x], "#", {})[0]
            while x < len(cmdlist)-1 and (delspace(cmdlist[x+1]) == "" or iswhite(cmdlist[x+1][0])):
                cmdlist[x] += "\n"+self.e.outersplit(cmdlist.pop(x+1), "#", {})[0]
            self.process(cmdlist[x])
            x += 1

    def process(self, inputstring):
        """Processes A Command."""
        inputstring = basicformat(inputstring)
        if inputstring != "":
            if self.debug:
                info = self.info
            else:
                info = " <<| Traceback"
            self.saferun(self.e.process, inputstring, info, self.normcommand)

    def addcommand(self, inputsring):
        """Adds A Command To The Commands."""
        self.commands.append(inputstring)

    def normcommand(self, test):
        """Does The Processing."""
        if not isnull(test):
            self.ans.append(test)
            if self.doshow:
                self.show(self.e.prepare(self.ans[-1], True, True))
                self.e.setreturned()

    def debugcall(self, variables):
        """Controls Debugging."""
        if not variables:
            out = not self.debug
        elif len(variables) == 1:
            if isinstance(variables[0], strcalc):
                original = str(variables[0])
                if formatisyes(original):
                    out = True
                elif formatisno(original):
                    out = False
                else:
                    raise ValueError("Unrecognized debug state of "+original)
            else:
                out = bool(variables[0])
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to debug")
        self.e.setreturned()
        self.setdebug(out)
        return float(out)

    def runcall(self, variables):
        """Performs run."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to run")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                if not self.evalfile(original):
                    raise ExecutionError("IOError", "Could not find file "+str(original))
                else:
                    self.e.setspawned()
                    self.dumpdebug(True)
            else:
                raise ExecutionError("StatementError", "Can only call run as a statement")
        else:
            for arg in variables:
                self.runcall([arg])
        return matrix(0)

    def assertcall(self, variables):
        """Checks For Errors By Asserting That Something Is True."""
        if not variables:
            raise ExecutionError("ArgumentError", "Assertion failed that nothing")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                out = self.e.calc(original, "| assert")
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

    def delcall(self, variables):
        """Deletes A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to del")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], False, False)
            if original in self.e.variables:
                del self.e.variables[original]
            elif "." in original:
                test = original.split(".")
                item = test.pop()
                useclass = self.e.find(test[0], True)
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
            self.e.setreturned()
            self.printdebug("< "+original+" >")
        else:
            for arg in variables:
                self.delcall([arg])
        return matrix(0)

    def makecall(self, variables):
        """Sets A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to make")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                test = self.e.cmd_set(original)
                if test is None:
                    raise ExecutionError("DefinitionError", "No definition was done in the statement "+original)
                else:
                    return test
            else:
                raise ExecutionError("StatementError", "Can only call make as a statement")
        else:
            for arg in variables:
                self.makecall([arg])
        return matrix(0)

    def defcall(self, original):
        """Defines A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to def")
        elif len(variables) == 1:
            original = self.e.prepare(variables[0], True, True)
            self.redef = True
            test = self.e.cmd_set(original)
            self.redef = False
            if test:
                self.e.setreturned()
                return test
            else:
                raise ExecutionError("DefinitionError", "No definition was done in the statement "+original)
        else:
            for arg in variables:
                self.defcall([arg])
        return matrix(0)

    def printcall(self, variables, func=None):
        """Performs print."""
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
        self.e.setreturned()
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
                self.e.setreturned()
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
                self.e.setreturned()
        else:
            for x in variables:
                self.savecall([x])
        return matrix(0)

    def trycalc(self, inputobject):
        """Attempts To Calculate A Variable."""
        if istext(inputobject):
            return self.e.calc(inputobject)
        else:
            return inputobject

    def call(self, item, value, varname="x"):
        """Evaluates An Item With A Value."""
        return self.e.call(item, value, varname)

if __name__ == "__main__":
    mathbase().start()
