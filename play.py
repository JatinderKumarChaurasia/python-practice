
def find_pivot(xs):
    listof_sums = []
    running_sum = 0
    for x in xs:
        running_sum += x
        listof_sums.append(running_sum)
    print(listof_sums)
    listof_sums_backwards = []
    running_sum = 0
    for x in reversed(xs):
        running_sum += x
        listof_sums_backwards.append(running_sum)
    print(listof_sums_backwards)
    print(list(reversed(listof_sums_backwards)))
    try:
        candidates = [ x - y for x, y in zip(listof_sums, reversed(listof_sums_backwards))]
        return candidates.index(0)

    except ValueError:
        return -1

