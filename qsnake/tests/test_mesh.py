from numpy import array

from qsnake.mesh import mesh_exp

def test_mesh_exp1():
    eps = 1e-10
    r = mesh_exp(0, 10, 2, 1)
    correct = array([0., 10.])
    assert (abs(r-correct) < eps).all()

def test_mesh_exp2():
    eps = 1e-10
    r = mesh_exp(0, 10, 2, 2)
    correct = array([0, 3 + 1./3, 10])
    assert (abs(r-correct) < eps).all()

def test_mesh_exp3():
    eps = 1e-10
    r = mesh_exp(0, 10, 2, 3)
    correct = array([0, 2.2654091966098644, 5.4691816067802712, 10])
    assert (abs(r-correct) < eps).all()

def test_mesh_exp4():
    eps = 1e-10
    r = mesh_exp(0, 10, 2, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 2) < eps

    r = mesh_exp(0, 10, 3, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 3) < eps

    r = mesh_exp(0, 10, 4, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 4) < eps

    r = mesh_exp(0, 10, 10.5, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 10.5) < eps

    r = mesh_exp(0, 10, 1, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 1) < eps

    r = mesh_exp(0, 10, 0.5, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 0.5) < eps

    r = mesh_exp(0, 10, 0.1, 50)
    a = (r[-1] - r[-2]) / (r[1] - r[0])
    assert abs(a - 0.1) < eps

def test_mesh_exp5():
    eps = 1e-8
    r = mesh_exp(0, 100, a=20, N=4)
    correct = array([0. , 3.21724644, 11.95019684, 35.65507127, 100.])
    assert (abs(r-correct) < eps).all()

    r = mesh_exp(0, 100, a=40, N=4)
    correct = array([0. , 1.78202223, 7.87645252, 28.71911092, 100.])
    assert (abs(r-correct) < eps).all()

    r = mesh_exp(0, 100, a=100, N=4)
    correct = array([0. , 0.78625046, 4.43570179, 21.37495437, 100.])
    assert (abs(r-correct) < eps).all()
