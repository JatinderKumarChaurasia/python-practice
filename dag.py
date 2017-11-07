from collections import deque
from copy import deepcopy


class Arc:
    """
    Represents a graph node, with a value and list on neighbours
    """

    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight

    def __str__(self):
        return "{0} -> {1}".format(self.origin, self.destination)

    def __repr__(self):
        return "{0} -> {1}".format(self.origin, self.destination)

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination

    def __hash__(self):
        return hash(repr(self))


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
        curr_arc, history, visited = step
        visited.add(curr_arc)

        # we took a step - it may lead us to victory! so need to write it down
        history.append(curr_arc)

        if curr_arc.destination == to_node:
            all_paths.append(history)
            return

        new_edges = [(arc, deepcopy(history), visited) for arc in in_graph if
                     (arc.origin == curr_arc.destination and (arc not in visited or arc.destination == to_node))]
        paths_queue.extend(new_edges)

        return

    # get all the edges that start at the "from" node
    starting_paths = [(arc, [], set(arc.origin)) for arc in in_graph if arc.origin == from_node]
    paths_queue = deque()
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
    print("Paths1:", paths1)
    assert find_all_paths("X", "Z", triangles) == [[Arc("X", "V", 4), Arc("V", "Z", 3)],
                                                   [Arc("X", "Z", 9)],
                                                   [Arc("X", "Y", 2), Arc("Y","V", 5), Arc("V", "Z", 3)]]

    paths_to_self = find_all_paths("X", "X", triangles)
    assert paths_to_self == [[Arc("X", "V", 4), Arc("V", "Z", 3), Arc("Z", "X", 11)],
                             [Arc("X", "Z", 9), Arc("Z", "X", 11)],
                             [Arc("X", "Z", 9), Arc("Z", "Y", 6), Arc("Y", "V", 5), Arc("V","Z",3), Arc("Z","X", 11)],
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

    paths = find_all_paths("C", "C", my_graph)
    for path in paths:
        print("Path: {}".format(path))

    def paths_with_predicate(paths, predicate):
        """
        Half the problems presented will rely on the ability to filter paths by a predicate
        :param paths:
        :param predicate:
        :return:
        """
        return list(filter(lambda path: predicate(path), paths))

    def compute_path_cost(path):
        """
        just what it says
        :param path:
        :return:
        """
        cost = 0
        for arc in path:
            cost = cost + path[2]
        return cost
