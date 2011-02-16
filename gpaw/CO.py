from ase import Atoms, Atom
from gpaw import GPAW


d = 1.1   # bondlength of hydrogen molecule
a = 5.0   # sidelength of unit cell
c = a / 2
atoms = Atoms([Atom('C', [c - d / 2, c, c]),
                     Atom('O', [c + d / 2, c, c])],
                    cell=(a, a, a), pbc=False)

calc = GPAW(nbands=5, h=0.2, verbose=True)
atoms.set_calculator(calc)

# Start a calculation:
energy = atoms.get_potential_energy()

# Save wave functions:
calc.write('CO.gpw', mode='all')
