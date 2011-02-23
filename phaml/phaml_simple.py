"""
Python version of the example "simple".
"""
import os

from numpy import array

from phaml import Phaml
from femhub import Mesh, Solution

# This function is not used anywhere yet
def get_solution_points(polygons, orders):
    """
    Returns a list of x and y points for the values of the solution.
    """
    x = []
    y = []
    for e_id in polygons:
        e_x = list(polygons[e_id][:, 0])
        e_y = list(polygons[e_id][:, 1])
        x.extend(e_x)
        y.extend(e_y)
    return array(x), array(y)

def run(problem_number=1, params={}):
    """
    Allows to run phaml examples with various parameters.

    problem_number ... which example to run
    params         ... solver parameters (refinement strategy,
                       error tolerance, ...)

    Examples:

    >>> from femhub.examples.phaml_simple import run
    >>> import phaml
    >>> run(1, params = {
            "term_energy_err": 1e-6,
            "hp_strategy": phaml.HP_SMOOTH_PRED,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_SMOOTH_PRED,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_PRIOR2P_H1,
            })
    >>> run(2, params = {
            "term_energy_err": 1e-4,
            "hp_strategy": phaml.HP_REFSOLN_ELEM,
            })

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_file = os.path.join(current_dir, "data", "domain")
    p = Phaml(domain_file, problem_number)
    p.solve(params)
    x, y, elems, orders = p.get_mesh()
    nodes = zip(x, y)
    # Phaml counts nodes from 1, but we count from 0:
    elems = elems - 1

    mesh = Mesh(nodes, elems, [], [], orders=orders)
    sol = Solution(mesh)
    # Refine mesh for plotting purposes.
    x_plot, y_plot, elems_plot = sol.create_plotting_mesh()
    # Get solution at vertex values of the plotting mesh from Phaml.
    values_plot = p.get_solution_values(x_plot, y_plot)
    # Set the values for plotting back into the Solution
    sol.set_values(x_plot, y_plot, elems_plot, values_plot)
    # Return it to the user, so that he/she can decide what to do with it. To
    # plot it, just do sol.plot().
    return sol
