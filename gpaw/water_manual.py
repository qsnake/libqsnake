from math import pi
from ase import Atoms, BFGS
from gpaw import GPAW
import numpy as np
d = 0.9575
t = pi / 180 * 103
a = 4.
b = a/2
water = Atoms('H2O',
              positions=[(d+b, 0+b, 0+b),
                         (d * np.cos(t)+b, d * np.sin(t)+b, 0+b),
                         (0+b, 0+b, 0+b)],
              cell=(a, a, a),
              pbc=False,
              calculator=GPAW(nbands=4, h=0.1))
dyn = BFGS(water)
dyn.run(fmax=0.01)
