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

from .list import *
import string
import re

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def basicformat(inputstring, leading=True, tailing=True):
    """Performs Basic Formatting On A String."""
    out = str(inputstring).replace("\t", "    ")
    if leading:
        out = out.lstrip()
    if tailing:
        out = out.rstrip()
    return out

def superformat(inputstring):
    """Performs Advanced Formatting On A String."""
    return basicformat(inputstring).lower()

class lists(object):
    """A Container Class Used For Globals."""
    yes = ["yes", "y", "1", "1.0", "true", "t", "on"]
    no = ["no", "n", "0", "0.0", "false", "f", "off"]
    def __init__(self):
        """Initializes The Containers."""
        self.default()
    def default(self):
        """Sets The Container To Its Defaults."""
        self.yes = lists.yes
        self.no = lists.no
    def addyes(self, item):
        """Adds An Item To The List Of Things Considered To Affirm."""
        self.yes.append(item)
    def addno(self, item):
        """Adds An Item To The List Of Things Considered To Negate."""
        self.no.append(item)
    def delyes(self, item):
        """Removes An Item From The List Of Things Considered To Affirm."""
        self.yes.remove(item)
    def delno(self, item):
        """Removes An Item From The List Of Things Considered To Negate."""
        self.no.remove(item)       
    def clear(self):
        """Empties The Containers."""
        self.yes = []
        self.no = []

def isyes(inputstring, info=lists):
    """Determines If A String Is Affirming."""
    inputstring = basicformat(inputstring)
    if inputstring.endswith("."):
        inputstring = inputstring[:-1]
    if inputstring in info.yes:
        return True
    else:
        return False

def isno(inputstring, info=lists):
    """Determines If A String Is Negating."""
    inputstring = basicformat(inputstring)
    if inputstring.endswith("."):
        inputstring = inputstring[:-1]
    if inputstring in info.no:
        return True
    else:
        return False

def formatisyes(inputstring, info=None):
    """Determines If A String, When Formatted, Is Affirming."""
    if info is None:
        return isyes(superformat(inputstring))
    else:
        return isyes(superformat(inputstring), info)

def formatisno(inputstring, info=None):
    """Determines If A String, When Formatted, Is Negating."""
    if info is None:
        return isno(superformat(inputstring))
    else:
        return isno(superformat(inputstring), info)

def startswithany(inputstring, inputlist):
    """Determines If A String Starts With Any Of A Set Of Items."""
    for x in inputlist:
        if inputstring.startswith(x):
            return x
    return False

def endswithany(inputstring, inputlist):
    """Determines If A String Ends With Any Of A Set Of Items."""
    for x in inputlist:
        if inputstring.endswith(x):
            return x
    return False

def madeof(inputstring, findstr):
    """Determines If A String Is Made Of Another String."""
    for x in inputstring:
        if not x in findstr:
            return False
    return True

def table(freqs, delimiter=",", seperator=" | "):
    """Creates A Distribution Table."""
    delimiter = str(delimiter)
    seperator = str(seperator)
    out = ""
    items = freqs.keys()
    items.sort()
    for x in items:
        out += str(x)+seperator
        if islist(freqs[x]):
            out += strlist(freqs[x], delimiter)
        else:
            out += str(freqs[x])
        out += "\n"
    return out[:-1]

def sanitize(inputstring):
    """Insures A String Is Printable."""
    outputstring = ""
    for x in inputstring:
        if x in string.printable:
            outputstring += x
    return old_str(outputstring)

def listformat(inputlist):
    """Performs Basic Formatting On A List."""
    newlist = []
    for y in inputlist:
        newlist.append(basicformat(y))
    return newlist

def listsuperformat(inputlist):
    """Performs Advanced Formatting On A List."""
    newlist = []
    for y in inputlist:
        newlist.append(superformat(y))
    return newlist

def delspace(inputstring, wipestring=None):
    """Removes All Whitespace From A String."""
    if wipestring:
        wipestring = str(wipestring)
    else:
        regex = re.compile("\s")
    out = ""
    for x in str(inputstring):
        if wipestring:
            if not x in wipestring:
                out += x
        else:
            if not regex.match(x):
                out += x
    return out

def iswhite(inputstring):
    """Determines Whether A String Is Made Of Whitespace."""
    return re.compile("\s+").match(str(inputstring))

def leading(inputstring, check=iswhite, func=True):
    """Counts Leading Special Characters."""
    count = 0
    for x in inputstring:
        if func:
            if check(x):
                count += 1
            else:
                break
        else:
            if check == x:
                count += 1
            else:
                break
    return count

def repeating(inputstring):
    """Generates A Repeating Representation Of A String."""
    opts = [(inputstring,"")]
    for x in xrange(1, len(inputstring)/2+1):
        test = inputstring[-x:]
        left = inputstring[:-x]
        for i in xrange(1, len(inputstring)/x):
            if left[-x:] == test:
                left = left[:-x]
            else:
                break
        if len(left) < len(inputstring)-x:
            opts.append((left,test))
    for x in xrange(0, len(opts)):
        start,rep = opts[x]
        while len(rep) > 0 and len(start) > 0 and start[-1] == rep[-1]:
            rep = start[-1]+rep[:-1]
            start = start[:-1]
        opts[x] = start,rep
    opts.sort()
    return opts[0]

def strlist(inputlist, delimeter=" ", converter=str):
    """Formats A List Into A String."""
    out = []
    for x in inputlist:
        out.append(converter(x))
    return str(delimeter).join(out)

