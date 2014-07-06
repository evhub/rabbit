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

from __future__ import absolute_import, print_function, unicode_literals
from .cli import *
import cPickle

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class compiler(commandline):
    """The Rabbit Semi-Compiler."""
    debug = False
    doshow = False
    compiling = False

    def __init__(self, debugcolor="lightred", prompt=addcolor("Rabbit:", "pink")+" ", nprompt=addcolor(">>>", "pink")+" ", outcolor="cyan", *initializers):
        """Initializes The Command Line Interface."""
        self.app = terminal()
        self.populator()
        self.e.color = debugcolor
        self.prompt = str(prompt)
        self.nprompt = str(nprompt)
        self.color = outcolor
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def fresh(self):
        """Refreshes The Environment."""
        self.e.fresh()
        self.e.makevars({
            "print":funcfloat(self.printcall, self.e, "print")
            })
        self.commands = []
        self.makes = []

    def show(self, arg, message=None):
        """Prints A Message To The Console."""
        self.app.display(self.e.forshow(arg))

    def start(self):
        """Runs An Interactive Semi-Compiler Command Line Interface."""
        while self.on:
            cmd = superformat(raw_input(self.prompt))
            if cmd in ["h", "help"]:
                self.app.display(addcolor("Valid commands: help (h), interpret (i), compile (c), decompile (d), interactive (n), exit (x)", self.color))
            elif cmd in ["i", "interpret"]:
                self.interp()
            elif cmd in ["c", "compile"]:
                self.comp()
            elif cmd in ["d", "decompile"]:
                self.run()
            elif cmd in ["n", "interactive"]:
                cmd = raw_input(self.nprompt)
                while superformat(cmd) != "exit":
                    self.handler(cmd)
                    cmd = raw_input(self.nprompt)
            elif cmd in ["x", "exit"]:
                self.on = False
            else:
                self.app.display(addcolor("That isn't a valid command. Try 'help' for a list of valid commands.", self.color))

    def interp(self):
        """Runs The Interpreter On A Source File."""
        name = raw_input(self.prompt+addcolor("Evaluate Source File:", self.color)+" ")
        if not self.evalfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def comp(self):
        """Runs The Compiler On A Source File."""
        name = raw_input(self.prompt+addcolor("Compile Source File:", self.color)+" ")
        if not self.compfile(name, name+".rabbit"):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def run(self):
        """Runs The Decompiler On A Compiled File."""
        name = raw_input(self.prompt+addcolor("Execute Compiled File:", self.color)+" ")
        if not self.decompfile(name):
            self.app.display(addcolor("<!> IOError: Rabbit could not open file "+name, self.e.color))

    def decompfile(self, name):
        """Decompiles A File."""
        try:
            tempfile = openfile(name, "rb")
        except IOError:
            return False
        else:
            self.decomptext(readfile(tempfile))
            tempfile.close()
            return True

    def decomptext(self, inputstring):
        """Decompiles Text."""
        compiling = self.compiling
        self.compiling = False
        commands, variables = self.disassemble(inputstring)
        self.e.makevars(variables)
        for command in commands:
            self.calc(command)
        self.compiling = compiling
        return True

    def compfile(self, name, result):
        """Compiles A File."""
        compiling = self.compiling
        self.compiling = True
        self.evalfile(name)
        self.compiling = compiling
        resultfile = openfile(result, "wb")
        writefile(resultfile, self.assemble())
        resultfile.close()
        return True

    def comptext(self, inputstring):
        """Compiles Text."""
        compiling = self.compiling
        self.compiling = True
        self.evaltext(inputstring)
        self.compiling = compiling
        return self.assemble()

    def populator(self):
        """Creates An Evaluator And Lists Of Commands."""
        self.pre_cmds = [
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_clean,
            self.cmd_run,
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
        self.e = evaluator(processor=self, speedy=True)
        self.fresh()

    def pre_cmd(self, inputstring):
        """Evaluates Commands."""
        for original in carefulsplit(inputstring, ";;", '"`', {"{":"}", "\u201c":"\u201d"}):
            if delspace(original) != "":
                original = basicformat(original)
                for func in self.cmds:
                    if func(original) != None:
                        name = namestr(func).split("_")[-1]
                        if self.compiling and self.top:
                            if name == "make":
                                self.makes.append(original)
                            elif not name in ["assert", "run", "set", "def"]:
                                self.commands.append(original)
                        self.printdebug(":| "+name)
                        break

    def cmd_do(self, original):
        """Evaluates Functions Silently."""
        if superformat(original).startswith("do "):
            original = original[3:]
            self.calc(original)
            return True

    def cmd_normal(self, original):
        """Evaluates Functions."""
        self.returned = 0
        test = self.calc(original)
        if test != None:
            return True

    def getstates(self, variables):
        """Compiles Variables."""
        out = {}
        for k,v in variables.items():
            try:
                v.getstate
            except AttributeError:
                value = v
            else:
                value = v.getstate()
            out[k] = value
        return out

    def assemble(self, protocol=-1):
        """Compiles Code."""
        out = cPickle.dumps({
            "commands": self.commands,
            "makes": self.makes,
            "variables": self.getstates(self.e.variables)
            }, protocol=int(protocol))
        self.fresh()
        return out

    def deitem(self, item):
        """Decompiles An Item."""
        if isinstance(item, tuple):
            name = str(item[0])
            args = item[1:]
            if name == "reciprocal":
                value = reciprocal(self.deitem(args[0]))
            elif name == "fraction":
                value = fraction(self.deitem(args[0]), self.deitem(args[1]))
            elif name == "data":
                value = data(args[0], args[1])
            elif name == "multidata":
                value = multidata(args[0], args[1])
            elif name == "rollfunc":
                value = rollfunc(args[0], self.e, args[1], args[2], args[3])
            elif name == "matrix":
                value = matrix(args[1], args[2], converter=args[3], fake=args[4])
                for y in xrange(0, len(args[0])):
                    for x in xrange(0, len(args[0][y])):
                        value.store(y,x, self.deitem(args[0][y][x]))
            elif name == "strfunc":
                value = strfunc(args[0], self.e, args[1], self.devariables(args[2]), args[3], args[4], args[5])
            elif name == "strcalc":
                value = strcalc(args[0], self.e)
            elif name == "derivfunc":
                value = derivfunc(args[0], args[1], args[2], args[3], self.e, args[4], args[5], args[6])
            elif name == "integfunc":
                value = integfunc(args[0], args[1], self.e, args[2], args[3], args[4])
            elif name == "usefunc":
                value = usefunc(args[0], self.e, args[1], args[2], args[3], args[4], args[5])
            elif name == "classcalc":
                value = classcalc(self.e, self.devariables(args[0]))
            elif name == "instancecalc":
                value = instancecalc(self.e, self.devariables(args[0]), self.devariables(args[1]))
            elif name == "find":
                tofind = str(args[0])
                if tofind in self.e.variables:
                    value = self.e.variables[tofind]
                else:
                    raise ExecutionError("UnpicklingError", "Rabbit could not find "+tofind)
            else:
                raise ExecutionError("UnpicklingError", "Rabbit could not unpickle "+name)
        else:
            value = item
        return value

    def devariables(self, variables):
        """Decompiles Variables."""
        out = {}
        for k,v in variables.items():
            out[k] = self.deitem(v)
        return out

    def disassemble(self, inputstring):
        """Decompiles Code."""
        out = cPickle.loads(inputstring)
        for command in out["makes"]:
            self.calc(command)
        return out["commands"], self.devariables(out["variables"])

    def test(self):
        """Determines Whether Or Not Compilation Is Working Properly."""
        print("Compiling...")
        newvars = self.disassemble(self.assemble())[1]
        print("Compiled.\nTesting Compilation...")
        for k,v in self.e.variables.items():
            nv = haskey(newvars, k)
            if v != nv:
                print("<!> For variable "+str(k)+" the old value of "+repr(v)+" is not equal to the new value "+repr(nv))
        for k,v in newvars.items():
            ov = haskey(self.e.variables, k)
            if v != ov:
                print("<!> For variable "+str(k)+" the new value of "+repr(v)+" is not equal to the old value "+repr(ov))
        return self.e.variables == newvars
