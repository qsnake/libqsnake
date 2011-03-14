from numpy import array

from qsnake.mesh import mesh_log

eps = 1e-10

def test_mesh_log1():
    r = mesh_log(0, 10, 2, 1)
    correct = array([0., 10.])
    assert (abs(r-correct) < eps).all()

def test_mesh_log2():
    r = mesh_log(0, 10, 2, 2)
    correct = array([0, 3 + 1./3, 10])
    assert (abs(r-correct) < eps).all()

def test_mesh_log3():
    r = mesh_log(0, 10, 2, 3)
    correct = array([0, 2.2654091966098644, 5.4691816067802712, 10])
    assert (abs(r-correct) < eps).all()
