from math import sqrt

from qsnake import Atom

def eq(a, b, eps=1e-8):
    return (abs(a-b) < eps).all()

def test_basic1():
    a = Atom(1)
    assert a.number == 1
    assert a.symbol == "H"
    assert a.name == "Hydrogen"
    a = Atom("H")
    assert a.number == 1
    assert a.symbol == "H"
    assert a.name == "Hydrogen"

def test_basic2():
    a = Atom(5)
    assert a.number == 5
    assert a.symbol == "B"
    assert a.name == "Boron"
    a = Atom("B")
    assert a.number == 5
    assert a.symbol == "B"
    assert a.name == "Boron"

def test_basic3():
    a = Atom(82)
    assert a.number == 82
    assert a.symbol == "Pb"
    assert a.name == "Lead"
    a = Atom("Pb")
    assert a.number == 82
    assert a.symbol == "Pb"
    assert a.name == "Lead"

def test_str():
    a = Atom(82)
    s = str(a)
    assert s.find("Pb") != -1
    assert s.find("Br") == -1

def test_internal1():
    a = Atom("H")
    assert eq(a.position, [0, 0, 0])
    b = Atom("H", relative=[a, 1])
    assert eq(b.position, [1, 0, 0])
    c = Atom("H", relative=[a, 1, b, 90.])
    assert eq(c.position, [0, 1, 0])
    d = Atom("H", relative=[a, 1, b, -90.])
    assert eq(d.position, [0, -1, 0])
    e = Atom("H", relative=[a, 1, b, 120.])
    assert eq(e.position, [-0.5, sqrt(3)/2, 0])
    f = Atom("H", relative=[b, 1, a, 120., e, 0])
    assert eq(f.position, [1.5, sqrt(3)/2, 0])

    a = Atom("H", (0, 1, 0))
    assert eq(a.position, [0, 1, 0])
    b = Atom("H", relative=[a, 1])
    assert eq(b.position, [1, 1, 0])
    c = Atom("H", relative=[a, 1, b, 90.])
    assert eq(c.position, [0, 2, 0])
    d = Atom("H", relative=[a, 1, b, -90.])
    assert eq(d.position, [0, 0, 0])
    e = Atom("H", relative=[a, 1, b, 120.])
    assert eq(e.position, [-0.5, sqrt(3)/2+1, 0])
    f = Atom("H", relative=[b, 1, a, 120., e, 0])
    assert eq(f.position, [1.5, sqrt(3)/2+1, 0])

    a = Atom("H", (2.5, 1, 0))
    assert eq(a.position, [2.5, 1, 0])
    b = Atom("H", relative=[a, 1])
    assert eq(b.position, [3.5, 1, 0])
    c = Atom("H", relative=[a, 1, b, 90.])
    assert eq(c.position, [2.5, 2, 0])
    d = Atom("H", relative=[a, 1, b, -90.])
    assert eq(d.position, [2.5, 0, 0])
    e = Atom("H", relative=[a, 1, b, 120.])
    assert eq(e.position, [2, sqrt(3)/2+1, 0])
    f = Atom("H", relative=[b, 1, a, 120., e, 0])
    assert eq(f.position, [4, sqrt(3)/2+1, 0])

def test_internal2():
    a = Atom("H")
    b = Atom("H", relative=[a, 1])
    c = Atom("H", relative=[b, 1, a, 120])
    d = Atom("H", relative=[c, 1, b, 120, a, 0])
    e = Atom("H", relative=[d, 1, c, 120, b, 0])
    f = Atom("H", relative=[e, 1, d, 120, c, 0])
    a2 = Atom("H", relative=[f, 1, e, 120, d, 0])
    assert eq(a2.position, a.position)

def test_internal3():
    # methane CH_4
    a = Atom("C")
    b = Atom("H", relative=[a, 1.089])
    c = Atom("H", relative=[a, 1.089, b, 109.471])
    d = Atom("H", relative=[a, 1.089, b, 109.471, c, +120])
    e = Atom("H", relative=[a, 1.089, b, 109.471, c, -120])

    assert eq(b.position, [1.089, 0., 0.])
    assert eq(c.position, [-0.36299605, 1.02672044,  0.])
    assert eq(d.position, [-0.36299605, -0.51336022, -0.88916599])
    assert eq(e.position, [-0.36299605, -0.51336022,  0.88916599])

