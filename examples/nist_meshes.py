from math import sqrt, log
from numpy import exp, arange, array

from qsnake.mesh import get_mesh_exp_params, mesh_exp

def mesh_nist1_direct(r_min, r_max, N):
    r_min = float(r_min)
    r_max = float(r_max)
    n = arange(N+1)
    a = r_max / r_min
    N = float(N)
    return r_min * a ** (n/N)

def mesh_nist2_direct(a, b, r_max):
    r = []
    n = 1
    while True:
        r_n = a * (exp(b*(n-1)) - 1)
        r.append(r_n)
        if r_n > r_max:
            break
        n += 1
    r = array(r)
    return r[1:]

def mesh_nist3_direct(r_min, r_max, N):
    # Uniform mesh in rho:
    rho = mesh_exp(log(r_min), log(r_max), a=1, N=N)
    r = exp(rho)
    return r

Z = 92
eps = 1e-10

print "NIST meshes used for Uranium"

# 1
r = mesh_nist1_direct(1./(160*Z), 50, 15788)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "1)"
print r_min, r_max, "%e" % a, N

# 2
r = mesh_nist1_direct(1e-6/Z, 800/sqrt(Z), 8000)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "2)"
print r_min, r_max, "%e" % a, N

# 3
# H
#r = mesh_nist2_direct(4.34e-6/1, 0.002304, 50)
# U
r = mesh_nist2_direct(4.34e-6/Z, 0.002304, 50)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "3)"
print r_min, r_max, "%e" % a, N

# 4
r = mesh_nist3_direct(0.01e-4/Z, 50, 2837)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "4)"
print r_min, r_max, "%e" % a, N
