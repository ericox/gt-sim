class State(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "({}, {}, {})".format(self.a, self.b, self.c)


def next_nim_states(start):
    states = []
    for i in range(start.a, 0, -1):
        for j in range(start.b, 0, -1):
            for k in range(start.c, 0, -1):
                states.append(State(i, j, k))
    return states


def print_states(states):
    for s in states:
        print "    ", s


if __name__ == "__main__":
    print "(2, 1, 1)"
    s = next_nim_states(State(2, 1, 1))
    print_states(s)

    print "(2, 2, 1)"
    s = next_nim_states(State(2, 2, 1))
    print_states(s)

    print "(3, 2, 1)"
    s = next_nim_states(State(3, 2, 1))
    print_states(s)
