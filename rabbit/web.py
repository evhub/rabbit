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

from .obj import *
import socket
import urllib

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download(url, filename=None):
    """Downloads An Object Off The Web."""
    if filename == None:
        return urllib.urlretrieve(str(url))
    else:
        return urllib.urlretrieve(str(url), str(filename))

class server(object):
    """A Base Class For Servers."""
    def __init__(self, port, host=socket.gethostname(), debug=False):
        """Binds The Server To The Host And Port."""
        self.debug = debug
        self.s = socket.socket()
        self.s.bind((host, port))
        self.items = []
    def printdebug(self, message):
        """Prints A Debug Message."""
        if self.debug:
            print(str(message))
    def send(self, message):
        """Sends A Message."""
        message = str(message)
        self.printdebug("> "+message)
        self.c.send(message)
    def receive(self, amount=1024):
        """Receives A Message."""
        out = str(self.c.recv(amount))
        self.printdebug("< "+out)
        return out
    def retrieve(self, refresh=None, limit=100):
        """Retrieves Formatted Messages."""
        counter = 0
        while len(self.items) == 0:
            counter += 1
            test = self.receive().split("\\")
            for x in test:
                if x.startswith("~"):
                    self.items.append(x[1:])
            if counter > limit:
                raise IOError("Counter exceeds limit of "+str(limit))
            elif refresh != None and len(self.items) == 0:
                refresh()
        return self.items.pop(0)
    def getitems(self, refresh=None, limit=100):
        """Gets All Sent Messages."""
        out = [self.retrieve(refresh, limit)] + self.items[:]
        out.reverse()
        self.items = []
        return out
    def block(self, flag):
        """Sets The Blocking Value."""
        self.s.setblocking(flag)
    def fsend(self, item):
        """Sends A Formatted Message."""
        self.send("\\~"+str(item)+"\\")

class longserver(server):
    """A Server Class For Creating A Single-Client Server."""
    def start(self):
        """Opens Up The Server For A Connection."""
        self.s.listen(0)
        self.printdebug("->")
        self.c, self.a = self.s.accept()
        self.printdebug("<-")
    def close(self):
        """Ends The Connection."""
        self.c.close()

class shortserver(server):
    """A Server Class For Creating A Multi-Single-Client Server."""
    def __init__(self, port, host=socket.gethostname(), debug=False):
        """Binds The Server To The Host And Port."""
        self.debug = debug
        self.s = socket.socket()
        self.s.bind((host, port))
        self.up = 1
        self.items = []
    def start(self, backlog=5):
        """Opens Up The Server For Connections."""
        self.s.listen(int(backlog))
        self.printdebug("=>")
        while self.up == 1:
            self.c, self.a = self.s.accept()
            self.printdebug("<-")
            self.handle()
            self.c.close()
    def handle(self):
        """Handles A Connection."""
        self.send()
    def stop(self):
        """Stops Listening For Connections."""
        self.up = 0

class multiserver(server):
    """A Server Class For Creating A Multi-Client Server."""
    def __init__(self, port, host=socket.gethostname(), debug=False):
        """Binds The Server To The Host And Port."""
        self.debug = debug
        self.s = socket.socket()
        self.s.bind((host, port))
        self.c = {}
        self.items = {}
    def start(self, connections=5, backlog=0):
        """Begins Letting Connections In."""
        connections = int(connections)
        self.s.listen(int(backlog))
        self.printdebug("-"*connections+">")
        self.add(connections)
    def add(self, connections=1):
        """Add Connections."""
        for x in xrange(0, connections):
            connection, address = self.s.accept()
            self.printdebug("<-")
            self.c[address] = connection
            self.items[address] = []
    def close(self, address=None):
        """Disconnects A Certain Client."""
        if address == None:
            for a in self.c:
                self.close(a)
        else:
            self.c[address].close()
            del self.c[address]
    def send(self, address, message):
        """Sends A Message To A Certain Client."""
        if self.debug:
            print("> "+message)
        self.c[address].send(message)
    def receive(self, address, amount=1024):
        """Receives A Message From A Certain Client."""
        out = str(self.c[address].recv(amount))
        self.printdebug("< "+out)
        return out
    def retrieve(self, a, refresh=None, limit=100):
        """Retrieves Formatted Messages."""
        counter = 0
        while len(self.items[a]) == 0:
            counter += 1
            test = self.receive(a).split("\\")
            for x in test:
                if x.startswith("~"):
                    self.items[a].append(x[1:])
            if counter > limit:
                raise IOError("Counter exceeds limit of "+str(limit))
            elif refresh != None and len(self.items) == 0:
                refresh()
        return self.items[a].pop(0)
    def getitems(self, a, refresh=None, limit=100):
        """Gets All Sent Messages."""
        out = [self.retrieve(a, refresh, limit)] + self.items[a][:]
        out.reverse()
        self.items[a] = []
        return out
    def fsend(self, a, item):
        """Sends A Formatted Message."""
        self.send(a, "\\~"+str(item)+"\\")

class client(server):
    """A Client Class For Communicating To Servers."""
    def __init__(self, debug=False):
        """Initializes The Client."""
        self.debug = debug
        self.s = socket.socket()
        self.items = []
    def connect(self, port, host=socket.gethostname()):
        """Connects To A Server."""
        self.s.connect((host, port))
    def send(self, message):
        """Sends A Message."""
        if self.debug:
            print("> "+message)
        self.s.send(message)
    def receive(self, amount=1024):
        """Receives A Message."""
        out = str(self.s.recv(amount))
        self.printdebug("< "+out)
        return out
    def close(self):
        """Disconnects From A Server."""
        self.s.close()
