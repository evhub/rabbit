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

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division

from .carrot.stats import *
from .func import *

global e
try:
    set_e
except:
    old_set_e = None
else:
    old_set_e = set_e
def set_e(new_e):
    """Sets The Evaluator Global."""
    global e
    if old_set_e is not None:
        old_set_e(new_e)
    e = new_e

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def teq(v):
    """Finds The t Distribution For The Given Degrees Of Freedom."""
    n = v+1.0
    return strfunc(e.prepare(gamma(n/2.0) / ((math.pi*v)**0.5 * gamma(v/2.0))) + "/" + "(1+x^2/" + e.prepare(v) + ")^" + e.prepare(n/2.0), ["x"])

def tP(start, stop, df):
    """Finds The Cumulative Probability Between Two t Values."""
    eq = teq(df)
    return defint(lambda x: eq.call([x]), start, stop)

def chisqeq(v):
    """Finds The Chi Squared Distribution For The Given Degrees Of Freedom."""
    return strfunc("x^"+e.prepare((v-2.0)/2.0)+"*e^(-x/2)/"+e.prepare(2.0**(v/2.0)*gamma(v/2.0)), ["x"])

def chisqP(stop, df):
    """Finds The Probability Beyond A Chi Squared Value."""
    eq = chisqeq(df)
    return 1.0-defint(lambda x: eq.call([x]), 0.0, stop)

def Feq(v, w):
    """Finds The F Distribution For The Given Degrees Of Freedom."""
    return strfunc(e.prepare((v/w)**(v/2)*gamma((v+w)/2.0)/(gamma(v/2.0)*gamma(w/2.0)))+"*x^"+e.prepare((v-2.0)/2.0)+"/(1+"+e.prepare(v/w)+"x)^"+e.prepare((v+w)/2.0), ["x"])

def FP(stop, dfT, dfE):
    """Finds The Probability Beyond An F Value."""
    eq = Feq(dfT, dfE)
    return 1.0-defint(lambda x: eq.call([x]), 0.0, stop)

