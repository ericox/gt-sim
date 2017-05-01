"""
Project code for CSCI-GA1170 Fundamenal Algorithms, SP 2017, Prof. Joel Spencer

Author:
Eric Cox

Collaborators:
Willam Larche
Steven Balough 

$ python -m gtsim.sequence -h
Usage: sequence.py [options]

Options:
  -h, --help            show this help message and exit
  -n N, --nmoves=N      number of moves
  -f FIRST, --first=FIRST
                        first player
  -s SECOND, --second=SECOND
                        second player
  -b BASE, --base=BASE  base of sequence digits
  -r REPORT, --report=REPORT
                        generate report data

Example:
$ python -m gtsim.sequence -n 4 -f paul -s carole -b 2
"""
import random
import Queue

DEBUG = 1

class Node(object):
    """Node that stores a single value"""
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, x):
        return self.value == x.value

    def __str__(self):
        return self.value


class Graph(object):
    """A directed graph."""
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        """Adds an edge from u to v."""
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def add_leaf(self, u):
        """add a leaf with no children."""
        self.adj[u] = []

    def __str__(self):
        s = ""
        for k in self.adj.keys():
            s += str(k) + " -> "
            for items in self.adj[k]:
                s += str(items) + " "
            s += '\n'
        return s


class SequenceDFS(object):
    """
    Represents the sequence game. It builds a graph given the sequence size
    n, first players, second players and a base for digits added to string by
    each player

    Example:
        run a game and compute winnings for sequence of 0 and 1s of size n, paul
        plays first

        # make new graph
        g = Graph()

        # Create sequence graph
        sim = SequenceDFS(g, n, first='paul', second='carole')
        sim.build_sequence()

        # inspect graph
        print g
        
         -> 0 1
         010 ->
         00 -> 000 001
         01 -> 010 011
         011 ->
         1 -> 10 11
         0 -> 00 01
         001 ->
         000 ->
         111 ->
         110 ->
         11 -> 110 111
         100 ->
         101 ->
         10 -> 100 101

        # play the game
        start = Node("")
        paul_winnings, carole_winnings = sim.dfs_visit(start)
    """
    def __init__(self, graph, n, first='paul', second='carole', base=2):
        self.g = graph
        self.n = n
        self.first = first
        self.second = second 
        self.base = base
        self.moves = {} 
        self.values = {}

    def _assign_values(self):
        """assign random values on [-1, +1] to leaf nodes"""
        for node in self.g.adj.keys():
            if len(node.value) == self.n:
                self.values[node] = random.uniform(-1, 1)

    def _is_leaf(self, node):
        """predicate to determine if a node is a leaf"""
        return len(node.value) == self.n

    def v(self):
        """returns number of vertices in graph"""
        return len(self.g.adj)

    def parity_n(self):
        """count leafs"""
        return 'even' if self.n % 2 == 0 else 'odd'

    def e(self):
        """returns number of edges in graph"""
        count = 0
        for values in self.g.adj.values():
            count += 1
        return count 

    def dfs_visit(self, u, color={}):
        """Runs dfs_visit on a source node u. This also computes minimax values
        for each vertex for nim game play. dfs_visit assumes that values and
        moves are already initialized"""
       # Store the values if paul plays first or carole plays first
        p = -float('Inf')
        c = float('Inf')

        if self._is_leaf(u):
            return (self.values[u], self.values[u])

        color[u] = 0 
        for v in self.g.adj[u]:
            # white color is -1
            if color.get(v, -1) == -1:
                (p0, c0) = self.dfs_visit(v, color=color)
                # Need to max or min the value of the other player on the next level down.
                p = max(p, c0)
                c = min(c, p0)
                if DEBUG:
                    print "dfs_visit(g, {}) -> ({})".format(v, (p0, c0))

        # When u is black values for paul and carole are recusively defined and
        # p and c store repsective max an mins for paul and carole.
        color[u] = 1 
        return (p, c) 

    def build_sequence(self, start=Node("")):
        """Builds a graph for sequence game where final move has bitsring
        of length using a modified bfs."""
        q = Queue.Queue()
        color = {}
        dist = {}
        moves = {}

        # enqueue src vertex, and color -1 for white.
        color[start.value] = -1
        dist[start.value] = 0
        self.moves[start.value] = self.first 
        q.put(start.value)
        self.g.add_leaf(start)

        # Stop when we reach 2**n - 1 nodes which will have leafs of size n.
        i = 0
        while not q.empty() and i < base**(n)-1:
            u = q.get()
            # iterate over possible next strings 
            for v in range(0, self.base):
                print v
                s = u + str(v)
                print s
                next_bit = Node(s)
                if color.get(s, -1) == -1:
                    color[s] = 0
                    q.put(s)
                    dist[s] = dist[u] + 1

                    if dist[s] % 2 == 0:
                        self.moves[s] = self.first
                    else:
                        self.moves[s] = self.second

                    self.g.add_edge(Node(u), Node(s))
                    if len(s) == self.n:
                        self.g.add_leaf(Node(s))
            i += 1
        
        self._assign_values()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-n", "--nmoves", dest="n", help="number of moves")
    parser.add_option("-f", "--first", dest="first", help="first player")
    parser.add_option("-s", "--second", dest="second", help="second player")
    parser.add_option("-b", "--base", dest="base", help="base of sequence digits")
    parser.add_option("-r", "--report", dest="report", help="generate report data")
    (options, args) = parser.parse_args()

    n = int(options.n)
    first = options.first
    second = options.second
    base = int(options.base)
    report = bool(options.report)

    g = Graph()

    # Create sequence graph
    sim = SequenceDFS(g, n, base=base)
    sim.build_sequence()

    if DEBUG:
        print "----------------------------------"
        print g
        print "----------------------------------"
    
    # play the game
    start = Node("")
    p, c = sim.dfs_visit(start)

    parity = 'even' if sim.v() % 2 == 0 else 'odd'

    if DEBUG:
        print "----------------------------------"
        print "starting state: ", str(start), (p, c)
        print "first play: ", first
        print "last play: ", second 
        print "winnings first: ", p
        print "winnings second: ", c
        print "graph size v: ", sim.v()
        print "graph size e: ", sim.e()
        print "graph parity: ", 'even' if sim.v() % 2 == 0 else 'odd'
        print "n parity: ", 'even' if n % 2 == 0 else 'odd'
        print "----------------------------------"

    if report:
        info = "{}, {}, {}, {}, {}, {}".format(n, first, second, p, c, sim.parity_n()) 
        print info
