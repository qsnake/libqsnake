from qsnake import Atoms
from qsnake.calculators import Pyquante


atoms = Atoms.from_z_matrix_file("examples/baresmallsilicon.in")
#atoms.plot()

calculator = Pyquante(atoms)
result = calculator.calculate(verbose=True)
print result
