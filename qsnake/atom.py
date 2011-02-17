from math import sin, cos, pi
from numpy import array, dot, cross
from numpy.linalg import norm
from data import symbol2number, number2symbol, number2name, number2color
from mesh import mesh_log

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
    if solver == "dftatom":
        if "Z" not in params:
            raise Exception("Specify Z in params")
        Z = params["Z"]
        E_init = params.get("E_init", -3000)
        E_delta = params.get("E_delta", 2000)
        eps = params.get("eps", 1e-10)
        from dftatom.rdirac import solve_radial_eigenproblem
        E, R = solve_radial_eigenproblem(n, l, E_init, E_delta, eps,
                u, r, Z, relat)
        return E, R
    else:
        raise Exception("Uknown solver")

def solve_hydrogen_like_atom(Z, mesh_params, solver_params):
    r_min = mesh_params["r_min"]
    r_max = mesh_params["r_max"]
    a = mesh_params["a"]
    N = mesh_params["N"]
    print "Mesh parameters:"
    print "r_min =", r_min
    print "r_max =", r_max
    print "a =", a
    print "N =", N
    r = mesh_log(r_min, r_max, a, N)
    print r

    solver_params["Z"] = Z


    # Potential:
    vr = -Z/r

    # Speed of light taken from:
    # http://arxiv.org/abs/1012.3627
    #c = 137.035999037

    # Elk value:
    c  = 137.035999679

    # Polynomial degree for predictor-corrector:
    np = 4

    tot_error = -1
    # (n, l):
    # either k == l, or k == l + 1:
    for n in range(1, 7):
        for l in range(0, n):
            k_list = []
            if l > 0:
                k_list.append(l)
            k_list.append(l+1)

            for k in k_list:
                # Initial guess:
                E = -1.0
                spin_up = (k == l+1)
                if spin_up:
                    relat = 2
                else:
                    relat = 3
                E, R = solve_radial_eigenproblem(n, l, r, vr, relat,
                        solver_params)
                E_exact = E_nl_dirac(n, l, spin_up=spin_up, Z=Z, c=c)
                delta = abs(E-E_exact)
                if delta > tot_error:
                    tot_error = delta
                print ("(n=%d, l=%d, k=%d): E_calc=%12.6f    E_xact=%12.6f    " + \
                                                        "delta=%9.2e") % (n, l, k, E, E_exact, delta)
    print "tot_error = ", tot_error

    return tot_error
