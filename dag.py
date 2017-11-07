from collections import deque
from copy import deepcopy


def find_all_paths(from_node, to_node, in_graph):
    """
    Find all the paths from from_node to to_node in in_graph
    :param from_node:
    :param to_node:
    :param in_graph: list of tuples of the form (V1, V2, Weight)
    :return: list of paths
    """
    all_paths = deque()  # how many hours did I waste because I missed you?!

    def take(step, paths_queue):
        src, dst, weight, history, visited = step
        visited.add(dst)

        # we took a step - it may lead us to victory! so need to write it down
        history.append((src, dst, weight))

        if dst == to_node:
            all_paths.append(history)
            return

        new_edges = [(e[0], e[1], e[2], deepcopy(history), visited) for e in in_graph if e[0] == dst and e[1] not in visited]
        paths_queue.extend(new_edges)

        return

    # from our graph, which is a list of edges, get all the edges that start at the "from" node
    starting_paths = [(f, t, w, [], set()) for (f, t, w) in in_graph if f == from_node]
    paths_queue = deque()
    paths_queue.extend(starting_paths)
    # ...and dive in
    while len(paths_queue) != 0:
        step = paths_queue.pop()
        take(step, paths_queue)

    return all_paths;


if __name__ == "__main__":
    triangles = [
        ("X", "Y", 2),
        ("X", "Z", 9),
        ("X", "V", 4),
        ("Y", "V", 5),
        ("V", "Z", 3)
    ]
    # let's call this a test suite..
    assert find_all_paths("X", "Z", triangles) == deque([[("X", "V", 4), ("V", "Z", 3)],
                                                  [("X", "Z", 9)],
                                                  [("X", "Y", 2), ("Y","V", 5), ("V", "Z", 3)]])
    # graph in the original problem
    graph = [("A", "B", 5),
             ("A", "E", 7),
             ("A", "D", 5),
             ("B", "C", 4),
             ("C", "D", 8),
             ("C", "E", 2),
             ("D", "E", 6),
             ("E", "B", 3),
             ("D", "C", 8)]

    my_graph = [
        ("A", "B", 5),
        ("A", "E", 7),
        ("A", "D", 5),
        ("B", "C", 4),
        ("C", "D", 8),
        ("C", "E", 2),
        ("D", "E", 6),
        ("E", "B", 3),
        ("D", "C", 8),
        ("C", "A", 15)  # new edge from C back to A
    ]

    paths = find_all_paths("A", "A", my_graph)
    for path in paths:
        print("Path: {}".format(path))
