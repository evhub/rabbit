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

from __future__ import absolute_import, print_function, unicode_literals
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

    def __init__(self, debugcolor="lightred", prompt=addcolor("Rabbit:", "pink")+" ", nprompt=addcolor(">>>", "pink")+" ", outcolor="cyan", *initializers):
        """Initializes The Command Line Interface."""
        self.app = terminal()
        self.populator()
        self.e.color = debugcolor
        self.prompt = str(prompt)
        self.nprompt = str(nprompt)
        self.color = outcolor
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def show(self, arg, message=None):
        """Prints A Message To The Console."""
        self.app.display(self.e.forshow(arg))

    def start(self):
        """Runs An Interactive Semi-Compiler Command Line Interface."""
        while self.on:
            cmd = superformat(raw_input(self.prompt))
            if cmd in ["h", "help"]:
                self.app.display(addcolor("Valid commands: help (h), interpret (i), compile (c), decompile (d), interactive (n), exit (x)", self.color))
            elif cmd in ["i", "interpret"]:
                self.interp()
            elif cmd in ["c", "compile"]:
                self.comp()
            elif cmd in ["d", "decompile"]:
                self.run()
            elif cmd in ["n", "interactive"]:
                cmd = raw_input(self.nprompt)
                while superformat(cmd) != "exit":
                    self.handler(cmd)
                    cmd = raw_input(self.nprompt)
            elif cmd in ["x", "exit"]:
                self.on = False
            else:
                self.app.display(addcolor("That isn't a valid command. Try 'help' for a list of valid commands.", self.color))

    def interp(self):
        """Runs The Interpreter On A Source File."""
        name = raw_input(self.prompt+addcolor("Evaluate Source File:", self.color)+" ")
        if not self.evalfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def comp(self):
        """Runs The Compiler On A Source File."""
        name = raw_input(self.prompt+addcolor("Compile Source File:", self.color)+" ")
        if not self.compfile(name, name+".rabbit"):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def run(self):
        """Runs The Decompiler On A Compiled File."""
        name = raw_input(self.prompt+addcolor("Execute Compiled File:", self.color)+" ")
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
        oldvars = self.e.variables
        commands, self.e.variables = self.disassemble(inputstring)
        for command in commands:
            self.calc(command)
        self.e.variables = oldvars
        self.compiling = compiling
        return True

    def compfile(self, name, result):
        """Compiles A File."""
        compiling = self.compiling
        self.compiling = True
        self.evalfile(name)
        self.compiling = compiling
        resultfile = openfile(result, "wb")
        try:
            writefile(resultfile, self.assemble())
        finally:
            resultfile.close()
            return True

    def comptext(self, inputstring):
        """Compiles Text."""
        compiling = self.compiling
        self.compiling = True
        self.evaltext(inputstring)
        self.compiling = compiling
        return self.assemble()

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_clean,
            self.cmd_run,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_show,
            self.cmd_del,
            self.cmd_def,
            self.cmd_set,
            self.cmd_normal
            ]
        self.set_cmds = [
            self.set_import,
            self.set_def,
            self.set_normal
            ]
        self.e = evaluator(processor=self, speedy=True)
        self.e.makevars({
            "print":funcfloat(self.printcall, self.e, "print")
            })

    def cmd_do(self, original):
        """Evaluates Functions Silently."""
        if superformat(original).startswith("do "):
            self.calc(original[3:])
            return True

    def cmd_normal(self, original):
        """Evaluates Functions."""
        self.returned = 0
        if self.compiling and self.top:
            self.commands.append(original)
        else:
            test = self.calc(original)
            if test != None:
                return True

    def assemble(self, inputcode):
        """Compiles Code."""
        raise NotImplementedError("Semi-compilation is not currently possible in Rabbit.")

    def disassemble(self, inputstring):
        """Decompiles Code."""
        raise NotImplementedError("Semi-compilation is not currently possible in Rabbit.")
