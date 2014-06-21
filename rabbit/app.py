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

from .web import *
from .gui import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class base(object):
    """Base Class For A PythonPlus Application."""
    returned = 0

    def __init__(self, name="PythonPlus Application", message="Welcome!", height=None, debug=False, *initializers):
        """Initializes A PythonPlus Application."""
        self.debug = bool(debug)
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name), int(height))
        self.show = self.app.display
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def printdebug(self, *args, **kwargs):
        """Prints Debug Output."""
        if self.debug:
            print(*args, **kwargs)

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

    def die(self, error=None):
        """Kills The App With An Error."""
        self.root.destroy()
        if error != None:
            raise error
        else:
            raise IOError("Application was killed.")

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

    def geterrors(self):
        """Gets A String Of Errors."""
        errorstring = ""
        for x in self.errorlog:
            errorstring += x+": "+strlist(self.errorlog[x], "; ")+"\n"
        self.errorlog = {}
        return errorstring[:-1]

    def showerrors(self):
        """Shows Logged Errors."""
        errorstring = self.geterrors()
        if errorstring == "":
            popup("Info", "No Errors.", "Error Log")
        else:
            popup("Info", errorstring[:-1], "Error Log")

class serverbase(base):
    """A Universal Server And Client Application."""

    def __init__(self, name="Web Client", message="Initializing...", height=None, speed=400, debug=False):
        """Creates The Server Or Client."""
        self.ready = False
        self.debug = bool(debug)
        if height == None:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name))
        else:
            self.root, self.app, self.box = startconsole(self.handler, str(message), str(name), int(height))
        rootbind(self.root, self.disconnect)
        self.show = self.app.display
        self.speed = int(speed)
        self.server = bool(isno(popup("Question", "Client(Y) or Server(n)?")))
        if not self.server:
            self.host = None
            while not self.host:
                self.host = popup("Entry", "Host?")
                if "." not in self.host:
                    popup("Error", "That isn't a valid host name. Please try again.")
                    self.host = ""
        self.port = 0
        while self.port <= 0:
            self.port = popup("Integer", "Port?")
        if self.server:
            self.number = 0
            while self.number <= 0:
                self.number = popup("Integer", "Number of clients?")
            self.app.display("Waiting For Connections...")
        else:
            self.app.display("Connecting...")
        self.register(self.connect, 200)

    def connect(self):
        """Connects To The Server Or Clients."""
        if self.server:
            self.c = multiserver(self.port, debug=self.debug)
            self.c.start(self.number)
        else:
            self.c = client(debug=self.debug)
            if self.host == "":
                self.c.connect(self.port)
            else:
                self.c.connect(self.port, self.host)
        self.app.display("Connected.")
        self.app.display("Retrieving Names...")
        if self.server:
            self.queue = {}
            self.sent = {}
            for a in self.c.c:
                self.queue[a] = []
                self.sent[a] = []
            self.names = {None: popup("Entry", "Name?") or "Host"}
            self.register(self.namer, self.speed+200)
        else:
            self.name = popup("Entry", "Name?") or "Guest"
            self.queue = [self.name]
            self.sent = []
            self.app.display("Names Retreived.\nLoading...")
            self.register(self.begin, self.speed+400)
        self.register(self.refresh, self.speed)

    def namer(self):
        """Retrieves Names."""
        for n,a in self.getsent():
            self.names[a] = n
        self.app.display("Names Retreived.\nLoading...")
        self.register(self.begin, 200)

    def begin(self):
        """Begins the main process."""
        self.app.display("Done.")
        self.ready = True

    def handler(self, event=None):
        """Handles input."""
        if self.ready:
            self.textmsg(self.box.output())

    def refresh(self, empty="#"):
        """Sends Items In The Queue, Adds Items To Sent."""
        empty = str(empty)
        if self.server:
            for a in self.c.c:
                if len(self.queue[a]) > 0:
                    self.queue[a].reverse()
                    self.c.fsend(a, self.queue[a].pop())
                    self.queue[a].reverse()
                else:
                    self.c.fsend(a, empty)
            self.root.update()
            for a in self.c.c:
                for test in self.cget(a):
                    test = test.strip(empty)
                    if test:
                        self.addsent((test,a))
        elif self.server != None:
            for test in self.cget():
                test = test.strip(empty)
                if test:
                    self.addsent(test)
            self.root.update()
            if len(self.queue) > 0:
                self.queue.reverse()
                self.c.fsend(self.queue.pop())
                self.queue.reverse()
            else:
                self.c.fsend(empty)
        else:
            return False
        self.register(self.refresh, self.speed)
        return True

    def send(self, item, to=None, exempt=None):
        """Sends A Message."""
        item = str(item)
        if self.server:
            for a in self.c.c:
                if (not to or a == to) and (not exempt or a != exempt):
                    self.queue[a].append(item)
        elif self.server != None:
            self.queue.append(item)
        else:
            return False
        return True

    def getsent(self):
        """Gets The Next Sent Item."""
        out = None
        if self.server:
            out = []
            for a in self.c.c:
                if len(self.sent[a]) == 0:
                    out.append(("", a))
                else:
                    out.append((self.sent[a].pop(0), a))
        elif self.server != None:
            if len(self.sent) == 0:
                out = ""
            else:
                out = self.sent.pop(0)
        return out

    def responded(self):
        """Determines Whether There Has Been A Response."""
        if self.server:
            for a in self.c.c:
                if len(self.sent[a]) == 0:
                    return False
            return True
        elif self.server != None:
            return len(self.sent) > 0
        else:
            return None

    def receive(self):
        """Receives A Message At A High Level."""
        if self.server:
            while not self.responded():
                self.root.update()
            return self.getsent()
        elif self.server != None:
            while not self.responded():
                self.root.update()
            return self.getsent()
        else:
            return None

    def chat(self, msg, name=""):
        """Displays A Chat Message."""
        out = str(name) + ":"*bool(name) + " "*(bool(name) and bool(msg)) + str(msg)
        self.app.display(out)
        return out

    def textmsg(self, item):
        """Sends A Chat Message."""
        item = str(item)
        if self.server:
            out = self.chat(item, self.names[None])
        elif self.server != None:
            out = self.chat(item, self.name)
        else:
            return False
        self.broadcast(out)
        return True

    def broadcast(self, item, to=None, exempt=None):
        """Broadcasts A Message."""
        if self.server == None:
            return False
        else:
            self.send("+:"+str(item), to, exempt)
            return True

    def addsent(self, item):
        """Adds A Received Message To The Sent."""
        if self.server:
            item, a = item
            if item.startswith("+:"):
                item = item[2:]
                self.app.display(item)
                self.broadcast(item, exempt=a)
            else:
                self.sent[a].append(item)
        elif self.server != None:
            if item.startswith("+:"):
                self.app.display(item[2:])
            else:
                self.sent.append(item)
        else:
            return False
        return True

    def sync(self, test="$"):
        """Insures The Server And Clients Are Synced Up."""
        test = str(test)
        if self.server:
            out = self.receive()
            self.send(test)
        elif self.server != None:
            self.send(test)
            out = self.receive()
        else:
            return False
        return test == out

    def disconnect(self):
        """Disconnects From The Server Or Clients."""
        self.c.close()
        self.server = None
        self.app.display("Disconnected.")
        self.root.update()
        self.die(IOError("The connection was terminated."))

    def cget(self, a=None):
        """Retrieves Messages At A Base Level."""
        try:
            if a == None:
                out = self.c.getitems(self.root.update)
            else:
                out = self.c.getitems(a, self.root.update)
        except IOError:
            self.disconnect()
        else:
            return out
