"""
All these functions use the following notation. The n-th point in the grid is
defined on the reference domain [0, 1] as::

    r_n = r_n(N, a, b, c, d, ...)

where::

    0 <= r_n <= 1
    n = 0, 1, 2, ... N
    r_0 = 0
    r_N = 1

    N ... number of elements (intervals) in the mesh
    a, b, c, d .... are additional adjustable parameters

At the end, the mesh is converted to the physical domain/interval
[r_min, r_max] according to the formula:

    r_n_phys = r_n * (r_max - r_min) + r_min

All the meshes are thus translation invariant (the spacing of the points will
be exactly the same, as long as r_max - r_min doesn't change).

The functions return a numpy array "r" with the points. It has the following
properties::

    r[0]   == r_min
    r[-1]  == r_max
    len(r) == N + 1

You can use this module for both finite element meshes as well as grids for
time stepping solvers.

Basic types of meshes:

    mesh_exp()
    mesh_hyp()

Derived meshes (parameters are first converted and then one of the above
functions is called):

    mesh_exp2()
    mesh_hyperbolic()
    mesh_nist1(), mesh_nist1_direct()
    mesh_nist2(), mesh_nist2_direct()

"""

import sys
import math

from numpy import array, arange
import numpy

from cmesh import mesh_exp

def mesh_exp2(r_min, r_max, a, N):
    """
    Calculates the exponential mesh using a formula:

    r_n = (a**(n/N) - 1) / (a - 1)

    with a > 1. By substitution a -> a**((N-1.)/N), we can just call
    mesh_exp().

    """
    a = float(a)
    assert a > 1
    assert N >= 1
    return mesh_exp(r_min, r_max, a**((N-1.)/N), N)

def mesh_hyp(r_min, r_max, a, N):
    """
    Calculates hyperbolic mesh.

    It uses a formula:

    r_n = n * (a - 1) / (a*N - n)

    with a > 1.

    """
    a = float(a)
    assert a > 1
    assert N >= 1
    n = arange(N+1)
    exp = numpy.exp
    log = math.log
    r = n * (a - 1) / (a*N - n)

    def ref2phys(r, r_min, r_max):
        return r * (r_max - r_min) + r_min

    return ref2phys(r, r_min, r_max)

def mesh_hyperbolic(ap, jm, N):
    """
    Calculates the hyperbolic mesh using the formula:

    r_n_phys = ap * n / (jm - n)

    for n = 0, 1, 2, ... N.

    This formula is obtained from mesh_hyp() using:

    r_min = 0
    r_max = ap * N / (jm - N)
    a = jm / N

    """

    ap = float(ap)
    jm = float(jm)

    r_min = 0
    r_max = ap * N / (jm - N)
    a = jm / N

    return mesh_hyp(r_min, r_max, a, N)

def mesh_hyperbolic_direct(ap, jm, N):
    """
    Calculates the hyperbolic mesh using the formula directly:

    r_n_phys = ap * n / (jm - n)

    for n = 0, 1, 2, ... N.
    """

    n = arange(N+1)
    ap = float(ap)
    jm = float(jm)
    return ap * n / (jm - n)

def get_mesh_exp_params(r):
    """
    Obtains the mesh parameters from a given mesh "r".

    This assumes that the mesh "r" is exponential. Only the first two and the
    last two point values are used (and the length of the array "r").
    """
    r_min = r[0]
    r_max = r[-1]
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    N = len(r) - 1
    return r_min, r_max, a, N

def mesh_nist1(r_min, r_max, N):
    """
    Calculates the NIST I mesh.

    Uses the formula in physical domain [r_min, r_max]:

    r_n_phys = r_min * (r_max/r_min)**(n/N)

    which is obtained from mesh_exp2() by substituting a = r_max / r_min.

    """
    r_min = float(r_min)
    r_max = float(r_max)
    assert r_max > r_min
    assert r_min > 0
    a = r_max / r_min
    return mesh_exp2(r_min, r_max, a, N)

def mesh_nist1_direct(r_min, r_max, N):
    """
    Calculates the NIST I mesh.

    Uses the formula in physical domain directly:

    r_n_phys = r_min * (r_max/r_min)**(n/N)

    This function is equivalent to mesh_nist1() and is meant for testing
    purposes only.

    """
    r_min = float(r_min)
    r_max = float(r_max)
    n = arange(N+1)
    a = r_max / r_min
    N = float(N)
    return r_min * a ** (n/N)

