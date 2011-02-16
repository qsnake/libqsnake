from qsnake import Atoms, Atom
from qsnake.calculators import Gpaw


atoms = Atoms([
    Atom("O", (0, 0, 0)),
    Atom("H", (-1, 0, 0.5)),
    Atom("H", (1, 0, 0.5)),
    ])

calculator = Gpaw(atoms)
result = calculator.calculate(nbands=5, verbose=True)
print result
