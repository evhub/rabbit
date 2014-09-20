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

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class commandline(mathbase):
    """The Rabbit Command Line Interface."""
    on = True
    info = " <<--"
    
    def __init__(self, message=None, prompt=addcolor(">>>", "pink")+" ", moreprompt=addcolor("...", "pink")+" ", outcolor="cyan", debugcolor="lightred", debug=False, *initializers):
        """Initializes The Command Line Interface."""
        self.startup(debug)
        if message:
            message = str(message)
            self.messages.append(message)
        self.prompt = str(prompt)
        self.moreprompt = str(moreprompt)
        self.app = terminal(message, color=outcolor)
        self.show = self.appshow
        self.populator(debugcolor)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self, debugcolor):
        """Creates An Evaluator And Lists Of Commands."""
        self.e = evaluator(processor=self, color=debugcolor)
        self.fresh(True)
        self.printdebug(": ON")

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, "debug"),
            "make":funcfloat(self.e.funcs.docalc, "make", reqargs=1),
            "cmd":funcfloat(self.e.funcs.docalc, "cmd", reqargs=1),
            "save":funcfloat(self.savecall, "save", reqargs=1),
            "print":funcfloat(self.printcall, "print"),
            "show":funcfloat(self.showcall, "show"),
            "ans":funcfloat(self.anscall, "ans"),
            "grab":funcfloat(self.grabcall, "grab"),
            "exit":usefunc(self.doexit, "exit")
            })

    def doexit(self):
        """Exits The Command Line Interface."""
        self.e.setreturned()
        self.on = False

    def fatalerror(self):
        """Has A Fatal Error."""
        pass

    def start(self):
        """Starts The Command Line Main Loop."""
        while self.on:
            try:
                old = self.handler(raw_input(self.prompt))
                while old:
                    old = self.handler(raw_input(self.moreprompt), old)
            except KeyboardInterrupt as detail:
                print(addcolor("\n<!> KeyboardInterrupt: Action has been terminated, to quit type exit()", self.e.color))
            except EOFError as detail:
                print(addcolor("\n<!!> EOFInterrupt: Program has been terminated", self.e.color))
                self.on = False

    def handler(self, original, old=None):
        """Handles Raw Input."""
        cmd = self.e.remcomment(original)
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
                if self.e.insideouter(old):
                    old = 'raise("SyntaxError", "Unmatched tokens in "+ ' + self.e.prepare(rawstrcalc(old), False, True) + ' )'
                return old+"\n"+cmd
        elif fcmd and endswithany(fcmd, self.e.multiargops):
            return whole
        elif self.e.insideouter(whole):
            return whole
        self.evaltext(whole)
