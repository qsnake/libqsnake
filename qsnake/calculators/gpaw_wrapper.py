import logging

class Gpaw(object):

    def __init__(self, atoms=None):
        """
        Creates a GPAW calculator.
        """
        self._atoms = atoms

    def calculate(self, nbands=50, verbose=False):
        from ase import Atoms, Atom
        from gpaw import GPAW
        ase_atoms = []
        a = 13.
        b = 6.
        for atom in self._atoms:
            ase_atoms.append( Atom(atom.symbol, atom.position + [b, b, b]) )
        atoms = Atoms(ase_atoms, cell=(a, a, a), pbc=False)
        calc = GPAW(nbands=nbands, h=0.4, verbose=verbose)
        atoms.set_calculator(calc)
        energy = atoms.get_potential_energy()
        result = {
                "total_energy": energy,
                }
        return result
