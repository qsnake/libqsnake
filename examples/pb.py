from qsnake.atom import solve_hydrogen_like_atom
from qsnake.mesh import n_minimize

def f(a):
    r = solve_hydrogen_like_atom(82, {
            "r_min": 1e-6,
            "r_max": 42.4813927645,
            "a": a,
            "N": 2000,
        }, {
            "solver": "dftatom",
        })
    return r
#optimize_parameter(f, (1620246.055619, 1, None))
n_minimize(f, (20000, 1, None), method="simplex")
stop

solve_hydrogen_like_atom(82, {
        "r_min": 1e-10,
        "r_max": 42.4813927645,
        "a": 7928200510.27,
        "N": 5382,
        }, {
        "solver": "elk",
        }
    )
