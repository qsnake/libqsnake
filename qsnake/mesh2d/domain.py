import sys
from mesh import Mesh

class Domain:
    """
    Represents an FE domain.

    Currently the domain is 2D and is defined by a set of nodes and
    boundary edges.

    The edges representing the domain are sorted and positevly oriented in
    a counter clockwise  manner.  If your domain (polygon) includes holes,
    the edges representing the holes will be sorted and negatively oriented
    in a clockwise manner.  If the edges do not form a closed curve an
    exception is raised.

    Example:

    >>> import qsnake
    >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
    >>> d.nodes
    [[0, 0], [0, 1], [1, 1], [1, 0], [0.25, 0.25], [0.25, 0.75], [0.75,
    0.5]]
    >>> d.edges
    [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 4]]
    >>> d.edit() # launches a javascript editor

    The last line in the example above "d.edit()" launches a javascript editor
    to view or modify your domain.  In the example above, "edges" are made up
    by vertices in the "nodes" list.

    """

    @classmethod
    def geometry(cls, nodes, edges):
        """
        Constructs the Domain() class from the output of the graph_editor.

        The graph_editor returns nodes and edges in a specific format (as
        dictionaries), so we need to convert them into the Domain() format.

        Example:

        >>> d = Domain.geometry({0:[69,269],1:[284,267],2:[285,107],
                3:[75,99]}, {0:[1,3],1:[0,2],2:[1,3],3:[2,0]})
        >>> d.nodes
        [[0.0, 0.99999999999999989], [0.99537037037037024, 0.98823529411764699], [1.0, 0.047058823529411709], [0.02777777777777779, 0.0]]
        >>> d.edges
        [(0, 3), (3, 2), (2, 1), (1, 0)]

        """
        from triangulation import convert_graph
        nodes, edges = convert_graph(nodes, edges)
        d = Domain(nodes, edges)
        d.normalize()
        return d

    def __init__(self, nodes=[], edges=[]):
        from triangulation import (find_loops, orient_loops,
                any_edges_intersect)
        if len(edges) != 0:
            loops = find_loops(edges)
            edges = orient_loops(nodes, loops)
            if any_edges_intersect(nodes, edges):
                raise Exception("Two or more edges intersect.")
        self._nodes = nodes
        self._edges = edges

        try:
            #only used in old online lab
            import sagenb.notebook.interact
            self._cell_id_init = sagenb.notebook.interact.SAGE_CELL_ID
        except:
            pass

    def __str__(self):
        return """Domain:
        nodes:
        %s
        boundary edges:
        %s""" % (self._nodes, self._edges)

    @property
    def nodes(self):
        """
        Returns the nodes of your domain.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.nodes
        [[0, 0], [0, 1], [1, 1], [1, 0], [0.25, 0.25], [0.25, 0.75], [0.75,
        0.5]]

        A node is made up by the coordinates of a vertex.  For example, in the
        example above "[0,1]" represents a node.

        """
        return self._nodes

    @property
    def edges(self):
        """
        Returns the edges of your domain in a sorted and positively oriented
        (counter clockwise) manner.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.edges
        [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 4]]

        An edge is made up by two corresponding nodes from the "nodes" list. For
        example, in the example above "(0,3)" respresents an edge made up by nodes
        "0" and "3".

        """
        return self._edges

    def get_html(self, self_name="d", editor="js"):
        """
        Returns an html to launch an editor.

        Example:

        >>> d = Domain([[0, 1], [1, 1], [1, 0], [0, 0]], [(0, 3), (3, 2), (2, 1), (1, 0)])
        >>> d.get_html()
        '<html>...</html>'

        """
        try:
            #This is only for oldonline lab
            import sagenb.notebook.interact
            self._cell_id_edit = sagenb.notebook.interact.SAGE_CELL_ID
        except:
            pass

        if editor != "js":
            raise Exception("Editor is not implemented.")

        if editor == "js":
            path = "/javascript/graph_editor"
            edges = [[a, b] for a, b in self._edges]
            b_max = -1
            for a, b in self._nodes:
                if b > b_max:
                    b_max = b
            nodes = [[a, b_max-b] for a, b in self._nodes]
            return
        """\
        <html><font color='black'><div
        id="graph_editor_%(cell_id)s"><table><tbody><tr><td><iframe style="width: 800px;
        height: 400px; border: 0;" id="iframe_graph_editor_%(cell_id)s"
        src="%(path)s/graph_editor.html?cell_id=%(cell_id)s"></iframe><input
        type="hidden" id="graph_data_%(cell_id)s"
        value="num_vertices=%(nodes_len)s;edges=%(edges)s;pos=%(nodes)s;"><input
        type="hidden" id="graph_name_%(cell_id)s"
        value="%(var_name)s"></td></tr><tr><td><button onclick="
        var f, g;
        g = $('#iframe_graph_editor_%(cell_id)s')[0].contentWindow.update_sage();
        if (g[2] == '') {
        alert('You need to give a Sage variable name to the graph, before saving it.');
        return;
        }

        f = g[2] + ' = Domain.geometry(' + g[1] + ', ' + g[0] + ')';
        autogenerated_cell(%(cell_id)s, f);
        ">Save</button><button
        onclick="cell_delete_output(%(cell_id)s);">Close</button></td></tr></tbody></table></div></font></html>
        """ % {"path": path,
        "cell_id_save": self._cell_id_init,
        "cell_id": self._cell_id_edit,
        "nodes": nodes,
        "nodes_len": len(self._nodes),
        "edges": edges,
        "var_name": self_name}

    def edit(self, editor="js"):
        """
        Launches a javascript editor to view or edit the domain.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.nodes
        [[0, 0], [0, 1], [1, 1], [1, 0], [0.25, 0.25], [0.25, 0.75], [0.75,
        0.5]]
        >>> d.edges
        [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 4]]
        d.edit()

        In the example above, the commands "d.nodes" and "d.edges" were inserted
        simply to compare the javascript editor with what we have.  The command
        "d.edit()" launches the javascript editor.

        """
        self_name = "d"
        locs = sys._getframe(1).f_locals
        for var in locs:
            if id(locs[var]) == id(self):
                self_name = var
        print self.get_html(self_name=self_name, editor=editor)

    def fit_into_rectangle(self, x0, y0, w, h):
        """
        Resizes the domain to fit within the given rectangle.

        The first two parameters inserted "x0, y0" make up the bottom left origin
        of the rectangle.  Followed by this are the paramters "w" and "h" which
        make up the width and height of the rectangle respectively.

        The angles of the original domain are preserved.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.fit_into_rectangle(0, 0, 2, 2)
        >>> d.nodes
        [[0.0, 0.0], [0.0, 2.0], [2.0, 2.0], [2.0, 0.0], [0.5, 0.5], [0.5, 1.5], [1.5, 1.0]]
        >>> d.edges
        [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 4]]

        In the example above, notice how our domain was resized according to the
        parameters fed; this can be verified and seen after the "d.nodes" command.
        The  command "d.fit_into_rectangle(0, 0, 2, 2)" accomplished the job of resizing
        our domain.

        """
        if w <= 0 or h <= 0:
            raise Exception("The width and height must be positive.")
        pts_list = self._nodes
        min_x, min_y = max_x, max_y = pts_list[0]
        for x, y in pts_list:
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y
        def transform(x, x0, w, min, max):
            if abs(max - min) < 1e-12:
                c2 = 0
            else:
                c2 = float(w)/(max-min)
            c1 = x0 - c2*min
            return c1 + c2*x
        pts_list = [ [
                transform(x, x0, w, min_x, max_x),
                transform(y, y0, h, min_y, max_y)
                ] for x, y in pts_list]
        self._nodes = pts_list

    def normalize(self):
        """
        Transforms the domain to fit within a (0, 1)x(0, 1) rectangle.

        The vertex coordinates which make up the nodes are transformed accordingly
        and the angles of the domain are preserved.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0.0,0.0],[0.0,2.0],[2.0,2.0],[2.0,0.0],[0.5,0.5],[0.5,1.5],[1.5,1.0]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.nodes
        [[0.0, 0.0], [0.0, 2.0], [2.0, 2.0], [2.0, 0.0], [0.5, 0.5], [0.5, 1.5],
        [1.5, 1.0]]
        >>> d.normalize()
        >>> d.nodes
        [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.25, 0.25], [0.25,
        0.75], [0.75, 0.5]]

        In the example above, to illustrate the post "normalization", we first went ahead
        and displayed the original node coordinates with the command "d.nodes".  We then
        normalized with the command "d.normalize()", and displayed the node coordinates
        post normalization.  In the example above, as an example, "[0.75, 0.5]" represents
        a node.

        """
        self.fit_into_rectangle(0, 0, 1, 1)

    @property
    def boundary_closed(self):
        """
        Returns True if the boundary edges form a closed curve.  Otherwise
        an exception is raised.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
        >>> d.boundary_closed
        True
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[4,5],[5,6],[6,4]])
        Exception: Boundary is not closed.

        Notice in the example above that there was no need to execute the command
        "d.boundary_closed" a second time.  This is because after we evaluated
        the command "d = qsnake.Domain()" the second time, the algorithm immediately
        noticed that our boundary edges did not form a closed curve, and the proper
        exception was raised!

        """
        from triangulation import edges_is_closed_curve
        return edges_is_closed_curve(self._edges)

    def boundary_area(self):
        """
        Calculates the (oriented) area of the domain.

        Note that this evaluation also works with domains with holes.  The area of
        the hole(s) will simply be subtracted from the total area.

        Example:

        >>> import qsnake
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.75],[0.75,0.25]],[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],
        [6,7],[7,4]])
        >>> d.edges
        [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 7], [7, 4]]
        >>> d.boundary_area()
        0.75
        >>> d = qsnake.Domain([[0,0],[0,1],[1,1],[1,0]],[[0,3],[3,2],[2,1],[1,0]])
        >>> d.boundary_area()
        1.0

        Notice from the command "d.edges" that the outside domain edges are first sorted
        and positively oriented in a counter clockwise fashion before the calculation;
        The hole edges in the domain are negatively (clockwise) oriented so as to be
        subtracted from the total area.  This can further be observed when we evaluate
        for the second time "d.boundary_area()" for the domain without the hole.

        """
        from triangulation import polygon_area
        return polygon_area(self._nodes, self._edges)

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
            print "List of boundary edges:", self._edges
        elems = triangulate_af(self._nodes, self._edges)
        boundaries = [list(b)+[1] for b in self._edges]
        if debug:
            print "List of elements:", elems
            print "List of boundaries:", boundaries
        return Mesh(self._nodes, elems, boundaries)
