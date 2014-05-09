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
    <command> [~~ <command> ~~ <command>...]
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
    clean
Control Commands:
    if <condition> do <command>
    for <list> do <command>
    while <condition> do <command>
    do <command>
    del <variable>
    get [variable]
Import Commands:
    <name> = import <file>
    run <file>
        save <file>"""

    def __init__(self, name="RIDE", width=100, height=40, helpstring=None, refresh=600, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.debug = bool(debug)
        self.debug_old = self.debug
        self.root = Tkinter.Tk()
        self.root.title(str(name))
        self.refresh = int(refresh)
        self.root.bind("<Escape>", lambda event: self.destroy())
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        self.root.bind("<Control-r>", lambda event: self.run())
        self.root.bind("<Control-s>", lambda event: self.handle(self.save))
        self.root.bind("<Control-l>", lambda event: self.handle(self.load))
        self.root.bind("<Control-n>", lambda event: self.box.clear())
        self.root.bind("<Key>", lambda event: self.endchar())
        self.root.bind("<Return>", lambda event: self.endline())
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
        self.box.colortag("reserved", "orange")
        self.box.colortag("string", "darkgreen")
        self.box.colortag("comment", "red")
        self.box.colortag("variable", "blue")
        self.box.colortag("modifier", "cyan")
        self.box.colortag("digit", "darkgrey")
        self.box.colortag("builtin", "purple")
        self.box.colortag("stringmod", "green")
        self.errorlog = {}
        self.ans = [matrix(0)]
        self.populator()
        if helpstring != None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)
        self.register(lambda: self.endfile(True), self.refresh)

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
        self.e = evaluator(processor=self)
        self.e.makevars({
            "print":funcfloat(self.printcall, self.e, "print"),
            "ans":funcfloat(self.anscall, self.e, "ans")
            })

    def handle(self, func):
        """Handles A Function."""
        if not func(popup("Entry", "Enter The Name Of The File:", "File Control")):
            popup("Error", "Unable To Find File.")

    def endline(self):
        """Checks The Last Line."""
        last = self.box.output("insert-1l", "insert-1c")
        if last.endswith("?"):
            self.box.clear("insert-1l", "insert-1c")
            self.box.insert(self.findhelp(last[:-1]), "-1l")
        else:
            space = 0
            start = True
            instring = False
            for x in last:
                if start:
                    if start == 2:
                        if x == "-":
                            instring = True
                            space -= 1
                        else:
                            start = False
                    elif x in string.whitespace:
                        space += 1
                    elif x == "\\":
                        start = 2
                    else:
                        start = False
                if x == '"':
                    instring = not instring
                elif not instring and x in ["(", "[", "{"]:
                    space += 1
                elif not instring and x in [")", "]", "}"]:
                    space -= 1
            space += instring
            if space <= 0 and endswithany(basicformat(last), "=:*+-%/^@~\\|&;<>.,([{"):
                space = 1
            insert = " "*space
            if instring:
                insert += "\\-"*space
            self.box.insert(insert)

    def endchar(self, point="insert"):
        """Checks The Last Character."""
        point = str(point)
        test = self.box.output(point+"-1c", point)
        if test == "#":
            self.box.placetag("comment", point+"-1c", point)
        elif test == '"':
            self.box.placetag("string", point+"-1c", point)
        elif test in "'":
            self.box.placetag("modifier", point+"-1c", point)
        elif test in string.digits:
            self.box.placetag("digit", point+"-1c", point)
        elif self.e.isreserved(test):
            self.box.placetag("reserved", point+"-1c", point)
        return test

    def remtags(self, start="1.0", end="end"):
        """Clears Highlighting."""
        self.box.remtag("comment", start, end)
        self.box.remtag("string", start, end)
        self.box.remtag("reserved", start, end)
        self.box.remtag("variable", start, end)
        self.box.remtag("modifier", start, end)
        self.box.remtag("digit", start, end)
        self.box.remtag("builtin", start, end)
        self.box.remtag("stringmod", start, end)

    def endfile(self, refresh=False):
        """Checks All Characters."""
        self.remtags()
        linelist = self.box.output().split("\n")
        instring = False
        incomment = False
        decimal = False
        strmod = False
        last = ("", "1.0")
        for l in xrange(0, len(linelist)):
            for c in xrange(0, len(linelist[l])+1):
                point = str(l+1)+"."+str(c)
                test = self.endchar(point)
                if c == 1 and not test in string.whitespace:
                    if last[0] == funcfloat.allargs:
                        self.box.placetag("builtin", last[1], point+"-2c")
                    elif last[0] in self.e.variables:
                        if isinstance(self.e.variables[last[0]], usefunc) or (isinstance(self.e.variables[last[0]], funcfloat) and not isinstance(self.e.variables[last[0]], strfunc)):
                            self.box.placetag("builtin", last[1], point+"-2c")
                        else:
                            self.box.placetag("variable", last[1], point+"-2c")
                    elif "'"+last[0] in self.e.variables:
                        if isinstance(self.e.variables["'"+last[0]], usefunc) or (isinstance(self.e.variables["'"+last[0]], funcfloat) and not isinstance(self.e.variables["'"+last[0]], strfunc)):
                            self.box.placetag("builtin", last[1], point+"-2c")
                        else:
                            self.box.placetag("variable", last[1], point+"-2c")
                    elif last[0] in ["inf", "nan"]:
                        self.box.placetag("digit", last[1], point+"-2c")
                    incomment = False
                    instring = False
                    decimal = False
                    strmod = False
                    last = ("", point+"-1c")
                normal = False
                if incomment:
                    self.remtags(point+"-1c", point)
                    self.box.placetag("comment", point+"-1c", point)
                elif test == '"':
                    instring = not instring
                    decimal = False
                    strmod = False
                elif instring:
                    self.remtags(point+"-1c", point)
                    if strmod:
                        if test in "n'-":
                            self.box.placetag("stringmod", point+"-1c", point)
                        else:
                            self.box.placetag("string", point+"-1c", point)
                        strmod = False
                    elif test == "\\":
                        self.box.placetag("stringmod", point+"-1c", point)
                        strmod = True
                    else:
                        self.box.placetag("string", point+"-1c", point)
                elif test == "#":
                    incomment = True
                    decimal = False
                elif test == ".":
                    decimal = not decimal
                    if decimal:
                        decimal = point
                elif decimal:
                    if test in string.digits:
                        self.box.remtag("reserved", decimal+"-1c", point+"-1c")
                        self.box.placetag("digit", decimal+"-1c", point+"-1c")
                    elif not self.e.isreserved(test):
                        normal = True
                    if not test in string.whitespace:
                        decimal = False
                elif not self.e.isreserved(test):
                    normal = True
                if normal:
                    last = (last[0]+delspace(test), last[1])
                else:
                    if last[0] == funcfloat.allargs:
                        self.box.placetag("builtin", last[1], point+"-1c")
                    elif last[0] in self.e.variables:
                        if isinstance(self.e.variables[last[0]], usefunc) or (isinstance(self.e.variables[last[0]], funcfloat) and not isinstance(self.e.variables[last[0]], strfunc)):
                            self.box.placetag("builtin", last[1], point+"-1c")
                        else:
                            self.box.placetag("variable", last[1], point+"-1c")
                    elif "'"+last[0] in self.e.variables:
                        if isinstance(self.e.variables["'"+last[0]], usefunc) or (isinstance(self.e.variables["'"+last[0]], funcfloat) and not isinstance(self.e.variables["'"+last[0]], strfunc)):
                            self.box.placetag("builtin", last[1], point+"-1c")
                        else:
                            self.box.placetag("variable", last[1], point+"-1c")
                    elif last[0] in ["inf", "nan"]:
                        self.box.placetag("digit", last[1], point+"-1c")
                    last = ("", point)
        if refresh:
            self.register(lambda: self.endfile(True), self.refresh)

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
            self.endfile()
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
