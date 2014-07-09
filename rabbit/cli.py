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

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class commandline(mathbase):
    """The Rabbit Command Line Interface."""
    on = True
    commands = []
    
    def __init__(self, message=None, prompt=addcolor(">>>", "pink")+" ", helpstring=None, outcolor="cyan", debugcolor="lightred", debug=False, *initializers):
        """Initializes The Command Line Interface."""
        self.debug = bool(debug)
        if message:
            message = str(message)
            self.messages.append(message)
        self.prompt = str(prompt)
        self.app = terminal(message, color=outcolor)
        self.show = self.appshow
        self.populator()
        self.e.color = debugcolor
        self.printdebug(": ON")
        if helpstring is not None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.pre_help,
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_debug,
            self.cmd_exit,
            self.cmd_clean,
            self.cmd_run,
            self.cmd_save,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_show,
            self.cmd_del,
            self.cmd_make,
            self.cmd_def,
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

    def start(self):
        """Starts The Command Line Main Loop."""
        while self.on:
            self.handler(raw_input(self.prompt))

    def handler(self, original):
        """Handles Raw Input."""
        self.reset()
        self.commands.append(original)
        cmd = carefulsplit(original, "#", '"`', {"\u201c":"\u201d"})[0]
        if delspace(cmd) != "":
            self.process(cmd)

    def calc(self, expression):
        """Safely Evaluates An Expression."""
        if self.top:
            self.e.info = -1
            self.top = False
        else:
            self.e.info = " <<--"
        return self.saferun(self.e.calc, expression)