class data(mctobject):
    """Implements A Data Set."""
    evaltype = "Stats.data"

    def __init__(self, units=None, gotsort=False):
        """Initializes The Data."""
        self.units = []
        self.gotsort = bool(gotsort)
        if units is not None:
            self.extend(units)

    def copy(self):
        """Creates A Copy Of The Data Set."""
        return data(self.items(), self.gotsort)

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("data", self.units, self.gotsort)

    @rabbit
    def __len__(self):
        """Performs len"""
        return len(self.units)

    @rabbit
    def items(self, sort=False):
        """Returns A List Of Items."""
        if sort:
            return sorted(self.units)
        else:
            return self.units[:]

    def code(self, func):
        """Codes A Function Onto The Data Set."""
        new = []
        for x in self.units:
            new.append(float(func(x)))
        self.units = new

    def extend(self, units):
        """Adds More Data."""
        if isinstance(units, dict):
            for x in units:
                for i in xrange(0, int(units[x])):
                    self.units.append(float(x))
        else:
            for x in units:
                self.units.append(float(x))
        self.gotsort = False

    def sample(self, func=lambda: random().getdigits(1), n=50):
        """Samples From A Function For Data."""
        for i in xrange(0,n):
            self.units.append(float(func()))
        self.gotsort = False

    def distsample(self, func=lambda x: normdist(x, 5.0, 2.0)*50.0, start=0.0, stop=10.0, step=1.0):
        """Samples From A Frequency Distribution Function For Data."""
        start = float(start)
        stop = float(stop)
        step = float(step)
        for x in xrange(0, int((stop-start)/step)):
            x *= step
            x += start
            for y in xrange(0, int(func(x))):
                self.units.append(x)
        self.gotsort = False

    @dirty_rabbit
    def choose(self, gen=None):
        """Returns A Random Value."""
        if gen is None:
            gen = random()
        return gen.choose(self.units)

    @dirty_rabbit
    def take(self, num=None, gen=None):
        """Samples From The Data."""
        if gen is None:
            gen = random()
        if num is None:
            num = len(self)
        return gen.take(self.units)

    def append(self, unit):
        """Adds A Single Data Piece."""
        self.units.append(float(unit))
        self.gotsort = False

    def remove(self, unit):
        """Removes A Single Data Piece."""
        self.units.remove(float(unit))

    def sort(self):
        """Sorts The Data."""
        if not self.gotsort:
            self.units.sort()
            self.gotsort = True

    @rabbit
    def sum(self):
        """Finds The Sum."""
        return sum(self.units)

    @rabbit
    def mean(self):
        """Finds The Arithmetic Mean."""
        return sum(self.units)/float(len(self))

    @rabbit
    def geomean(self):
        """Finds The Geometric Mean."""
        tot = 1.0
        for x in self.units:
            tot *= x
        return tot**(1.0/len(self))

    @rabbit
    def harmean(self):
        """Finds The Harmonic Mean."""
        tot = 0.0
        for x in self.units:
            tot += 1.0/x
        return len(self)/tot

    @rabbit
    def rms(self):
        """Finds The Root Mean Square."""
        out = 0.0
        for x in self.units:
            out += x**2
        return math.sqrt(out/len(self))

    @rabbit
    def mad(self, mean=None):
        """Finds The Mean Absolute Deviation."""
        if mean is None:
            mean = self.mean()
        else:
            mean = float(mean)
        out = 0.0
        for x in self.units:
            out += abs(x-mean)
        return out/len(self)

    @rabbit
    def stdev(self, sample=True, mean=None):
        """Finds The Standard Deviation."""
        if mean is None:
            mean = self.mean()
        else:
            mean = float(mean)
        sample = bool(sample)
        out = 0.0
        for x in self.units:
            out += (x-mean)**2.0
        return math.sqrt(out/(len(self)-float(sample)))

    @rabbit
    def truncmean(self, trunc=0.05):
        """Finds The Truncated Mean."""
        self.sort()
        first = int(float(trunc)*len(self))
        last = len(self)-first
        tot = 0.0
        for x in xrange(first, last):
            tot += self.units[x]
        return tot/(last-first)

    @rabbit
    def devs(self, point=None):
        """Finds The Deviation From A Point."""
        if point is None:
            point = self.mean()
        else:
            point = float(point)
        out = {}
        for x in self.units:
            out[x] = x-point
        return out

    @rabbit
    def freq(self):
        """Returns A Frequency Dictionary."""
        out = {}
        for x in self.units:
            if x in out:
                out[x] += 1
            else:
                out[x] = 1
        return out

    @rabbit
    def relfreq(self):
        """Returns A Relative Frequency Dictionary."""
        out = self.freq()
        for x in out:
            out[x] /= float(len(self))
        return out

    @rabbit
    def cumfreq(self):
        """Returns A Cumulative Frequency Dictionary."""
        out = self.freq()
        items = out.keys()
        items.sort()
        last = 0
        for x in items:
            out[x] += last
            last = out[x]
        return out

    @rabbit
    def mode(self, dev=0.0):
        """Finds The Modes."""
        dev = float(dev)
        freqs = self.freq()
        out = {None:0}
        for x in freqs:
            if freqs[x] == out[None]:
                out[x] = freqs[x]
            elif freqs[x] > out[None]:
                del out[None]
                old = out
                out = {None:freqs[x]}
                for z in old:
                    if old[z] >= out[None]-dev:
                        out[z] = old[z]
                out[x] = freqs[x]
            elif freqs[x] >= out[None]-dev:
                out[x] = freqs[x]
        del out[None]
        out = out.keys()
        out.sort()
        return out

    @rabbit
    def med(self, point=None, sort=True):
        """Finds The Median."""
        if sort:
            self.sort()
        if point is None:
            point = len(self)/2.0
        else:
            point = float(point)
        return (self.units[int(math.floor(point))]+self.units[int(math.ceil(point)-1)])/2.0

    @rabbit
    def quantiles(self, num=3):
        """Finds The Quantiles."""
        self.sort()
        num = int(num)
        if num <= 1:
            raise ValueError
        elif num == 2:
            return self.med(sort=False)
        else:
            dividers = []
            interval = len(self)/float(num+1)
            point = 0
            for x in xrange(0, num):
                point += interval
                dividers.append(self.med(point, sort=False))
            return dividers

    @rabbit
    def iqr(self, num=3):
        """Finds The Inter-Quantile Range."""
        quantiles = self.quantiles(num)
        return quantiles[num-1]-quantiles[0]

    @rabbit
    def max(self):
        """Finds The Maximum."""
        self.sort()
        return self.units[-1]

    @rabbit
    def min(self):
        """Finds The Minimum."""
        self.sort()
        return self.units[0]

    @rabbit
    def full(self, diff=0):
        """Finds The Range."""
        self.sort()
        point = int(diff)
        return self.units[-1*(diff+1)]-self.units[diff]

    @rabbit
    def midrange(self, diff=0):
        """Finds The Mean Of The Minimum And Maximum."""
        return self.full(diff)/2.0

    @rabbit
    def display(self, interval):
        """Creates A Table Of Values."""
        self.sort()
        interval = float(interval)
        point = self.units[0]
        out = str(point)+" - "+str(point+interval)+" | "
        for x in self.units:
            if x > point:
                point += interval
                while x > point:
                    point += interval
                out = out[:-2]+"\n"+str(point)+" - "+str(point+interval)+" | "+str(x)+", "
            else:
                out += str(x)+", "
        return out[:-2]

    @rabbit
    def graph(self, interval, dot="x"):
        """Creates A Dot Plot."""
        self.sort()
        interval = float(interval)
        dot = str(dot)
        point = self.units[0]
        out = ""
        for x in self.units:
            if x > point:
                point += interval
                while x > point:
                    point += interval
                    out += "\n"
                out += "\n"+dot
            else:
                out += dot
        return out

    @rabbit
    def plot(self, scale=None, edge="-", center="_", left="[", right="]", divider="|"):
        """Creates A Box Plot."""
        if scale is None:
            scale = (self.units[-1]-self.units[0])/50.0
        else:
            scale = float(scale)
        if scale <= 0.0:
            return left+divider+right
        else:
            quartiles = self.quantiles()
            first = self.units[0]
            last = self.units[-1]
            toplot = [int((quartiles[0]-first)/scale), int((quartiles[1]-quartiles[0])/scale), int((quartiles[2]-quartiles[1])/scale), int((last-quartiles[2])/scale)]
            return edge*toplot[0] +left+ center*toplot[1] +divider+ center*toplot[2] +right+ edge*toplot[3]

    @rabbit
    def posplot(self, start, end, plotfunc=None, scale=None, edge="-", center="_", left="[", right="]", divider="|", space=" "):
        """Creates A Box Plot Between Two Specific Values."""
        start = float(start)
        end = float(end)
        if scale is None:
            scale = (end-start)/50.0
        else:
            scale = float(scale)
        if scale <= 0.0:
            return left+divider+right
        else:
            first = self.units[0]
            last = self.units[-1]
            toplot = [int((first-start)/scale), int((end-last)/scale)]
            if plotfunc is None:
                plotfunc = self.plot
            return space*toplot[0]+ plotfunc(scale, edge, center, left, right, divider) +space*toplot[1]

    @rabbit
    def modplot(self, scale=None, edge="-", center="_", left="[", right="]", divider="|", point=".", space=" "):
        """Creates A Modified Box Plot."""
        if scale is None:
            scale = (self.units[-1]-self.units[0])/50.0
        else:
            scale = float(scale)
        if scale <= 0.0:
            return left+divider+right
        else:
            quartiles = self.quantiles()
            lowdev = quartiles[0]-(quartiles[2]-quartiles[0])*1.5
            lows = []
            first = self.units[0]
            x = 0
            while first < lowdev:
                lows.append(first)
                x += 1
                first = self.units[x]
            atstart = ""
            for x in xrange(0, len(lows)):
                if x < len(lows)-1:
                    highpoint = lows[x+1]
                else:
                    highpoint = first
                atstart += point+space*int((highpoint-lows[x])/scale)
            updev = quartiles[2]+(quartiles[2]-quartiles[0])*1.5
            ups = []
            last = self.units[-1]
            x = -1
            while last > updev:
                ups.append(last)
                x -= 1
                last = self.units[x]
            atend = ""
            for x in xrange(0, len(ups)):
                if x == 0:
                    belowpoint = last
                else:
                    belowpoint = ups[x-1]
                atend += space*int((ups[x]-belowpoint)/scale)+point
            return atstart+ self.plot(scale, edge, center, left, right, divider) +atend

    @rabbit
    def basic(self, num=3):
        """Finds The Quantiles With The Maximum And Minimum."""
        out = self.quantiles(num)
        out.reverse()
        out.append(self.units[0])
        out.reverse()
        out.append(self.units[-1])
        return out

    @rabbit
    def midhinge(self, num=3):
        """Finds The Mean Of The First And Last Quantiles."""
        out = self.quantiles(num)
        return (out[0]+out[num-1])/2.0

    @rabbit
    def trimean(self):
        """Finds The Trimean."""
        quantiles = self.quantiles()
        return (quantiles[0]+2*quantiles[1]+quantiles[2])/4.0

    @rabbit
    def p(self, result, dev=0):
        """Finds The Proportional Probability Of An Event."""
        correct = 0.0
        for x in self.units:
            if abs(result-x) <= dev:
                correct += 1.0
        return correct/len(self)

    @rabbit
    def funcp(self, testfunc):
        """Finds The Proportional Probability Of A Function."""
        acc = 0.0
        for x in self.units:
            acc += float(testfunc(x))
        return acc/len(self)

    @rabbit
    def rangep(self, start, stop):
        """Finds The Proportional Probability Of A Range."""
        start = float(start)
        stop = float(stop)
        return self.p((start+stop)/2.0, abs(stop-start)/2.0)

    @rabbit
    def finpopcor(self, N):
        """Finds The Finite Population Correction Factor."""
        n = len(self)
        N = float(N)
        return ((N-n)/(N-1))**0.5

    @rabbit
    def medme(self, dev=1.96, N=None):
        """Finds The Rank Margin Of Error For A Median."""
        dev = float(dev)
        n = float(len(self))
        if N is not None:
            dev *= self.finpopcor(N)
        return dev*n**0.5/2.0

    @rabbit
    def meanme(self, dev=1.96, stdev=None, N=None):
        """Finds The Margin Of Error For A Mean."""
        dev = float(dev)
        if stdev is None:
            stdev = self.stdev()
        else:
            stdev = float(stdev)
        n = float(len(self))
        if N is not None:
            stdev *= self.finpopcor(N)
        return dev*stdev/n**0.5

    @rabbit
    def me(self, dev=1.96, num=1.0, stdev=None, N=None):
        """Finds The Margin Of Error For Multiple Of The Same Item."""
        dev = float(dev)
        num = float(num)
        if stdev is None:
            stdev = self.stdev()
        else:
            stdev = float(stdev)
        if N is not None:
            stdev *= self.finpopcor(N)
        return dev*stdev*num**0.5

    @rabbit
    def addme(self, dev=1.96, stdevs=None, N=None):
        """Finds The Margin Of Error For Multiple Different Items."""
        dev = float(dev)
        if stdevs is None:
            stdevs = [self.stdev()]
        elif not islist(stdevs):
            return self.me(dev, stdevs, None, N)
        stdev = 0.0
        for s in stdevs:
            stdev += s**0.5
        stdev **= 0.5
        if N is not None:
            stdev *= self.finpopcor(N)
        return dev*stdev

    @rabbit
    def propme(self, dev=1.96, plist=None, N=None):
        """Finds The Margin Of Error For Proportions."""
        dev = float(dev)
        if plist is None:
            plist = [0.5]
        elif not islist(plist):
            plist = float(p)
        n = float(len(self))
        stdev = 0.0
        for p in plist:
            stdev += p*(1.0-p)/n
        stdev **= 0.5
        if N is not None:
            stdev *= self.finpopcor(N)
        return dev*stdev

    @rabbit
    def var(self):
        """Finds The Variance."""
        return self.stdev()**2.0

    @rabbit
    def cv(self):
        """Finds The Coefficient Of Variation."""
        return self.stdev()/self.mean()

    @rabbit
    def dev(self, point, stdev=None, mean=None):
        """Finds The Standard Deviations From The Mean."""
        point = float(point)
        if stdev is None:
            stdev = self.stdev()
        else:
            stdev = float(stdev)
        if mean is None:
            mean = self.mean()
        else:
            mean = float(mean)
        return abs(mean-point)/stdev


    @rabbit
    def combine(self, other, func=lambda x,y: x+y):
        """Combines Two Data Sets."""
        if islist(other):
            units = other[:]
        elif isinstance(other, dict):
            units = data(other).items()
        else:
            units = other.items()
        new = []
        for x in self.items():
            for y in units:
                new.append(func(x,y))
        return data(new)

    @rabbit
    def chisqn(self, expected, n=None):
        """Calculates Chi Squared Based On Size."""
        expected = float(expected)
        if n is None:
            n = len(self)
        n = float(n)
        return (n-expected)**2.0/expected

    @rabbit
    def chisq(self, expected):
        """Calculates Chi Squared Based On Data."""
        chisum = 0.0
        for x in xrange(0, len(self)):
            chisum += (self.units[x]-expected[x])**2.0/expected[x]
        return chisum

    @rabbit
    def vartest(self, expected):
        """Calculates Chi Squared Based On Variance."""
        return (len(self)-1.0)*self.var()/float(expected)

    @rabbit
    def df(self):
        """Finds The Degrees Of Freedom."""
        return len(self)-1.0

    def tomatrix(self):
        """Creates A Matrix Out Of The Data."""
        return diagmatrixlist(self.items())

    @rabbit
    def teststat(self, expected=0.0, observed=None, mefunc=None):
        """Calculates A z Or t Value For A Hypothesis Test."""
        expected = float(expected)
        if observed is None:
            observed = self.mean()
        else:
            observed = float(observed)
        if mefunc is None:
            mefunc = self.meanme
        return (observed-expected)/float(mefunc(dev=1.0))

    @rabbit
    def skew(self):
        """Finds The Coefficient Of Skewness."""
        mean = float(self.mean())
        tot = 0.0
        for x in self.items():
            tot += (x-mean)**3.0
        return tot/(float(len(self))*float(self.stdev())**3.0)

    @rabbit
    def I(self, med=None, stdev=None):
        """Finds The Spearnan Index Of Skewness."""
        if med is None:
            med = float(self.med())
        else:
            med = float(med)
        if stdev is None:
            stdev = float(self.stdev())
        else:
            stdev = float(stdev)
        mean = float(self.mean())
        return (mean-median)*3.0/stdev

    @rabbit
    def __contains__(self, other):
        """Searches For An Item."""
        if float(other) in self.units:
            return True
        else:
            return False

    @rabbit
    def __repr__(self):
        """Performs str."""
        return str(self.units)

    @rabbit
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, data):
            other.sort()
            self.sort()
            return self.items() == other.items()
        elif islist(other):
            test = other[:]
            test.sort()
            self.sort()
            return self.items() == test
        else:
            return False

    @rabbit
    def __getitem__(self, index, sort=False):
        """Finds An Item."""
        if sort:
            self.sort()
        return self.units[int(index)]

