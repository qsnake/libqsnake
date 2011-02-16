cdef extern from "arrayobject.h":

    ctypedef int intp

    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags

cdef extern void args_subr1_(signed char *, short *, int *, long *, long *)
cdef extern long args_func1_(signed char *, short *, int *, long *)
cdef extern int int_arg_(int *, int *, int *)
cdef extern float single_arg_(float *, float *, float *)
cdef extern double double_arg_(double *, double *, double *)
cdef extern void string_arg1_(char *, int)
cdef extern void string_arg2_(char *, char *, char *, int, int, int)
cdef extern void string_arg3_(char *, char *, int *, char *, int *,
        int, int, int)
cdef extern void single_array1_(float *)
cdef extern void double_array1_(double *)
cdef extern void double_array2_(double *, int *)
cdef extern void int4_array1_(int *)
cdef extern void int8_array1_(long *)

def args_subr1(signed char a, short b, int c, long d):
    cdef long o
    args_subr1_(&a, &b, &c, &d, &o)
    return o

def args_func1(signed char a, short b, int c, long d):
    return args_func1_(&a, &b, &c, &d)

def int_arg(int a, int b, int c):
    return int_arg_(&a, &b, &c)

def float_arg(float a, float b, float c):
    return single_arg_(&a, &b, &c)

def double_arg(double a, double b, double c):
    return double_arg_(&a, &b, &c)

def string_arg1(char *a):
    string_arg1_(a, len(a))
    return a

def string_arg2(char *a, char *b, char *c):
    string_arg2_(a, b, c, len(a), len(b), len(c))
    return a, b, c

def string_arg3(char *a, char *b, int n1, char *c, int n2):
    string_arg3_(a, b, &n1, c, &n2, len(a), len(b), len(c))
    return a, b, n1, c, n2

def float_array1(ndarray a):
    single_array1_(<float *>(a.data))

def double_array1(ndarray a):
    double_array1_(<double *>(a.data))

def double_array2(ndarray a):
    cdef int n = len(a)
    double_array2_(<double *>(a.data), &n)

def int4_array1(ndarray a):
    int4_array1_(<int *>(a.data))

def int8_array1(ndarray a):
    int8_array1_(<long *>(a.data))
