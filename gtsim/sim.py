class State(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "({}, {}, {})".format(self.a, self.b, self.c)


def nim_states(start_state):
    states = []
    for i in range(start_state.a, -1, -1):
        for j in range(start_state.b, -1, -1):
            for k in range(start_state.c, -1, -1):
                states.append(State(i, j, k))
    return states


if __name__ == "__main__":
    start = State(3, 5, 7)
    all = nim_states(start)
    for a in all:
        print a
