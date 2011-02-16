"""
Calculates the H2 molecule using DFT.

And plots the charge density along the x-axis.
"""

from PyQuante import SCF, Molecule
from PyQuante.NumWrap import arange
from pylab import plot, savefig

# Do the lda calculation:
h2 = Molecule('h2',[(1, (-0.7, 0, 0)), (1, (0.7, 0, 0))])
lda = SCF(h2,method="DFT")
lda.iterate()

# print some info:
print "DFT Results: LDA energy =", lda.energy
print "orbital energies:", lda.solver.orbe

# Get the items we'll need to compute the density with
orbs = lda.solver.orbs
bfs = lda.basis_set.get()
nclosed,nopen = h2.get_closedopen()
nbf = len(bfs)

x,y,z = 0, 0, 0
xs = arange(-1.0, 1.1, 0.1)
ds = []
for x in xs:
    amp_xyz = 0
    for i in range(nclosed):
        for j in range(nbf):
            amp_xyz += orbs[j,i]*bfs[j].amp(x, y, z)
    ds.append(amp_xyz**2)
plot(xs, ds)
savefig("h2-dft-dens-x.png", dpi=72)

# optionally plot it if you want:
#show()
