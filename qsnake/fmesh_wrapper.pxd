cdef extern:
    void c_mesh_log(double *r_min, double *r_max, double *a, int *N,
            double *mesh)
    void c_mesh_exp(double *r_min, double *r_max, double *a, int *N,
            double *mesh)
