from numpy cimport ndarray
from numpy import empty

from fmesh_wrapper cimport c_mesh_hyp, c_mesh_exp

def mesh_hyp(double r_min, double r_max, double a, int N):
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    c_mesh_hyp(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh

def mesh_exp(double r_min, double r_max, double a, int N):
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    c_mesh_exp(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh
