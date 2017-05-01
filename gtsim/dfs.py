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
    """
    Runs dfs to initialize game moves and leaf node values

    Note:
        The first move is at the depth 1 and every odd depth. The second player
        moves on nodes at even depth. We mark leaf nodes with +1 if the first
        player wins, and -1 if the second player wins.
    """
    global time
    color[u] = GRAY

    time += 1
    depth[u] = time
    u.set_start(time)

    # Odd depth is the first player.
    if depth[u] % 2 != 0:
        moves[u] = first
        if u is not None and u == Node(0, 0, 0):
            value[u] = 1
    # Even depth is the second player.
    else:
        moves[u] = last
        if u is not None and u == Node(0, 0, 0):
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


def dfs_visit(graph, u):
    """Runs dfs_visit on a source node u. This also computes minimax values
    for each vertex for nim game play. dfs_visit assumes that values and
    moves are already initialized"""
    global time
    # Store the values if paul plays first or carole plays first
    p = -float('Inf')
    c = float('Inf')

    if u == Node(0, 0, 0):
        return (1, -1)

    time += 1
    u.set_start(time)

    color[u] = GRAY
    for v in graph.adj[u]:
        if color.get(v, WHITE) == WHITE:
            (p0, c0) = dfs_visit(graph, v)
            p = max(p, c0)
            c = min(c, p0)
            if DEBUG:
                print "dfs_visit(g, {}) -> ({})".format(v, (p0, c0))

    # When u is black values for paul and carole are recusively defined and
    # p and c store repsective max an mins for paul and carole.
    color[u] = BLACK
    time += 1
    u.set_finish(time)
    return (p, c) 


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
    parser.add_option("-c", "--csv",
                      dest="csv", help="csv file output")

    (options, args) = parser.parse_args()

    x = int(options.x)
    y = int(options.y)
    z = int(options.z)

    first = options.first
    last = options.last
    filename = ""
    if options.csv:
        filename = "nim_{}_{}_{}_{}_{}.csv".format(x, y, z, first, last)

    # Create nim states
    start = Node(x, y, z)
    nim = Graph()
    make_graph(start, graph=nim)

    # Init dfs to assign moves and leaf nodes
    time = 0
    dfs_init(nim, first, last)

    # Reset colors otherwise dfs won't traverse graph after init
    reset_dfs_colors(nim)
    time = 0
    vpaul, vcarole = dfs_visit(nim, start)

    print "----------------------------------"
    print "starting state: ", str(start), (vpaul, vcarole)
    print "first play: ", first
    print "last play: ", last
    print "winner: ", vpaul if first == 'paul' else vcarole 
    print "graph size n: ", len(nim.adj)
    print "graph parity: ", 'even' if len(nim.adj) % 2 == 0 else 'odd'
    print "----------------------------------"

    if filename:
        z = Node(0, 0, 0)
        outcomes = [value[k] for k in value.keys() if k == z]
        o = ""
        for i in range(0, len(outcomes)):
            o += str(outcomes[i]) + ", "
        o += str(outcomes[-1])
        with open(filename, 'w') as f:
            f.write(str(winner) + '\n')
            f.write(o)
