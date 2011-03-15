from numpy cimport ndarray
from numpy import empty

from fmesh_wrapper cimport c_mesh_hyp, c_mesh_exp

def mesh_hyp(double r_min, double r_max, double a, int N):
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    c_mesh_hyp(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh

def mesh_exp(double r_min, double r_max, double a, int N):
    """
    Creates an exponential mesh.

    Example::

    >>> mesh_exp(0, 100, a=20, N=4)
    array([   0.        ,    3.21724644,   11.95019684,   35.65507127,  100.        ])
    >>> mesh_exp(0, 100, a=40, N=4)
    array([   0.        ,    1.78202223,    7.87645252,   28.71911092,  100.        ])
    >>> mesh_exp(0, 100, a=100, N=4)
    array([   0.        ,    0.78625046,    4.43570179,   21.37495437,  100.        ])

    Here:

        r_n = (a**(n/(N-1)) - 1) / (a**(N/(N-1)) - 1)

    which can be obtain from the following "classic" exponential formula by
    using a -> a ** (N/(N-1))::

        r_n = (a**(n/N) - 1) / (a - 1)

    The meaning of the parameter "a" is the ratio of lenghts of the last and
    first elements. I.e.::

        a = (r_N - r_(N-1)) / (r_1 - r_0)

    as can be checked by easy calculation.

    The advantage of this formula is that the meaning of "a" is very physical.
    From any exponential mesh, one can quickly calculate "a" by simply taking
    the fraction of the largest/smallest element in the mesh.

    The actual formula used for evaluation of the mesh points is:

        r_n = (exp(n*log(a)/(N-1)) - 1) / (a**(N/(N-1)) - 1)

    So that we can reuse the exp() function, which is very fast and robust.

    """
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    c_mesh_exp(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh
