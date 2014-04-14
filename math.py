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
import math

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def gcd(a, b):
    """Calculates The Greatest Common Denominator Of Two Numbers."""
    if a == 0:
        return b
    else:
        return gcd(b%a, a)

def lcm(a, b, maxtries=float("inf")):
    """Calculates The Least Common Multiple Of Two Numbers."""
    xa = a
    xb = b
    x = 0
    while xa != xb and x < maxtries:
        if xa < xb:
            xa += a
        elif xb < xa:
            xb += b
        x += 1
    return xa

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
        while x <= int(math.sqrt(float(checknumber))):
            if checknumber % x == 0:
                return False
            x += 2
    return True

def factor(checknumber):
    """Determines The Factors Of A Number."""
    checknumber = int(checknumber)
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
    checknumber = int(checknumber)
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
    a = float(a)
    b = float(b)
    c = float(c)
    discriminant = b*b-4.0*a*c
    if discriminant < 0:
        return None, None
    elif discriminant == 0:
        return -b/(2.0*a), None
    else:
        return (-b+math.sqrt(discriminant))/(2.0*a), (-b-math.sqrt(discriminant))/(2.0*a)

def iroots(a, b, c):
    """Determines The Complex Roots Of A Quadratic."""
    a = float(a)
    b = float(b)
    c = float(c)
    discriminant = b*b-4.0*a*c
    if discriminant == 0:
        return -b/(2.0*a), None
    else:
        return (-b+isqrt(discriminant))/(2.0*a), (-b-isqrt(discriminant))/(2.0*a)

def perm(n, k):
    """Determines The Possible Number Of Permutations In n Choose k."""
    n = float(n)
    k = float(k)
    return float(factorial(n))/float(factorial(n-k))

def comb(n, k):
    """Determines The Possible Number Of Combinations In n Choose k."""
    n = float(n)
    k = float(k)
    return perm(n,k)/float(factorial(k))

def deriv(func, x, n=1, accuracy=0.0001, scaledown=1.25):
    """Finds The nth Derivative Of A Function At x."""
    n = int(n)
    x = float(x)
    if n <= 0:
        return func(x)
    else:
        accuracy = float(accuracy)
        scaledown = float(scaledown)
        return (deriv(func, x+accuracy, n-1, accuracy/scaledown, scaledown) - deriv(func, x, n-1, accuracy/scaledown, scaledown))/accuracy

def defint(func, start, stop, accuracy=0.0001):
    """Finds The Definite Integral Of A Function From start To stop."""
    start = float(start)
    accuracy = float(accuracy)
    step = (float(stop)-start)*accuracy
    out = 0.0
    try:
        last = func(start)
    except:
        last = None
    for x in xrange(0, int(1.0/accuracy)):
        start += step
        try:
            new = func(start)
        except:
            new = last
        if last == None:
            out += step*new
        else:
            out += step*(last+new)/2.0
        last = new
    return out

def factorial(x):
    """Implements The Factorial Function Over 0, The Positive Integers, And The Half-Integers."""
    if x == -0.5:
        return math.pi**0.5
    elif x-0.5 == int(x-0.5):
        return x*factorial(x-1.0)
    else:
        return math.factorial(x)

def gamma(n, accuracy=0.00000001, stop=None):
    """Implements The Gamma Function Over The Positive Numbers."""
    n = float(n)
    accuracy = float(accuracy)
    if stop == None:
        stop = -n*math.log(accuracy**(1/n)/n)/math.log(2.0)
    return defint(lambda x: x**(n-1.0)*math.e**(-1.0*x), 0.0, stop)
