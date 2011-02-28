from numpy import loadtxt
from pylab import plot, show, legend
a = loadtxt("Na2_spectrum.dat")
om = a[:, 0]
osz = a[:, 1]
osz_x = a[:, 2]
osz_y = a[:, 3]
osz_z = a[:, 4]

plot(om, osz, label="osz")
#plot(om, osz_x, label="osz_x")
#plot(om, osz_y, label="osz_y")
#plot(om, osz_z, label="osz_z")
legend()
show()
