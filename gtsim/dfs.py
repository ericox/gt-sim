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


def dfs_visit_init(graph, u, first, second, time=0):
    """Runs dfs to initialize game moves and leaf node values"""
    color[u] = GRAY

    # Use the parity of the depth to determine who moves on what level.
    time += 1
    depth[u] = time

    # The first move is at the depth 1 and every odd depth.
    # Second player moves on even nodes.
    if depth[u] % 2 == 0:
        moves[u] = second
        if u is not None and u == Node(0, 0, 0):
            # assign a -1 for the second player for a leaf
            value[u] = -1
    else:
        moves[u] = first
        if u is not None and u == Node(0, 0, 0):
            # assign a +1 for the first player for a leaf
            value[u] = 1

    for v in graph.adj[u]:
        if color.get(v, WHITE) == WHITE:
            dfs_visit_init(graph, v, first, second, time=time)
    color[u] = BLACK


def dfs_init(graph, first, second):
    """Assign moves and leaf nodes +1 or -1 depending on if paul or carole
    wins"""
    t = 0
    for v in graph.adj.keys():
        color[v] = WHITE
    for v in graph.adj.keys():
        if color.get(v, WHITE) == WHITE:
            dfs_visit_init(graph, v, first, second, time=t)


def dfs_visit(graph, u):
    """Runs dfs_visit on a source node u. This also computes minimax values
    for each vertex for nim game play. dfs_visit assumes that values and
    moves are already initialized"""
    # Store the values if paul plays first or carole plays first
    p = 0
    c = float('Inf')

    # Base case
    if u == Node(0, 0, 0):
        return value[u]

    color[u] = GRAY
    for v in graph.adj[u]:
        if color.get(v, WHITE) == WHITE:
            y = dfs_visit(graph, v)
            p = max(p, y)
            c = min(c, y)
            if DEBUG:
                print "dfs_visit(g, {}) -> ({})".format(v, y)
                print "    (p, c) -> ({}, {})".format(p, c)

    # When u is black values for paul and carole are recusively defined and
    # p and c store repsective max an mins for paul and carole.
    color[u] = BLACK
    if moves[u] == 'paul':
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
    # Create nim states
    start = Node(1, 2, 0)
    nim = Graph()
    make_graph(start, graph=nim)

    # Init dfs to assign moves and leaf nodes
    first = 'paul'
    second = 'carole'
    dfs_init(nim, first, second)

    # Reset colors otherwise dfs won't traverse graph after init
    reset_dfs_colors(nim)
    winner = dfs_visit(nim, start)

    if DEBUG:
        print "values computed = ", len(value.keys())
        for v in value.keys():
            print v, value[v]

    print "----------------------------------"
    print "starting state: ", str(start)
    print "first play: ", first
    print "second play: ", second
    print "winner: ", 'paul' if winner == 1 else 'carole'
    print "graph size n: ", len(nim.adj)
    print "graph parity: ", 'even' if len(nim.adj) % 2 == 0 else 'odd'
    print "----------------------------------"
