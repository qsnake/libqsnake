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
        }, verbose=False)
    return r
#n_minimize(f, (1620246.055619, 1, None), method="simplex")
n_minimize(f, (1618205.360366, 1, 2000000), method="brent")
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
