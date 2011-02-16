"""
Calculates the Boron atom using DFT.
"""

from PyQuante import SCF, Molecule, dft, Atom
B = Molecule('Boron',[(5, (0,0,0))])
B.multiplicity = 2
E, eigs, orbitals = dft.dft(B)
print "total energy:", E
print "KS energies:", eigs
