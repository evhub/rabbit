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
from .format import *
from .sys import *
import codecs
import zipfile
import Tkinter

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def openfile(filename, opentype="r+b"):
    """Returns An Open File Object."""
    return codecs.open(str(filename), str(opentype), "UTF")

def writefile(openfile, writer):
    """Sets The Contents Of A File."""
    openfile.seek(0)
    openfile.truncate()
    openfile.write(str(writer).encode("UTF"))

def readfile(openfile):
    """Reads The Contents Of A File."""
    return openfile.read()

def createfile(filename, opentype="r+b"):
    """Creates A File And Returns An Open File Object For It."""
    writelist = ["w", "wb"]
    filename = str(filename)
    if opentype not in writelist:
        out = openfile(filename, "wb")
    out = openfile(filename, str(opentype))
    return out

def getfile(filename, opentype="r+b"):
    """Returns An Open File Object, Regardless Of Whether The File Already Exists."""
    try:
        out = openfile(filename, opentype)
    except IOError:
        out = createfile(filename, opentype)
    return out

def runfile(filename, currentos=None):
    """Opens A File With Its Default Program."""
    if currentos == None:
        currentos = getos()
    else:
        currentos = str(currentos)
    if currentos.startswith("win"):
        os.startfile(str(filename))
    else:
        newfilename = ""
        for x in filename:
            if x == " ":
                newfilename += "\ "
            else:
                newfilename += x
        runcmd("open " + newfilename)

def makedir(directory):
    """Creates A Directory."""
    directory = str(directory)
    if not os.path.isdir(directory):
        os.makedirs(directory)

def openzip(filename, mode="r"):
    """Returns An Open Zip File Object."""
    return zipfile.ZipFile(str(filename), str(mode))

def unzip(openzip, path=None):
    """Unzips A Zip File."""
    if path == None:
        path = os.getcwd()
    else:
        makedir(path)
    for x in openzip.namelist():
        if not x.endswith("/"):
            base, name = os.path.split(x)
            directory = os.path.normpath(os.path.join(path, base))
            makedir(directory)
            try:
                openx = openfile(os.path.join(directory, name), "wb")
                openx.write(openzip.read(x))
            finally:
                openx.close()

def search(directory, symlinks=True):
    """Determines The Contents Of A Directory."""
    dirfiles = {}
    for path, dirs, files in os.walk(str(directory), followlinks=symlinks):
        dirfiles[path] = files, dirs
    return dirfiles

def openphoto(filename):
    """Opens An Image File."""
    return Tkinter.PhotoImage(file=str(filename))
