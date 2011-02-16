"""
Calculates the angle in the H20 molecule.
"""
from numpy import array, dot
from numpy.linalg import norm
from math import acos, pi
s_example = """
  0 H     2.8192    2.0459    2.0000
  1 H     1.4760    2.7489    2.0000
  2 O     1.8789    1.8823    2.0000
"""
s = """
  0 H     2.8136    2.0878    2.0000
    1 H     1.4548    2.7370    2.0000
      2 O     1.8785    1.8849    2.0000
"""

s = s.split()
s = s[2:5]+s[7:10]+s[12:15]
s = [float(x) for x in s]
a = array(s[:3])
b = array(s[3:6])
c = array(s[6:])
#a = array([1.7601, 2.9270, 2.0000])
#b = array([2.9575,    2.0000,    2.0000])
#c = array([2, 2, 2.])
x = a-c
y = b-c
print norm(x), norm(y), "(exact: 0.9584)"
x = x/norm(x)
y = y/norm(y)
print acos(dot(x, y)) / pi * 180, "(exact: 104.45)"
