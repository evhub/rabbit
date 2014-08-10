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

from .math import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def updateP(priorP, Pe_h, Pe_nh):
    """Performs Bayes's Theorem."""
    return priorP*Pe_h / (priorP*Pe_h + Pe_nh*(1-priorP))

def priorP(bits=1.0, total=1.0):
    """Determines The Propper Prior Probability Of A Hypothesis."""
    return 2.0**(-bits)/total

def binomP(n, p, x):
    """Determines The Probability Of p Happening x Times In n Bionomial Trials."""
    return comb(n,x) * p**x * (1.0-p)**(n-x)

def binomE(n, p):
    """Determines The Mean Of The Binomial Distribution Given."""
    return n*p

def binomstdev(n, p):
    """Determines The Standard Deviation Of n Binomial Trials With Probability Of Success Equal To p."""
    return (n*p*(1.0-p))**0.5

def poissonP(np, x):
    """Calculates The Poisson Approximation Of The Binomial."""
    return np**x*math.e**(-1.0*np)/factorial(x)

def poissonE(np):
    """Determines The Mean Of The Given Poisson Distribution."""
    return np

def poissonstdev(np):
    """Determines The Standard Deviation Of The Given Poisson Distribution."""
    return np**0.5

def geoP(p, x):
    """Determines The Probability Of It Taking x Times For p To Happen."""
    return (1.0-p)**(x-1.0) * p

def geoE(p):
    """Determines The Mean Of The Geometric Distribution Given."""
    return 1.0/p

def hypgeoP(k, n, K, N):
    """Determines The Probability Of k Successes In n Draws From A Population N Containing K Successes."""
    return comb(K,k)*comb(N-K,n-k)/comb(N,n)

def hypgeoE(n, K, N):
    """Determines The Mean Of The Hypergeometric Distribution Given."""
    return binomE(n, K/N)

def hypgeostdev(n, K, N):
    """Determines The Standard Deviation Of The Hypergeometric Distribution Given."""
    return binomstdev(n, K/N) * ((N-n)/(N-1.0))**0.5

def birthdayP(n, x):
    """Determines The Probability Of An Overlap With N Possible States And X Being Used."""
    return perm(n, x)/n**x

def normdist(x, mean=0.0, stdev=1.0):
    """Implements The Normal Distribution."""
    return 1.0/(stdev*math.sqrt(2.0*math.pi)) * math.e**(-1.0*(x-mean)**2.0/(2.0*stdev**2.0))

def normP(start, stop, mean=0.0, stdev=1.0):
    """Finds The Cumulative Probability Between Two z Values."""
    return defint(lambda x: normdist(x, mean, stdev), start, stop)

def tstdev(df):
    """Determines The Standard Deviation Of The t Distribution Given."""
    return (df/(df-2.0))**0.5

def tdist(x, df):
    """Implements The t Distribution For The Given Degrees Of Freedom"""
    n = v+1.0
    return gamma(n/2.0) / ((math.pi*v)**0.5 * gamma(v/2.0) * (1.0+x**2.0/v)**(n/2.0))

def teq(df, e):
    """Finds The t Distribution For The Given Degrees Of Freedom."""
    n = v+1.0
    return strfunc(e.prepare(gamma(n/2.0) / ((math.pi*v)**0.5 * gamma(v/2.0))) + "/" + "(1+x^2/" + e.prepare(v) + ")^" + e.prepare(n/2.0), e, ["x"])

def tP(start, stop, df, e):
    """Finds The Cumulative Probability Between Two t Values."""
    eq = teq(df, e)
    return defint(lambda x: eq.call([x]), start, stop)

def chisqE(df):
    """Determines The Mean Of The Chi Squared Distribution Given."""
    return df

def chisqstdev(df):
    """Determines The Standard Deviation Of The Chi Squared Distribution Given."""
    return (2.0*df)**0.5

def chisqmode(df):
    """Determines The Mode Of The Chi Squared Distribution Given."""
    return df-2.0

def chisqmed(df):
    """Determines The Median Of The Chi Squared Distribution Given."""
    return df-2.0/3.0

def chisqdist(x, df):
    """Implements The Chi Squared Distribution For The Given Degrees Of Freedom"""
    return x**((v-2.0)/2.0)*math.e**(-1.0*x/2.0)*2.0**(-1.0*v/2.0)/gamma(v/2.0)

def chisqeq(df, e):
    """Finds The Chi Squared Distribution For The Given Degrees Of Freedom."""
    return strfunc("x^"+e.prepare((v-2.0)/2.0)+"*e^(-x/2)/"+e.prepare(2.0**(v/2.0)*gamma(v/2.0)), e, ["x"])

def chisqP(stop, df, e):
    """Finds The Probability Beyond A Chi Squared Value."""
    return 1.0-defint(lambda x: eq.call([x]), 0.0, stop)

def FE(dfE):
    """Determines The Mean Of The F Distribution Given."""
    return w/(w-2.0)

def Fdist(x, dfT, dfE):
    """Implements The F Distribution For The Given Degrees Of Freedom."""
    return gamma((v+w)/2.0)*(v/w)**(v/2.0)*x**((v-2.0)/2.0)/(gamma(v/2.0)*gamma(w/2.0)*(1+x*v/w)**((v+w)/2.0))

def Feq(dfT, dfE, e):
    """Finds The F Distribution For The Given Degrees Of Freedom."""
    return strfunc(e.prepare((v/w)**(v/2.0)*gamma((v+w)/2.0)/(gamma(v/2.0)*gamma(w/2.0)))+"*x^"+e.prepare((v-2.0)/2.0)+"/(1+"+e.prepare(v/w)+"x)^"+e.prepare((v+w)/2.0), e, ["x"])

def FP(stop, dfT, dfE, e):
    """Finds The Probability Beyond An F Value."""
    eq = Feq(dfT, dfE, e)
    return 1.0-defint(lambda x: eq.call([x]), 0.0, stop)

def contmean(func, start=-20.0, stop=20.0, accuracy=0.0001):
    """Finds The Mean Of A Continous Function."""
    return defint(lambda x: func(x)*x, start, stop, accuracy)

def contstdev(func, start=-20.0, stop=20.0, mean=None, accuracy=0.0001):
    """Finds The Standard Deviation Of A Continuous Function."""
    if mean is None:
        mean = contmean(func, start, stop, accuracy)
    return defint(lambda x: func(x)*(x-mean)**2.0, start, stop, accuracy)**0.5
