from qsnake.atom import solve_hydrogen_like_atom

solve_hydrogen_like_atom(82, {
        "r_min": 1e-10,
        "r_max": 42.4813927645,
        "a": 7928200510.27,
        "N": 5382,
        }, {
        "solver": "dftatom",
        }
    )
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
