from math import log
from numpy import array, arange, exp
from scipy.optimize import fmin
from sympy.physics.hydrogen import E_nl_dirac

from elk.pyelk import rdirac
from elk.mesh import mesh_log, get_params_log, mesh_elk_direct

def fmin_pos(f, x0):

    def _f(a):
        assert len(a) == 1
        a = a[0]
        a = 1 + exp(a)
        return f(a)

    a0 = log(x0-1)
    return fmin(_f, a0)

# orig:
sprmin = 0.220863E-06
rmt = 2.0000
sprmax = 42.8183
nrmt = 700

# new:
sprmin = 1e-10
nrmt = 3000

r0 = mesh_elk_direct(sprmin, rmt, sprmax, nrmt)


Z = 82
r_min, r_max, a, N = get_params_log(r0)

print r_min, r_max, a, N
N = 5382
a = 7928200510.27

def f(a):
    print "Evaluating a =", a
    print "Mesh parameters:"
    print "r_min =", r_min
    print "r_max =", r_max
    print "a =", a
    print "N =", N
    r = mesh_log(r_min, r_max, a, N)
    print r


    # Potential:
    vr = -Z/r

    # Speed of light taken from:
    # http://arxiv.org/abs/1012.3627
    #c = 137.035999037

    # Elk value:
    c  = 137.035999679

    # Polynomial degree for predictor-corrector:
    np = 4

    tot_error = -1
    # (n, l):
    # either k == l, or k == l + 1:
    for n in range(1, 7):
        for l in range(0, n):
            k_list = []
            if l > 0:
                k_list.append(l)
            k_list.append(l+1)

            for k in k_list:
                # Initial guess:
                E = -1.0
                E, g, f = rdirac(c, n, l, k, np, r, vr, E)
                E_exact = E_nl_dirac(n, l, spin_up=(k == l+1), Z=Z, c=c)
                delta = abs(E-E_exact)
                if delta > tot_error:
                    tot_error = delta
                print ("(n=%d, l=%d, k=%d): E_calc=%12.6f    E_xact=%12.6f    " + \
                                                        "delta=%9.2e") % (n, l, k, E, E_exact, delta)
    print "tot_error = ", tot_error

    return tot_error


#print fmin_pos(f, a_orig)
print f(a)
#print f(a_min)
