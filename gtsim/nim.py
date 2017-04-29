class Node(object):
    """Node representation for nim game."""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

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
        a graph containing the game nodes
    """
    base = Node(0, 0, 0)

    # Base case.
    if s == base:
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

    t = Node(2, 2, 3)

    g = Graph()
    s = make_graph(t, graph=g)

    print g
