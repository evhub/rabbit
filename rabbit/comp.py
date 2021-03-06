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

from .cli import *
try:
    import cPickle
except ImportError:
    import pickle as cPickle

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class compiler(commandline):
    """The Rabbit Semi-Compiler."""
    compext = ".rabbit"
    debug = False
    doshow = False
    compiling = False
    normcommand = always(None)
    addcommand = always(None)
    protocol = 0

    def __init__(self, debugcolor="lightred", mainprompt=addcolor("Rabbit:", "pink")+" ", prompt=addcolor(">>>", "pink")+" ", moreprompt=addcolor("...", "pink")+" ", outcolor="cyan", *initializers):
        """Initializes The Command Line Interface."""
        self.startup()
        self.app = terminal()
        self.populator(debugcolor)
        self.mainprompt = str(mainprompt)
        self.prompt = str(prompt)
        self.moreprompt = str(moreprompt)
        self.color = outcolor
        self.cli_start = self.start
        self.start = self.comp_start
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self, debugcolor):
        """Creates An Evaluator And Lists Of Commands."""
        self.e = evaluator(processor=self, color=debugcolor, speedy=True)
        self.fresh(True)

    def show(self, arg, message=None):
        """Prints A Message To The Console."""
        self.app.display(self.e.forshow(arg))

    def comp_start(self):
        """Runs An Interactive Semi-Compiler Command Line Interface."""
        while self.on:
            cmd = superformat(raw_input(self.mainprompt))
            if cmd in ["h", "help"]:
                self.app.display(addcolor("Valid commands: help (h), interpret (i), compile (c), decompile (d), interactive (n), exit (x)", self.color))
            elif cmd in ["i", "interpret"]:
                self.interp()
            elif cmd in ["c", "compile"]:
                self.comp()
            elif cmd in ["d", "decompile"]:
                self.run()
            elif cmd in ["n", "interactive"]:
                on, self.on = self.on, True
                oldvars = self.e.setvars({
                    "exit":usefunc(self.doexit, "exit", [])
                    })
                self.cli_start()
                self.e.setvars(oldvars)
                self.on = on
            elif cmd in ["x", "exit"]:
                self.on = False
            else:
                self.app.display(addcolor("That isn't a valid command. Try 'help' for a list of valid commands.", self.color))

    def fatalerror(self):
        """Handles A Fatal Error."""
        self.on = False
        raise ExecutionError("RabbitError", "A fatal error occured")

    def interp(self):
        """Runs The Interpreter On A Source File."""
        name = raw_input(self.mainprompt+addcolor("Evaluate Source File:", self.color)+" ")
        if not self.evalfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def comp(self):
        """Runs The Compiler On A Source File."""
        name = raw_input(self.mainprompt+addcolor("Compile Source File:", self.color)+" ")
        if not self.compfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def run(self):
        """Runs The Decompiler On A Compiled File."""
        name = raw_input(self.mainprompt+addcolor("Execute Compiled File:", self.color)+" ")
        if not self.decompfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def decompfile(self, name=None):
        """Decompiles A File."""
        if not name:
            name = self.compext
        try:
            tempfile = open(name, "rb")
        except IOError:
            return False
        else:
            self.decomptext(readfile(tempfile))
            tempfile.close()
            return True

    def decomptext(self, inputstring):
        """Decompiles Text."""
        compiling = self.compiling
        self.compiling = False
        commands, variables, parens = self.disassemble(inputstring)
        self.e.makevars(variables)
        self.e.makeparens(parens)
        for command in commands:
            self.calc(command)
        self.compiling = compiling
        return True

    def compfile(self, name=None, result=None):
        """Compiles A File."""
        if not name:
            name = ""
        if not result:
            result = name+self.compext
        compiling = self.compext
        self.compiling = True
        if name:
            self.evalfile(name)
        self.compiling = compiling
        resultfile = open(result, "wb")
        writefile(resultfile, self.assemble())
        resultfile.close()
        return True

    def comptext(self, inputstring):
        """Compiles Text."""
        compiling = self.compiling
        self.compiling = True
        self.evaltext(inputstring)
        self.compiling = compiling
        return self.assemble()

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "make":funcfloat(self.makecall, "make", reqargs=1),
            "cmd":funcfloat(self.cmdcall, "cmd", reqargs=1),
            "print":funcfloat(self.printcall, "print"),
            "show":funcfloat(self.showcall, "show")
            })
        self.commands = []
        self.makes = []

    def makecall(self, variables):
        """Adds To Make Commands."""
        self.e.setreturned()
        out = []
        for x in variables:
            inputstring = self.e.prepare(x, False, False)
            self.makes.append(inputstring)
            out.append(self.e.calc(inputstring, " | calc"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def cmdcall(self, variables):
        """Adds To Make Commands."""
        self.e.setreturned()
        out = []
        for x in variables:
            inputstring = self.e.prepare(x, False, False)
            self.commands.append(inputstring)
            out.append(self.e.calc(inputstring, " | calc"))
        if len(out) == 1:
            return out[0]
        else:
            return diagmatrixlist(out)

    def assemble(self):
        """Compiles Code."""
        state = {
            "commands": self.commands,
            "makes": self.makes,
            "variables": getstates(self.e.variables),
            "parens": liststate(self.e.parens)
            }
        out = cPickle.dumps(state, protocol=self.protocol)
        self.fresh()
        return getbytes(out)

    def disassemble(self, inputstring):
        """Decompiles Code."""
        out = cPickle.loads(getbytes(inputstring))
        for command in out["makes"]:
            self.calc(command)
        return out["commands"], self.e.devariables(out["variables"]), self.e.delist(out["parens"])
