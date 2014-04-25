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

from .file import *
import tkMessageBox
import tkSimpleDialog

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class console(object):
    """A Graphical Class Used For Creating The PythonPlus Console."""
    def __init__(self, root, display=None, height=35, width=100, side="bottom"):
        """Base Constructor For The PythonPlus Console."""
        self.message = Tkinter.StringVar()
        if display != None:
            self.message.set(str(display))
        self.history = []
        height = int(height)
        width = int(width)
        self.main = Tkinter.Frame(root, width=width)
        self.main.pack(side=str(side))
        self.text = Tkinter.Label(self.main, textvariable=self.message, height=height, width=width, wraplength=800, justify="left", anchor="sw")
        self.text.pack(side="top")

    def clear(self, message=""):
        """Clears The Display."""
        self.message.set(str(message))
        self.history = []

    def display(self, message=None, *messages):
        """Displays A Message."""
        newmessage = "\n"
        if message != None:
            newmessage += str(message)
        for x in messages:
            newmessage += " " + str(x)
        self.drop()
        self.message.set(self.message.get() + newmessage)

    def up(self, event=None):
        """Moves The Display Up."""
        if self.message.get().replace("\n", "") != "":
            split = self.message.get().split("\n")
            self.history.append(split.pop())
            newmsg = ""
            for x in split:
                newmsg += "\n"
                newmsg += x
            self.message.set(newmsg)

    def down(self, event=None):
        """Moves The Display Down."""
        if self.history != []:
            split = self.message.get().split("\n")
            split.append(self.history.pop())
            newmsg = ""
            for x in split:
                newmsg += "\n"
                newmsg += x
            self.message.set(newmsg)

    def scroll(self, event):
        """Handles A Scroll Event."""
        delta = event.delta
        if delta >= 1:
            self.up(event)
        elif delta <= -1:
            self.down(event)

    def drop(self, amount=0):
        """Moves The Display To The Bottom."""
        for x in xrange(0, len(self.history)-int(amount)):
            self.down()

    def top(self, amount=0):
        """Moves The Display To The Top."""
        for x in xrange(0, len(self.message.get().split("\n"))-len(self.history)-int(amount)):
            self.up()

    def get(self):
        """Retreives The Currently Displayed String."""
        return self.message.get()

    def getlines(self):
        """Retreives All The Lines."""
        return self.message.get().split("\n") + self.history

def startconsole(handler=None, message=None, name="PythonPlus", height=None, root=None):
    """Initializes An Instance Of The PythonPlus Console."""
    if root == None:
        root = Tkinter.Tk()
    rootbind(root)
    root.title(str(name))
    if height != None:
        app = console(root, message, height)
    else:
        app = console(root, message)
    appbind(app)
    if handler != None:
        box = entry(app)
        boxbind(box, handler)
        return root, app, box
    else:
        return root, app

def rootbind(root):
    """Makes The Conventional Root Bindings."""
    root.bind("<Escape>", lambda event: root.destroy())

def appbind(app):
    """Makes The Conventional App Bindings."""
    app.text.bind("<MouseWheel>", app.scroll)
    app.text.bind("<Tab>", lambda event: app.drop())
    app.text.bind("<Shift-Tab>", lambda event: app.top())

def boxbind(box, handler):
    """Makes The Conventional Box Bindings."""
    box.main.bind("<Up>", lambda event: box.back())
    box.main.bind("<Down>", lambda event: box.forth())
    box.main.bind("<Control-z>", lambda event: box.main.delete(0, "end"))
    box.main.bind("<Control-f>", lambda event: box.clean())
    box.main.bind("<Return>", handler)

def popup(which, message, title=None):
    """Displays A Pop-Up Message."""
    if title == None:
        title = which
    which = superformat(which)
    if which == "info":
        return tkMessageBox.showinfo(str(title), str(message))
    elif which == "warning":
        return tkMessageBox.showwarning(str(title), str(message))
    elif which == "error":
        return tkMessageBox.showerror(str(title), str(message))
    elif which == "question":
        return tkMessageBox.askquestion(str(title), str(message))
    elif which == "proceed":
        return tkMessageBox.askokcancel(str(title), str(message))
    elif which == "yesorno":
        return tkMessageBox.askyesno(str(title), str(message))
    elif which == "retry":
        return tkMessageBox.askretrycancel(str(title), str(message))
    elif which == "entry":
        return tkSimpleDialog.askstring(str(title), str(message))
    elif which == "integer":
        return tkSimpleDialog.askinteger(str(title), str(message))
    elif which == "float":
        return tkSimpleDialog.askfloat(str(title), str(message))

