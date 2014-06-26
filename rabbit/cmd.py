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
from .app import *
from .eval import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class mathbase(safebase):
    """A Base Class For PythonPlus Evaluators."""
    helpstring = """Basic Commands:
    <command> [;; <command> ;; <command>...]
    <name> [:]= <expression>
Expressions:
    <item>, [<item>, <item>...]
    <function> [:](<variables>)[:(<variables>):(<variables>)...]
    <expression> [@<condition>[; <expression>@<condition>; <expression>@<condition>;... <expression>]]
    "string"
Console Commands:
    show <expression>
    help [string]
    errors
    clear
    clean
Control Commands:
    do <command>
    del <variable>
    get [variable]
Import Commands:
    <name> = import <file>
    run <file>
    save <file>"""

    def __init__(self, name="Evaluator", message="Enter A Rabbit Command:", height=None, helpstring=None, debug=False, *initializers):
        """Initializes A PythonPlus Evaluator"""
        self.debug = bool(debug)
        self.printdebug(": ON")
        self.messages = []
        if message:
            message = str(message)
            self.messages.append(message)
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, message, str(name), int(height))
        self.errorlog = {}
        self.ans = [matrix(0)]
        self.returned = 1
        self.populator()
        if helpstring != None:
            self.helpstring = str(helpstring)
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def setdebug(self, state):
        """Sets The Debugging State."""
        self.e.debug = True
        if self.debug:
            self.e.printdebug(": OFF")
        else:
            self.e.printdebug(": ON")
        self.debug = bool(state)
        self.e.debug = self.debug

    def printdebug(self, message):
        """Prints Debug Output."""
        if self.debug:
            self.e.printdebug(str(message))

    def adderror(self, error, detail):
        """Adds An Error To The Log."""
        error = str(error)
        detail = str(detail)
        if self.debug:
            self.printdebug("<!> "+error+": "+detail)
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
            self.app.display(arg)
            for line in arg.split("\n"):
                self.messages.append(line)
        elif arg == "()":
            self.adderror("NoneError", "Nothing to display")
        else:
            self.app.display(arg)

    def calc(self, expression):
        """Safely Evaluates An Expression."""
        self.e.info = 1
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
        return matrix(0)

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
            self.pre_help,
            self.pre_cmd
            ]
        self.cmds = [
            self.do_find,
            self.cmd_debug,
            self.cmd_errors,
            self.cmd_clear,
            self.cmd_clean,
            self.cmd_get,
            self.cmd_run,
            self.cmd_save,
            self.cmd_assert,
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
            "ans":funcfloat(self.anscall, self.e, "ans"),
            "grab":funcfloat(self.grabcall, self.e, "grab")
            })

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
        cmd = carefulsplit(original, "#", '"`')[0]
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
            cmdlist[x] = carefulsplit(cmdlist[x], "#", '"`')[0]
            while x < len(cmdlist)-1 and (delspace(cmdlist[x+1]) == "" or iswhite(cmdlist[x+1][0])):
                cmdlist[x] += "\n"+carefulsplit(cmdlist.pop(x+1), "#", '"`')[0]
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
                self.show(self.helpstring, True)
            else:
                self.show(self.findhelp(basicformat(inputstring)))
            return True

    def pre_cmd(self, inputstring):
        """Evaluates Commands."""
        for original in carefulsplit(inputstring, ";;", '"`', "{", "}"):
            if delspace(original) != "":
                original = basicformat(original)
                for func in self.cmds:
                    if func(original) != None:
                        break
        return True

    def cmd_debug(self, original):
        """Controls Debugging."""
        if superformat(original) == "debug":
            self.setdebug(not self.debug)
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
                if self.e.parenchar in x:
                    todel.append(x)
            for x in todel:
                del self.e.variables[x]
                self.printdebug("< "+x+" >")
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
            if not hasmatrix(forlist[0]):
                self.e.variables[varname] = forlist[0]
                self.process(forlist[1])
            else:
                for x in getmatrix(forlist[0]).getitems():
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
        if superformat(original).startswith("get ") or superformat(original) == "get":
            original = basicformat(original[3:])
            if delspace(original) == "":
                showbuiltins = []
                showfuncs = {}
                showvars = {}
                showparens = {}
                for x in self.e.variables:
                    if x.startswith(self.e.parenchar):
                        showparens[int(x[1:-1])] = self.e.prepare(self.e.variables[x], False, True)
                    elif isinstance(self.e.variables[x], strfunc):
                        showfuncs[x] = self.e.prepare(self.e.variables[x], False, True)
                    elif istext(self.e.variables[x]) or (hasnum(self.e.variables[x]) and not isinstance(self.e.variables[x], funcfloat)):
                        showvars[x] = self.e.prepare(self.e.variables[x], False, True)
                    else:
                        showbuiltins.append(x)
                showbuiltins.sort()
                self.show("Built-Ins: "+str(showbuiltins)+"\n\nVariables: "+dictdisplay(showvars)+"\n\nFunctions: "+dictdisplay(showfuncs)+"\n\nParentheses: "+dictdisplay(showparens), True)
            elif original in self.e.variables:
                self.show(self.e.prepare(self.e.variables[original], True, True))
            else:
                self.adderror("VariableError", "Could not get variable "+original)
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

    def cmd_assert(self, original):
        """Checks For Errors By Asserting That Something Is True."""
        if superformat(original).startswith("assert "):
            original = original[7:]
            if not self.e.test(original):
                raise AssertionError("Assertion failed that "+original)
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
        if superformat(original).startswith("del "):
            original = original[4:]
            if original in self.e.variables:
                del self.e.variables[original]
            elif "." in original:
                test = original.split(".")
                item = test.pop()
                useclass = self.e.find(test[0], True, False)
                if isinstance(useclass, classcalc):
                    last = useclass
                    for x in xrange(1, len(test)):
                        useclass = useclass.retrieve(test[x])
                        if not isinstance(useclass, classcalc):
                            self.adderror("ClassError", "Could not delete "+test[x]+" in "+self.e.prepare(last, False, True, True))
                            return True
                else:
                    self.adderror("VariableError", "Could not find class "+test[0])
                    return True
                useclass.remove(item)
            else:
                self.adderror("VariableError", "Could not find "+original)
                return True
            self.printdebug("< "+original+" >")
            return True

    def cmd_set(self, original):
        """Evaluates Definition Commands."""
        if "=" in original:
            sides = original.split("=", 1)
            sides[0] = basicformat(sides[0])
            sides[1] = basicformat(sides[1])
            docalc = False
            if sides[0].endswith(":"):
                sides[0] = sides[0][:-1]
                docalc = True
            test = endswithany(sides[0], ["+", "**", "*", "^", "%", "-", "/", ":", "&", "|", "@", "..", ";", ",", "(", ".", "$"])
            if test:
                sides[0] = sides[0][:-1*len(test)]
                sides[1] = "("+sides[0]+")"+test+"("+sides[1]+")"
                docalc = True
            sides[0] = carefulsplit(sides[0], ",", '"`', openstr="(", closestr=")")
            if len(sides[0]) > 1:
                test = True
                for x in sides[0]:
                    test = test and self.readytofunc(x)
                if test:
                    sides[1] = self.calc(sides[1])
                    func = diagmatrixlist
                    if isinstance(sides[1], matrix):
                        if sides[1].onlydiag():
                            sides[1] = sides[1].getitems()
                        else:
                            sides[1] = sides[1].items()
                            func = rowmatrixlist
                    elif isinstance(sides[1], strcalc):
                        sides[1] = sides[1].tomatrix().getitems()
                        func = None
                    else:
                        sides[1] = [sides[1]]
                    out = False
                    for x in xrange(0, len(sides[0])):
                        if x == len(sides[0])-1:
                            toset = sides[1][x:]
                        else:
                            toset = sides[1][x:x+1]
                        if len(toset) == 0:
                            toset = matrix(0)
                        elif len(toset) == 1:
                            toset = toset[0]
                        elif func != None:
                            toset = func(toset)
                        else:
                            itemlist = toset
                            toset = itemlist.pop(0)
                            for item in itemlist:
                                toset += item
                        out = self.cmd_set_do([sides[0][x], self.e.wrap(toset)], docalc) or out
                    return out
            else:
                sides[0] = sides[0][0]
                return self.cmd_set_do(sides, docalc)
                
    def cmd_set_do(self, sides, docalc):
        """Performs The Definition Command."""
        sides[0] = sides[0].split("(", 1)
        if len(sides[0]) > 1:
            sides[0] = delspace(sides[0][0])+"("+sides[0][1]
        else:
            sides[0] = delspace(sides[0][0])
        if self.readytofunc(sides[0], allowed="."):
            useclass = None
            classlist = []
            if "." in sides[0]:
                classlist += sides[0].split(".")
                for x in xrange(0, len(classlist)-1):
                    if self.e.isreserved(classlist[x]):
                        return False
                sides[0] = classlist.pop()
                useclass = self.e.find(classlist[0], True, False)
                if isinstance(useclass, classcalc):
                    for x in xrange(1, len(classlist)):
                        last = useclass
                        useclass = useclass.retrieve(classlist[x])
                        if not isinstance(useclass, classcalc):
                            if istext(useclass) and len(classlist) == x+1:
                                sides[1] = "( "+useclass+" )"+" + { "+sides[0]+" :"*docalc+" "*(not docalc)+"= "+sides[1]+" }"
                                sides[0] = classlist[x]
                                useclass = last
                                classlist = classlist[:x]
                                docalc = False
                                break
                            else:
                                self.adderror("ClassError", "Could not set "+classlist[x]+" in "+self.e.prepare(last, False, True, True))
                                return True
                elif classlist[0] in self.e.variables and istext(self.e.variables[classlist[0]]) and len(classlist) == 1:
                    sides[1] = "( "+self.e.variables[classlist[0]]+" )"+" + { "+sides[0]+" :"*docalc+" "*(not docalc)+"= "+sides[1]+" }"
                    sides[0] = classlist[0]
                    useclass = None
                    classlist = []
                    docalc = False
                else:
                    self.adderror("VariableError", "Could not find class "+classlist[0])
                    return True
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
                        self.printdebug(": "+strlist(classlist, ".")+"."*bool(classlist)+value[0]+" = "+self.e.prepare(value[1], False, True, True))
                        if useclass == None:
                            self.e.variables[value[0]] = value[1]
                        else:
                            useclass.store(value[0], value[1])
                    else:
                        if docalc:
                            value = self.trycalc(value)
                        self.printdebug(": "+strlist(classlist, ".")+"."*bool(classlist)+sides[0]+" = "+self.e.prepare(value, False, True, True))
                        if useclass == None:
                            self.e.variables[sides[0]] = value
                        else:
                            useclass.store(sides[0], value)
                    return True

    def readytofunc(self, expression, extra="", allowed=""):
        """Determines If An Expression Could Be Turned Into A Function."""
        top = True
        funcparts = expression.split("(", 1)
        if len(funcparts) == 1 and self.e.parenchar in funcparts[0]:
            funcparts = funcparts[0].split(self.e.parenchar, 1)
            top = False
        return funcparts[0] != "" and not self.e.isreserved(funcparts[0], extra, allowed) and (len(funcparts) == 1 or funcparts[1].endswith(")"*top or self.e.parenchar))

    def set_import(self, sides):
        """Performs x = import."""
        if superformat(sides[1]).startswith("import ") and not self.e.isreserved(sides[0]):
            sides[1] = sides[1][7:]
            try:
                impclass = dirimport(sides[1]).interface
            except IOError:
                self.adderror("IOError", "Could not find for import file "+str(sides[1]))
            else:
                if iseval(impclass):
                    return impclass(self)
                elif hascall(impclass):
                    return funcfloat(impclass(self).call, self.e, sides[0])
                else:
                    try:
                        impclass.precall
                    except AttributeError:
                        try:
                            impclass.unicall
                        except AttributeError:
                            return impclass(self)
                        else:
                            return unifunc(impclass(self).unicall, self.e, sides[0])
                    else:
                        return usefunc(impclass(self).precall, self.e, sides[0])

    def set_def(self, sides):
        """Creates Functions."""
        top = None
        if "(" in sides[0] and sides[0].endswith(")"):
            top = True
        elif self.e.parenchar in sides[0] and sides[0].endswith(self.e.parenchar):
            top = False
        if top != None:
            if top:
                sides[0] = sides[0][:-1].split("(", 1)
            else:
                sides[0] = sides[0].split(self.e.parenchar, 1)
                sides[0][1] = self.e.namefind(self.e.parenchar+sides[0][1])
            params = []
            personals = {}
            allargs = None
            for x in sides[0][1].split(","):
                if x:
                    doparam = True
                    if x.startswith("*"):
                        x = x[1:]
                        doallargs = True
                    else:
                        doallargs = False
                    if ":" in x:
                        if x.startswith("+"):
                            x = x[1:]
                            doparam = True
                        elif not doallargs:
                            doparam = False
                        x = x.split(":", 1)
                        x[0] = delspace(x[0])
                        if not x[0] or self.e.isreserved(x[0]):
                            self.adderror("VariableError", "Could not set to invalid personal "+x[0])
                            doparam = False
                        else:
                            self.e.info = " <\\"
                            personals[x[0]] = self.e.calc(x[1])
                        x = x[0]
                    else:
                        x = delspace(x)
                    if doallargs:
                        if not x or self.e.isreserved(x):
                            self.adderror("VariableError", "Could not set to invalid allargs "+x)
                            doparam = False
                        else:
                            allargs = x
                    if doparam:
                        if not x or self.e.isreserved(x):
                            self.adderror("VariableError", "Could not set to invalid variable "+x)
                        else:
                            params.append(x)
            if allargs:
                return (sides[0][0], strfunc(sides[1], self.e, params, personals, allargs=allargs))
            else:
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
