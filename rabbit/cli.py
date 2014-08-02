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
    info = " <<--"
    
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
        self.populator(debugcolor)
        self.printdebug(": ON")
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def populator(self, debugcolor):
        """Creates An Evaluator And Lists Of Commands."""
        self.e = evaluator(processor=self, color=debugcolor)
        self.fresh(True)

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, self.e, "debug"),
            "run":funcfloat(self.runcall, self.e, "run"),
            "assert":funcfloat(self.assertcall, self.e, "assert"),
            "make":funcfloat(self.makecall, self.e, "make"),
            "save":funcfloat(self.savecall, self.e, "save"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab"),
            "exit":usefunc(self.doexit, self.e, "exit", [])
            })

    def doexit(self):
        """Exits The Command Line Interface."""
        self.e.setreturned()
        self.on = False

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
                print(addcolor("\n<!> EOFInterrupt: Program has been terminated", self.e.color))
                self.doexit()

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
            elif isinside(old, '"`', {"\u201c":"\u201d"}, self.e.groupers):
                return 'raise("SyntaxError", "Unmatched tokens in "+ ' + self.e.prepare(rawstrcalc(old, self.e), False, True) + ' )\n;;\n'+cmd
            else:
                return old+"\n;;\n"+cmd
        elif fcmd and endswithany(fcmd, self.e.multiargops):
            return whole
        elif isinside(whole, '"`', {"\u201c":"\u201d"}, self.e.groupers):
            return whole
        self.reset()
        self.process(whole)
