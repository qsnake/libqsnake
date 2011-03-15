from sympy.physics.hydrogen import E_nl_dirac

from elk.pyelk import rdirac
from qsnake.mesh import mesh_exp

def f(a):
    # Mesh:
    #r = create_hyperbolic_grid(rmin=5e-8, rmax=20, k0=30000)
    #r = create_log_mesh(a=1e-5, b=100, par=10000, n_elem=10000)
    r = mesh_exp(r_min=1e-8, r_max=50, a=a, N=1000)

    Z = 82

    # Potential:
    vr = -Z/r

    # Speed of light taken from:
    # http://arxiv.org/abs/1012.3627
    c = 137.035999037

    # Polynomial degree for predictor-corrector:
    np = 2

    tot_error = -1
    # (n, l):
    # either k == l, or k == l + 1:
    for n in range(1, 5):
        for l in range(0, n):
            k_list = []
            if l > 0:
                k_list.append(l)
            k_list.append(l+1)

            for k in k_list:
                # Initial guess:
                E = -1.0
                E, R = rdirac(c, n, l, k, np, r, vr, E)
                E_exact = E_nl_dirac(n, l, spin_up=(k == l+1), Z=Z, c=c)
                delta = abs(E-E_exact)
                if delta > tot_error:
                    tot_error = delta

    return tot_error

def test_precision1():
    assert f(20000) < 0.1
