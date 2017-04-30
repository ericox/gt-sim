class Node(object):
    """Node representation for nim game."""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.start_time = 0
        self.finish_time = 0

    def set_start(self, val):
        self.start_time = val

    def set_finish(self, val):
        self.finish_time = val

    def __str__(self):
        return "({}, {}, {}, {}/{})".format(self.x,
                                            self.y,
                                            self.z,
                                            self.start_time,
                                            self.finish_time)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y and self.z == p.z


class Graph(object):
    """A basic directed graph."""
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        """Adds an edge from u to v."""
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def add_leaf(self, u):
        self.adj[u] = []

    def __str__(self):
        s = ""
        for k in self.adj.keys():
            s += str(k) + " -> "
            for items in self.adj[k]:
                s += str(items) + " "
            s += '\n'
        return s


def make_graph(s, graph=Graph()):
    """make a graph for nim given a starting state s.

    Args:
        g (Graph) a graph that is built during recursive calls.
        s (Node) a starting state for the game nim e.g., (3, 5, 7).

    Returns:
        The starting state s.
    """
    base = Node(0, 0, 0)

    # Base case.
    if s == base:
        # add graph.add_edge(s, []) or add_edge(s, None) tricky.
        graph.add_leaf(s)
        return s

    # Remove stones from pile s[k] and make recursive calls for next states.
    for k in ['x', 'y', 'z']:
        for j in range(s[k], 0, -1):
            if k == 'x':
                q = make_graph(Node(s.x-j, s.y, s.z), graph=graph)
            elif k == 'y':
                q = make_graph(Node(s.x, s.y-j, s.z), graph=graph)
            elif k == 'z':
                q = make_graph(Node(s.x, s.y, s.z-j), graph=graph)
            graph.add_edge(s, q)
    return s


if __name__ == "__main__":
    t = Node(1, 2, 0)

    g = Graph()
    make_graph(t, graph=g)
    print g

    d = {}
    d[t] = 10
    d[t] = 11
    print d
