from math import sin, cos, pi
from numpy import array, dot, cross
from numpy.linalg import norm
from data import symbol2number, number2symbol, number2name, number2color

def R_x(alpha):
    return array([
        [1, 0, 0],
        [0, cos(alpha), -sin(alpha)],
        [0, sin(alpha), cos(alpha)],
        ])

def R_y(alpha):
    return array([
        [cos(alpha), 0, sin(alpha)],
        [0, 1, 0],
        [-sin(alpha), 0, cos(alpha)],
        ])

def R_z(alpha):
    return array([
        [cos(alpha), -sin(alpha), 0],
        [sin(alpha), cos(alpha), 0],
        [0, 0, 1],
        ])

def deg2rad(alpha_deg):
    return alpha_deg * pi / 180


class Atom(object):

    def __init__(self, symbol_or_Z=None, position=(0, 0, 0), relative=None):
        try:
            self._Z = int(symbol_or_Z)
        except ValueError:
            self._Z = symbol2number(str(symbol_or_Z))
        if relative is None:
            self._position = array(position)
        else:
            if len(relative) == 2:
                atom = Atom("H", relative[0].position + (1, 0, 0))
                A = 0
                relative = relative + [atom, A]
            if len(relative) == 4:
                atom = Atom("H", relative[2].position + (0, 1, 0))
                D = 0
                relative = relative + [atom, D]
            self._position = self.get_position_from_relative(relative)

    def get_position_from_relative(self, relative):
        atom1, B, atom2, A, atom3, D = relative
        A = deg2rad(A)
        D = deg2rad(D)

        # (e1, e2, e3) in this order is an orthonormal right handed basis
        # in the plane formed by the atom1, atom2 and atom3. The e1 points
        # in the direction from atom2 to atom1.
        e1 = atom1.position - atom2.position
        e1 = e1/norm(e1)
        e3 = cross(atom2.position - atom3.position, e1)
        e3 = e3/norm(e3)
        e2 = cross(e3, e1)
        e2 = e2/norm(e2)

        vec = array([[-B, 0, 0]]).T
        vec = dot(R_x(D), dot(R_z(-A), vec))
        vec = vec.reshape((3,))
        x_transformed = vec[0]*e1 + vec[1]*e2 + vec[2]*e3
        return atom1.position + x_transformed

    @property
    def number(self):
        """
        Returns the atomic number.

        Example:
        >>> Atom("B").number
        5
        """
        return self._Z

    @property
    def symbol(self):
        """
        Returns the symbol of the atom.

        Example:
        >>> Atom("B").symbol
        'B'
        """
        return number2symbol(self._Z)

    @property
    def name(self):
        """
        Returns the atom's name.

        Example:
        >>> Atom("B").name
        'Boron'
        """
        return number2name(self._Z)

    def __str__(self):
        return "<%s: %s>" % (number2symbol(self._Z), self._position)

    @property
    def position(self):
        return self._position

    def _plot_mayavi_(self):
        from enthought.mayavi import mlab
        color = number2color(self._Z)
        mlab.points3d(self.position[:1], self.position[1:2], self.position[2:],
                scale_factor=3,
                resolution=20,
                color=color,
                scale_mode="none")
