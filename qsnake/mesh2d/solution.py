from numpy import array

from plot import return_mayavi_figure, plot_sln_mayavi

class Solution(object):

    def __init__(self, mesh):
        self._mesh = mesh
        self._plot_data = None

    def _need_values(self):
        if self._plot_data is None:
            raise Exception("You need to call set_values() first")

    @property
    def mesh(self):
        return self._mesh

    def get_xy_points(self):
        x = [n[0] for n in self.mesh.nodes]
        y = [n[1] for n in self.mesh.nodes]
        return array(x), array(y)

    def set_values(self, x, y, elems, values):
        self._plot_data = (x, y, elems, values)

    # This assumes that the method create_plotting_mesh() was
    # called in advance, and it produced the arrays x_plot, y_plot, elems_plot.
    # It also assumes that Phaml was called to provide a list "values_plot" of
    # values at the points x_plot, y_plot. Finally, that set_values() were
    # called to get those values into the Solution instance.
    def plot(self):
        self._need_values()
        x_plot, y_plot, elems_plot, values_plot = self._plot_data
        f = plot_sln_mayavi(x_plot, y_plot, elems_plot, values_plot)
        return_mayavi_figure(f)

    # Splits a quadrilateral into two triangles.
    # Assumes CCW orientation of the quadrilateral.
    def split_quad(x, y, elem):
        a = elem[0]
        b = elem[1]
        c = elem[2]
        d = elem[3]
        diag_ac = sqrt((x[c] - x[a])*(x[c] - x[a]) + (y[c] - y[a])*(y[c] - y[a]))
        diag_bd = sqrt((x[d] - x[b])*(x[d] - x[b]) + (y[d] - y[b])*(y[d] - y[b]))
        # If diag_bd is shorter than diag_ac, then the resulting 
        # two triangles are abd, bcd. Otherwise they are abc, acd.
        if diag_bd < diag_ac:
            tria_1 = [a, b, d]
            tria_2 = [b, c, d]
        else:
            tria_1 = [a, b, c]
            tria_2 = [a, c, d]
        return tria_1, tria_2

    # Converts a mesh into triangles.
    # Assumes that elements in the mesh are either 
    # triangles or quadrilaterals. Assumes only
    # one order in quad elements (no directional
    # orders).
    def convert_to_triangles(self, x, y, elems, orders):
        if orders is None:
            raise ValueError("'orders' cannot be None")
        tria_elems = []
        tria_orders = []
        for elem, order in zip(elems, orders):
            if len(elem) == 3: 
                # elem is a triangle
                tria_elems.append(elem)
                tria_orders.append(order)
            else:
                # elem is a quad
                tria_1, tria_2 = split_quad(x, y, elem)
                tria_elems.append(tria_1)
                tria_elems.append(tria_2)
                tria_orders.append(order)
                tria_orders.append(order)
        return tria_elems, tria_orders

    # Raises all indices in the list of elements by offset.
    def offset_node_indices(self, offset, elems):
        for elem in elems:
            elem[0] = elem[0] + offset
            elem[1] = elem[1] + offset
            elem[2] = elem[2] + offset

    # First converts a triangular/quadrilateral mesh into
    # a purely triangular mesh, then refines it for plotting.
    # Each triangular element of order 'p' is split into
    # (p+1)*(p+2)/2 equally large triangles.
    def create_plotting_mesh(self):
        x = [n[0] for n in self.mesh.nodes]
        y = [n[1] for n in self.mesh.nodes]
        # Convert the list to triangles
        elems, orders = self.convert_to_triangles(x, y, self._mesh.elems, self._mesh.orders)
        # Create new lists for x_coordinates, y_coordinates, and 
        # elements for plotting.
        x_fine = []
        y_fine = []
        elems_fine = []
        for elem, order in zip(elems, orders):
            # This splits the element into (p+1)*(p+2)/2 smaller elements. 
            # Node indices in the resulting sub-mesh start from zero.
            new_x_list, new_y_list, new_elems = self.split(x, y, elem, order)
            # Offset node indices by the number of existing nodes.
            self.offset_node_indices(len(x_fine), new_elems)
            # Appending the new lists to the global lists.
            x_fine.extend(new_x_list)
            y_fine.extend(new_y_list)
            elems_fine.extend(new_elems)
        return array(x_fine), array(y_fine), array(elems_fine)

    
    # This splits a triangular element into (p+1)*(p+2)/2 smaller elements. 
    # Node indices in the resulting sub-mesh start from zero.
    def split(self, x, y, elem, order):
        # Denote the vertices of the triangle by a, b, c
        a = elem[0]
        b = elem[1]
        c = elem[2]
        # We need the coordinates of the point 'a'.
        ax = float(x[a])
        ay = float(y[a])
        # First we create a vector 'u' in the direction ab
        # of length |b-a|/order.
        ux = (x[b] - ax)/float(order) 
        uy = (y[b] - ay)/float(order) 
        # Next we create a vector 'v' in the direction ac
        # of length |c-a|/order.
        vx = (x[c] - ax)/float(order) 
        vy = (y[c] - ay)/float(order) 
        # The vectors u and v will help us define new points
        # inside of the triangular element "elem".
        x_new = []
        y_new = []
        for i in range(order + 1):
            for j in range(order - i + 1):
                coord_x = ax + i * ux + j * vx
                coord_y = ay + i * uy + j * vy
                x_new.append(coord_x)
                y_new.append(coord_y)
        # Now the new equidistant points in the triangular
        # element are created. They include the vertices of the
        # original triangle. Each edge of the original triangle 
        # is split into "order" equally long pieces.
        # As a last step, we need to add the small triangles.
        # We start with those aligned with the original big triangle.
        elems_new = []
        a_new = -1
        b_new = 0
        c_new = order + 1
        for i in range(order):
            a_new = a_new + 1
            b_new = b_new + 1
            for j in range(order - i):
                elems_new.append([a_new, b_new, c_new])
                a_new = a_new + 1
                b_new = b_new + 1
                c_new = c_new + 1
        # We continue with the rest.
        a_new = -1
        b_new = order + 1
        c_new = order
        for i in range(order - 1):
            a_new = a_new + 2
            b_new = b_new + 1
            c_new = c_new + 1
            for j in range(order - i - 1):
                elems_new.append([a_new, b_new, c_new])
                a_new = a_new + 1
                b_new = b_new + 1
                c_new = c_new + 1
        # Returning the new local mesh inside the original big triangle.
        # Do not forget, nodes are enumerated locally starting from zero,
        # and thus they need to be offset. 
        return x_new, y_new, elems_new
