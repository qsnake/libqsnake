"""
Calculates the angle in the H20 molecule.
"""
from numpy import array, dot
from numpy.linalg import norm
from math import acos, pi
s = """
           1     O [    0.0000000000    -0.0649996069     0.0000000000]
           2     H [    0.7570792742     0.5284727939     0.0000000000]
           3     H [   -0.7570792742     0.5284727939     0.0000000000]
"""
s = s.replace("[", "")
s = s.replace("]", "")
s = s.split()
s = s[2:5]+s[7:10]+s[12:15]
s = [float(x) for x in s]
a = array(s[:3])
b = array(s[3:6])
c = array(s[6:])
#a = array([1.7601, 2.9270, 2.0000])
#b = array([2.9575,    2.0000,    2.0000])
#c = array([2, 2, 2.])
x = a-b
y = a-c
print norm(x), norm(y), "(exact: 0.9584)"
x = x/norm(x)
y = y/norm(y)
print acos(dot(x, y)) / pi * 180, "(exact: 104.45)"
