from qsnake.atom import solve_hydrogen_like_atom, ConvergeError
from qsnake.mesh import n_minimize
from sympy import TableForm
from numpy import arange
from json import dump, encoder

def optimize(r_min=1e-6, r_max=50, N=700, solver="elk"):
    def f(a):
        r_min = params[0]
        r_max = params[1]
        N = params[2]
        try:
            r = solve_hydrogen_like_atom(82, {
                    "r_min": r_min,
                    "r_max": r_max,
                    "a": a,
                    "N": N,
                }, {
                    "solver": solver,
                }, verbose=False)
        except ConvergeError, e:
            e.a = a
            raise e
        return r

    a_min = 1
    a_max = 1e8
    # temporary:
    #a_min = 3982631.666582 - 1
    #a_max = 3982631.666582 + 1
    params = [r_min, r_max, N]
    done = False
    while not done:
        try:
            print "Minimizing on (%f, %f)" % (a_min, a_max)
            a_opt, error = n_minimize(f, ((a_min + a_max) / 2., a_min, a_max),
                    method="brent")
            done = True
        except ConvergeError, e:
            print "Didn't converge at a=", e.a
            a_min = e.a
    print
    return a_opt, error

def optimize_mesh(r_min=1e-8):
    r_max = 50
    N = 700
    solver = "dftatom"

    a, error = optimize(r_min=r_min, r_max=50, N=700, solver=solver)
    print "'a' is optimized:"
    print TableForm([[r_min], [r_max], [a], [N]],
                headings=(("r_min", "r_max", "a", "N"), ("Mesh parameters",)))
    print "total error: %e" % error
    result = {
            "r_min": r_min,
            "r_max": r_max,
            "a": a,
            "N": N,
            "solver": solver,
            "error": error,
        }
    return result

a = 1e-7
b = 1e-6
results = []
r_min_list = arange(a, b, (b-a)/20.)
print "Optimizing for:"
print r_min_list
for r_min in r_min_list:
    print "Calculating:", r_min
    r = optimize_mesh(r_min)
    results.append(r)
    print "Done calculating:", r_min

f = open("results.json", "w")
encoder.FLOAT_REPR = lambda o: format(o, '.15e')
dump(results, f)
