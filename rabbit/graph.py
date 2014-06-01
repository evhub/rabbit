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

from rabbit.cmd import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class grapher(mathbase):
    """Rabbit Graphing Module."""
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
Grid Control:
    render
        axis
        ticks
    origin
    grid
    cleargrid
Window Control:
    stretch = <value>
        xstretch = <value>
        ystretch = <value>
    up = <value>
        xup = <value>
        yup = <value>
    display
        center
Special Functions:
    sum <function>
    inv <function>
        invsum <function>
    at <list> do <function>
        atinv <list> do <function>
    intersect <function> and <function>
    parametric <x_function> and <y_function>
    polar <theta_function>
    scroll <times> do <function>
Control Commands:
    do <command>
    del <variable>
    get [variable]
Import Commands:
    <name> = import <file>
    run <file>
    save <file>"""

    def __init__(self, name="Grapher", directory="rabbit/", width=800, height=600, helpstring=None, debug=False, *initializers):
        """Initializes A PythonPlus Grapher."""
        self.debug = bool(debug)
        self.root = Tkinter.Tk()
        self.root.title(str(name))
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
            popup("Error", "Unable to find Pixel.gif. This file is necessary for rendering anything.")
            raise IOError("Unable to find Pixel.gif")
        try:
            self.graph = openphoto(directory+"Graph.gif")
        except:
            pass
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
        self.errorlog = {}
        self.returned = 1
        self.populator()
        if initializers == ():
            self.initialize()
        else:
            self.initialize(args=initializers)

    def show(self, arg):
        """Displays Something."""
        if not istext(arg):
            arg = self.e.prepare(arg)
        if arg != "()":
            popup("Info", arg, "Output")

    def convert(self, x=0.0, y=0.0):
        """Converts From Mathematical To Canvas Coordinates."""
        x = float(x)
        y = float(y)
        top, side = self.width/self.xsize, self.height/self.ysize
        xpoint = int((x+self.xup())/self.xstretch())
        ypoint = side - int((y+self.yup())/self.ystretch())
        if 0 <= xpoint and xpoint <= top and ypoint <= side and ypoint >= 0:
            xpoint *= self.xsize
            ypoint *= self.ysize
            return xpoint, ypoint
        else:
            return False

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
        testx = -1.0*self.xup()
        self.returned = 0
        for x in xrange(0, self.width/self.xsize+1):
            testy = self.saferun(function, testx)
            if self.returned == 1:
                break
            elif testy != None and testy != matrix(0):
                new = self.convert(testx, testy)
                if new:
                    newx, newy = new
                    self.identifiers.append(self.app.new(self.pixel, newx, newy))
            testx += self.xstretch()
        self.returned = 1

    def swaprender(self, function):
        """Renders The Inverse Of A Function."""
        testy = -1.0*self.yup()
        self.returned = 0
        for y in xrange(0, self.height/self.ysize+1):
            testx = self.saferun(function, testy)
            if self.returned == 1:
                break
            elif testx != None and testx != matrix(0):
                new = self.convert(testx, testy)
                if new:
                    newx, newy = new
                    self.identifiers.append(self.app.new(self.pixel, newx, newy))
            testy += self.xstretch()
        self.returned = 1

    def atrender(self, x, function):
        """Renders A Function At A Point."""
        y = self.saferun(function, x)
        if y != None:
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
                    self.identifiers.append(self.app.new(self.pixel, xpoint+a, ypoint+b))

    def atswaprender(self, y, function):
        """Renders The Inverse Of A Function At A Point."""
        x = self.saferun(function, y)
        if x != None:
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
                    if self.sepgrid:
                        self.grid.append(self.app.new(self.gridline, xpoint+a, ypoint+b))
                    else:
                        self.grid.append(self.app.new(self.pixel, xpoint+a, ypoint+b))

    def singlerender(self, x=0, y=0):
        """Renders A Single Point."""
        new = self.convert(x, y)
        if new:
            newx, newy = new
            self.identifiers.append(self.app.new(self.pixel, newx, newy))

    def intersectrender(self, f, g):
        """Renders The Intersection Of Two Functions."""
        testx = -1.0*self.xup()
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
                    self.identifiers.append(self.app.new(self.pixel, newx, fnewy))
                    self.identifiers.append(self.app.new(self.pixel, newx, gnewy))
            elif fnew:
                newx, newy = fnew
                self.identifiers.append(self.app.new(self.pixel, newx, newy))
            elif gnew:
                newx, newy = gnew
                self.identifiers.append(self.app.new(self.pixel, newx, newy))
            testx += self.xstretch()
        self.returned = 1

    def gridrender(self):
        """Renders The Grid."""
        xgrid, ygrid = self.xsize/self.xstretch(), self.ysize/self.ystretch()
        test = 0
        for x in xrange(0, int(float(self.width+xgrid-1)/float(xgrid+1)+(self.width/2.0)*self.xstretch())):
            test += xgrid
            for y in xrange(0, self.height+1):
                if self.sepgrid:
                    self.grid.append(self.app.new(self.gridline, test, y))
                else:
                    self.grid.append(self.app.new(self.pixel, test, y))
        test = 0
        for y in xrange(0, int(float(self.height+ygrid-1)/float(ygrid+1)+(self.height/2.0)*self.ystretch())):
            test += ygrid
            for x in xrange(0, self.width+1):
                if self.sepgrid:
                    self.grid.append(self.app.new(self.gridline, x, test))
                else:
                    self.grid.append(self.app.new(self.pixel, x, test))

    def tickrender(self):
        """Renders Axis Ticks."""
        xgrid, ygrid = self.xsize/self.xstretch(), self.ysize/self.ystretch()
        xstart, ystart = self.xup()*xgrid, self.height-(self.yup()*ygrid)
        test = 0
        for x in xrange(0, int(float(self.width+xgrid-1)/float(xgrid+1)+(self.width/2.0)*self.xstretch())):
            test += xgrid
            for y in xrange(-2, 3):
                if self.sepgrid:
                    self.grid.append(self.app.new(self.gridline, test, y+ystart))
                else:
                    self.grid.append(self.app.new(self.pixel, test, y+ystart))
        test = 0
        for y in xrange(0, int(float(self.height+ygrid-1)/float(ygrid+1)+(self.height/2.0)*self.ystretch())):
            test += ygrid
            for x in xrange(-2, 3):
                if self.sepgrid:
                    self.grid.append(self.app.new(self.gridline, x+xstart, test))
                else:
                    self.grid.append(self.app.new(self.pixel, x+xstart, test))

    def axisrender(self):
        """Renders The Axis."""
        xgrid, ygrid = self.xsize/self.xstretch(), self.ysize/self.ystretch()
        xstart, ystart = self.xup()*xgrid, self.height-(self.yup()*ygrid)
        for x in xrange(0, self.width+1):
            if self.sepgrid:
                self.grid.append(self.app.new(self.gridline, x, ystart))
            else:
                self.grid.append(self.app.new(self.pixel, x, ystart))
        for x in xrange(0, self.height+1):
            if self.sepgrid:
                self.grid.append(self.app.new(self.gridline, xstart, x))
            else:
                self.grid.append(self.app.new(self.pixel, xstart, x))

    def scroll(self):
        """Advances The Scroll."""
        if self.marker < self.end:
            self.process(self.cmd)
            self.marker += 1
            self.register(self.scroll, 200)

    def populator(self):
        """Populates The Grapher."""
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
            self.cmd_get,
            self.cmd_run,
            self.cmd_save,
            self.cmd_assert,
            self.cmd_do,
            self.cmd_show,
            self.cmd_del,

            self.cmd_grapher,

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
            "render":"cleargrid;;axis;;ticks",
            "display":"center;;render", "stretch":1.0,
            "'xstretch":"stretch",
            "'ystretch":"stretch",
            "'up":1.0,
            "'xup":"up",
            "'yup":"up",
            "'scroller":"xstretch",
            "'interval":"(xstretch+ystretch)*0.005",
            "'start":"_stop-stop",
            "'stop":2.0*math.pi,
            "'base":1.0,
            "'points":"points_box",
            "points_fill":"matrix:(1,0):(0,1):(0,-1):(-1,0):(1,1):(-1,1):(1,-1):(-1,-1):(-2,-2):(-2,-1):(-2,0):(-2,1):(-2,2):(2,-2):(2,-1):(2,0):(2,1):(2,2):(-1,2):(0,2):(1,2):(-1,-2):(0,-2):(1,-2)",
            "points_box":"matrix:(-2,-2):(-2,-1):(-2,0):(-2,1):(-2,2):(2,-2):(2,-1):(2,0):(2,1):(2,2):(-1,2):(0,2):(1,2):(-1,-2):(0,-2):(1,-2)",
            "points_cross":"matrix:(1,0):(0,1):(0,-1):(-1,0):(2,0):(0,2):(0,-2):(-2,0)",
            "points_bold":"matrix:(1,0):(0,1):(0,-1):(-1,0):(1,1):(-1,1):(1,-1):(-1,-1)",
            "points_plus":"matrix:(1,0):(0,1):(0,-1):(-1,0)",
            "points_dot":"()",
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

    def final(self):
        """Gets The Value Of The stop Variable."""
        return self.calc("stop")

    def initial(self):
        """Gets The Value Of The start Variable."""
        return self.calc("start")

    def xstretch(self):
        """Gets The Value Of The xstretch Variable."""
        return self.calc("xstretch")*0.01

    def ystretch(self):
        """Gets The Value Of The ystretch Variable."""
        return self.calc("ystretch")*0.01

    def xup(self):
        """Gets The Value Of The xup Variable."""
        return self.calc("xup")

    def yup(self):
        """Gets The Value Of The yup Variable."""
        return self.calc("yup")

    def interval(self):
        """Gets The Value Of The interval Variable."""
        return self.calc("interval")

    def base(self):
        """Gets The Value Of The base Variable."""
        return self.calc("base")

    def cmd_clear(self, original):
        """Processes clear."""
        if superformat(original) == "clear":
            self.clear()
            return True

    def cmd_grapher(self, original):
        """Processes Graphing Commands."""
        if superformat(original).startswith("sum "):
            original = original[4:]
            self.temp = 0
            self.render(lambda x: self.sumcall(original, x))
            return True
        if superformat(original) == "center":
            self.e.variables["xup"] = str((self.width/2.0)*self.xstretch())
            self.e.variables["yup"] = str((self.height/2.0)*self.ystretch())
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
            self.swaprender(lambda x: self.call(original, x))
            return True
        if superformat(original).startswith("invsum "):
            original = original[7:]
            self.temp = 0
            self.swaprender(lambda x: self.sumcall(original, x))
            return True
        if superformat(original).startswith("at "):
            original = original[3:]
            atlist = original.split(" do ", 1)
            atlist[0] = self.calc(atlist[0])
            if not isinstance(atlist[0], matrix):
                self.atrender(atlist[0], lambda x: self.call(atlist[1], x))
            else:
                for x in atlist[0].getitems():
                    self.atrender(x, lambda x: self.call(atlist[1], x))
            return True
        if superformat(original).startswith("atinv "):
            original = original[6:]
            atlist = original.split(" do ", 1)
            atlist[0] = self.calc(atlist[0])
            if not isinstance(atlist[0], matrix):
                self.atswaprender(atlist[0], lambda x: self.call(atlist[1], x))
            else:
                for x in atlist[0].getitems():
                    self.atswaprender(x, lambda x: self.call(atlist[1], x))
            return True
        if superformat(original).startswith("intersect "):
            original = original[10:]
            interlist = original.split(" and ", 1)
            self.intersectrender(lambda x: self.call(interlist[0], x), lambda x: self.call(interlist[1], x))
            return True
        if superformat(original).startswith("parametric "):
            original = self.e.find(original[11:])
            paralist = original.split(" and ", 1)
            stop = self.final()
            x = self.initial()
            inter = self.interval()
            while x <= stop:
                self.singlerender(self.call(paralist[0], x), self.call(paralist[1], x))
                x += inter
            return True
        if superformat(original).startswith("polar "):
            original = self.e.find(original[6:])
            angle = self.initial()
            inter = self.interval()
            stop = self.final()
            while angle < stop:
                r = self.call(original, angle)
                if r != None:
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
        test = self.calc(original)
        if self.returned == 0:
            if isinstance(test, strcalc):
                self.show(self.e.prepare(test, True, True))
            elif isinstance(test, data):
                for x in test.items():
                    self.pointrender(x,self.base())
            elif isinstance(test, multidata):
                for x,y in test.items():
                    self.pointrender(x,y)
            elif isinstance(test, matrix):
                self.matrixrender(test)
            else:
                self.render(lambda x: self.call(test, x))
            self.returned = 1
        return True

    def matrixrender(self, inputmatrix):
        """Renders A Matrix."""
        temp = inputmatrix.getitems()
        if len(temp) == 2 and not (isinstance(temp[0], matrix) or isinstance(temp[1], matrix)):
            self.pointrender(self.calc(temp[0]), self.calc(temp[1]))
            return True
        elif len(temp) > 0:
            out = False
            for x in temp:
                if isinstance(x, matrix):
                    out = self.matrixrender(x) or out
            return out
        return False

    def sumcall(self, func, x):
        """Renders A Sum."""
        if x > 0:
            self.temp += self.call(func, x)
            return self.temp
