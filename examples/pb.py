from qsnake.atom import solve_hydrogen_like_atom
from qsnake.mesh import optimize_parameter

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
optimize_parameter(f, (20000, 1, None))
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
