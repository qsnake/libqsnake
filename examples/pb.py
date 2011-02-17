from qsnake.atom import solve_hydrogen_like_atom

Z = 82
mesh_params = {
        "r_min": 5e-8,
        "r_max": 20,
        "a": 20000,
        "N": 30000,
        }
solver_params = {
        "solver": "elk",
        }
solve_hydrogen_like_atom(Z, mesh_params, solver_params)
