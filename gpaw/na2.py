from ase import Atoms, Atom
from gpaw import GPAW

a = 8.  # Size of unit cell (Angstrom)
c = a / 2
# Hydrogen atom:
atom = Atoms('Na',
             positions=[(c, c, c)],
             magmoms=[1],
             cell=(a, a, a))

# gpaw calculator:
calc = GPAW(h=0.18, nbands=1, xc='PBE', txt='Na.out')
atom.set_calculator(calc)

e1 = atom.get_potential_energy()
calc.write('Na.gpw')

# Hydrogen molecule:
d = 1.5  # Experimental bond length
molecule = Atoms('Na2',
                 positions=([c - d / 2, c, c],
                            [c + d / 2, c, c]),
                 cell=(a, a, a))

calc.set(txt='Na2.out')
molecule.set_calculator(calc)
e2 = molecule.get_potential_energy()
calc.write('Na2.gpw')

print 'Na atom energy:     %5.2f eV' % e1
print 'Na2 molecule energy: %5.2f eV' % e2
print 'atomization energy:       %5.2f eV' % (2 * e1 - e2)
