from .nim import Node, Graph, make_graph

# Global variables for dfs state
color = {}
value = {}
depth = {}
moves = {}

# dfs colors
WHITE = -1
GRAY = 0
BLACK = 1

# print debug statements
DEBUG = 1


def dfs_visit_init(graph, u, first, last):
    """Runs dfs to initialize game moves and leaf node values"""
    global time
    color[u] = GRAY

    # Use the parity of the depth to determine who moves on what level.
    time += 1
    depth[u] = time
    u.set_start(time)

    # The first move is at the depth 1 and every odd depth.
    # Second player moves on even nodes.
    if depth[u] % 2 != 0:
        moves[u] = first
        if u is not None and u == Node(0, 0, 0):
            # assign a +1 for the first player for a leaf
            value[u] = 1
    else:
        moves[u] = last
        if u is not None and u == Node(0, 0, 0):
            # assign a -1 for the last player for a leaf
            value[u] = -1

    for v in graph.adj[u]:
        if color.get(v, WHITE) == WHITE:
            dfs_visit_init(graph, v, first, last)

    color[u] = BLACK
    time += 1
    u.set_finish(time)


def dfs_init(graph, first, last):
    """Assign moves and leaf nodes +1 or -1 depending on if paul or carole
    wins"""
    for v in graph.adj.keys():
        color[v] = WHITE
    for v in graph.adj.keys():
        if color.get(v, WHITE) == WHITE:
            dfs_visit_init(graph, v, first, last)


def dfs_visit(graph, u, first, last):
    """Runs dfs_visit on a source node u. This also computes minimax values
    for each vertex for nim game play. dfs_visit assumes that values and
    moves are already initialized"""
    global time
    # Store the values if paul plays first or carole plays first
    p = -float('Inf')
    c = float('Inf')

    time += 1
    u.set_start(time)

    # Base case
    if u == Node(0, 0, 0):
        return value[u]

    color[u] = GRAY
    for v in graph.adj[u]:
        if color.get(v, WHITE) == WHITE:
            y = dfs_visit(graph, v, first, last)
            p = max(p, y)
            c = min(c, y)
            if DEBUG:
                print "dfs_visit(g, {}) -> ({})".format(v, y)
                print "    (p, c) -> ({}, {})".format(p, c)

    # When u is black values for paul and carole are recusively defined and
    # p and c store repsective max an mins for paul and carole.
    color[u] = BLACK
    time += 1
    u.set_finish(time)

    if moves[u] == first:
        value[u] = p
        return p
    else:
        value[u] = c
        return c


def reset_dfs_all():
    global color
    global value
    global depth
    global moves
    color = {}
    value = {}
    depth = {}
    moves = {}


def reset_dfs_colors(graph):
    global color
    color = {}
    for k in graph.adj.keys():
        color[k] = WHITE


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-x", "--xpile",
                      dest="x", help="size of pile 1")
    parser.add_option("-y", "--ypile",
                      dest="y", help="size of pile 2")
    parser.add_option("-z", "--zpile",
                      dest="z", help="size of pile 3")
    parser.add_option("-f", "--first",
                      dest="first", help="first player name")
    parser.add_option("-l", "--last",
                      dest="last", help="last player name")
    (options, args) = parser.parse_args()

    x = int(options.x)
    y = int(options.y)
    z = int(options.z)

    first = options.first
    last = options.last

    # Create nim states
    start = Node(x, y, z)
    nim = Graph()
    make_graph(start, graph=nim)

    print nim

    # Init dfs to assign moves and leaf nodes
    time = 0
    dfs_init(nim, first, last)

    # Reset colors otherwise dfs won't traverse graph after init
    reset_dfs_colors(nim)
    time = 0
    winner = dfs_visit(nim, start, first, last)

    print nim
    if DEBUG:
        print "values computed = ", len(value.keys())
        for v in value.keys():
            print v, value[v]

    print "----------------------------------"
    print "starting state: ", str(start), winner
    print "first play: ", first
    print "last play: ", last
    print "winner: ", 'paul' if winner == 1 else 'carole'
    print "graph size n: ", len(nim.adj)
    print "graph parity: ", 'even' if len(nim.adj) % 2 == 0 else 'odd'
    print "----------------------------------"
