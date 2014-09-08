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
            "make":funcfloat(self.e.funcs.docalc, self.e, "make", reqargs=1),
            "cmd":funcfloat(self.e.funcs.docalc, self.e, "cmd", reqargs=1),
            "save":funcfloat(self.savecall, self.e, "save", reqargs=1),
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
            self.evaltext(original)
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
        lines = inputstring.splitlines()
        for x in xrange(0, len(lines)):
            line = lines[x]
            if line:
                if not iswhite(line[0]):
                    cmds.append(line)
                elif cmds:
                    cmds[-1] += "\n"+line
                else:
                    self.adderror("IndentationError", "Illegal starting indent in line "+line+" (#"+str(x)+")", True)
                    break
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

    def savecall(self, variables):
        """Performs save."""
        if not variables:
            raise ExecutionError("NoneError", "Nothing is not a file name")
        else:
            self.e.overflow = variables[1:]
            self.e.setreturned()
            original = self.e.prepare(variables[0], False, False)
            try:
                writefile(getfile(original, "wb"), strlist(self.commands, "\n"))
            except IOError:
                raise ExecutionError("IOError", "Could not find for save file "+original)
            return matrix(0)

    def call(self, item, value, varname="x"):
        """Evaluates An Item With A Value."""
        return self.e.call(item, value, varname)

if __name__ == "__main__":
    mathbase().start()