def test_internal3b():
    # methane CH_4
    # set positions of the first 3 atoms by hand
    a = Atom("C")
    b = Atom("H", position=(0, 0, 1.089))
    c = Atom("H", position=(1.02672044, 0, -0.36299605))
    d = Atom("H", relative=[a, 1.089, b, 109.471, c, +120])
    e = Atom("H", relative=[a, 1.089, b, 109.471, c, -120])

    assert eq(d.position, [-0.51336022, -0.88916599, -0.36299605])
    assert eq(e.position, [-0.51336022,  0.88916599, -0.36299605])


def test_internal4():
    # Methyl Cyanide
    C1 = Atom("C")
    C2 = Atom("C", relative=[C1, 1.54])
    H3 = Atom("H", relative=[C1, 1.09, C2, 110])
    H4 = Atom("H", relative=[C1, 1.09, C2, 110, H3, 120])
    H5 = Atom("H", relative=[C1, 1.09, C2, 110, H3, -120])
    N6 = Atom("N", relative=[C1, 2.70, H3, 110, C2, 0])
    assert eq(C2.position, [ 1.54, 0, 0])
    assert eq(H3.position, [-0.37280196, 1.02426496, 0])
    assert eq(H4.position, [-0.37280196, -0.51213248, -0.88703947])
    assert eq(H5.position, [-0.37280196, -0.51213248,  0.88703947])
    assert eq(N6.position, [2.7, 0, 0])

def test_internal5():
    # Butane
    C1 = Atom("C")
    C2 = Atom("C", relative=[C1, 1.54])
    C3 = Atom("C", relative=[C2, 1.54, C1, 110])
    C4 = Atom("C", relative=[C3, 1.54, C2, 110, C1, 120])
    H5 = Atom("H", relative=[C1, 1.09, C2, 110, C3, 120])
    H6 = Atom("H", relative=[C1, 1.09, C2, 110, C3, 120])
    H7 = Atom("H", relative=[C1, 1.09, C2, 110, C3, 120])
    H8 = Atom("H", relative=[C2, 1.09, C3, 110, C4, 120])
    H9 = Atom("H", relative=[C2, 1.09, C3, 110, C4, 120])
    H10 = Atom("H", relative=[C3, 1.09, C2, 110, C1, 120])
    H11 = Atom("H", relative=[C3, 1.09, C2, 110, C1, 120])
    H12 = Atom("H", relative=[C4, 1.09, C3, 110, C2, 120])
    H13 = Atom("H", relative=[C4, 1.09, C3, 110, C2, 120])
    H14 = Atom("H", relative=[C4, 1.09, C3, 110, C2, 120])

    assert eq(C1.position, [0, 0, 0])
    assert eq(C2.position, [1.54, 0, 0])
    assert eq(C3.position, [2.06671102,  1.44712664,  0])
    assert eq(C4.position, [2.92678391,  1.69459987,  1.25324843])
    assert eq(H5.position, [-0.37280196, -0.51213248, -0.88703947])
    assert eq(H6.position, [-0.37280196, -0.51213248, -0.88703947])
    assert eq(H7.position, [-0.37280196, -0.51213248, -0.88703947])
    assert eq(H8.position, [4.50000000e-01, 0, 0])
    assert eq(H9.position, [4.50000000e-01, 0, 0])
    assert eq(H10.position, [2.67546391, 1.62228626, 0.88703947])
    assert eq(H11.position, [2.67546391, 1.62228626, 0.88703947])
    assert eq(H12.position, [3.93915843, 1.97394697, 0.96142138])
    assert eq(H13.position, [3.93915843, 1.97394697, 0.96142138])
    assert eq(H14.position, [3.93915843, 1.97394697, 0.96142138])
