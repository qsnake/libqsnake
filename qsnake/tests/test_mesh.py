from numpy import array

from qsnake.mesh import mesh_exp

eps = 1e-10

def test_mesh_log1():
    r = mesh_exp(0, 10, 2, 1)
    correct = array([0., 10.])
    assert (abs(r-correct) < eps).all()

def test_mesh_log2():
    r = mesh_exp(0, 10, 2, 2)
    correct = array([0, 3 + 1./3, 10])
    assert (abs(r-correct) < eps).all()

def test_mesh_log3():
    r = mesh_exp(0, 10, 2, 3)
    correct = array([0, 2.2654091966098644, 5.4691816067802712, 10])
    assert (abs(r-correct) < eps).all()

def test_mesh_log4():
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
