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

from .obj import *
import math

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def succ(x=0):
    """Calculates The Successor Number."""
    return 1+x

def gcd(a, b):
    """Calculates The Greatest Common Denominator Of Two Numbers."""
    if not a:
        return b
    else:
        a = abs(a)
        b = abs(b)
        return gcd(b%a, a)

def lcm(a, b):
    """Calculates The Least Common Multiple Of Two Numbers."""
    if not (a or b):
        return 0
    else:
        a = abs(a)
        b = abs(b)
        return a*b/gcd(a,b)

def isqrt(inputnum):
    """Performs sqrt In The Complex Plane."""
    if inputnum >= 0:
        return math.sqrt(inputnum)
    else:
        return complex(0, math.sqrt(-inputnum))

def isprime(checknumber):
    """Determines If A Number Is Prime."""
    isprime = 0
    if checknumber % 2 == 0:
        if checknumber != 2:
            return False
    else:
        x = 3
        while x <= int(math.sqrt(checknumber)):
            if checknumber % x == 0:
                return False
            x += 2
    return True

def factor(checknumber):
    """Determines The Factors Of A Number."""
    if checknumber < 0:
        checknumber *= -1
        factorlist = [-1]
    else:
        factorlist = [1]
    for x in xrange(2, int(math.sqrt(checknumber))+1):
        if checknumber % x == 0:
            factorlist.append(x)
    templist = factorlist
    for x in templist:
        test = checknumber/x 
        if test not in factorlist:
            factorlist.append(test)
    return factorlist

def primefactor(checknumber):
    """Determines The Prime Factors Of A Number."""
    if checknumber < 0:
        checknumber *= -1
        extra = [-1]
    else:
        extra = []
    factorlist = factor(checknumber)
    factorlist.remove(1)
    newfactorlist = []
    for x in factorlist:
        if isprime(x):
            newfactorlist.append(x)
    if newfactorlist != []:
        factorlist = []
        while checknumber != 1:
            for x in newfactorlist:
                if checknumber % x == 0:
                    checknumber /= x
                    factorlist.append(x)
    return extra+factorlist

def roots(a, b, c):
    """Determines The Real Roots Of A Quadratic."""
    discriminant = b*b-4*a*c
    if discriminant < 0:
        return None, None
    elif discriminant == 0:
        return -b/(2*a), None
    else:
        return (-b+math.sqrt(discriminant))/(2*a), (-b-math.sqrt(discriminant))/(2*a)

def iroots(a, b, c):
    """Determines The Complex Roots Of A Quadratic."""
    discriminant = b*b-4*a*c
    if discriminant == 0:
        return -b/(2*a), None
    else:
        return (-b+isqrt(discriminant))/(2*a), (-b-isqrt(discriminant))/(2*a)

def perm(n, k):
    """Determines The Possible Number Of Permutations In n Choose k."""
    return factorial(n)/factorial(n-k)

def comb(n, k):
    """Determines The Possible Number Of Combinations In n Choose k."""
    return perm(n,k)/factorial(k)

def deriv(func, x, n=1, accuracy=0.0001, scaledown=1.25):
    """Finds The nth Derivative Of A Function At x."""
    n = int(n)
    if n <= 0:
        return func(x)
    else:
        return (deriv(func, x+accuracy, n-1, accuracy/scaledown, scaledown) - deriv(func, x, n-1, accuracy/scaledown, scaledown))/accuracy

def defint(func, start, stop, accuracy=0.0001, strict=False):
    """Finds The Definite Integral Of A Function From start To stop."""
    if strict:
        step = accuracy
        endpoint = int((stop-start)/accuracy)+1
    else:
        start += accuracy
        step = (stop-start)*accuracy
        endpoint = int(1/accuracy)
    out = 0
    for x in xrange(0, endpoint):
        point = func(start)
        if x == 0 or x == endpoint:
            point /= 2
        out += step*point
        start += step
    return out

def polar_defint(func, start, stop, accuracy=0.0001, strict=False):
    """Performs A Polar Definite Integral."""
    return defint(lambda x: func(x)**2, start, stop, accuracy, strict)/2

def length_defint(func, start, stop, accuracy=0.0001, strict=False, scaledown=1.25):
    """Performs A Length Definite Integral."""
    return defint(lambda x: isqrt(1+deriv(func, x, accuracy=accuracy, scaledown=scaledown)**2))

def simpson(func, start, stop):
    """Uses Simpson's Rule To Approximate The Definite Integral."""
    return (func(start) + 4*func((start+stop)/2) + func(stop)) * (stop-start)/6

def simpson2(func, start, stop):
    """Uses Simpson's 3/8ths Rule To Approximate The Definite Integral."""
    return (func(start) + 3*func((2*start+stop)/3) + 3*func((start+2*stop)/3) + func(stop)) * (stop-start)/8

def Bnum(n):
    """Calculates The nth Second Bernouli Number."""
    n = int(n)
    a = {}
    for m in xrange(0, n+1):
        a[m] = 1/(m+1)
        for j in reversed(xrange(1, m+1)):
            a[j-1] = j*(a[j-1] - a[j])
    return a[0]

def Bpoly(n, x):
    """Calculates The nth Second Bernouli Polynomial."""
    n = int(n)
    out = 0
    for k in xrange(0, n+1):
        out += comb(n,k)*Bnum(n-k)*x**float(k)
    return out

