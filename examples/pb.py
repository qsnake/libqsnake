from qsnake.atom import solve_hydrogen_like_atom

Z = 82
mesh_params = {
        "r_min": 1e-8,
        "r_max": 50,
        "a": 200000,
        "N": 2000,
        }
solver_params = {
        }
solve_hydrogen_like_atom(Z, mesh_params, solver_params)