class entry(object):
    """A Graphical Class That Allows The Use Of A Text Entry Box."""
    def __init__(self, app, pack=True, width=100, **kwargs):
        """Initializes A Text Entry Box."""
        try:
            app.main
        except AttributeError:
            root = app
        else:
            root = app.main
        width = int(width)
        self.main = Tkinter.Entry(root, width=width, **kwargs)
        if pack:
            self.main.pack(side="bottom")
        self.empty()

    def clear(self):
        """Clears The Text Box."""
        self.main.delete(0, "end")

    def output(self):
        """Gets Text Box Output."""
        contents = sanitize(self.main.get())
        self.clear()
        return contents

    def clean(self):
        """Sanitizes The Text Box."""
        self.insert(self.output())

    def insert(self, text):
        """Inserts Text Into The Text Box."""
        self.main.insert("end", text)

    def back(self):
        """Returns To Previous In Commands."""
        newposition = self.position - 1
        if newposition >= 0:
            try:
                self.commands[newposition]
            except IndexError:
                self.clean()
            else:
                self.clear()
                self.insert(self.commands[newposition])
                self.position = newposition
        else:
            self.clean()

    def forth(self):
        """Moves To Next In Commands."""
        newposition = self.position + 1
        if newposition >= 0:
            try:
                self.commands[newposition]
            except IndexError:
                self.clean()
            else:
                self.clear()
                self.insert(self.commands[newposition])
                self.position = newposition
        else:
            self.clean()

    def empty(self):
        """Empties The Commands."""
        self.commands = [""]
        self.position = 0

    def add(self, message=""):
        """Adds A String To The Commands."""
        message = str(message)
        if message != "":
            self.commands.remove("")
            self.commands.append(message)
            self.commands.append("")
        self.position = len(self.commands)-1

class texter(object):
    """A Graphical Class That Allows The Use Of A Text Entry Area."""
    def __init__(self, root, x=100, y=None, pack=True, **kwargs):
        """Initializes A Text Entry Area."""
        if y != None:
            kwargs["height"] = y
        self.main = Tkinter.Text(root, width=x, **kwargs)
        if pack:
            self.main.pack(side="bottom")

    def output(self):
        """Gets Text Box Output."""
        return sanitize(self.main.get(1.0, "end"))

    def display(self, text):
        """Sets The Contents Of The Text Entry Area."""
        self.main.insert("insert", str(text))

    def clear(self):
        """Clears The Contents Of The Text Entry Area."""
        self.main.delete(1.0, "end")

class button(object):
    """A Graphical Class That Implements A Button."""
    def __init__(self, root, text, command, default=None, pack=True, **kwargs):
        if default != None:
            kwargs["default"] = default
        self.main = Tkinter.Button(root, text=str(text), command=command, **kwargs)
        if pack:
            self.main.pack(side="left")

    def flash(self):
        """Flashes The Button."""
        self.main.flash()

    def invoke(self):
        """Calls The Button Function."""
        self.main.invoke()

class displayer(object):
    """A Graphical Class That Allows The Use Of Images."""
    def __init__(self, root, x=800, y=400, pack=True, **kwargs):
        """Initializes An Image Container."""
        x = int(x)
        y = int(y)
        self.main = Tkinter.Canvas(root, width=x, height=y, **kwargs)
        if pack:
            self.main.pack(side="top")
        self.x = x
        self.y = y

    def create(self, photo, x, y):
        """Attempts To Display An Image."""
        if 0 <= x and x <= self.x and 0 <= y and y <= self.y:
            return self.new(photo, x, y)

    def new(self, photo, x=None, y=None):
        """Displays An Image."""
        if x == None:
            x = self.x/2
        if y == None:
            y = self.y/2
        if typestr(photo) != "instance":
            photo = openphoto(str(photo))
            return photo, self.main.create_image(x, y, image=photo)
        else:
            return self.main.create_image(x, y, image=photo)

    def change(self, identifier, photo):
        """Changes A Displayed Image."""
        if typestr(photo) == "instance":
            photo = openphoto(str(photo))
            return photo, self.main.itemconfigure(identifier, image=openphoto(photo))
        else:
            return self.main.itemconfigure(identifier, image=photo)

    def clear(self, identifier="all"):
        """Deletes Displayed Images."""
        self.main.delete(identifier)

    def up(self, identifier, amount=10):
        """Moves An Image Up."""
        return self.move(identifier, 0, -1*int(amount))

    def down(self, identifier, amount=10):
        """Moves An Image Down."""
        return self.move(identifier, 0, int(amount))

    def left(self, identifier, amount=10):
        """Moves An Image Left."""
        return self.move(identifier, -1*int(amount), 0)

    def right(self, identifier, amount=10):
        """Moves An Image Right."""
        return self.move(identifier, int(amount), 0)

    def move(self, identifier, x, y):
        """Moves A Displayed Image."""
        oldx, oldy = self.main.coords(identifier)
        x, y = int(x), int(y)
        if 0 < oldx+x < self.x:
            if 0 < oldy+y < self.y:
                self.main.move(identifier, x, y)
                return True
            else:
                return False
        else:
            return False

    def moveto(self, identifier, x, y):
        """Moves A Displayed Image To A Set Of Coordinates."""
        x, y = int(x), int(y)
        if 0 < x < self.x:
            if 0 < y < self.y:
                oldx, oldy = self.main.coords(identifier)
                self.main.move(identifier, x-oldx, y-oldy)
                return True
            else:
                return False
        else:
            return False

    def convert(self, event):
        """Returns The Canvas Coordinates Of An Event."""
        return self.main.canvasx(event.x), self.main.canvasy(event.y)
