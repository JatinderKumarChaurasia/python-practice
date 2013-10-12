# Breadth-first and depth-first searches.
# The only difference is how you pop from the queue of nodes left to visit.

from collections import deque


class Node:
    """
    Represents a graph node, with a value and list on neighbours
    """

    def __init__(self, value):
        self.value = value
        self.neighbours = []


def bdfs(node, visited, to_visit, do_work, breadth_first=True):
    """
    Performs either breadth-first or depth-first search, depending on the flag value
    """

    if node in visited:
        return

    do_work(node)

    visited.append(node)

    neighbours = node.neighbours

    for n in neighbours:
        if not n in visited:
            to_visit.append(n)

    if (len(to_visit) == 0):
        return

    next_node = to_visit.popleft() if breadth_first else to_visit.pop()

    bdfs(next_node, visited, to_visit, do_work, breadth_first)

if __name__ == "__main__":

    def print_node(node):
        print(node.value)

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)

    n1.neighbours = [n2, n3]
    n2.neighbours = [n1]
    n3.neighbours = [n1, n4, n5]
    n4.neighbours = [n3, n1]
    n5.neighbours = [n3]

    print("BFS traversal:")
    bdfs(n1, [], deque(), print_node, True)

    print("DFS traversal:")
    bdfs(n1, [], deque(), print_node, False)
