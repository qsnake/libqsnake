from math import sin, cos

def replace_dict(s, d):
    for v in d:
        s = s.replace(v, str(d[v]))
    return s

class Atoms(object):

    def __init__(self, atom_list):
        self._atoms = atom_list

    def get_atoms_list(self):
        return self._atoms

    def __getitem__(self, key):
        """
        Allows to access Atoms() like a list.

        Example:
        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> atoms[1] == a2
        True

        """
        return self._atoms[key]

    def __len__(self):
        """
        Returns the number of atoms.

        Example:
        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> len(atoms)
        3
        """
        return len(self._atoms)

    def get_atomic_numbers(self):
        """
        Returns the list of atomic numbers.

        Example:
        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> atoms.get_atomic_numbers()
        [1, 1, 8]

        """
        return [a.number for a in self]

    @staticmethod
    def from_z_matrix_file(filename):
        f = open(filename)
        line = f.readline()
        while len(line) > 0 and line[0] in ["#", "%", "$"]:
            line = f.readline()
        assert line == "\n"
        line = f.readline()
        while line != "\n":
            line = f.readline()
        line = f.readline()
        charge, multiplicity = line.split()
        charge = float(charge)
        multiplicity = int(multiplicity)

        atom_list = []
        line = f.readline()
        while line != "\n":
            atom_list.append(line.split())
            line = f.readline()

        var_list = {}
        line = f.readline()
        while line != "\n":
            var, val = line.split()
            var_list[var] = float(val)
            line = f.readline()

        z_matrix = []
        for atom in atom_list:
            atom = [replace_dict(x, var_list) for x in atom]
            assert len(atom) in [1, 3, 5, 7]
            z_matrix.append(atom)

        return Atoms.from_z_matrix(z_matrix)

    @staticmethod
    def from_z_matrix(z_matrix):
        from atom import Atom
        atoms = []
        for line in z_matrix:
            if len(line) == 1:
                sym, = line
                atoms.append(Atom(sym))
            elif len(line) == 3:
                sym, atom1_id, B = line
                atom1_id = int(atom1_id)-1
                B = float(B)
                atom1 = atoms[atom1_id]
                atoms.append(Atom(sym, relative=[atom1, B]))
            elif len(line) == 5:
                sym, atom1_id, B, atom2_id, A = line
                atom1_id = int(atom1_id)-1
                B = float(B)
                atom1 = atoms[atom1_id]
                atom2_id = int(atom2_id)-1
                A = float(A)
                atom2 = atoms[atom2_id]
                atoms.append(Atom(sym, relative=[atom1, B, atom2, A]))
            elif len(line) == 7:
                sym, atom1_id, B, atom2_id, A, atom3_id, D = line
                atom1_id = int(atom1_id)-1
                B = float(B)
                atom1 = atoms[atom1_id]
                atom2_id = int(atom2_id)-1
                A = float(A)
                atom2 = atoms[atom2_id]
                atom3_id = int(atom3_id)-1
                D = float(D)
                atom3 = atoms[atom3_id]
                atoms.append(Atom(sym, relative=[atom1, B, atom2, A, atom3, D]))
            else:
                raise NotImplementedError()
        return Atoms(atoms)

    def __str__(self):
        s = "Atom positions:\n"
        for a in self._atoms:
            s += str(a)+"\n"
        return s

    def get_coordinates_str(self):
        """
        Return a string of coordinates of all atoms.

        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> print atoms.get_coordinates_str()
        0 0 0
        0 0 1
        1 0 1

        """

        s = ""
        for a in self._atoms:
            s += "%s %s %s\n" % tuple(a.position)
        return s[:-1]

    def get_coordinates(self):
        """
        Returns coordinates as a list.

        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> print atoms.get_coordinates()
        [[0, 0, 0], [0, 0, 1], [1, 0, 1]]

        """

        s = []
        for a in self._atoms:
            s.append(a.position)
        return s

    def get_number_of_types_of_atoms(self):
        """
        Return a number of types of atoms.

        >>> from qsnake import Atom
        >>> a1 = Atom("H", (0, 0, 0))
        >>> a2 = Atom("H", (0, 0, 1))
        >>> a3 = Atom("O", (1, 0, 1))
        >>> atoms = Atoms([a1, a2, a3])
        >>> print atoms.get_number_of_types_of_atoms()
        2
        """
        r = {}
        for a in self._atoms:
            r[a.number] = 1
        return len(r)

    def _plot_mayavi_(self):
        for a in self._atoms:
            a._plot_mayavi_()

    def plot(self, lib="mayavi", show=True):
        if lib == "mayavi":
            self._plot_mayavi_()
            if show:
                from enthought.mayavi import mlab
                mlab.show()
        else:
            raise NotImplementedError()
