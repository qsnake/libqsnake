from qsnake.atom import solve_hydrogen_like_atom

Z = 82
mesh_params = {
        "r_min": 1e-6,
        "r_max": 50,
        "a": 20000,
        "N": 1000,
        }
solver_params = {
        }
solve_hydrogen_like_atom(Z, mesh_params, solver_params)
