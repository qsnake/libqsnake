"""
Calculates the Radon atom using HF.
"""

import logging

from PyQuante import SCF, Molecule, dft, Atom

from basis_rn_ano import basis_data

logging.basicConfig(level=logging.DEBUG)

R = Molecule('Radon',[(86, (0,0,0))])
R.multiplicity = 1
hf = SCF(R, method="HF", basis="6-31G**", basis_data=basis_data)
hf.iterate()

# print some info:
print "HF Results: energy =", hf.energy
print "orbital energies:", hf.solver.orbe