def strdict(inputdict, seperator=":", delimeter=" ", termconverter=str, keyconverter=str):
    """Formats A Dictionary Into A String."""
    outstring = ""
    for x in inputdict:
        outstring += keyconverter(x) + seperator + termconverter(inputdict[x]) + delimeter
    return outstring[:-1]

def dictdisplay(inputdict):
    """Displays A Sorted And Processed Dictionary."""
    inputlist = inputdict.keys()
    inputlist.sort()
    out = ""
    for x in inputlist:
        out += repr(x).replace("\\\\", "\\") + ": " + repr(inputdict[x]).replace("\\\\", "\\") + ", "
    return "{"+out[:-2]+"}"

def dictstr(inputstring, keyconverter=None, termconverter=None, seperator=":", delimeter=" "):
    """Formats A String Into A Dictionary."""
    outlist = inputstring.split(delimeter)
    outdict = {}
    for x in outlist:
        templist = x.split(seperator)
        if keyconverter is not None:
            templist[0] = keyconverter(templist[0])
        if termconverter is not None:
            templist[1] = termconverter(templist[1])
        outdict[templist[0]] = templist[1]
    return outdict

def reassemble(inputlist, seperators):
    """Reassembles A List Of Lists."""
    if not islist(inputlist):
        return str(inputlist)
    elif len(seperators) == 0:
        return strlist(inputlist, "")
    else:
        return strlist(inputlist, seperators[0], lambda x: reassemble(x, seperators[1:]))

def splitany(inputstring, inputlist):
    """Splits A String By Any Of The Items In A List."""
    if len(inputlist) == 0:
        return [inputstring]
    else:
        out = inputstring.split(inputlist[0])
        for x in xrange(1, len(inputlist)):
            new = []
            for item in out:
                new += item.split(inputlist[x])
            out = new
        return out

def fullsplit(expression, openstr="(", closestr=")", maxlevel=float("inf")):
    """Splits A List By An Open And A Close."""
    outlist = [""]
    feed = outlist
    directory = [feed]
    level = 0
    for x in expression:
        if x == openstr:
            if -level < maxlevel:
                feed.append([""])
                feed = feed[len(feed)-1]
                directory.append(feed)
            else:
                feed[len(feed)-1] += openstr
            level -= 1
        elif x == closestr:
            if -(1+level) < maxlevel:
                if len(directory) <= 1:
                    raise ExecutionError("SyntaxError", "Unmatched close token "+str(closestr))
                else:
                    directory.pop()
                    feed = directory[-1]
                    feed.append("")
            else:
                feed[len(feed)-1] += closestr
            level += 1
        else:
            feed[len(feed)-1] += x
    if len(directory) > 1:
        raise ExecutionError("SyntaxError", "Unmatched open token "+str(openstr))
    return clean(outlist)

def splitinplace(inputlist, findstr, reserved="", domod=None):
    """Splits A List In-Place By A String."""
    outlist = []
    for x in inputlist:
        test = x.split(findstr)
        i = 0
        while i < len(test):
            if i > 0 and haskey(test, i-1):
                last = test[i-1][-1]
            else:
                last = ""
            if last and last in reserved:
                new = test.pop(i)
                test[i-1] = test[i-1]+findstr+new
            elif test[i] == "":
                test.pop(i)
                if i < len(test):
                    test[i] = findstr+test[i]
            else:
                if madeof(test[i], findstr):
                    temp = len(test[i])
                    test.pop(i)
                    if i < len(test):
                        temp += 1
                        if domod is not None:
                            temp %= domod
                        test[i] = temp*findstr+test[i]
                else:
                    i += 1
        for i in xrange(0, len(test)):
            if i == 0:
                outlist.append(test[i])
            else:
                outlist.append(findstr+test[i])
    return outlist

def carefulsplit(inputstring, splitstring, holdstrings='"', closers={}):
    """Splits A String By Something Not Inside Something Else."""
    out = [""]
    hold = False
    check = 0
    for x in inputstring:
        if not hold and x == splitstring[check]:
            check += 1
            if check == len(splitstring):
                out.append("")
                check = 0
        else:
            if check > 0:
                out[-1] += splitstring[:check]
                check = 0
            if hold:
                if x == hold:
                    hold = not hold
            else:
                if x in closers:
                    hold = closers[x]
                if x in holdstrings:
                    hold = x
            out[-1] += x
    out[-1] += splitstring[:check]
    return out

def switchsplit(inputstring, splitstring, otherstring=None):
    """Splits A String By Whenever It Switches From Being In Something To Not In It."""
    out = [""]
    old = -1
    for x in inputstring:
        if x in splitstring:
            new = 1
        elif not x in splitstring and (not otherstring or x in otherstring):
            new = 0
        else:
            new = -1
        if old > -1 and new > -1 and old != new:
            out.append("")
        out[-1] += x
        old = new
    return out

def eithersplit(inputstring, holdstrings, closers={}):
    """Splists A String By Any Of The Hold Strings."""
    out = [""]
    inside = False
    for x in inputstring:
        if inside:
            if x == out[-1][0]:
                out.append("")
                inside = False
            else:
                out[-1][1] += x
        else:
            if x in closers:
                out.append([closers[x], ""])
                inside = True
            elif x in holdstrings:
                out.append([x, ""])
                inside = True
            elif x in closers.values():
                raise ExecutionError("SyntaxError", "Misplaced token "+x)
            else:
                out[-1] += x
    if inside:
        raise ExecutionError("SyntaxError", "Unmatched token "+out[-1][0])
    return out
