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

from __future__ import absolute_import, print_function

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class commandline(mathbase):
    """The Rabbit Command Line Interface."""
    def __init__(self, message="Enter A Rabbit Command:", prompt=">>> ", helpstring=None, debug=False, *initializers):
        """Initializes The Command Line Interface."""
        self.on = True
        self.debug = bool(debug)
        self.messages = [str(message)]
        self.prompt = str(prompt)
        self.app = terminal(self.messages[0])
        self.errorlog = {}
        self.ans = [matrix(0)]
        self.commands = []
        self.returned = 1
        self.top = False
        self.populator()
        if helpstring != None:
            self.helpstring = str(helpstring)
        if self.debug:
            print(self.e.recursion*"  "+": ON")
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.do_find,
            self.pre_help,
            self.pre_cmd
            ]
        self.cmds = [
            self.do_find,
            self.cmd_debug,
            self.cmd_errors,
            self.cmd_exit,
            self.cmd_clean,
            self.cmd_get,
            self.cmd_run,
            self.cmd_save,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_show,
            self.cmd_del,
            self.cmd_set,
            self.cmd_normal
            ]
        self.set_cmds = [
            self.set_import,
            self.set_def,
            self.set_normal
            ]
        self.e = evaluator(processor=self)
        self.e.makevars({
            "print":funcfloat(self.printcall, self.e, "print"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab")
            })

    def cmd_exit(self, original):
        """Exits The Command Line Interface."""
        if superformat(original) == "exit":
            self.on = False
            return True

    def cmd_show(self, original):
        """Shows A Message."""
        if superformat(original).startswith("show "):
            self.app.display(self.e.prepare(self.calc(original[5:]), True, False))
            return True

    def cmd_save(self, original):
        """Performs save."""
        if superformat(original).startswith("save "):
            writefile(getfile(original[5:], "wb"), strlist(self.commands[:-1], "\n"))
            return True

    def showerrors(self):
        """Shows Logged Errors."""
        errorstring = self.geterrors()
        if errorstring == "":
            errorstring = "No Errors."
        self.show(errorstring, True)

    def start(self):
        """Starts The Command Line Main Loop."""
        while self.on:
            self.handler(raw_input(self.prompt))

    def handler(self, original):
        """Handles Raw Input."""
        self.e.recursion = 0
        self.commands.append(original)
        cmd = carefulsplit(original, "#", '"')[0]
        if delspace(cmd) == "":
            self.adderror("NoneError", "Nothing cannot be executed.")
        else:
            self.top = True
            self.process(cmd)

    def calc(self, expression):
        """Safely Evaluates An Expression."""
        if self.top:
            self.e.info = -1
            self.top = False
        else:
            self.e.info = " <<"
        return self.saferun(self.e.calc, expression)
