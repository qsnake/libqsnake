from math import sqrt

from qsnake.mesh import (get_mesh_exp_params, mesh_exp, mesh_nist1_direct,
        mesh_nist2_direct, mesh_nist3_direct)

Z = 92
eps = 1e-10

print "NIST meshes used for Uranium"

# 1
r = mesh_nist1_direct(1./(160*Z), 50, 15788)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "1)"
print r_min, r_max, a, N

# 2
r = mesh_nist1_direct(1e-6/Z, 800/sqrt(Z), 8000)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "2)"
print r_min, r_max, a, N

# 3
# H
#r = mesh_nist2_direct(4.34e-6/1, 0.002304, 7058)
# U
r = mesh_nist2_direct(4.34e-6/Z, 0.002304, 9021)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "3)"
print r_min, r_max, a, N

# 4
r = mesh_nist3_direct(0.01e-4/Z, 50, 2837)
r_min, r_max, a, N = get_mesh_exp_params(r)
assert (abs(mesh_exp(r_min, r_max, a, N) - r) < eps).all()
print "4)"
print r_min, r_max, a, N
