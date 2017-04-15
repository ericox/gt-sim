class Node(object):
    """
    Node class representing a node with a single value
    in a graph
    """
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x

    def __str__(self):
        return str(self._value)


class Digraph(object):
    """
    A directed acyclic graph ADT.

    Interface:
        V() (int) the number of vertices
        E() (int) the number of edges
        addEdge(u, v) add an edge from u to v
        adj(v) (iterable) of neighbors of v
    """
    def __init__(self):
        self._adj = {}
        self._v = 0
        self._e = 0

    @property
    def v(self):
        return self._v

    @property
    def e(self):
        return self._e

    def addEdge(self, u, v):
        if u not in self._adj:
            self._adj[u] = []
        self._adj[u].append(v)
        self._v += 2
        self._e += 1

    def adj(self, u):
        return self._adj[u]

if __name__ == "__main__":
    u = Node(10)
    v = Node(20)
    g = Digraph()
    print u
    print v
    g.addEdge(u, v)
    g.addEdge(v, None)
    for e in g.adj(v):
        print e
