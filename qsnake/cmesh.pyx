from numpy cimport ndarray
from numpy import empty

cimport fmesh

def mesh_log(double r_min, double r_max, double a, int N):
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    fmesh.c_mesh_log(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh

def mesh_exp(double r_min, double r_max, double a, int N):
    cdef ndarray[double, mode="c"] mesh = empty(N+1, dtype="double")
    fmesh.c_mesh_exp(&r_min, &r_max, &a, &N, &mesh[0])
    return mesh
