import logging

from numpy import array

from PyQuante import SCF, Molecule

atoms = [(14, array([0, 0, 0])), (14, array([ 2.3419588,  0.       ,  0.       ])), (14, array([ 3.21218834,  2.05887837,  0.        ])), (14, array([ 1.23984519,  3.29297073, -0.42228815])), (14, array([-0.05485092,  1.72185148, -1.63972761])), (14, array([ 1.15882181,  0.99278059, -3.55206339])), (14, array([ 3.39816913,  0.26950033, -3.1977073 ])), (14, array([ 4.55928267,  1.90791736, -1.93502226])), (14, array([ 3.39316637, -1.42643782, -1.53138653])), (1, array([-0.6106289 ,  0.43621736,  1.28608097])), (1, array([-0.5834327 , -1.31182802, -0.39633738])), (1, array([-1.43155677,  2.12871605, -2.08077878])), (1, array([ 1.53825752,  4.55183661, -1.16374012])), (1, array([ 0.53075288,  3.66105357,  0.83588437])), (1, array([ 5.94172312,  1.43875952, -1.62950356])), (1, array([ 4.67251821,  3.2307785 , -2.61584443])), (1, array([ 3.97839267, -0.14357093, -4.51963896])), (1, array([ 2.59722827, -2.64784197, -1.83682433])), (1, array([ 4.77261873, -1.8301562 , -1.14139106])), (1, array([ 0.40165221, -0.13112135, -4.18238283])), (1, array([ 1.17882996,  2.10638397, -4.5476595 ]))]

logging.basicConfig(level=logging.DEBUG)
m = Molecule('molecule', atoms)
lda = SCF(m, method="DFT")
lda.iterate()
