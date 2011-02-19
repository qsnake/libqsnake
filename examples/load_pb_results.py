from numpy import array, savetxt
from pylab import plot, savefig, legend, subplot
from json import load

f = open("results.json")
data = load(f)
r_min = array([r["r_min"] for r in data])
error = array([r["error"] for r in data])
a_min = array([r["a_min"] for r in data])
a = array([r["a"] for r in data])
a_max = array([r["a_max"] for r in data])

i = error.argmin()
print r_min[i], error[i], a[i]

d = array([r_min, error, a_min, a, a_max])
savetxt("data.txt", d)

subplot(211)
plot(r_min, a, label="a")
#plot(r_min, a_min, label="a_min")
#plot(r_min, a_max, label="a_max")
legend()
subplot(212)
plot(r_min, error, label="error")
legend()
savefig("pb_meshes.png")
print "Plot saved to pb_meshes.png"
