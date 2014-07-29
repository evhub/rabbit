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
    
    def __init__(self, message=None, prompt=addcolor(">>>", "pink")+" ", moreprompt=addcolor("...", "pink")+" ", outcolor="cyan", debugcolor="lightred", debug=False, *initializers):
        """Initializes The Command Line Interface."""
        self.debug = bool(debug)
        self.startup()
        if message:
            message = str(message)
            self.messages.append(message)
        self.prompt = str(prompt)
        self.moreprompt = str(moreprompt)
        self.app = terminal(message, color=outcolor)
        self.show = self.appshow
        self.populator()
        self.e.color = debugcolor
        self.printdebug(": ON")
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_help,
            self.cmd_debug,
            self.cmd_exit,
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

    def cmd_exit(self, original):
        """Exits The Command Line Interface."""
        if superformat(original) == "exit":
            self.on = False
            self.setreturned()
            return True

    def start(self):
        """Starts The Command Line Main Loop."""
        while self.on:
            try:
                old = self.handler(raw_input(self.prompt))
                while old:
                    old = self.handler(raw_input(self.moreprompt), old)
            except KeyboardInterrupt as detail:
                self.app.display(addcolor("\n<!> KeyboardInterrupt: Action has been terminated, to quit type exit", self.e.color))
            except EOFError as detail:
                self.app.display(addcolor("\n<!> EOFInterrupt: Program has been terminated", self.e.color))
                self.cmd_exit("exit")

    def handler(self, original, old=None):
        """Handles Raw Input."""
        cmd = carefulsplit(original, "#", '"`', {"\u201c":"\u201d"})[0]
        fcmd = basicformat(cmd)
        if old is not None:
            whole = old+"\n"+cmd
        else:
            whole = cmd
        if iswhite(whole):
            return None
        elif old is not None and not cmd == "":
            if iswhite(cmd[0]):
                return whole
            else:
                return old+"\n;;\n"+cmd
        elif fcmd and endswithany(fcmd, self.multiargops):
            return whole
        elif isinside(whole, '"`', {"\u201c":"\u201d"}, {"(":")", "{":"}", "[":"]"}):
            return whole
        self.reset()
        self.process(whole, True)

    def calc(self, expression):
        """Safely Evaluates An Expression."""
        if self.debug:
            self.e.info = " <<--"
        else:
            self.e.info = " <<| Traceback"
        return self.e.calc(expression)
