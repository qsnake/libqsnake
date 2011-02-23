import sys
from math import sqrt

from numpy import array

from plot import plot_mesh_mpl, return_mpl_figure
import triangulation

class Mesh:
    """
    Represents a FE mesh.

    Currently the mesh is 2D and is defined by a set of nodes and elements.
    Elements could be either a set of 3 nodes (triangle) or 4 nodes (quad).  It
    can be made more general in the future.

    This "class" contains methods to export this mesh in the hermes2d (and
    other) formats. For more information refer to the export_mesh() function.

    Example:

    >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
    >>> m.nodes
    [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]
    >>> m.elements
    [[1, 0, 2], [2, 0, 3]]
    >>> m.boundaries
    [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
    >>> m.curves
    []
    """

    def __init__(self, nodes=[], elements=[], boundaries=[], curves=[],
            orders=[]):
        self._nodes = nodes
        self._elements = elements
        self._boundaries = boundaries
        self._curves = curves
        self._orders = orders

    def __str__(self):
        return """Mesh:
        nodes:
        %s
        elements:
        %s
        boundaries:
        %s
        curves:
        %s""" % (self._nodes, self._elements, self._boundaries, self._curves)

    @property
    def nodes(self):
        """
        Returns the mesh nodes.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.nodes
        [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]
        >>> m.elements
        [[1, 0, 2], [2, 0, 3]]
        >>> m.boundaries
        [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
        >>> m.curves
        []

        """
        return self._nodes

    @property
    def elements(self):
        """
        Returns the mesh elements.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.nodes
        [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]
        >>> m.elements
        [[1, 0, 2], [2, 0, 3]]
        >>> m.boundaries
        [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
        >>> m.curves
        []

        """
        return self._elements

    @property
    def elems(self):
        """
        Returns the mesh elements.

        This is a shortcut for self.elements.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.elems
        [[1, 0, 2], [2, 0, 3]]

        """
        return self.elements

    @property
    def boundaries(self):
        """
        Returns the mesh boundaries.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.nodes
        [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]
        >>> m.elements
        [[1, 0, 2], [2, 0, 3]]
        >>> m.boundaries
        [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
        >>> m.curves
        []

        """
        return self._boundaries

    @property
    def orders(self):
        return self._orders

    @property
    def bdy(self):
        """
        Returns the mesh boundaries.

        This is a shortcut for self.boundaries.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.bdy
        [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
        >>> m.curves
        []

        """
        return self.boundaries

    @property
    def curves(self):
        """
        Returns the mesh curves.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.nodes
        [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]
        >>> m.elements
        [[1, 0, 2], [2, 0, 3]]
        >>> m.boundaries
        [[3, 2, 1], [2, 1, 2], [1, 0, 3], [0, 3, 4]]
        >>> m.curves
        []

        """
        return self._curves

    def plot(self, filename="a.png", method="nice", lab=True):
        """
        Plots the mesh using matplotlib.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.plot() # plots the mesh

        """
        if method == "simple":
            f = triangulation.plot_tria_mesh(self._nodes, self._elements,
                    filename=filename, save=not lab)
            if lab:
                return_mpl_figure(f)
            else:
                f.savefig(filename, format='png', dpi=80)
        elif method == "nice":
            polygons, orders = self.to_polygons_orders()
            f = plot_mesh_mpl(polygons, orders)
            if lab:
                return_mpl_figure(f)
            else:
                f.savefig(filename, format='png', dpi=80)
        else:
            raise ValueError("Unknown method")

    def show(self, filename="a.png"):
        """
        Plots the mesh using matplotlib.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.show() # plots the mesh

        """
        self.plot(filename=filename)

    def to_polygons_orders(self):
        """
        Convert the mesh from Phaml representation to qsnake representation.
        """
        polygons = {}
        for n, elem in enumerate(self.elems):
            polygons[n] = array([self._nodes[i] for i in elem ])
        if self._orders == []:
            orders = None
        else:
            orders = {}
            for n, order in enumerate(self._orders):
                orders[n] = order
        return polygons, orders

    def _convert_nodes(self, a):
        """
        Internal function: prepares nodes for the flash.
        """
        s = ""
        for x, y in a:
            s += "%s %s," % (x, y)
        return s

    def _convert_elements(self, a):
        """
        Internal function: prepares elements for the flash.
        """
        s = ""
        for e in a:
            if len(e) == 3:
                s += "%s %s %s 0," % tuple(e)
            elif len(e) == 4:
                s += "%s %s %s %s 0," % tuple(e)
        return s

    def _convert_boundaries(self, a):
        """
        Internal function: prepares boundaries for the flash.
        """
        s = ""
        for b in a:
            s += ("%s %s %s,") % tuple(b)
        return s

    def _convert_curves(self, a):
        """
        Internal function: prepares curves for the flash.
        """
        s = ""
        for c in a:
            s += ("%s %s %s,") % tuple(c)
        return s

    def get_html(self, self_name="d", editor="flex"):
        """
        Returns an html for launching the flex editor.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.get_html()
        '<html>...</html>'

        """
        import sagenb.notebook.interact
        self._cell_id_edit = sagenb.notebook.interact.SAGE_CELL_ID

        if editor == "flex":
            path = "/javascript/mesh_editor"
            return """\
        <html>
        <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
        width="830" height="600">
        <param name="movie" value="%(path)s/MeshEditor.swf">
        <param name="flashvars" value="output_cell=%(cn)s&nodes=%(nodes)s&elements=%(elements)s&boundaries=%(boundaries)s&curves=%(curves)s&var_name=%(var_name)s" />
        <!--[if !IE]>-->
        <object type="application/x-shockwave-flash"
        data="%(path)s/MeshEditor.swf" width="830" height="600">
        <!--<![endif]-->
        <param name="flashvars" value="output_cell=%(cn)s&nodes=%(nodes)s&elements=%(elements)s& boundaries=%(boundaries)s&curves=%(curves)s&var_name=%(var_name)s" />
        <p>Alternative Content</p>
        <!--[if !IE]>-->
        </object>
        <!--<![endif]-->
        </object>
        </html> """ % {"path": path, "cn": self._cell_id_edit,
            "nodes": self._convert_nodes(self._nodes),
            "elements": self._convert_elements(self._elements),
            "boundaries": self._convert_boundaries(self._boundaries),
            "curves": self._convert_curves(self._curves),
            "var_name": self_name}
        else:
            raise Exception("Not implemented.")

    def export_mesh(self, lib="hermes2d"):
        """
        Exports the mesh in various FE solver formats.

        lib == "hermes2d" ... returns the hermes2d Mesh

        Currently only hermes2d is implemented.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> h = m.export_mesh()
        >>> h
        <hermes2d._hermes2d.Mesh object at 0x7f07284721c8>

        """
        if lib == "hermes2d":
            from hermes2d import Mesh
            m = Mesh()
            nodes = self._nodes
            elements = [list(e)+[0] for e in self._elements]
            boundaries = self._boundaries
            curves = self._curves
            m.create(nodes, elements, boundaries, curves)
            return m
        else:
            raise NotImplementedError("unknown library")

    def edit(self, editor="flex"):
        """
        Launches a flex editor to edit the mesh.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.edit()
        [prints an html code]

        """

        self_name = "d"
        locs = sys._getframe(1).f_locals
        for var in locs:
            if id(locs[var]) == id(self):
                self_name = var
        print self.get_html(self_name=self_name, editor=editor)

    def check_element_orientations(self):
        """
        Checks whether all elements are positively oriented.

        Example:

        >>> from qsnake import Mesh
        >>> nodes = [[-1., -1.], [1., -1.], [-1., 1.]]
        >>> elems = [(0, 1, 2)]
        >>> bdy = [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
        >>> mesh = Mesh(nodes, elems, bdy)
        >>> mesh.check_element_orientations()
        True
        >>> elems2 = [(0, 2, 1)]
        >>> mesh2 = Mesh(nodes, elems2, bdy)
        >>> mesh2.check_element_orientations()
        False

        """

        ok = True
        for elem in self.elems:
            a,b,c = elem
            ax = self.nodes[a][0]
            ay = self.nodes[a][1]
            bx = self.nodes[b][0]
            by = self.nodes[b][1]
            cx = self.nodes[c][0]
            cy = self.nodes[c][1]
            abx = bx - ax
            aby = by - ay
            acx = cx - ax
            acy = cy - ay
            z = abx*acy - aby*acx
            if z <= 0: ok = False
        return ok

    def look_up_node(self, x, y, min_edge_length):
        """
        Search the list of nodes for node with coordinates [x, y].

        Here, min_edge_length/100. is used as tolerance. If the node is
        found, return its index. If not, append it to the end of the
        list and return its index.

        Example:

        >>> from qsnake import Mesh
        >>> nodes = [[-1., -1.], [1., -1.], [-1., 1.]]
        >>> elems = [(0, 1, 2)]
        >>> bdy = [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
        >>> mesh = Mesh(nodes, elems, bdy)
        >>> min_edge_length = mesh.calc_min_edge_length()
        >>> mesh.look_up_node(1.0, -1.0, min_edge_length)
        1
        >>> mesh.look_up_node(1.0, 1.0, min_edge_length)
        3
        >>> print mesh.nodes
        [[-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0], [1.0, 1.0]]

        """
        counter = 0
        for node in self.nodes:
            x0, y0 = node
            dx = float(x0 - x)
            dy = float(y0 - y)
            if sqrt(dx**2 + dy**2) < 0.01*min_edge_length:
                found = 1
                return counter
            counter += 1
        self.nodes.append([x, y])
        return counter

    def triangulate(self, debug=False):
        """
        Triangulates the domain.

        Returns an instance of the Mesh() class that contains the triangular
        mesh.

        Example:

        >>> d = Domain([[0, 1], [1, 1], [1, 0], [0, 0]], [(0, 3), (3, 2), (2, 1), (1, 0)])
        >>> m = d.triangulate()
        >>> m
        <qsnake.domain.Mesh instance at 0x2d4c0e0>
        >>> m.nodes
        [[0, 1], [1, 1], [1, 0], [0, 0]]
        >>> m.elements
        [(1, 0, 2), (2, 0, 3)]
        >>> m.boundaries
        [[0, 3, 1], [3, 2, 1], [2, 1, 1], [1, 0, 1]]

        """
        from triangulation import triangulate_af
        if debug:
            print "Triangulating..."
            print "List of points:", self._nodes
            print "List of boundary edges:", self._boundaries

        boundaries = [(b[0],b[1]) for b in self._boundaries]
        elems = triangulate_af(self._nodes, boundaries)
        #boundaries = [list(b)+[1] for b in self._edges]
        if debug:
            print "List of elements:", elems

        self._elements = elems

    def refine_element(self, elem, min_edge_length):
        """
        Refine a triangular element

        Here 'elem' is a triple of indices [a,b,c], and
        min_edge_length is the length of the shortest edge
        in the mesh.

        Example:

        >>> from qsnake import Mesh
        >>> nodes = [[-1., -1.], [1., -1.], [-1., 1.]]
        >>> elems = [(0, 1, 2)]
        >>> bdy = [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
        >>> mesh = Mesh(nodes, elems, bdy)
        >>> print mesh
        Mesh:
            nodes:
                [[-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]]
            elements:
                [(0, 1, 2)]
            boundaries:
                [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
            curves:
                []
        >>> min_edge_length = mesh.calc_min_edge_length()
        >>> mesh.refine_element((0, 1, 2), min_edge_length)
        >>> print mesh
        Mesh:
        nodes:
            [[-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0], (0.0, -1.0), (0.0, 0.0), (-1.0, 0.0)]
        elements:
            [(0, 3, 5), (3, 1, 4), (5, 3, 4), (5, 4, 2)]
        boundaries:
            [[0, 3, 1], [3, 1, 1], [1, 4, 2], [4, 2, 2], [2, 5, 3], [5, 0, 3]]
        curves:
            []

        """
        assert len(elem) == 3
        a, b, c = elem
        ax = self.nodes[a][0]
        ay = self.nodes[a][1]
        bx = self.nodes[b][0]
        by = self.nodes[b][1]
        cx = self.nodes[c][0]
        cy = self.nodes[c][1]
        self.elems.remove(elem)
        d = self.look_up_node((ax + bx)/2., (ay + by)/2., min_edge_length)
        e = self.look_up_node((bx + cx)/2., (by + cy)/2., min_edge_length)
        f = self.look_up_node((cx + ax)/2., (cy + ay)/2., min_edge_length)
        self.elems.append((a, d, f))
        self.elems.append((d, b, e))
        self.elems.append((f, d, e))
        self.elems.append((f, e, c))
        # updating the list of bdy edges if necessary
        bdy_temp = self.bdy[:]
        for edge in bdy_temp:
            a0,b0,marker = edge
            if (a == a0 and b == b0) or (b == a0 and a == b0):
                self.bdy.remove(edge)
                self.bdy.append([a,d,marker])
                self.bdy.append([d,b,marker])
            if (b == a0 and c == b0) or (c == a0 and b == b0):
                self.bdy.remove(edge)
                self.bdy.append([b,e,marker])
                self.bdy.append([e,c,marker])
            if (c == a0 and a == b0) or (a == a0 and c == b0):
                self.bdy.remove(edge)
                self.bdy.append([c,f,marker])
                self.bdy.append([f,a,marker])

    def refine_all_elements(self):
        """
        Call refine_all_elements() to refine certain elements in the mesh.

        Example:

        >>> m = Mesh([[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0],],[[1,0,2],[2,0,3],],[[3,2,1],[2,1,2],[1,0,3],[0,3,4],],[])
        >>> m.elems
        [[1, 0, 2], [2, 0, 3]]
        >>> m.refine_all_elements()
        >>> m.elems
        [(1, 9, 11), (9, 4, 10), (11, 9, 10), (11, 10, 6), (4, 12, 14), (12, 0,
        13), (14, 12, 13), (14, 13, 5), (6, 10, 15), (10, 4, 14), (15, 10, 14),
        (15, 14, 5), (6, 15, 17), (15, 5, 16), (17, 15, 16), (17, 16, 2), (2,
        16, 19), (16, 5, 18), (19, 16, 18), (19, 18, 8), (5, 13, 21), (13, 0,
        20), (21, 13, 20), (21, 20, 7), (8, 18, 22), (18, 5, 21), (22, 18, 21),
        (22, 21, 7), (8, 22, 24), (22, 7, 23), (24, 22, 23), (24, 23, 3)]

        """
        elems_tmp = self.elems[:]
        min_edge_length = self.calc_min_edge_length()
        for elem in elems_tmp:
            self.refine_element(elem, min_edge_length)

    def calc_min_edge_length(self):
        """
        Calculates min elem edge length.

        This parameter divided by 100.0 is used as tolerance
        to decide whether two nodes are the same or not.

        Example:

        >>> from qsnake import Mesh
        >>> nodes = [[-1., -1.], [1., -1.], [-1., 1.]]
        >>> elems = [(0, 1, 2)]
        >>> bdy = [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
        >>> mesh = Mesh(nodes, elems, bdy)
        >>> print mesh.calc_min_edge_length()
        2.0
        >>> mesh.refine_all_elements()
        >>> print mesh.calc_min_edge_length()
        1.0

        """
        min_edge_length = 10e10
        for elem in self.elems:
            a, b, c = elem
            ax = self.nodes[a][0]
            ay = self.nodes[a][1]
            bx = self.nodes[b][0]
            by = self.nodes[b][1]
            cx = self.nodes[c][0]
            cy = self.nodes[c][1]
            ab_length = sqrt((bx - ax)**2 + (by - ay)**2)
            bc_length = sqrt((cx - bx)**2 + (cy - by)**2)
            ca_length = sqrt((cx - ax)**2 + (cy - ay)**2)
            if ab_length < min_edge_length: min_edge_length = ab_length
            if bc_length < min_edge_length: min_edge_length = bc_length
            if ca_length < min_edge_length: min_edge_length = ca_length
        return min_edge_length

    def is_boundary_node(self, i):
        """
        Decides whether a node lies on the boundary, if it does it
        will return True, otherwise it will return False.

        Here 'i' is the node's index.

        Example:

        >>> from qsnake import Mesh
        >>> nodes = [[-1., -1.], [1., -1.], [-1., 1.]]
        >>> elems = [(0, 1, 2)]
        >>> bdy = [[0, 1, 1], [1, 2, 2], [2, 0, 3]]
        >>> mesh = Mesh(nodes, elems, bdy)
        >>> mesh.is_boundary_node(2)
        True
        >>> mesh.is_boundary_node(3)
        False

        """
        for edge in self.bdy:
            a,b,marker = edge
            if i == a or i == b:
                return True
        return False
