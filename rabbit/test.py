#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# WRAPPER made in 2012
# This program is a Python interpeter for testing purposes.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import absolute_import, print_function, unicode_literals
from .app import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class interpreter(base):
    """A Runnable Class That Runs The PythonPlus Interpreter Console."""
    def __init__(self, height=None):
        """Initializes The PythonPlus Interpreter Console."""
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, "Welcome to a Python interactive procesor.\nTo See The Help Enter: printhelp\nEnter A Command:")
        else:
            self.root, self.app, self.box = startconsole(self.handler, "Welcome to a Python interactive procesor.\nTo See The Help Enter: printhelp\nEnter A Command:", int(height))
        self.show = self.app.display
        self.codehelp = "0"
        self.safety = "1"
        self.log = "0"
        self.commands =["def ", "for ", "while ", "if ", "try", "import ", "from ", "class ", "global ", "except", "elif ", "else", "exec ", "eval ", "with ", "return ", "yield "]
        self.charlist = [":", "=", "#"]
        self.maxcommand = 1
        for testcommand in self.commands:
            commandlength = len(testcommand)
            if commandlength > self.maxcommand:
                self.maxcommand = commandlength
        self.maxcommand += 1

    def docmd(self, cmd):
        if formatisyes(self.log):
            self.show("> "+cmd)
        runcode(cmd, locals())

    def process(self, codestring):
        """Evaluates PythonPlus Console Input."""
        if codestring == "stop":
            self.codehelp = "0"
            self.show("Code Formatting Stopped. To Start It Again Enter: start")
        elif codestring == "printhelp":
            self.show("""Python Processor Help:
  To Get A List Of All Functions And Classes Enter: list
  To Use Automatic Code Formatting Enter: start
  To Toggle Error Handling Enter: safety
  To Toggle Command Logging Enter: log
  To Print To The Console Enter: print <arguments>
  To Execute A File Enter: run <file>
  To Format A File Enter: format <file>
  To Execute Safe Code Enter: compute <code>
  To Get Help On A Function Or Class Enter: help <name>
  To Clear The History Enter: clear""")
        elif codestring == "safety":
            if formatisyes(self.safety):
                self.safety = "0"
                self.show("Error Handling Disabled.")
            else:
                self.safety = "1"
                self.show("Error Handling Enabled.")
        elif codestring == "log":
            if formatisyes(self.log):
                self.log = "0"
                self.show("Command Logging Disabled.")
            else:
                self.log = "1"
                self.show("Command Logging Enabled.")
        elif codestring == "clear":
            self.app.clear()
            self.box.empty()
            self.show("History Cleared.")
        elif codestring == "list":
            self.show("All Functions And Classes:")
            for x in globals():
                if not x.startswith("_"):
                    self.show("  "+x)
        elif codestring.startswith("help "):
            stringname = codestring[5:]
            self.docmd("self.app.display(" + stringname + ".__doc__)")
        elif codestring.startswith("print "):
            stringname = codestring[6:]
            self.docmd("self.app.display(" + stringname + ")")
        elif codestring.startswith("run "):
            stringname = codestring[4:]
            execfile(stringname)
        elif codestring.startswith("format "):
            stringname = codestring[7:]
            openedfile = openfile(stringname, "r+b")
            writefile(openedfile, readfile(openedfile))
            openedfile.close()
        elif codestring.startswith("compute "):
            stringname = codestring[8:]
            compute("__builtins__(" + stringname + ")", self.app.display)
        else:
            if formatisyes(self.codehelp):
                doprint = 1
                for command in self.commands:
                    if codestring.startswith(command):
                        doprint = 0
                        break
                if doprint == 1:
                    for x in self.charlist:
                        if x in codestring:
                            doprint = 0
                            break
                if doprint == 1:
                    self.docmd("self.app.display(" + codestring + ")")
                else:
                    self.docmd(codestring)
            else:
                self.docmd(codestring)

    def handler(self, event):
        """Handles A Return Event."""
        original = self.box.output()
        if delspace(original) != "":
            self.box.add(original)
            if formatisyes(self.codehelp):
                codestring = basicformat(original)
            else:
                codestring = str(original)
            if formatisyes(self.safety):
                try:
                    self.process(codestring)
                except SyntaxError as detail:
                    self.show("Invalid Syntax: " + str(detail))
                except NameError as detail:
                    self.show("Invalid Naming: " + str(detail))
                except ValueError as detail:
                    self.show("Invalid Value: " + str(detail))
                except TypeError as detail:
                    self.show("Invalid Type: " + str(detail))
                except ImportError as detail:
                    self.show("Invalid Import: " + str(detail))
                except AttributeError as detail:
                    self.show("Invalid Attribute: " + str(detail))
                except IOError as detail:
                    self.show("Invalid File: " + str(detail))
                except OverflowError as detail:
                    self.show("Invalid Size: " + str(detail))
                except ZeroDivisionError as detail:
                    self.show("Division By Zero Is Not Allowed: " + str(detail))
                except:
                    self.show("Unknown Error.")
            else:
                self.process(codestring)

if __name__ == "__main__":
    interpreter().start()
