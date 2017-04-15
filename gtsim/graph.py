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


class Edge(object):
    """
    Edge class representing an edge with src and dst nodes.
    """
    def __init__(self, src, dst):
        """
        _src: (Node) source node of an edge
        _dst: (Node) destination node of an edge
        """
        self._src = src
        self._dst = dst

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, node):
        self._src = node

    @property
    def dst(self):
        return self._dst

    @dst.setter
    def dst(self, node):
        self._dst = node
