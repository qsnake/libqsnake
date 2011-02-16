import logging

class Pyquante(object):

    def __init__(self, atoms=None):
        """
        Creates a PyQuante calculator.
        """
        self._atoms = atoms

    def calculate(self, verbose=False):
        from PyQuante import SCF, Molecule
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        pyquante_atoms = []
        for a in self._atoms:
            pyquante_atoms.append( (a.number, a.position) )
        m = Molecule('molecule', pyquante_atoms)
        lda = SCF(m, method="DFT")
        lda.iterate()

        result = {
                "total_energy": lda.energy,
                "orbital_energies": lda.solver.orbe,
                }
        return result
