import random


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_seq_tree(n, s=""):
    """Builds a game tree for sequence game where final move has bitsring
    of length n."""
    if n == 0:
        return None

    p = Node(s)

    p.left = build_seq_tree(n-1, s=p.value + "0")
    p.right = build_seq_tree(n-1, s=p.value + "1")
    return p


def intrav_print(root):
    if root is None:
        return

    intrav_print(root.left)
    print root.value
    intrav_print(root.right)


def assign_moves(root, first, second, moves={}):
    """Assigns moves alternating between first and second names."""
    if root is None:
        return

    assign_moves(root.left, first, second, moves=moves)
    if len(root.value) % 2 != 0:
        moves[root.value] = first
    else:
        moves[root.value] = second
    assign_moves(root.right, first, second, moves=moves)


def assign_values(root, values={}):
    """Assigns random values on [-1, +1] to leaf nodes of tree"""
    if root.left is None and root.right is None:
        values[root.value] = random.uniform(-1, 1)
        return
    assign_values(root.left, values=values)
    assign_values(root.right, values=values)


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-n", "--nmoves", dest="n", help="number of moves")
    parser.add_option("-f", "--first", dest="first", help="first player")
    parser.add_option("-s", "--second", dest="second", help="second player")

    (options, args) = parser.parse_args()

    n = int(options.n)
    first = options.first
    second = options.second

    tree = build_seq_tree(n)
    intrav_print(tree)

    moves = {}
    assign_moves(tree, first, second, moves=moves)
    del moves[""]

    print "Moves = "
    for k, v in moves.items():
        print k, v

    val = {}
    assign_values(tree, values=val)
    print "values = "
    for k, v in val.items():
        print k, v
