from qsnake import Atoms
from qsnake.calculators import Gpaw


atoms = Atoms.from_z_matrix_file("examples/baresmallsilicon.in")
#atoms.plot()

calculator = Gpaw(atoms)
result = calculator.calculate(verbose=True)
print result