def mesh_nist2(a, b, N):
    """
    Calculates the NIST II mesh.

    Uses a formula::

    r_n_phys = a * (exp(b*n) - 1)

    for n = 0, 1, ..., N.

    This formula is obtained from mesh_exp2(r_min, r_max, a, N) by a
    substituation:

    r_min = 0
    r_max = a * (exp(b*N) - 1)
    a = exp(b*N)

    In other words, by choosing the parameters "a, b, N", the domain is set to
    [0, a * (exp(b*N) - 1)] and the parameter "a" in mesh_exp2() (don't confuse
    it with a parameter of this function of the same name) is set to
    a=exp(b*N).

    """
    exp = math.exp
    r_min = 0
    r_max = a * (exp(b*N) - 1)
    return mesh_exp2(r_min, r_max, exp(b*N), N)

def mesh_nist2_direct(a, b, N):
    """
    Calculates the NIST II mesh directly.

    Uses the formula in physical domain directly:

    r_n_phys = a * (exp(b*n) - 1)

    This function is equivalent to mesh_nist2() and is meant for testing
    purposes only.

    """
    exp = numpy.exp
    n = arange(N+1)
    r = a * (exp(b*(n-1)) - 1)
    return r[2:]

def mesh_nist3_direct(r_min, r_max, N):
    """
    Calculates the NIST III mesh directly.

    """
    exp = numpy.exp
    log = math.log
    # Uniform mesh in rho:
    rho = mesh_exp(log(r_min), log(r_max), a=1, N=N)
    r = exp(rho)
    return r

def mesh_elk_direct(sprmin, rmt, sprmax, nrmt, lradstp=4):
    """
    Calculates the Elk radial mesh.

    'sprmin, rmt, sprmax, nrmt' parameters are read from the species file.

    For example Pb.in contains:

      0.220863E-06    2.0000   42.8183   700    : sprmin, rmt, sprmax, nrmt

    And these paremeters need to be fed into mesh_elk_direct() to produce the
    mesh. The 'lradstp' is a paremeter in Elk, and it is used to adjust the
    number of points in the mesh.

    """

    log = math.log
    exp = numpy.exp

    # This is what is done inside Elk, so we need to do it as well:
    # ! make the muffin-tin mesh commensurate with lradstp
    nrmt -= (nrmt - 1) % lradstp

    t1 = log(sprmax/sprmin) / log(rmt/sprmin)
    t2 = (nrmt-1)*t1
    spnr = int(t2) + 1

    t1 = 1. / (nrmt-1)
    t2 = log(rmt/sprmin)
    n = arange(spnr)
    r = sprmin * exp(n*t1*t2)

    return r

def n_minimize(f, t, method="automatic"):
    from scipy.optimize import fmin, fmin_l_bfgs_b, fminbound
    a0, a_min, a_max = t

    _minimum = [None]
    if method == "automatic":
        method = "simplex"

    def _f(a):
        if method in ["simplex", "l-bfgs-b"]:
            assert len(a) == 1
            a = a[0]
        sys.stdout.write(".")
        sys.stdout.flush()
        if method == "simplex":
            a = a_min + math.exp(a)
        r = f(a)
        if _minimum[0] is None:
            _minimum[0] = [a, r]
            print "\nMinimum: f(%f) = %e" % (a, r)
        elif r < _minimum[0][1]:
            _minimum[0] = [a, r]
            print "\nMinimum: f(%f) = %e" % (a, r)
        return r

    if method == "simplex":
        assert a_max is None
        a0 = math.log(a0 - a_min)
        r = fmin(_f, a0)
        return _minimum[0]
    elif method == "l-bfgs-b":
        r = fmin_l_bfgs_b(_f, [a0], bounds=[(a_min, a_max)],
                approx_grad=True)
        return _minimum[0]
    elif method == "brent":
        if a_max is None:
            a_max = 1e12
        r = fminbound(_f, a_min, a_max)
        return _minimum[0]
    else:
        raise ValueError("Unknown method")
