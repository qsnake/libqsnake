from math import sin, cos, pi
from numpy import array, dot, cross
from numpy.linalg import norm
from data import symbol2number, number2symbol, number2name, number2color
from mesh import mesh_log
import numpy

class ConvergeError(Exception):
    pass

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

def solve_radial_eigenproblem(n, l, r, u, relat=0, params=None):
    """
    Solves the radial Schroedinger (Dirac) eigenproblem.

    Input::

        n, l ..... quantum numbers
        r ........ radial mesh (NumPy array)
        u ........ Potential on the radial mesh (for example -Z/r)
        relat .... 0 solves Schroedinger equation
                   2 solves Dirac equation, spin up
                   3 solves Dirac equation, spin down
        params ... optional dictionary with solver specific parameters (not all
                    parameters apply for each solver):
                solver ... type of solver (dftatom, elk)
                Z ... atomic number Z in the potential -Z/r
                E_init, E_delta ... energy is sought in the interval
                        (Emin, Emax), where
                            E_min = E_init - E_delta
                            E_max = E_init + E_delta
                eps ... accuracy for |Emax - Emin| < eps, default 1e-10
                c ... speed of light in atomic units (default c = 137.035999037,
                        from http://arxiv.org/abs/1012.3627)


    Returns (E, R), where E is the energy, and R(r) is the radial wave
    function (normalized as \int R(r)**2 * r**2 \d r = 1)
    """
    if params is None:
        params = {}
    solver = params.get("solver", "dftatom")
    c = params.get("c", 137.035999037)
    if solver == "dftatom":
        if "Z" in params:
            Z = params["Z"]
        else:
            # Disable the fragile estimation of Z below for now:
            raise NotImplementedError("Z not specified. You can enable automatic determination of Z in qsnake/atom.py.")
            # Estimate Z by assuming a coulombic potential u = -Z/r near the
            # origin:
            Z = -u[0] * r[0]
        E_init = params.get("E_init", -3000)
        E_delta = params.get("E_delta", 2000)
        eps = params.get("eps", 1e-9)
        from dftatom.rdirac import (solve_radial_eigenproblem,
                ConvergeError as dftatom_ConvergeError)
        try:
            E, R = solve_radial_eigenproblem(c, n, l, E_init, E_delta, eps,
                    u, r, Z, relat)
        except dftatom_ConvergeError, e:
            raise ConvergeError(str(e))
        return E, R
    elif solver == "elk":
        from elk.pyelk import rdirac
        if relat == 2:
            k = l + 1
        elif relat == 3:
            k = l
        else:
            raise ValueError("relat must be 2 or 3")
        #E_init = params.get("E_init", -3000)
        E_init = params.get("E_init", -1)
        # Polynomial degree for predictor-corrector:
        np = params.get("np", 4)
        E, R = rdirac(c, n, l, k, np, r, u, E_init)
        if abs(E) > 1e6:
            raise ConvergeError("Elk solver didn't converge")
        return E, R
    else:
        raise Exception("Uknown solver")

def solve_hydrogen_like_atom(Z, mesh_params, solver_params, verbose=False):
    from sympy.physics.hydrogen import E_nl_dirac
    from sympy import TableForm
    r_min = mesh_params["r_min"]
    r_max = mesh_params["r_max"]
    a = mesh_params["a"]
    N = mesh_params["N"]
    r = mesh_log(r_min, r_max, a, N)
    if verbose:
        print "Mesh parameters:"
        print TableForm([[r_min], [r_max], [a], [N]],
                headings=(("r_min", "r_max", "a", "N"), ("Mesh parameters",)))
        print r

    c = solver_params.get("c", 137.035999037)
    solver_params["c"] = c
    solver_params["Z"] = Z


    # Potential:
    vr = -Z/r

    tot_error = -1
    data = []
    # (n, l):
    # either k == l, or k == l + 1:
    for n in range(1, 7):
        for l in range(0, n):
            relat_list = [2]
            if l > 0:
                relat_list.append(3)

            for relat in relat_list:
                spin_up = (relat == 2)
                try:
                    E, R = solve_radial_eigenproblem(n, l, r, vr, relat,
                            solver_params)
                except ConvergeError:
                    if verbose:
                        print "Radial solver didn't converge"
                    raise
                    return 1e6
                E_exact = E_nl_dirac(n, l, spin_up=spin_up, Z=Z, c=c)
                E_exact = float(E_exact)
                delta = abs(E-E_exact)
                if delta > tot_error:
                    tot_error = delta
                k = int(spin_up)
                data.append([n, l, k,
                    "%.6f" % E, "%.6f" % E_exact, "%.2e" % delta])
    t = TableForm(data, alignment="right",
            headings=(None, ("n", "l", "k", "E_calc", "E_exact", "delta")))
    if verbose:
        print t
    return tot_error