class multidata(mctobject):
    """Implements A Multivariate Data Set."""
    evaltype = "Stats.data"

    def __init__(self, x=None, y=None):
        """Creates A Joint Data Set."""
        if y is None and x is not None:
            if isinstance(x, dict):
                x, y = x.keys(), x.values()
            else:
                nx, ny = [], []
                for tx,ty in x:
                    nx.append(tx)
                    ny.append(ty)
                x = nx
                y = ny
        elif x is None and y is not None:
            x = range(1,len(y)+1)
        if isinstance(x, data):
            self.x = x
        else:
            self.x = data(x)
        if isinstance(y, data):
            self.y = y
        else:
            self.y = data(y)
        self.x.gotsort = True
        self.y.gotsort = True

    def getstate(self):
        """Returns A Pickleable Reference Object."""
        return ("multidata", self.x.units, self.y.units)

    def code(self, func):
        """Codes Over All The Data With A Function."""
        self.x.code(func)
        self.y.code(func)

    def extend(self, x, y):
        """Adds Pairs."""
        self.x.extend(x)
        self.y.extend(y)

    def append(self, x, y):
        """Appends A Pair."""
        self.x.append(x)
        self.y.append(y)

    def remove(self, x, y):
        """Removes A Pair."""
        for n in xrange(0, len(self)):
            if self.x.units[n] == x and self.y.units[n] == y:
                self.x.units.pop(n)
                self.y.units.pop(n)
                return True
        return False

    @rabbit
    def items(self):
        """Returns A List Of Pairs."""
        out = []
        for n in xrange(0, len(self)):
            out.append((self.x.units[n], self.y.units[n]))
        return out

    @rabbit
    def todict(self):
        """Returns A Dictionary Of Pairs."""
        out = {}
        for x,y in self.items():
            out[x] = y
        return out

    @rabbit
    def itemdict(self):
        """Returns A Dictionary Of Items."""
        out = {}
        for x,y in self.items():
            if x in out:
                out[x].append(y)
            else:
                out[x] = [y]
        return out

    @rabbit
    def covar(self):
        """Finds The Covariance."""
        tot = 0.0
        xmean = self.x.mean()
        ymean = self.y.mean()
        for x,y in self.items():
            tot += (x-xmean)*(y-ymean)
        return tot/(len(self)-1.0)

    @rabbit
    def rankdata(self):
        """Creates Data Based On Ranks."""
        tx = self.x.copy()
        tx.gotsort = False
        tx.sort()
        ty = self.y.copy()
        ty.gotsort = False
        ty.sort()
        nx = []
        ny = []
        for i in xrange(0, len(self)):
            nx.append(tx.units.index(self.x.units[i]))
            ny.append(ty.units.index(self.y.units[i]))
        out = getcopy(self)
        out.x.units = nx
        out.y.units = ny
        return out

    @rabbit
    def rs(self):
        """Finds The Spearman Correlation Coefficient."""
        tot = 0.0
        for x,y in self.items():
            tot += (x-y)**2.0
        return 1.0-6.0*tot/(len(self)*(len(self)**2.0-1.0))

    @rabbit
    def r(self):
        """Finds The Corellation Coefficient."""
        return self.covar()/(self.x.stdev()*self.y.stdev())

    @rabbit
    def rsq(self, p=2.0):
        """Finds The Coefficient Of Determination."""
        p = float(p)
        return 1.0 - (1.0-self.r()**2.0) * (len(self)-1.0)/(len(self)-p-1.0)

    @rabbit
    def b(self):
        """Finds The Slope Of The Regression Line."""
        return self.r()*self.y.stdev()/self.x.stdev()

    @rabbit
    def a(self):
        """Finds The Y-Intercept Of The Regression Line."""
        return self.y.mean()-self.b()*self.x.mean()

    @rabbit
    def flip(self):
        """Swaps x And y."""
        self.x, self.y = self.y, self.x

    def copy(self):
        """Creates A Copy Of The Data Set."""
        return multidata(self.x.copy(), self.y.copy())

    @rabbit
    def expdata(self):
        """Takes ln Of All The y Values."""
        new = getcopy(self)
        new.y.code(math.log)
        return new

    @rabbit
    def powdata(self):
        """Takes ln Of All The Values."""
        new = getcopy(self)
        new.y.code(math.log)
        new.x.code(math.log)
        return new

    @rabbit
    def linreg(self):
        """Finds The Linear Regression Line."""
        b = self.b()
        a = self.a()
        return strfunc(e.prepare(a, False, True)+"+"+e.prepare(b, False, True)+"*x", ["x"])

    @rabbit
    def medmed(self):
        """Finds The Median-Median Regression Line."""
        first = multidata(self.items()[0:int(math.floor(len(self)/3.0))])
        mid = multidata(self.items()[int(math.ceil(len(self)/3.0)):int(math.floor(2.0*len(self)/3.0))])
        last = multidata(self.items()[int(math.ceil(2.0*len(self)/3.0)):len(self)])
        xfirst = first.x.med()
        yfirst = first.y.med()
        xmid = mid.x.med()
        ymid = mid.y.med()
        xlast = last.x.med()
        ylast = last.y.med()
        b = (ylast-yfirst)/(xlast-xfirst)
        yhat = b*(xmid-xfirst)+yfirst
        a = yhat + (ymid-yhat)/3.0 - b*xmid
        return strfunc(e.prepare(a, False, True)+"+"+e.prepare(b, False, True)+"*x", ["x"])

    @rabbit
    def poweq(self):
        """Finds The Power Regression Line Given That This Is powdata."""
        a = math.e**self.a()
        b = self.b()
        return strfunc(e.prepare(a, False, True)+"*x^"+e.prepare(b, False, True), ["x"])

    @rabbit
    def expeq(self):
        """Finds The Exponential Regression Line Given That This Is expdata."""
        a = math.e**self.a()
        b = math.e**self.b()
        return strfunc(e.prepare(a, False, True)+"*"+e.prepare(b, False, True)+"^x", ["x"])

    @rabbit
    def powreg(self):
        """Performs Power Regression."""
        return self.powdata().poweq()

    @rabbit
    def expreg(self):
        """Performs Exponential Regression."""
        return self.expdata().expeq()

    @rabbit
    def regs(self):
        """Finds Regression Lines."""
        eqs = {}
        eqs[self.r()] = self.linreg()
        test = self.powdata()
        eqs[test.r()] = test.poweq()
        test = self.expdata()
        eqs[test.r()] = test.expeq()
        return eqs

    @rabbit
    def bestfit(self):
        """Finds The Best Fit Regression Equation."""
        eqs = self.regs()
        test = eqs.keys()
        test.sort()
        return eqs[test[-1]]

    @rabbit
    def resid(self, func, x):
        """Finds A Residual."""
        return func(x)-self.y.units[self.x.units.index(x)]

    @rabbit
    def gof(self, expected="x"):
        """Calculates Chi Squared For Goodness Of Fit."""
        if expected == "x":
            return self.y.chisq(self.x.units)
        elif expected == "y":
            return self.x.chisq(self.y.units)
        else:
            raise ValueError

    @rabbit
    def chisq(self):
        """Calculates Chi Squared For Independence."""
        return self.tomatrix().chisq()

    @rabbit
    def resids(self, func=None):
        """Finds Residuals."""
        if func is None:
            func = self.linreg()
        values = {}
        for z in xrange(0, len(self)):
            values[self.x.units[z]] = func(self.x.units[z])-self.y.units[z]
        return values

    @rabbit
    def se(self, func=None):
        """Calculates The Standard Error Of The Estimate."""
        tot = 0.0
        n = len(self)
        for x in self.resids(func):
            tot += x**2.0/(n-2.0)
        return tot**0.5

    @rabbit
    def sb(self, func=None):
        """Calculates The Standard Error Of The Slope Of A Regression Line."""
        return self.se(func)/(self.x.stdev()*(len(self)-1.0)**0.5)

    @rabbit
    def df(self):
        """Finds The Degrees Of Freedom."""
        return self.x.df()-1.0

    @rabbit
    def dfE(self):
        """Finds The Error Degrees Of Freedom."""
        return self.x.df()+self.y.df()

    def tomatrix(self):
        """Creates A Matrix Out Of The Data."""
        out = matrix(len(self), 2)
        for y in xrange(0, out.y):
            out.store(y,0, self.x[y])
            out.store(y,1, self.y[y])
        return out

    @rabbit
    def regtest(self, func=None, expected=0.0, observed=None, mefunc=None):
        """Finds The t Value For The Slope Of The Regression Line."""
        if func is None:
            func = self.linreg()
        expected = float(expected)
        if observed is None:
            observed = self.b()
        else:
            observed = float(observed)
        if mefunc is None:
            mefunc = self.sb
        return (observed-expected)/float(mefunc(func=func))

    @rabbit
    def __len__(self):
        """Performs len."""
        if len(self.x) >= len(self.y):
            return len(self.x)
        else:
            return len(self.y)

    @rabbit
    def __getitem__(self, index):
        """Retrieves A Data Point."""
        return (self.x.units[index], self.y.units[index])

    @rabbit
    def __eq__(self, other):
        """Performs ==."""
        if isinstance(other, multidata):
            return self.x == other.x and self.y == other.y
        else:
            return self.items() == other

    @rabbit
    def itemcall(self, params):
        """Performs A Colon Call."""
        if len(params) == 0:
            value = self.x.units[0]
        else:
            self.overflow = params[1:]
            if params[0] in self.x.units:
                value = self.y.units[self.x.units.index(params[0])]
            else:
                value = matrix(0)
        return value

def datamatrix(inputmatrix):
    """Converts A Matrix Into Data."""
    inputmatrix = getmatrix(inputmatrix)
    if inputmatrix.x == 2 and not inputmatrix.onlydiag():
        datax = []
        datay = []
        for y in xrange(0, inputmatrix.y):
            datax.append(inputmatrix.retrieve(y,0))
            datay.append(inputmatrix.retrieve(y,1))
        return multidata(datax, datay)
    else:
        return data(inputmatrix.getitems())
