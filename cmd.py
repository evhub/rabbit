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

from .app import *
from .eval import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class mathbase(safebase):
    """A Base Class For PythonPlus Evaluators."""
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

    def __init__(self, name="PythonPlus Evaluator", message="Enter A Calculator Command:", height=None, helpstring=None, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.debug = bool(debug)
        self.messages = [str(message)]
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, self.messages[0], str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, self.messages[0], str(name), int(height))
        self.errorlog = {}
        self.ans = [matrix(0)]
        self.populator()
        if helpstring != None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def adderror(self, error, detail):
        """Adds An Error To The Log."""
        error = str(error)
        detail = str(detail)
        if self.debug:
            print(self.e.recursion*"  "+"<!> "+error+": "+detail)
        elif error not in self.errorlog:
            self.errorlog[error] = [detail]
        elif detail not in self.errorlog[error]:
            self.errorlog[error].append(detail)

    def show(self, arg, message=False):
        """Displays Something."""
        if not istext(arg):
            arg = self.e.prepare(arg, True, True)
        else:
            arg = str(arg)
        if message:
            self.messages.append(arg)
            self.app.display(self.messages[-1])
        elif arg == "()":
            self.adderror("NoneError", "Nothing to display")
        else:
            self.app.display(arg)

    def calc(self, expression):
        """Safely Evaluates An Expression."""
        self.e.info = "*"
        return self.saferun(self.e.calc, expression)

    def test(self, expression):
        """Safely Tests An Expression."""
        return self.saferun(self.e.test, expression)

    def printcall(self, variables):
        """Performs print."""
        self.returned = 1
        if variables == None or len(variables) == 0:
            out = self.e.prepare(matrix(0), True, False)
        else:
            out = ""
            for x in variables:
                out += self.e.prepare(x, True, False)+"\n"
            out = out[:-1]
        self.show(out)
        return strcalc(out, self.e)

    def anscall(self, variables):
        """Performs ans."""
        if variables == None or len(variables) == 0:
            return self.ans[-1]
        else:
            self.e.overflow = variables[1:]
            return self.ans[getint(variables[0])]

    def grabcall(self, variables):
        """Performs grab."""
        if variables == None or len(variables) == 0:
            out = self.app.get().split("\n")[-1]
            if out in self.messages:
                return strcalc(out, self.e)
            else:
                return strfloat(out, self.e)
        else:
            self.e.overflow = variables[1:]
            out = self.app.getlines()[getint(variables[0])]
            if out in self.messages:
                return strcalc(out, self.e)
            else:
                return strfloat(out, self.e)

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
            "print":funcfloat(self.printcall, self.e, "print"),
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab")
            }, self)

    def initialize(self, args=()):
        """Runs Any Files Fed To The Constructor."""
        if istext(args):
            self.evalfile(args)
        else:
            for x in args:
                self.initialize(x)

    def handler(self, event=None):
        """Handles A Return Event."""
        self.e.recursion = 0
        original = self.box.output()
        cmd = carefulsplit(original, "#")[0]
        if delspace(cmd) == "":
            self.process(self.box.commands[-2])
        else:
            self.box.add(original)
            self.process(cmd)

    def evalfile(self, name):
        """Runs A File."""
        try:
            tempfile = openfile(name, "rb")
        except IOError:
            return None
        else:
            self.evaltext(readfile(tempfile))
            tempfile.close()
            return True

    def evaltext(self, inputstring):
        """Runs Text."""
        cmdlist = inputstring.splitlines()
        x = 0
        while True:
            if x == len(cmdlist):
                break
            cmdlist[x] = carefulsplit(cmdlist[x], "#")[0]
            while x < len(cmdlist)-1 and (delspace(cmdlist[x+1]) == "" or cmdlist[x+1][0] in string.whitespace):
                cmdlist[x] += "\n"+cmdlist.pop(x+1)
            self.process(cmdlist[x])
            x += 1

    def process(self, inputstring):
        """Processes A Command."""
        if delspace(inputstring) != "":
            self.returned = 1
            inputstring = basicformat(inputstring)
            for func in self.pre_cmds:
                if func(inputstring) != None:
                    return True

    def do_find(self, item):
        """Unpacks A Variable."""
        if item in self.e.variables:
            if istext(self.e.variables[item]):
                self.process(self.e.find(item, False, False))
                return True

    def pre_question(self, inputstring):
        """Performs ?."""
        if superformat(inputstring).endswith("?"):
            self.box.clear()
            self.box.insert(inputstring[:-1])
            self.complete()
            return True

    def pre_help(self, inputstring):
        """Performs help."""
        if superformat(inputstring).startswith("help"):
            inputstring = inputstring[4:]
            if delspace(inputstring) == "":
                popup("Info", self.helpstring, "Help")
            else:
                self.show(self.findhelp(basicformat(inputstring)))
            return True

    def pre_cmd(self, inputstring):
        """Evaluates Commands."""
        for original in carefulsplit(inputstring, ">>"):
            if delspace(original) != "":
                original = basicformat(original)
                for func in self.cmds:
                    if func(original) != None:
                        break
        return True

    def cmd_debug(self, original):
        """Controls Debugging."""
        if superformat(original) == "debug":
            self.debug = not self.debug
            self.e.debug = self.debug
            return True

    def cmd_errors(self, original):
        """Performs errors."""
        if superformat(original) == "errors":
            self.showerrors()
            return True

    def cmd_clear(self, original):
        """Performs clear."""
        if superformat(original) == "clear":
            self.app.clear()
            return True

    def cmd_clean(self, original):
        """Removes Extra Parentheses."""
        if superformat(original) == "clean":
            todel = []
            for x in self.e.variables:
                if "`" in x:
                    todel.append(x)
            for x in todel:
                del self.e.variables[x]
            self.e.count = 0

    def cmd_while(self, original):
        """Performs while x do y."""
        if superformat(original).startswith("while "):
            original = original[6:]
            whilelist = original.split(" do ", 1)
            while self.test(whilelist[0]):
                self.process(whilelist[1])
            return True

    def cmd_for(self, original, varname="x"):
        """Performs for x do y."""
        if superformat(original).startswith("for "):
            original = original[4:]
            forlist = original.split(" do ", 1)
            forlist[0] = self.calc(forlist[0])
            if not isinstance(forlist[0], matrix):
                self.e.variables[varname] = forlist[0]
                self.process(forlist[1])
            else:
                for x in forlist[0].getitems():
                    self.e.variables[varname] = x
                    self.process(forlist[1])
            return True

    def cmd_if(self, inputstring):
        """Performs if x do y."""
        if superformat(inputstring).startswith("if "):
            inputstring = basicformat(inputstring[3:]).split(" do ", 1)
            if self.e.test(delspace(inputstring[0])):
                self.process(basicformat(inputstring[1]))
            return True

    def cmd_get(self, original):
        """Performs get."""
        if superformat(original).startswith("get"):
            original = original[3:]
            if delspace(original) == "":
                showbuiltins = []
                showfuncs = {}
                showvars = {}
                showparens = {}
                for x in self.e.variables:
                    if x.startswith("`"):
                        showparens[int(x[1:-1])] = self.e.prepare(self.e.variables[x], False, True)
                    elif isinstance(self.e.variables[x], strfunc):
                        showfuncs[x] = self.e.prepare(self.e.variables[x], False, True)
                    elif istext(self.e.variables[x]) or (hasnum(self.e.variables[x]) and not isinstance(self.e.variables[x], funcfloat)):
                        showvars[x] = self.e.prepare(self.e.variables[x], False, True)
                    else:
                        showbuiltins.append(x)
                showbuiltins.sort()
                popup("Info", "Built-Ins: "+str(showbuiltins)+"\n\nVariables: "+dictdisplay(showvars)+"\n\nFunctions: "+dictdisplay(showfuncs)+"\n\nParentheses: "+dictdisplay(showparens))
            else:
                self.show(self.e.prepare(self.e.variables[basicformat(original)], True, True))
            return True

    def cmd_run(self, original):
        """Performs run."""
        if superformat(original).startswith("run "):
            original = original[4:]
            if not self.evalfile(original):
                self.adderror("IOError", "Could not find file "+str(original))
            return True

    def cmd_save(self, original):
        """Performs save."""
        if superformat(original).startswith("save "):
            writefile(getfile(original[5:], "wb"), strlist(self.box.commands[:-2], "\n"))
            return True

    def cmd_do(self, original):
        """Evaluates Functions Silently."""
        if superformat(original).startswith("do "):
            test = self.calc(original[3:])
            if test != None and not isnull(test):
                self.ans.append(test)
            return True

    def cmd_show(self, original):
        """Shows A Popup."""
        if superformat(original).startswith("show "):
            popup("Info", self.e.prepare(self.calc(original[5:]), True, False), "Output")
            return True

    def cmd_del(self, original):
        """Deletes A Variable."""
        if superformat(original).startswith("del ") and original[4:] in self.e.variables:
            del self.e.variables[original[4:]]

    def cmd_set(self, original, varname="_"):
        """Evaluates Definition Commands."""
        if "=" in original:
            sides = original.split("=", 1)
            sides[0] = basicformat(sides[0])
            sides[1] = basicformat(sides[1])
            if sides[0].endswith(":"):
                sides[0] = sides[0][:-1]
                docalc = True
            elif sides[0][-1] in ["+", "*", "^", "%", "-", "/"]:
                sides[1] = sides[0]+"("+sides[1]+")"
                sides[0] = sides[0][:-1]
                docalc = True
            else:
                docalc = False
            if sides[0].endswith("<") and sides[1].startswith(">"):
                sides[0] = sides[0][:-1]
                sides[1] = sides[1][1:]
                if (delspace(sides[0]) in self.e.variables or not self.readytofunc(sides[0])) and not delspace(sides[1]) in self.e.variables and self.readytofunc(sides[1]):
                    sides.reverse()
            elif sides[1].startswith(">"):
                sides[1] = sides[1][1:]
                sides.reverse()
            elif sides[0].endswith("<"):
                sides[0] = sides[0][:-1]
            sides[0] = delspace(sides[0])
            if self.readytofunc(sides[0]):
                sides[1] = basicformat(sides[1])
                for func in self.set_cmds:
                    value = func(sides)
                    if value != None:
                        if istext(value):
                            check = 0
                        else:
                            try:
                                check = len(value)
                            except:
                                check = -1
                        if check >= 2:
                            if docalc:
                                value[1] = self.trycalc(value[1])
                            if self.debug:
                                print(self.e.recursion*"  "+": "+self.e.prepare(value[0], False, True, True)+" = "+self.e.prepare(value[1], False, True, True))
                            self.e.variables[value[0]] = value[1]
                        else:
                            if docalc:
                                value = self.trycalc(value)
                            if self.debug:
                                print(self.e.recursion*"  "+": "+self.e.prepare(sides[0], False, True, True)+" = "+self.e.prepare(value, False, True, True))
                            self.e.variables[sides[0]] = value
                        return True

    def readytofunc(self, expression, extra=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        funcparts = expression.split("(", 1)
        return funcparts[0] != "" and not self.e.isreserved(funcparts[0], extra) and (len(funcparts) == 1 or funcparts[1].endswith(")"))

    def set_import(self, sides):
        """Performs x = import."""
        if superformat(sides[1]).startswith("import ") and not self.e.isreserved(sides[0]):
            sides[1] = sides[1][7:]
            try:
                impclass = dirimport(sides[1]).interface
            except IOError:
                self.adderror("IOError", "Could not find for import file "+str(sides[1]))
            else:
                impclass.Hook = self
                try:
                    impclass.call
                except AttributeError:
                    try:
                        impclass.precall
                    except AttributeError:
                        try:
                            impclass.unicall
                        except AttributeError:
                            return impclass()
                        else:
                            return unifunc(impclass().unicall, self.e)
                    else:
                        return usefunc(impclass().precall, self.e)
                else:
                    return impclass()

    def set_def(self, sides):
        """Creates Functions."""
        if "(" in sides[0] and sides[0].endswith(")"):
            sides[0] = sides[0][:-1].split("(", 1)
            params = []
            personals = {}
            for x in sides[0][1].split(","):
                if ":" in x:
                    x = x.split(":", 1)
                    personals[x[0]] = self.e.find(x[1], True, False)
                elif x != "":
                    params.append(x)
            return (sides[0][0], strfunc(sides[1], self.e, params, personals))

    def set_normal(self, sides):
        """Performs =."""
        if not self.e.isreserved(sides[0]):
            return sides[1]

    def cmd_normal(self, original):
        """Evaluates Functions."""
        self.returned = 0
        test = self.calc(original)
        if test != None and not isnull(test):
            self.ans.append(test)
            if self.returned == 0:
                self.show(self.e.prepare(self.ans[-1], True, True))
        else:
            self.adderror("NoneError", "Nothing was returned")
        return True

    def trycalc(self, inputobject):
        """Attempts To Calculate A Variable."""
        if istext(inputobject):
            return self.calc(inputobject)
        else:
            return inputobject

    def call(self, item, value, varname="x"):
        """Evaluates An Item With A Value."""
        out = self.e.call(item, value, varname)
        if out == None:
            self.adderror("NoneError", "Nothing to call")
        return out

if __name__ == "__main__":
    mathbase().start()
