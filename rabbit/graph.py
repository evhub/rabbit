#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# INTERACTIVE made in 2012
# This program will graph user-defined and built-in functions.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class grapher(mathbase):
    """Rabbit Graphing Module."""

    def __init__(self, directory=None, name="Grapher", width=800, height=600, debug=False, *initializers):
        """Initializes A PythonPlus Grapher."""
        self.startup(debug)
        self.root = Tkinter.Tk()
        self.root.title(str(name))
        self.show = self.popshow
        self.width = width
        self.height = height
        self.app = displayer(self.root, self.width, self.height)
        self.box = entry(self.root)
        rootbind(self.root)
        self.box.dobind(self.handler)
        if directory is None:
            try:
                __file__
            except:
                directory = ""
            else:
                directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        else:
            directory = str(directory)
        try:
            self.pixel = openphoto(os.path.join(directory, "Pixel.gif"))
        except:
            go = False
            while not go:
                inputstring = popup("Entry", "Unable to find Pixel.gif. This file is necessary for rendering anything. Please enter the location where the file can be found:")
                if inputstring:
                    try:
                        self.pixel = openphoto(sanitize(inputstring)+"/Pixel.gif")
                    except:
                        go = False
                    else:
                        go = True
                else:
                    raise IOError("Unable to find Pixel.gif.")
        try:
            self.graph = openphoto(directory+"Graph.gif")
        except:
            self.graph = None
        else:
            self.app.new(self.graph)
        try:
            self.gridline = openphoto(directory+"Grid.gif")
        except:
            self.sepgrid = False
        else:
            self.sepgrid = True
        self.ysize = self.pixel.height()
        self.xsize = self.pixel.width()
        self.identifiers = []
        self.grid = []
        self.populator()
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def convert(self, x=0.0, y=0.0):
        """Converts From Mathematical To Canvas Coordinates."""
        x = float(x)
        y = float(y)
        top, side = self.width//self.xsize, self.height//self.ysize
        xpoint = (x+self.xup)//self.xstretch
        ypoint = side - (y+self.yup)//self.ystretch
        if 0 <= xpoint and xpoint <= top and ypoint <= side and ypoint >= 0:
            xpoint *= self.xsize
            ypoint *= self.ysize
            return xpoint, ypoint
        else:
            return False

    def dorender(self, newx, newy, grid=False):
        """Renders A Converted Point."""
        if grid:
            if self.sepgrid:
                self.grid.append(self.app.new(self.gridline, newx, newy))
            else:
                self.grid.append(self.app.new(self.pixel, newx, newy))
        else:
            self.identifiers.append(self.app.new(self.pixel, newx, newy))

    def singlerender(self, x=0, y=0):
        """Renders A Single Point."""
        new = self.convert(x, y)
        if new:
            newx, newy = new
            self.dorender(newx, newy)

    def clear(self):
        """Clears The Graph."""
        self.e.setreturned()
        for x in self.identifiers:
            self.app.clear(x)
        self.identifiers = []

    def cleargrid(self):
        """Clears The Grid."""
        self.e.setreturned()
        for x in self.grid:
            self.app.clear(x)
        self.grid = []

    def render(self, function):
        """Renders A Function."""
        testx = -1.0*self.xup
        self.e.setreturned(False)
        for x in xrange(0, self.width//self.xsize+1):
            testy = self.saferun(function, testx)
            if self.e.returned:
                break
            elif testy is not None and testy != matrix(0):
                self.singlerender(testx, testy)
            testx += self.xstretch
        self.e.setreturned()

    def swaprender(self, function):
        """Renders The Inverse Of A Function."""
        testy = -1.0*self.yup
        self.e.setreturned(False)
        for y in xrange(0, self.height//self.ysize+1):
            testx = self.saferun(function, testy)
            if self.e.returned:
                break
            elif testx is not None and testx != matrix(0):
                self.singlerender(testx, testy)
            testy += self.xstretch
        self.e.setreturned()

    def atrender(self, x, function):
        """Renders A Function At A Point."""
        y = self.saferun(function, x)
        if y is not None:
            self.pointrender(x,y)

    def pointrender(self, x, y):
        """Renders A Single Point With A Box."""
        new = self.convert(x, y)
        if new:
            xpoint, ypoint = new
            self.identifiers.append(self.app.new(self.pixel, xpoint, ypoint))
            points = self.points()
            while points != []:
                a,b = points.pop()
                if ypoint+b <= self.height//self.ysize and ypoint+b >= 0 and 0 <= xpoint+a and xpoint+a <= self.width//self.xsize:
                    self.dorender(xpoint+a, ypoint+b)

    def atswaprender(self, y, function):
        """Renders The Inverse Of A Function At A Point."""
        x = self.saferun(function, y)
        if x is not None:
            self.pointrender(x,y)

    def gridpoint(self, x=0, y=0):
        """Renders The Grid At A Point."""
        point = self.convert(x, y)
        if point:
            xpoint, ypoint = point
            if self.sepgrid:
                self.grid.append(self.app.new(self.gridline, xpoint, ypoint))
            else:
                self.grid.append(self.app.new(self.pixel, xpoint, ypoint))
            points = self.points()
            while points != []:
                a,b = points.pop()
                if ypoint+b <= self.height//self.ysize and ypoint+b >= 0 and 0 <= xpoint+a and xpoint+a <= self.width//self.xsize:
                    self.dorender(xpoint+a, ypoint+b, True)

    def intersectrender(self, f, g):
        """Renders The Intersection Of Two Functions."""
        testx = -1.0*self.xup
        self.e.setreturned(False)
        for x in xrange(0, self.width//self.xsize+1):
            fy = self.saferun(f, testx)
            fnew = self.convert(testx, fy)
            gy = self.saferun(g, testx)
            gnew = self.convert(testx, gy)
            if self.e.returned:
                break
            elif fnew and gnew:
                newx, fnewy = fnew
                newx, gnewy = gnew
                if fnewy == gnewy:
                    self.atrender(testx, lambda x: fy)
                else:
                    self.dorender(newx, fnewy)
                    self.dorender(newx, gnewy)
            elif fnew:
                newx, newy = fnew
                self.dorender(newx, newy)
            elif gnew:
                newx, newy = gnew
                self.dorender(newx, newy)
            testx += self.xstretch
        self.e.setreturned()

    def gridrender(self):
        """Renders The Grid."""
        self.e.setreturned()
        xgrid, ygrid = self.xsize//self.xstretch, self.ysize//self.ystretch
        test = 0
        for x in xrange(0, int(float(self.width+xgrid-1)/float(xgrid+1)+(self.width/2.0)*self.xstretch)):
            test += xgrid
            for y in xrange(0, self.height+1):
                self.dorender(test, y, True)
        test = 0
        for y in xrange(0, int(float(self.height+ygrid-1)/float(ygrid+1)+(self.height/2.0)*self.ystretch)):
            test += ygrid
            for x in xrange(0, self.width+1):
                self.dorender(x, test, True)

    def tickrender(self):
        """Renders Axis Ticks."""
        self.e.setreturned()
        xgrid, ygrid = self.xsize//self.xstretch, self.ysize//self.ystretch
        xstart, ystart = self.xup*xgrid, self.height-(self.yup*ygrid)
        test = 0
        for x in xrange(0, int(float(self.width+xgrid-1)/float(xgrid+1)+(self.width/2.0)*self.xstretch)):
            test += xgrid
            for y in xrange(-2, 3):
                self.dorender(test, y+ystart, True)
        test = 0
        for y in xrange(0, int(float(self.height+ygrid-1)/float(ygrid+1)+(self.height/2.0)*self.ystretch)):
            test += ygrid
            for x in xrange(-2, 3):
                self.dorender(x+xstart, test, True)

    def axisrender(self):
        """Renders The Axis."""
        self.e.setreturned()
        xgrid, ygrid = self.xsize//self.xstretch, self.ysize//self.ystretch
        xstart, ystart = self.xup*xgrid, self.height-(self.yup*ygrid)
        for x in xrange(0, self.width+1):
            self.dorender(x, ystart, True)
        for y in xrange(0, self.height+1):
            self.dorender(xstart, y, True)

    def scroll(self):
        """Advances The Scroll."""
        if self.marker < self.end:
            self.process(self.cmd)
            self.marker += 1
            self.register(self.scroll, 200)

    def points(self):
        """Gets The Value Of The points Variable."""
        points = self.calc("points").a
        out = []
        for xs in points:
            out.append((xs[0],xs[1]))
        return out

    def reset(self):
        """Sets The Rendering Variables."""
        self.dumpdebug(True)
        self.e.recursion = 0
        self.xstretch = self.e.funcfind("xstretch")*0.01
        self.ystretch = self.e.funcfind("ystretch")*0.01
        self.xup = self.e.funcfind("xup")
        self.yup = self.e.funcfind("yup")
        self.dumpdebug(True)

    def center(self):
        """Centers The Origin."""
        self.e.setreturned()
        self.e.variables["xup"] = str((self.width/2.0)*self.xstretch)
        self.e.variables["yup"] = str((self.height/2.0)*self.ystretch)

    def origin(self):
        """Plots The Origin."""
        self.e.setreturned()
        self.gridpoint(0,0)

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "debug":funcfloat(self.debugcall, self.e, "debug"),
            "run":funcfloat(self.runcall, self.e, "run", reqargs=1),
            "require":funcfloat(self.requirecall, self.e, "require", reqargs=1),
            "assert":funcfloat(self.assertcall, self.e, "assert", reqargs=1),
            "make":funcfloat(self.makecall, self.e, "make", reqargs=1),
            "save":funcfloat(self.savecall, self.e, "save", reqargs=1),
            "install":funcfloat(self.installcall, self.e, "install", reqargs=1),
            "cum":funcfloat(self.cumcall, self.e, "cum"),
            "inv":funcfloat(self.invcall, self.e, "inv"),
            "invcum":funcfloat(self.invcumcall, self.e, "invcum"),
            "at":funcfloat(self.atcall, self.e, "at"),
            "invat":funcfloat(self.invatcall, self.e, "invat"),
            "sect":funcfloat(self.sectcall, self.e, "sect"),
            "para":funcfloat(self.paracall, self.e, "para"),
            "polar":funcfloat(self.polarcall, self.e, "polar"),
            "scroll":funcfloat(self.scrollcall, self.e, "scroll"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "clear":usefunc(self.clear, self.e, "clear"),
            "cleargrid":usefunc(self.cleargrid, self.e, "cleargrid"),
            "center":usefunc(self.center, self.e, "center"),
            "grid":usefunc(self.gridrender, self.e, "grid"),
            "ticks":usefunc(self.tickrender, self.e, "ticks"),
            "axis":usefunc(self.axisrender, self.e, "axis"),
            "origin":usefunc(self.origin, self.e, "origin"),
            "render":strfunc("cleargrid()axis()ticks()", self.e, name="render"),
            "display":strfunc("center()render()", self.e, name="display"),
            "stretch":1.0,
            "xstretch":"stretch",
            "ystretch":"stretch",
            "up":1.0,
            "xup":"up",
            "yup":"up",
            "scroller":"xstretch",
            "interval":"(xstretch+ystretch)*0.005",
            "start":"2*pi-stop",
            "stop":2.0*math.pi,
            "base":1.0,
            "points":"points_box",
            "points_fill":"matrix:[1,0]:[0,1]:[0,-1]:[-1,0]:[1,1]:[-1,1]:[1,-1]:[-1,-1]:[-2,-2]:[-2,-1]:[-2,0]:[-2,1]:[-2,2]:[2,-2]:[2,-1]:[2,0]:[2,1]:[2,2]:[-1,2]:[0,2]:[1,2]:[-1,-2]:[0,-2]:[1,-2]",
            "points_box":"matrix:[-2,-2]:[-2,-1]:[-2,0]:[-2,1]:[-2,2]:[2,-2]:[2,-1]:[2,0]:[2,1]:[2,2]:[-1,2]:[0,2]:[1,2]:[-1,-2]:[0,-2]:[1,-2]",
            "points_cross":"matrix:[1,0]:[0,1]:[0,-1]:[-1,0]:[2,0]:[0,2]:[0,-2]:[-2,0]",
            "points_bold":"matrix:[1,0]:[0,1]:[0,-1]:[-1,0]:[1,1]:[-1,1]:[1,-1]:[-1,-1]",
            "points_plus":"matrix:[1,0]:[0,1]:[0,-1]:[-1,0]",
            "points_dot":"[]",
            "width":self.width/100.0,
            "height":self.height/100.0
            })

    def cumcall(self, variables, dorender=None):
        """Processes A Graphing Command."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to cum")
        elif len(variables) == 1:
            if not isnull(variables[0]):
                self.e.setreturned()
                if dorender is None:
                    dorender = self.render
                self.temp = 0
                dorender(lambda x: self.sumcall(variables[0], x))
        else:
            for arg in variables:
                self.cumcall([arg])
        return matrix(0)
                

    def invcall(self, variables):
        """Processes A Graphing Command."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to inv")
        elif len(variables) == 1:
            if not isnull(variables[0]):
                self.e.setreturned()
                self.swaprender(lambda x: self.call(variables[0], x))
        else:
            for arg in variables:
                self.invcall([arg])
        return matrix(0)

    def invcumcall(self, variables):
        """Processes A Graphing Command."""
        return self.cumcall(variables, self.invrender)

    def atcall(self, atlist, dorender=None):
        """Processes A Graphing Command."""
        if len(atlist) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to at")
        elif len(atlist) == 2:
            if not isnull(atlist[1]):
                self.e.setreturned()
                if dorender is None:
                    dorender = self.atrender
                if not isinstance(atlist[0], matrix):
                    dorender(atlist[0], lambda x: self.call(atlist[1], x))
                else:
                    for x in atlist[0].getitems():
                        dorender(x, lambda x: self.call(atlist[1], x))
            return matrix(0)
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to at")

    def invatcall(self, variables):
        """Processes A Graphing Command."""
        return self.atcall(variables, self.atswaprender)

    def sectcall(self, interlist):
        """Processes A Graphing Command."""
        if len(interlist) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to sect")
        elif len(interlist) == 2:
            if not (isnull(interlist[0]) or isnull(interlist[1])):
                self.e.setreturned()
                self.intersectrender(lambda x: self.call(interlist[0], x), lambda x: self.call(interlist[1], x))
            return matrix(0)
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to sect")

    def paracall(self, paralist):
        """Processes A Graphing Command."""
        if len(paralist) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to para")
        elif len(paralist) == 2:
            if not (isnull(paralist[0]) or isnull(paralist[1])):
                self.e.setreturned()
                stop = self.e.funcfind("stop")
                x = self.e.funcfind("start")
                inter = self.e.funcfind("interval")
                while x <= stop:
                    self.singlerender(self.call(paralist[0], x), self.call(paralist[1], x))
                    x += inter
            return matrix(0)
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to para")

    def polarcall(self, variables):
        """Processes A Graphing Command."""
        if not variables:
            raise ExecutionError("ArgumentError", "Not enough arguments to polar")
        elif len(variables) == 1:
            if not isnull(variables[0]):
                self.e.setreturned()
                angle = self.e.funcfind("start")
                inter = self.e.funcfind("interval")
                stop = self.e.funcfind("stop")
                while angle < stop:
                    r = self.call(variables[0], angle)
                    if r is not None:
                        self.singlerender(math.cos(angle)*r, math.sin(angle)*r)
                    angle += inter
        else:
            for arg in variables:
                self.polarcall([arg])
        return matrix(0)

    def scrollcall(self, variables):
        """Processes A Graphing Command."""
        if len(variables) < 2:
            raise ExecutionError("ArgumentError", "Not enough arguments to scroll")
        elif len(variables) == 2:
            if isinstance(variables[0], codestr) and isinstance(variables[1], codestr):
                self.e.setreturned()
                self.cmd = "cleargrid()clear();;xup:=x+0.01*scroller;;"+str(variables[1])
                self.marker = 0
                self.end = getint(self.e.calc(variables[0]))
                self.register(self.scroll, 200)
                return matrix(0)
            else:
                raise ExecutionError("StatementError", "Can only call scroll as a statement")
        else:
            raise ExecutionError("ArgumentError", "Too many arguments to scroll")

    def normcommand(self, item):
        """Graphs Normal Entries."""
        if not isnull(item) and self.doshow:
            self.e.setreturned()
            if isinstance(item, strcalc):
                self.show(self.e.prepare(item, True, True))
            elif isinstance(item, data):
                base = self.e.funcfind("base")
                for x in item.items():
                    self.pointrender(self.call(x, base), base)
            elif isinstance(item, multidata):
                for x,y in item.items():
                    self.pointrender(x,y)
            elif isinstance(item, matrix):
                self.matrixrender(item)
            else:
                self.render(lambda x: self.call(item, x))

    def matrixrender(self, inputmatrix, base=None):
        """Renders A Matrix."""
        temp = inputmatrix.getitems()
        if len(temp) == 2 and not (isinstance(temp[0], matrix) or isinstance(temp[1], matrix)):
            self.pointrender(temp[0], self.call(temp[1], temp[0]))
            return True
        elif len(temp) > 0:
            if base is None:
                base = self.e.funcfind("base")
            out = False
            for x in temp:
                if isinstance(x, matrix):
                    out = self.matrixrender(x, base) or out
                else:
                    self.pointrender(self.call(x, base), base)
            return out
        return False

    def sumcall(self, func, x):
        """Renders A Sum."""
        if x > 0:
            self.temp += self.call(func, x)
            return self.temp
