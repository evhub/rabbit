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

    def __init__(self, name="PythonPlus Application", message="Welcome!", height=None, *initializers):
        """Initializes A PythonPlus Application."""
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

    def __init__(self, name="Web Client", message="Loading...", height=None, speed=400, chatstring="+:", debug=False):
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
        self.chatstring = str(chatstring)
        self.server = bool(isno(popup("Question", "Client(Y) or Server(n)?")))
        if not self.server:
            self.host = popup("Entry", "Host?")
            if not self.host:
                self.die(ValueError("No host was given."))
        self.port = popup("Integer", "Port?")
        if not self.port:
            self.die(ValueError("No port was given."))
        if self.server:
            self.number = popup("Integer", "Number of clients?")
            if not self.number:
                self.die(ValueError("No client number was given."))
            self.app.display("Waiting For A Connection...")
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
        if self.server:
            self.queue = {}
            for a in self.c.c:
                self.queue[a] = []
            self.sent = []
            self.names = {None: popup("Entry", "Name?") or "Host"}
            self.register(self.namer, self.speed+200)
        else:
            self.queue = [popup("Entry", "Name?") or "Guest"]
            self.sent = ""
            self.register(self.begin, self.speed+400)
        self.register(self.refresh, self.speed)

    def namer(self):
        """Retrieves Names."""
        for n,a in self.sent:
            self.names[a] = n
        self.sent = []
        self.register(self.begin, 200)

    def begin(self):
        """Begins the main process."""
        self.app.display("Ready. Enter A Command:")
        self.ready = True

    def handler(self, event=None):
        """Handles input."""
        if self.ready:
            self.textmsg(self.box.output())

    def refresh(self, empty="#"):
        """Sends Items In The Que, Adds Items To Sent."""
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
                test = self.retrieve(a)
                if test != empty:
                    self.addsent((test,a))
        elif self.server != None:
            test = self.retrieve().strip(empty)
            if test != "":
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

    def send(self, item):
        """Sends A Message."""
        item = str(item)
        if self.server:
            for a in self.c.c:
                self.queue[a].append(item)
        elif self.server != None:
            self.queue.append(item)
        else:
            return False
        return True

    def receive(self):
        """Receives A Message At A High Level."""
        if self.server:
            while len(self.sent) < self.number:
                self.root.update()
            temp = self.sent
            self.sent = []
            return temp
        elif self.server != None:
            while self.sent == None:
                self.root.update()
            temp = self.sent
            self.sent = None
            return temp
        else:
            return None

    def chat(self, msg):
        """Displays A Chat Message."""
        self.app.display("> "+str(msg))

    def textmsg(self, item):
        """Sends A Chat Message."""
        item = str(item)
        if self.server:
            output = self.names[None]+": "+item
            self.chat(output)
            self.send(self.chatstring+output)
        elif self.server != None:
            self.send(self.chatstring+item)
        else:
            return False
        return True

    def addsent(self, item):
        """Adds A Received Message To The Sent."""
        if self.server:
            i,a = item
            if i.startswith(self.chatstring):
                i = i[2:]
                output = self.names[a]+i
                self.send(self.chatstring+output)
                self.chat(output)
            else:
                self.sent.append((i,a))
        elif self.server != None:
            if item.startswith(self.chatstring):
                self.chat(item[2:])
            else:
                self.sent = item
        else:
            return False
        return True

    def sync(self, test="$"):
        """Insures The Server And The Clients Are Synced Up."""
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
        if self.server:
            for a in dict(self.c.c):
                self.c.close(a)
        elif self.server != None:
            self.c.close()
        self.server = None
        self.app.display("Disconnected.")
        self.register(self.root.destroy, 200)

    def retrieve(self, a=None):
        """Retrieves A Message At A Base Level."""
        try:
            if a == None:
                out = self.c.retrieve(self.root.update)
            else:
                out = self.c.retrieve(a, self.root.update)
        except IOError:
            self.disconnect()
            self.die(IOError("Unable to retrieve data, partner most likely disconnected."))
        else:
            return out
