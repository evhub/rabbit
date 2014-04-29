#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# EDITOR made in 2012
# This program allows dynamic mathematical processing.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import absolute_import, print_function

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class editor(mathbase):
    """The Rabbit Integrated Development Environment."""
    helpstring = """Basic Commands:
    <command> [>> <command> >> <command>...]
    <name> [:]= <expression>
Expressions:
    <item>, [<item>, <item>...]
    <function> [:](<variables>)[:(<variables>):(<variables>)...]
    <expression> [@<condition>[; <expression>@<condition>; <expression>@<condition>;... <expression>]]
    [<variable>~]<list>~<expression>
    "string"
Console Commands:
    show <expression>
    <function>?
    help [string]
    errors
    clear
    clean
Control Commands:
    if <condition> then <command>
    for <list> do <command>
    while <condition> do <command>
    do <command>
    del <variable>
    get [variable]
Import Commands:
    <name> = import <file>
    run <file>
        save <file>"""

    def __init__(self, name="RIDE", width=100, height=40, helpstring=None, refresh=400, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.debug = bool(debug)
        self.debug_old = self.debug
        self.root = Tkinter.Tk()
        self.root.title(str(name))
        self.refresh = int(refresh)
        self.root.bind("<Escape>", lambda event: self.destroy())
        self.root.bind("<Control-r>", lambda event: self.run())
        self.root.bind("<Control-s>", lambda event: self.handle(self.save))
        self.root.bind("<Control-l>", lambda event: self.handle(self.load))
        self.root.bind("<Control-n>", lambda event: self.box.clear())
        self.root.bind("<Key>", lambda event: self.highlight())
        self.button_frame = Tkinter.Frame(self.root, height=1, width=40)
        self.button_frame.pack(side="bottom")
        self.button_run = button(self.button_frame, "Run", self.run, pack=False)
        self.button_run.main.pack(side="left")
        self.button_run = button(self.button_frame, "Check", self.check, pack=False)
        self.button_run.main.pack(side="left")
        self.button_save = button(self.button_frame, "Save", lambda: self.handle(self.save), pack=False)
        self.button_save.main.pack(side="left")
        self.button_load = button(self.button_frame, "Load", lambda: self.handle(self.load), pack=False)
        self.button_load.main.pack(side="left")
        self.box = texter(self.root, int(width), int(height), scroll=True)
        self.box.colortag("reserved", "blue")
        self.box.colortag("string", "darkgreen")
        self.box.colortag("comment", "red")
        self.errorlog = {}
        self.ans = [matrix(0)]
        self.populator()
        if helpstring != None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)
        self.register(lambda: self.highlightall(True), self.refresh)

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.do_find,
            self.pre_question,
            self.pre_help,
            self.pre_cmd
            ]
        self.cmds = [
            self.do_find,
            self.cmd_debug,
            self.cmd_errors,
            self.cmd_clear,
            self.cmd_clean,
            self.cmd_while,
            self.cmd_for,
            self.cmd_if,
            self.cmd_get,
            self.cmd_run,
            self.cmd_save,
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
        self.e = evaluator({
            "print":self.printcall,
            "ans":self.anscall
            }, self)

    def handle(self, func):
        """Handles A Function."""
        if not func(popup("Entry", "Enter The Name Of The File:", "File Control")):
            popup("Error", "Unable To Find File.")

    def highlight(self, point="insert"):
        """Checks The Last Character."""
        point = str(point)
        test = self.box.output(point+"-1c", point)
        if "#" in test:
            self.box.placetag("comment", point+"-1c", point)
        elif '"' in test:
            self.box.placetag("string", point+"-1c", point)
        elif self.e.isreserved(test) and not test in string.digits:
            self.box.placetag("reserved", point+"-1c", point)
        return test

    def clearhighlight(self):
        """Clears Highlighting."""
        self.box.remtag("comment")
        self.box.remtag("string")
        self.box.remtag("reserved")

    def highlightall(self, refresh=False):
        """Highlights All Characters."""
        self.clearhighlight()
        linelist = self.box.output().split("\n")
        instring = False
        incomment = False
        for l in xrange(0, len(linelist)):
            for c in xrange(0, len(linelist[l])+1):
                point = str(l+1)+"."+str(c)
                test = self.highlight(point)
                if c == 1 and not test in string.whitespace:
                    incomment = False
                    instring = False
                if not instring and test == "#":
                    incomment = True
                elif not incomment and test == '"':
                    instring = not instring
                elif incomment:
                    self.box.placetag("comment", point+"-1c", point)
                elif instring:
                    self.box.placetag("string", point+"-1c", point)
        if refresh:
            self.register(lambda: self.highlightall(True), self.refresh)

    def load(self, name):
        """Loads A File."""
        try:
            tempfile = openfile(name, "rb")
        except IOError:
            return None
        else:
            self.box.clear()
            self.box.display(readfile(tempfile))
            tempfile.close()
            self.highlightall()
            return True

    def save(self, name, load=True):
        """Saves To A File."""
        try:
            tempfile = openfile(name, "r+b")
        except IOError:
            return None
        else:
            writefile(tempfile, self.box.output())
            tempfile.close()
            if load:
                return self.load(name)
            else:
                return True

    def run(self):
        """Runs The Module."""
        self.debug = self.debug_old
        self.errorlog = {}
        self.returned = 0
        self.ans = [matrix(0)]
        self.populator()
        self.evaltext(self.box.output())

    def check(self):
        """Checks The Module."""
        self.run()
        self.showerrors()

    def show(self, arg):
        """Displays Something."""
        if not istext(arg):
            arg = self.e.prepare(arg)
        if arg != "()":
            popup("Info", arg, "Output")

    def destroy(self):
        """Ends The Editor."""
        if formatisyes(popup("Question", "Save First?", "Exit")):
            self.handle(lambda name: self.save(name, False))
        self.root.destroy()
