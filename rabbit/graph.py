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

from __future__ import with_statement, absolute_import, print_function, unicode_literals

from .cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class grapher(mathbase):
    """Rabbit Graphing Module."""

    def __init__(self, directory="rabbit/", name="Grapher", width=800, height=600, debug=False, *initializers):
        """Initializes A PythonPlus Grapher."""
        self.debug = bool(debug)
        self.root = Tkinter.Tk()
        self.root.title(str(name))
        self.show = self.popshow
        self.width = width
        self.height = height
        self.app = displayer(self.root, self.width, self.height)
        self.box = entry(self.root)
        rootbind(self.root)
        self.box.dobind(self.handler)
        directory = str(directory)
        try:
            self.pixel = openphoto(directory+"Pixel.gif")
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
        self.printdebug(": ON")
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def convert(self, x=0.0, y=0.0):
        """Converts From Mathematical To Canvas Coordinates."""
        x = float(x)
        y = float(y)
        top, side = self.width/self.xsize, self.height/self.ysize
        xpoint = int((x+self.xup)/self.xstretch)
        ypoint = side - int((y+self.yup)/self.ystretch)
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
        for x in self.identifiers:
            self.app.clear(x)
        self.identifiers = []

    def cleargrid(self):
        """Clears The Grid."""
        for x in self.grid:
            self.app.clear(x)
        self.grid = []

    def render(self, function):
        """Renders A Function."""
        testx = -1.0*self.xup
        self.returned = 0
        for x in xrange(0, self.width/self.xsize+1):
            testy = self.saferun(function, testx)
            if self.returned == 1:
                break
            elif testy is not None and testy != matrix(0):
                self.singlerender(testx, testy)
            testx += self.xstretch
        self.returned = 1

    def swaprender(self, function):
        """Renders The Inverse Of A Function."""
        testy = -1.0*self.yup
        self.returned = 0
        for y in xrange(0, self.height/self.ysize+1):
            testx = self.saferun(function, testy)
            if self.returned == 1:
                break
            elif testx is not None and testx != matrix(0):
                self.singlerender(testx, testy)
            testy += self.xstretch
        self.returned = 1

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
                if ypoint+b <= self.height/self.ysize and ypoint+b >= 0 and 0 <= xpoint+a and xpoint+a <= self.width/self.xsize:
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
                if ypoint+b <= self.height/self.ysize and ypoint+b >= 0 and 0 <= xpoint+a and xpoint+a <= self.width/self.xsize:
                    self.dorender(xpoint+a, ypoint+b, True)

    def intersectrender(self, f, g):
        """Renders The Intersection Of Two Functions."""
        testx = -1.0*self.xup
        self.returned = 0
        for x in xrange(0, self.width/self.xsize+1):
            fy = self.saferun(f, testx)
            fnew = self.convert(testx, fy)
            gy = self.saferun(g, testx)
            gnew = self.convert(testx, gy)
            if self.returned == 1:
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
        self.returned = 1

    def gridrender(self):
        """Renders The Grid."""
        xgrid, ygrid = self.xsize/self.xstretch, self.ysize/self.ystretch
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
        xgrid, ygrid = self.xsize/self.xstretch, self.ysize/self.ystretch
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
        xgrid, ygrid = self.xsize/self.xstretch, self.ysize/self.ystretch
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

    def populator(self):
        """Populates The Grapher."""
        self.pre_cmds = [
            self.pre_cmd
            ]
        self.cmds = [
            self.cmd_help,
            self.cmd_debug,
            self.cmd_clear,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_del,
            self.cmd_make,
            self.cmd_def,

            self.cmd_grapher,

            self.cmd_set,
            self.cmd_normal
            ]
        self.set_cmds = [
            self.set_def,
            self.set_normal
            ]
        self.e = evaluator(processor=self)
        self.fresh(True)
        self.genhelp()

    def fresh(self, top=True):
        """Refreshes The Environment."""
        if not top:
            self.e.fresh()
        self.e.makevars({
            "run":funcfloat(self.runcall, self.e, "run"),
            "save":funcfloat(self.savecall, self.e, "save"),
            "install":funcfloat(self.installcall, self.e, "install"),
            "print":funcfloat(self.printcall, self.e, "print"),
            "show":funcfloat(self.showcall, self.e, "show"),
            "render":strfunc('proc("cleargrid;;axis;;ticks")', self.e, name="render"),
            "display":strfunc('proc("center;;render")', self.e, name="display"),
            "stretch":1.0,
            "xstretch":strfunc('exec(val("stretch"))', self.e, name="xstretch"),
            "ystretch":strfunc('exec(val("stretch"))', self.e, name="ystretch"),
            "up":1.0,
            "xup":strfunc('exec(var("up"))', self.e, name="xup"),
            "yup":strfunc('exec(var("up"))', self.e, name="yup"),
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
        self.xstretch = self.calc("xstretch")*0.01
        self.ystretch = self.calc("ystretch")*0.01
        self.xup = self.calc("xup")
        self.yup = self.calc("yup")
        self.dumpdebug(True)

    def cmd_clear(self, original):
        """Processes clear."""
        if superformat(original) == "clear":
            self.clear()
            return True

    def cmd_grapher(self, original):
        """Processes Graphing Commands."""
        if superformat(original).startswith("sum "):
            original = original[4:]
            item = self.calc(original)
            if not isnull(item):
                self.temp = 0
                self.render(lambda x: self.sumcall(item, x))
                return True
        if superformat(original) == "center":
            self.e.variables["xup"] = str((self.width/2.0)*self.xstretch)
            self.e.variables["yup"] = str((self.height/2.0)*self.ystretch)
            return True
        if superformat(original) == "grid":
            self.gridrender()
            return True
        if superformat(original) == "ticks":
            self.tickrender()
            return True
        if superformat(original) == "axis":
            self.axisrender()
            return True
        if superformat(original) == "origin":
            self.gridpoint(0,0)
            return True
        if superformat(original) == "cleargrid":
            self.cleargrid()
            return True
        if superformat(original).startswith("inv "):
            original = original[4:]
            item = self.calc(original)
            if not isnull(item):
                self.swaprender(lambda x: self.call(item, x))
                return True
        if superformat(original).startswith("invsum "):
            original = original[7:]
            item = self.calc(original)
            if not isnull(item):
                self.temp = 0
                self.swaprender(lambda x: self.sumcall(original, x))
                return True
        if superformat(original).startswith("at "):
            original = self.e.find(original[3:])
            atlist = original.split(" do ", 1)
            atlist[1] = self.calc(atlist[1])
            if not isnull(atlist[1]):
                atlist[0] = self.calc(atlist[0])
                if not isinstance(atlist[0], matrix):
                    self.atrender(atlist[0], lambda x: self.call(atlist[1], x))
                else:
                    for x in atlist[0].getitems():
                        self.atrender(x, lambda x: self.call(atlist[1], x))
                return True
        if superformat(original).startswith("atinv "):
            original = self.e.find(original[6:])
            atlist = original.split(" do ", 1)
            atlist[1] = self.calc(atlist[1])
            if not isnull(atlist[1]):
                atlist[0] = self.calc(atlist[0])
                if not isinstance(atlist[0], matrix):
                    self.atswaprender(atlist[0], lambda x: self.call(atlist[1], x))
                else:
                    for x in atlist[0].getitems():
                        self.atswaprender(x, lambda x: self.call(atlist[1], x))
                return True
        if superformat(original).startswith("intersect "):
            original = self.e.find(original[10:])
            interlist = original.split(" and ", 1)
            interlist[0] = self.calc(interlist[0])
            interlist[1] = self.calc(interlist[1])
            if not isnull(interlist[0]) or isnull(interlist[1]):
                self.intersectrender(lambda x: self.call(interlist[0], x), lambda x: self.call(interlist[1], x))
                return True
        if superformat(original).startswith("parametric "):
            original = self.e.find(original[11:])
            paralist = original.split(" and ", 1)
            paralist[0] = self.calc(paralist[0])
            paralist[1] = self.calc(paralist[1])
            if not isnull(paralist[0]) or isnull(paralist[1]):
                stop = self.calc("stop")
                x = self.self.calc("start")
                inter = self.calc("interval")
                while x <= stop:
                    self.singlerender(self.call(paralist[0], x), self.call(paralist[1], x))
                    x += inter
                return True
        if superformat(original).startswith("polar "):
            item = self.calc(original)
            if not isnull(item):
                angle = self.calc("start")
                inter = self.calc("interval")
                stop = self.calc("stop")
                while angle < stop:
                    r = self.call(item, angle)
                    if r is not None:
                        self.singlerender(math.cos(angle)*r, math.sin(angle)*r)
                    angle += inter
                return True
        if superformat(original).startswith("scroll "):
            original = original[7:]
            forlist = original.split(" do ", 1)
            self.cmd = "cleargrid;;clear;;xup:=x+0.01*scroller;;"+self.e.find(forlist[1])
            self.marker = 0
            self.end = int(getnum(self.e.find(forlist[0])))
            self.register(self.scroll, 200)
            return True

    def cmd_do(self, original):
        """Evaluates Functions Silently."""
        if superformat(original).startswith("do "):
            self.calc(original[3:])
            return True

    def cmd_normal(self, original):
        """Graphs Normal Entries."""
        self.returned = 0
        item = self.calc(original)
        if self.returned == 0 and not isnull(item):
            if isinstance(item, strcalc):
                self.show(self.e.prepare(item, True, True))
            elif isinstance(item, data):
                for x in item.items():
                    base = self.calc("base")
                    self.pointrender(self.call(x, base), base)
            elif isinstance(item, multidata):
                for x,y in item.items():
                    self.pointrender(x,y)
            elif isinstance(item, matrix):
                self.matrixrender(item)
            else:
                self.render(lambda x: self.call(item, x))
            self.returned = 1
        return True

    def matrixrender(self, inputmatrix):
        """Renders A Matrix."""
        temp = inputmatrix.getitems()
        if len(temp) == 2 and not (isinstance(temp[0], matrix) or isinstance(temp[1], matrix)):
            self.pointrender(temp[0], self.call(temp[1], temp[0]))
            return True
        elif len(temp) > 0:
            out = False
            for x in temp:
                if isinstance(x, matrix):
                    out = self.matrixrender(x) or out
                else:
                    base = self.calc("base")
                    self.pointrender(self.call(x, base), base)
            return out
        return False

    def sumcall(self, func, x):
        """Renders A Sum."""
        if x > 0:
            self.temp += self.call(func, x)
            return self.temp
