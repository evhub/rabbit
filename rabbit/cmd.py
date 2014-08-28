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

    def startup(self, debug=None):
        """Initializes Containers."""
        if debug is not None:
            self.debug = bool(debug)
        self.messages = []
        self.commands = []
        self.ans = [matrix(0)]

    def __init__(self, name="Evaluator", message="Enter A Rabbit Command:", height=None, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator."""
        self.startup(debug)
        if message:
            message = str(message)
            self.messages.append(message)
        if height is None:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name), int(height))
        self.show = self.appshow
        self.populator()
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

    def adderror(self, error, detail, fatal=False, variables=None):
        """Adds An Error To The Log."""
        self.printdebug("<!"+"!"*fatal+"> "+str(error)+": "+str(detail))
        if variables is not None:
            self.e.recursion += 1
            for k,v in variables.items():
                self.printdebug(str(k)+" = "+self.e.prepare(v, True, True, True))
            self.e.recursion -= 1
        self.dumpdebug()
        if fatal:
            self.fatalerror()

    def fatalerror(self):
        """Raises A Fatal Error."""
        raise ExecutionError("RabbitError", "A fatal error occured")

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
        self.printdebug(": ON")

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, self.e, "debug"),
            "run":funcfloat(self.runcall, self.e, "run", reqargs=1),
            "require":funcfloat(self.requirecall, self.e, "require", reqargs=1),
            "assert":funcfloat(self.assertcall, self.e, "assert", reqargs=1),
            "make":funcfloat(self.makecall, self.e, "make", reqargs=1),
            "save":funcfloat(self.savecall, self.e, "save", reqargs=1),
            "install":funcfloat(self.installcall, self.e, "install", reqargs=1),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab"),
            "clear":usefunc(self.clear, self.e, "clear")
            })

    def clear(self):
        """Clears The Console."""
        self.e.setreturned()
        self.app.clear()

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
        original = self.box.output()
        if not iswhite(original):
            self.box.add(original)
            self.evaltext(cmd)
        elif len(self.box.commands) > 1:
            self.evaltext(self.box.commands[-2])

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
        cmds = []
        for line in inputstring.splitlines():
            if line:
                if not iswhite(line[0]):
                    cmds.append(line)
                elif cmds:
                    cmds[-1] += line
                else:
                    raise ExecutionError("IndentationError", "Illegal starting indent in line "+line)
        for cmd in cmds:
            self.reset()
            self.process(cmd)

    def process(self, inputstring):
        """Processes A Command."""
        inputstring = basicformat(inputstring)
        if inputstring != "":
            if self.debug:
                info = self.info
            else:
                info = " <<| Traceback"
            self.saferun(self.e.process, inputstring, info, self.normcommand)

    def addcommand(self, inputstring):
        """Adds A Command To The Commands."""
        self.commands.append(inputstring)

    def normcommand(self, test):
        """Does The Processing."""
        if not isnull(test):
            self.ans.append(test)
            if self.doshow:
                self.e.setreturned()
                self.show(self.e.prepare(self.ans[-1], True, True))

    def debugcall(self, variables):
        """Controls Debugging."""
        if not variables:
            self.e.setreturned()
            out = not self.debug
        elif len(variables) == 1:
            self.e.setreturned()
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
        self.setdebug(out)
        return float(out)

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
            if not self.evalfile(original):
                raise ExecutionError("IOError", "Failed to execute file "+str(original))
            else:
                self.dumpdebug(True)
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
            raise ExecutionError("ArgumentError", "Assertion failed that nothing")
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

    def makecall(self, variables):
        """Sets A Variable."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to make")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                out = self.e.calc(original, " | make")
                return out
            else:
                raise ExecutionError("StatementError", "Can only call make as a statement")
        else:
            out = []
            for arg in variables:
                out.append(self.makecall([arg]))
            return diagmatrixlist(out)

    def printcall(self, variables, func=None):
        """Performs print."""
        self.e.setreturned()
        if not variables:
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
        self.e.setreturned()
        if variables is None or len(variables) == 0:
            return self.ans[-1]
        else:
            self.e.overflow = variables[1:]
            return self.ans[getint(variables[0])]

    def grabcall(self, variables):
        """Performs grab."""
        self.e.setreturned()
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
        if not variables:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        elif len(variables) == 1:
            self.e.setreturned()
            inputstring = self.e.prepare(variables[0], False, False)
            name = delspace(delspace(inputstring), self.e.reserved)
            try:
                impclass = dirimport(inputstring).interface
            except IOError:
                raise ExecutionError("IOError", "Could not find for install file "+inputstring)
            else:
                if impclass is None:
                    return matrix(0)
                elif iseval(impclass):
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
        if not variables:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        elif len(variables) == 1:
            self.e.setreturned()
            original = self.e.prepare(variables[0], False, False)
            try:
                writefile(getfile(original, "wb"), strlist(self.commands, "\n"))
            except IOError:
                raise ExecutionError("IOError", "Could not find for save file "+original)
        else:
            for x in variables:
                self.savecall([x])
        return matrix(0)

    def call(self, item, value, varname="x"):
        """Evaluates An Item With A Value."""
        return self.e.call(item, value, varname)

if __name__ == "__main__":
    mathbase().start()
