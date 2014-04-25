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

from .gui import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class base(object):
    """Base Class For A PythonPlus Application"""
    returned = 0

    def __init__(self, name="PythonPlus Application", message="Welcome!", height=None, *initializers):
        """Initializes A PythonPlus Application"""
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name), int(height))
        self.show = self.app.display
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def initialize(self, *args):
        """Runs Any Initializers Fed To The Constructor."""
        for x in args:
            x()

    def register(self, function, delay=0):
        """Registers A Function To The Main Loop."""
        return self.root.after(int(delay), function)

    def handler(self, event=None):
        """Handles A Return Event."""
        self.returned = 1

    def get(self):
        """Pauses Code Until Data Entry And Returns The Data."""
        while self.returned == 0:
            self.root.update()
        self.returned = 0
        return self.box.output()

    def start(self):
        """Starts The Main Loop."""
        self.root.mainloop()

    def window(self):
        """Returns A New Window Root Object."""
        return Tkinter.Toplevel()

class safebase(base):
    """Base Class For An Error-Handling Application."""
    helpstring = "<Return>"

    def __init__(self, name="PythonPlus Application", message="Welcome!", height=None, helpstring=None, debug=False, *initializers):
        """Initializes A Safe PythonPlus Application"""
        self.debug = bool(debug)
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name), int(height))
        self.returned = 0
        self.show = self.app.display
        self.errorlog = {}
        if helpstring != None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def saferun(self, function, *args):
        """Safely Runs A Function."""
        if self.debug:
            return function(*args)
        else:
            try:
                result = function(*args)
            except ZeroDivisionError as detail:
                self.adderror("ZeroDivisionError", detail)
            except ValueError as detail:
                self.adderror("ValueError", detail)
            except OverflowError as detail:
                self.adderror("OverflowError", detail)
            except TypeError as detail:
                self.adderror("TypeError", detail)
            except KeyError as detail:
                self.adderror("KeyError", detail)
            except AttributeError as detail:
                self.adderror("AttributeError", detail)
            except IndexError as detail:
                self.adderror("IndexError", detail)
            except RuntimeError as detail:
                self.adderror("RuntimeError", detail)
            else:
                return result

    def adderror(self, error, detail):
        """Adds An Error To The Log."""
        error = str(error)
        detail = str(detail)
        if error not in self.errorlog:
            self.errorlog[error] = [detail]
        elif detail not in self.errorlog[error]:
            self.errorlog[error].append(detail)

    def findhelp(self, inputstring):
        """Finds A Command."""
        for x in self.helpstring.splitlines():
            if x.startswith("    "):
                x = basicformat(x)
                if inputstring.startswith(x.split(" ")[0]):
                    return x
        return "help"

    def complete(self):
        """Completes A Command Using The Helpstring."""
        self.box.insert(self.findhelp(self.box.output()))

    def showerrors(self):
        """Shows Logged Errors."""
        errorstring = ""
        for x in self.errorlog:
            errorstring += x+": "+strlist(self.errorlog[x], "; ")+"\n"
        if errorstring == "":
            popup("Info", "No Errors.", "Error Log")
        else:
            popup("Info", errorstring[:-1], "Error Log")
        self.errorlog = {}
