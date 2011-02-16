from numpy import array

from wrapper_tests import (args_subr1, args_func1, int_arg, float_arg,
        double_arg, string_arg1, string_arg2, string_arg3, float_array1,
        double_array1, double_array2, int4_array1, int8_array1)

eps_double = 1e-14
eps_single = 1e-7
eps = eps_double

def test_args1():
    # tests parameters order and their sizes
    assert args_subr1(1, 2, 3, 4) == 1234
    assert args_subr1(4, 3, 2, 1) == 4321

def test_args2():
    # tests parameters order and their sizes
    assert args_func1(1, 2, 3, 4) == 1234
    assert args_func1(4, 3, 2, 1) == 4321

def test_float():
    assert abs(float_arg(1.12, 2, 3.14) - 2) < eps_single
    assert abs(float_arg(1.12, 2., 3.14) - 2) < eps_single
    assert abs(float_arg(1.12, 2.1, 3.14) - 2.1) < eps_single
    assert abs(float_arg(1.12, 0.183, 3.14) - 0.183) < eps_single

def test_int():
    assert int_arg(1, 2, 3) == 2
    assert int_arg(1, 3, 3) == 3
    assert int_arg(1, 4, 3) == 4

def test_float_less_than_double():
    # This tests, that float has less precision than double:
    assert abs(float_arg(1.12, 0.183, 3.14) - 0.183) < eps_single
    assert abs(float_arg(1.12, 0.183, 3.14) - 0.183) > eps_double

def test_double():
    assert abs(double_arg(1.12, 2, 3.14) - 2) < eps_double
    assert abs(double_arg(1.12, 2., 3.14) - 2) < eps_double
    assert abs(double_arg(1.12, 2.1, 3.14) - 2.1) < eps_double
    assert abs(double_arg(1.12, 0.183, 3.14) - 0.183) < eps_double

def test_string1():
    c = "5"*40
    assert string_arg1(c) == "This is a sample"

def test_string2():
    a = "1"*40
    b = "2"*40
    c = "3"*40
    _a, _b, _c = string_arg2(a, b, c)
    assert _a == "2"*40
    assert _b == "3"*40
    assert _c == "1"*40

def test_string3():
    a = "1"*40
    b = "2"*40
    c = "3"*40
    e = 5
    f = 6
    _a, _b, _e, _c, _f = string_arg3(a, b, e, c, f)
    assert _a == "2"*40
    assert _b == "3"*40
    assert _c == "1"*40
    assert _e == 5
    assert _f == 11

def test_float_array():
    a = array([5, 5, 5, 5], dtype="f4")
    float_array1(a)
    a_correct = array([1.1, 2.1, 3.1, 4.1], dtype="f4")
    assert (abs(a - a_correct) < eps_single).all()

def test_double_array1():
    a = array([5, 5, 5, 5], dtype="f8")
    double_array1(a)
    a_correct = array([1.1, 2.1, 3.1, 4.1], dtype="f8")
    assert (abs(a - a_correct) < eps_double).all()

def test_double_array2():
    a = array([5, 5, 5, 5], dtype="f8")
    double_array2(a)
    a_correct = array([1.1, 2.1, 3.1, 4.1], dtype="f8")
    assert (abs(a - a_correct) < eps_double).all()

    a = array([5, 5, 5, 5, 5, 5], dtype="f8")
    double_array2(a)
    a_correct = array([1.1, 2.1, 3.1, 4.1, 5.1, 6.1], dtype="f8")
    assert (abs(a - a_correct) < eps_double).all()

def test_int4_array():
    a = array([5, 5, 5, 5], dtype="i4")
    int4_array1(a)
    a_correct = array([1, 2, 3, 4], dtype="i4")
    assert (a == a_correct).all()

def test_int8_array():
    a = array([5, 5, 5, 5], dtype="i8")
    int8_array1(a)
    a_correct = array([1, 2, 3, 4], dtype="i8")
    assert (a == a_correct).all()
