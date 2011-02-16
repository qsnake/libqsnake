"""
Calculates the H2 molecule using HF.

And plots the charge density along the x-axis.
"""

from PyQuante import SCF, Molecule
from PyQuante.NumWrap import arange
from pylab import plot, savefig

# Do the lda calculation:
h2 = Molecule('h2', [(1, (-0.7, 0, 0)), (1, (0.7, 0, 0))])
hf = SCF(h2, method="HF", basis="6-31G**")
hf.iterate()

# print some info:
print "HF Results: energy =", hf.energy
print "orbital energies:", hf.solver.orbe

# Get the items we'll need to compute the density with
orbs = hf.solver.orbs
bfs = hf.basis_set.get()
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
savefig("h2-hf-dens-x.png", dpi=72)

# optionally plot it if you want:
#show()
