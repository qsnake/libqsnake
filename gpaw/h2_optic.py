from ase import Atoms, Atom
from gpaw import GPAW, restart

atoms, calc = restart('H2_gs.gpw')
atoms.center(vacuum=6.0)
calc.set(nbands=20)
calc.set(txt='H2.out')
atoms.set_calculator(calc)
e2 = atoms.get_potential_energy()
calc.write('H2.gpw')

lr = LrTDDFT(calc, xc="LDA")
lr.write("Omega_H2.gz")
photoabsorption_spectrum(lr, 'H2_spectrum.dat', e_min=0.0, e_max=10)

