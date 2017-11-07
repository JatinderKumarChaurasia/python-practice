from collections import deque
from copy import deepcopy


class Arc:
    """
    Represents an edge(arc) of a directed graph node
    """

    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight

    def __str__(self):
        return "{0} -> {1}".format(self.origin, self.destination)

    def __repr__(self):
        return "{0} -({2})-> {1}".format(self.origin, self.destination, self.weight)

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination

    def __hash__(self):
        return hash(repr(self))


def paths_with_predicate(paths, predicate):
    """
    Half the problems presented will rely on the ability to filter paths by a predicate
    :param paths:
    :param predicate:
    :return:
    """
    return list(filter((lambda path: predicate(path)), paths))


def path_cost(path):
    """
    just what it says
    :param path:
    :return:
    """
    cost = 0
    for arc in path:
        cost = cost + arc.weight
    return cost


def find_all_paths(from_node, to_node, in_graph):
    """
    Find all the paths from from_node to to_node in in_graph
    :param from_node:
    :param to_node:
    :param in_graph: list of tuples of the form (V1, V2, Weight)
    :return: list of paths
    """
    all_paths = []

    def take(step, paths_queue):
        # each step carries a history of all of its preceding steps, and a set of nodes visited on those
        curr_arc, history, visited = step
        visited.add(curr_arc)

        # we took a step - write it down in history
        history.append(curr_arc)

        if curr_arc.destination == to_node:  # we've reached it - this path is done
            all_paths.append(history)
            return

        new_edges = [(arc, deepcopy(history), visited) for arc in in_graph if
                     (arc.origin == curr_arc.destination and (arc not in visited
                                                              or arc.destination == to_node))]
        # I feel bad about the line above: we're not considering edges that lead to nodes that are already
        # visited, _except_ if it happens to be our destination node. Makes me feel I've missed some elegance =)
        paths_queue.extend(new_edges)

        return

    # get all the edges that start at the "from" node
    starting_paths = [(arc, [], set(arc.origin)) for arc in in_graph if arc.origin == from_node]
    paths_queue = deque()  # a queue of active paths, representing a possible journey to the destination
    paths_queue.extend(starting_paths)
    # ...and dive in
    while len(paths_queue) != 0:
        step = paths_queue.pop()
        take(step, paths_queue)

    return all_paths;


if __name__ == "__main__":
    triangles = [
        Arc("X", "Y", 2),
        Arc("X", "Z", 9),
        Arc("X", "V", 4),
        Arc("Y", "V", 5),
        Arc("V", "Z", 3),
        Arc("Z", "Y", 6),
        Arc("Z", "X", 11)
    ]
    # let's call this a test suite..
    paths1 = find_all_paths("X", "Z", triangles)
    assert find_all_paths("X", "Z", triangles) == [[Arc("X", "V", 4), Arc("V", "Z", 3)],
                                                   [Arc("X", "Z", 9)],
                                                   [Arc("X", "Y", 2), Arc("Y", "V", 5), Arc("V", "Z", 3)]]

    paths_to_self = find_all_paths("X", "X", triangles)
    assert paths_to_self == [[Arc("X", "V", 4), Arc("V", "Z", 3), Arc("Z", "X", 11)],
                             [Arc("X", "Z", 9), Arc("Z", "X", 11)],
                             [Arc("X", "Z", 9), Arc("Z", "Y", 6), Arc("Y", "V", 5), Arc("V", "Z", 3),
                              Arc("Z", "X", 11)],
                             [Arc("X", "Y", 2), Arc("Y", "V", 5), Arc("V", "Z", 3), Arc("Z", "X", 11)]]

    # graph in the original problem
    graph = [Arc("A", "B", 5),
             Arc("A", "E", 7),
             Arc("A", "D", 5),
             Arc("B", "C", 4),
             Arc("C", "D", 8),
             Arc("C", "E", 2),
             Arc("D", "E", 6),
             Arc("E", "B", 3),
             Arc("D", "C", 8)]

    my_graph = [
        Arc("A", "B", 5),
        Arc("A", "E", 7),
        Arc("A", "D", 5),
        Arc("B", "C", 4),
        Arc("C", "D", 8),
        Arc("C", "E", 2),
        Arc("D", "E", 6),
        Arc("E", "B", 3),
        Arc("D", "C", 8),
        Arc("C", "A", 15)  # new edge from C back to A
    ]

    paths_c_c = find_all_paths("C", "C", my_graph)
    for path in paths_c_c:
        print("Path: {0}, cost: {1}".format(path, path_cost(path)))

    print('#' * 20)

    cheap_paths = paths_with_predicate(paths_c_c, lambda p: path_cost(p) > 26)
    for path in cheap_paths:
        print("Path: {0}, cost: {1}".format(path, path_cost(path)))