from qsnake.atom import solve_hydrogen_like_atom

Z = 82
mesh_params = {
        "r_min": 1e-10,
        "r_max": 42.4813927645,
        "a": 7928200510.27,
        "N": 5382,
        }
solver_params = {
        "solver": "elk",
        }
solve_hydrogen_like_atom(Z, mesh_params, solver_params)