def PBpoly(n, x):
    """Calculates The nth Second Periodic Bernouli Polynomial."""
    n = int(n)
    return Bpoly(n, x-math.floor(x))

def eulermaclaurin(func, start, stop, p=2, R=True, accuracy=0.0001, scaledown=1.25):
    """Calculates The Error Of The Strict Definite Integral Approximation With An Accuracy Of 1."""
    p = int(p)
    out = 0
    for k in xrange(2, p+1):
        out -= (deriv(func, start, k-1, accuracy, scaledown) - deriv(func, start, k-1, accuracy, scaledown))*Bnum(k)/math.factorial(k)
    if R:
        out -= defint(lambda x: deriv(func, x, 2*p, accuracy, scaledown)*PBpoly(2*p, x)*x/math.factorial(2*p+1), start, stop, accuracy)
    return out

def factorial(x):
    """Implements The Factorial Function Over 0, The Positive Integers, And The Half-Integers."""
    if x == -0.5:
        return math.pi**0.5
    elif x > 0 and x-0.5 == int(x-0.5):
        return x*factorial(x-1)
    else:
        return math.factorial(x)

def gamma(n, accuracy=0.00000001, stop=None):
    """Implements The Gamma Function Over The Positive Numbers."""
    if stop is None:
        stop = -n*math.log(accuracy**(1/n)/n)/math.log(2)
    return defint(lambda x: x**(n-1)*math.e**(-1*x), 0, stop)

def stirling(n):
    """Implements The Stirling Approximation Of The Factorial."""
    return n**n*isqrt(2*math.pi*n)/math.e**n

def knuth(a, b, n):
    """Implements The Knuth Up-Arrow Operator."""
    n = int(n)
    if n < 0:
        raise IndexError("Can't perform Knuth up-arrow with n="+str(n))
    elif n == 0:
        return a * b
    elif b == 0:
        return 1
    elif n == 1:
        return a ** b
    elif int(a) != a or int(b) != b or a < 0 or b < 0:
        raise ValueError("Knuth up-arrow is only defined over the positive integers")
    else:
        return knuth(a, knuth(a, b-1, n), n-1)

def E10(x):
    """Implements 1e(x)."""
    return 10**x

def collatz(n, out=None):
    """Implements The Collatz Function."""
    if out is None:
        out = []
    if n in out:
        return out+[n]
    else:
        out.append(n)
        if n%2 == 0:
            return collatz(n//2, out)
        else:
            return collatz(n*3+1, out)

def agnesi(x):
    """Implements The Witch Of Agnesi."""
    return 1/(1+x**2)

def taylor_terms(f, p=0, n=5, accuracy=0.0001, scaledown=1.25):
    """Terms Of The Taylor Series."""
    for i in xrange(0, n):
        coef = deriv(f, p, i, accuracy, scaledown)/math.factorial(i)
        yield lambda x: coef*(x-p)**i
def taylor(f, p=0, n=5, accuracy=0.0001, scaledown=1.25):
    """Returns The Taylor Expansion For The Function."""
    terms = taylor_terms(f, p, n, accuracy, scaledown)
    def expansion(x):
        """The Series Expansion Of A Function."""
        return sum((term(x) for term in terms))
    return expansion
def maclaurin(f, n=5, accuracy=0.0001, scaledown=1.25):
    """Returns The Maclaurin Series For The Function."""
    return taylor(f, 0, n, accuracy, scaledown)

def LHopital(n, top, bot, accuracy=0.0001, scaledown=1.25):
    """Uses L'Hopital To Solve lim[x->n](top(x)/bottom(x))."""
    vtop = top(n)
    vbot = bot(n)
    i = 1
    while vtop == 0 and vbot == 0:
        vtop = deriv(top, n, i, accuracy, scaledown)
        vbot = deriv(bot, n, i, accuracy, scaledown)
        i += 1
    return vtop/vbot

def alternate(i, term):
    """Alternates A Term By i."""
    if i%2 == 0:
        return term
    else:
        return -term

def exp_term(x, i):
    """Term Of The Series For e**x."""
    return x**i/math.factorial(i)
def exp_series(x, n):
    """Expansion Of The Series For e**x."""
    return sum((exp_term(x, i) for i in xrange(0, n)))

def sin_term(x, i):
    """Term Of The Series For sin(x)."""
    n = 2*i+1
    return alternate(i, exp_term(x, n))
def sin_series(x, n):
    """Expansion Of The Series For sin(x)."""
    return sum((sin_term(x, i) for i in xrange(0, n)))

def cos_term(x, i):
    """Term Of The Series For cos(x)."""
    n = 2*i
    return alternate(i, exp_term(x, n))
def cos_series(x, n):
    """Expansion Of The Series For cos(x)."""
    return sum((cos_term(x, i) for i in xrange(0, n)))

def atan_term(x, i):
    """Term Of The Series For atan(x)."""
    n = 2*i+1
    return alternate(i, x**n/n)
def atan_series(x, n):
    """Expansion Of The Series For atan(x)."""
    return sum((atan_term(x, i) for i in xrange(0, n)))

def polarline(m, b):
    """Converts A Slope Y-Intercept Line To Polar.""""
    return lambda theta: b/(math.sin(theta)-m*math.cos(theta))

def sqcos(x):
    """Calculates cos(x)**2."""
    return (1+math.cos(2*x))/2

def sqsin(x):
    """Calculates sin(x)**2."""
    return (1-math.cos(2*x))/2
