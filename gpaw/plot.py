from ase import *
from gpaw import *

basename = 'CO'

# load nc binary file and get calculator
atoms, calc = restart(basename + '.gpw')

# write atomic positions to xyz-file
write(basename + '.xyz', atoms)
# loop over all wfs and write their cube files
nbands = calc.get_number_of_bands()
wf = calc.get_pseudo_wave_function(band=0)

from enthought.mayavi import mlab
#mlab.figure(1, bgcolor=(0, 0, 0), size=(350, 350))
mlab.clf()

data = wf

source = mlab.pipeline.scalar_field(data)
mlab.view(132, 54, 45, [21, 20, 21.5])

engine = mlab.get_engine()
from enthought.mayavi.modules.scalar_cut_plane import ScalarCutPlane
scalar_cut_plane = ScalarCutPlane()
engine.add_module(scalar_cut_plane, obj=None)
scene = engine.scenes[0]
scene.scene.render()

mlab.show()
