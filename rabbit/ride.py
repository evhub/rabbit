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

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class editor(mathbase):
    """The Rabbit Integrated Development Environment."""

    def __init__(self, name="RIDE", tablen=1, width=100, height=40, refresh=600, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.startup(debug)
        self.debug_old = self.debug
        self.root = Tkinter.Tk()
        self.root.title(str(name))
        self.show = self.popshow
        self.refresh = int(refresh)
        self.tablen = int(tablen)
        rootbind(self.root, self.destroy)
        self.root.bind("<Control-r>", lambda event: self.run())
        self.root.bind("<Control-s>", lambda event: self.handle(self.save))
        self.root.bind("<Control-l>", lambda event: self.handle(self.load))
        self.root.bind("<Control-n>", lambda event: self.clear())
        self.root.bind("<Control-f>", lambda event: self.search())
        self.root.bind("<Control-Tab>", lambda event: self.endsearch())
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
        self.box.colortag("digit", "darkgrey")
        self.box.colortag("builtin", "purple")
        self.box.colortag("stringmod", "green")
        self.box.colortag("search", highlight="yellow")
        self.populator()
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)
        self.register(lambda: self.endfile(True), self.refresh)

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, self.e, "debug"),
            "run":funcfloat(self.runcall, self.e, "run"),
            "require":funcfloat(self.requirecall, self.e, "require"),
            "assert":funcfloat(self.assertcall, self.e, "assert"),
            "make":funcfloat(self.makecall, self.e, "make"),
            "save":funcfloat(self.savecall, self.e, "save"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "ans":funcfloat(self.anscall, self.e, "ans")
            })

    def handle(self, func):
        """Handles A Function."""
        inputstring = popup("Entry", "Enter The Name Of The File:", "File Control")
        if inputstring and not func(inputstring):
            popup("Error", "Unable To Find File.")

    def search(self):
        """Starts A Search."""
        inputstring = popup("Entry", "Search For What:", "Search Dialog")
        if inputstring:
            for x in self.box.search(inputstring):
                self.box.placetag("search", x, x+"+"+str(len(inputstring))+"c")

    def endline(self):
        """Checks The Last Line."""
        last = self.e.remcomment(self.box.output("insert-1l", "insert-1c"))
        space = 0
        start = True
        instring = False
        for x in last:
            if start:
                if start == 2:
                    if x == "-":
                        instring = True
                        space -= 1
                    start = False
                elif iswhite(x):
                    space += 1
                elif x == "\\":
                    start = 2
                else:
                    start = False
            if instring:
                if x == instring:
                    instring = not instring
            elif x in ['"', "`"]:
                instring = x
            elif x == "\u201c":
                instring = "\u201d"
            elif x in self.e.groupers.keys():
                space += self.tablen
            elif x in self.e.groupers.values():
                space -= self.tablen
        if instring:
            space += self.tablen
        elif space <= 0 and endswithany(basicformat(last), self.e.multiargops):
            space = self.tablen
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
        elif test in ['"', "`", "\u201c", "\u201d"]:
            self.box.placetag("string", point+"-1c", point)
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
        self.box.remtag("digit", start, end)
        self.box.remtag("builtin", start, end)
        self.box.remtag("stringmod", start, end)

    def endsearch(self):
        """Clears Search Highlighting."""
        self.box.remtag("search", "1.0", "end")

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
            incomment = False
            for c in xrange(0, len(linelist[l])+1):
                point = str(l+1)+"."+str(c)
                test = self.endchar(point)
                if c == 1 and not iswhite(test):
                    if last[0] in [funcfloat.allargs, strfunc.autoarg]:
                        self.box.placetag("builtin", last[1], point+"-2c")
                    elif last[0] in self.e.variables:
                        if isbuiltin(self.e.variables[last[0]]):
                            self.box.placetag("builtin", last[1], point+"-2c")
                        else:
                            self.box.placetag("variable", last[1], point+"-2c")
                    elif last[0] in ["inf", "nan"]:
                        self.box.placetag("digit", last[1], point+"-2c")
                    instring = False
                    decimal = False
                    strmod = False
                    last = ("", point+"-1c")
                normal = False
                if incomment:
                    self.remtags(point+"-1c", point)
                    self.box.placetag("comment", point+"-1c", point)
                elif instring:
                    if test == instring:
                        instring = not instring
                        decimal = False
                        strmod = False
                    else:
                        self.remtags(point+"-1c", point)
                        if strmod:
                            if test in "-'abfnNrtuUvx":
                                self.box.placetag("stringmod", point+"-1c", point)
                            else:
                                self.box.placetag("string", point+"-1c", point)
                            strmod = False
                        elif instring != "`" and test == "\\":
                            self.box.placetag("stringmod", point+"-1c", point)
                            strmod = True
                        else:
                            self.box.placetag("string", point+"-1c", point)
                elif test in ['"', "`"]:
                    instring = test
                    decimal = False
                    strmod = False
                elif test == "\u201c":
                    instring = "\u201d"
                    decimal = False
                    strmod = False
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
                    if not iswhite(test):
                        decimal = False
                elif not self.e.isreserved(test):
                    normal = True
                if normal:
                    if last[0] == "":
                        last = (delspace(test), point+"-1c")
                    else:
                        last = (last[0]+delspace(test), last[1])
                else:
                    if last[0] in [funcfloat.allargs, strfunc.autoarg]:
                        self.box.placetag("builtin", last[1], point+"-1c")
                    elif last[0] in self.e.variables:
                        if isbuiltin(self.e.variables[last[0]]):
                            self.box.placetag("builtin", last[1], point+"-1c")
                        else:
                            self.box.placetag("variable", last[1], point+"-1c")
                    elif last[0] in ["inf", "nan"]:
                        self.box.placetag("digit", last[1], point+"-1c")
                    last = ("", point)
        if refresh:
            self.register(lambda: self.endfile(True), self.refresh)

    def clear(self):
        """Clears The Box."""
        self.endsearch()
        self.remtags()
        self.box.clear()

    def load(self, name, tempfile=None):
        """Loads A File."""
        try:
            tempfile = tempfile or openfile(name, "rb")
        except IOError:
            return None
        else:
            self.clear()
            self.box.display(readfile(tempfile))
            tempfile.close()
            self.endfile()
            return True

    def save(self, name, load=True, tempfile=None):
        """Saves To A File."""
        try:
            tempfile = tempfile or getfile(name, "r+b")
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
        self.setdebug(self.debug_old)
        self.startup()
        self.fresh()
        self.evaltext(self.box.output())

    def check(self):
        """Checks The Module."""
        self.doshow = False
        self.run()
        self.doshow = True

    def destroy(self):
        """Ends The Editor."""
        if formatisyes(popup("Question", "Save First?", "Exit")):
            self.handle(lambda name: self.save(name, False))
        self.root.destroy()
