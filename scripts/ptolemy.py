#!/usr/bin/env python
"""
Handles map calculations
"""
from util import *
from math import sqrt

gps = GPS()

def ENError(X, Y, Z, psrX, psrY, psrZ):
    """set the true position as the origin and get position as error"""
    origin  = (X, Y, Z)
    ecef = (psrX, psrY, psrZ)
    n, e, _ = gps.ecef2ned(ecef, origin)
    return euclideanDistance((n, e))
