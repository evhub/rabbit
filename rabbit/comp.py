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

from .cli import *
import cPickle

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class compiler(commandline):
    """The Rabbit Semi-Compiler."""
    debug = False
    doshow = False
    compiling = False
    normcommand = lambda: None

    def __init__(self, debugcolor="lightred", mainprompt=addcolor("Rabbit:", "pink")+" ", prompt=addcolor(">>>", "pink")+" ", moreprompt=addcolor("...", "pink")+" ", outcolor="cyan", *initializers):
        """Initializes The Command Line Interface."""
        self.startup()
        self.app = terminal()
        self.populator()
        self.e.color = debugcolor
        self.e.proc_set = self.proc_set
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
                on = self.on
                self.on = True
                oldvars = self.e.setvars({
                    "exit":usefunc(self.doexit, self.e, "exit", [])
                    })
                self.cli_start()
                self.e.setvars(oldvars)
                self.on = on
            elif cmd in ["x", "exit"]:
                self.on = False
            else:
                self.app.display(addcolor("That isn't a valid command. Try 'help' for a list of valid commands.", self.color))

    def interp(self):
        """Runs The Interpreter On A Source File."""
        name = raw_input(self.mainprompt+addcolor("Evaluate Source File:", self.color)+" ")
        if not self.evalfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def comp(self):
        """Runs The Compiler On A Source File."""
        name = raw_input(self.mainprompt+addcolor("Compile Source File:", self.color)+" ")
        if not self.compfile(name, name+".rabbit"):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def run(self):
        """Runs The Decompiler On A Compiled File."""
        name = raw_input(self.mainprompt+addcolor("Execute Compiled File:", self.color)+" ")
        if not self.decompfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def decompfile(self, name):
        """Decompiles A File."""
        try:
            tempfile = openfile(name, "rb")
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

    def compfile(self, name, result):
        """Compiles A File."""
        compiling = self.compiling
        self.compiling = True
        self.evalfile(name)
        self.compiling = compiling
        resultfile = openfile(result, "wt")
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
            "run":funcfloat(self.runcall, self.e, "run"),
            "del":funcfloat(self.delcall, self.e, "del"),
            "make":funcfloat(self.makecall, self.e, "make"),
            "assert":funcfloat(self.comp_assertcall, self.e, "assert"),
            "def":funcfloat(self.comp_defcall, self.e, "def"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show")
            })
        self.commands = []
        self.makes = []

    def comp_assertcall(self, variables):
        """Wrapper around assertcall."""
        out = self.assertcall(variables)
        self.e.setspawned()
        return out

    def comp_defcall(self, variables):
        """Wrapper around defcall."""
        out = self.defcall(variables)
        self.e.setspawned()
        return out

    def proc_set(self, inputstring):
        """Replaces self.e.proc_set."""
        if self.e.cmd_set(inputstring):
            self.e.setspawned()
            return matrix(0)
        else:
            return self.e.proc_calc(inputstring)

    def makecall(self, variables):
        """Adds To Make Commands."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to make")
        elif len(variables) == 1:
            if isinstance(variables[0], codestr):
                original = str(variables[0])
                test = self.e.cmd_set(original)
                if test is None:
                    raise ExecutionError("DefinitionError", "No definition was done in the statement "+original)
                else:
                    self.makes.append(original)
                    self.e.setspawned()
                    return test
            else:
                raise ExecutionError("StatementError", "Can only call make as a statement")
        else:
            for arg in variables:
                self.makecall([arg])
        return matrix(0)

    def assemble(self, protocol=0):
        """Compiles Code."""
        out = cPickle.dumps({
            "commands": self.commands,
            "makes": self.makes,
            "variables": self.e.getstates(self.e.variables),
            "parens": self.e.liststate(self.e.parens)
            }, protocol=int(protocol))
        self.fresh()
        return out

    def disassemble(self, inputstring):
        """Decompiles Code."""
        out = cPickle.loads(inputstring)
        for command in out["makes"]:
            self.calc(command)
        return out["commands"], self.e.devariables(out["variables"]), self.e.delist(out["parens"])
