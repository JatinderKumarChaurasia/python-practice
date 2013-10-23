import unittest


def purge_overlaps(alist, interval):
    overlaps = set()
    for another in alist:
        if ((interval[0] < another[0] < interval[1]) or
                (interval[0] < another[1] < interval[1]) or
                (another[0] < interval[0] < another[1]) or
                (another[0] < interval[1] < another[1]) or
                (another[0] == interval[0] and another[1] == interval[1])):
            overlaps.add(another)
    for overlap in overlaps:
        alist.remove(overlap)
    return alist


def find_earliest(alist):
    candidate = alist[0]
    for interval in alist[1:]:
        if interval[1] < candidate[1]:
            candidate = interval
    return candidate


def interval_scheduling(alist):
    result = []
    while alist:
        earliest = find_earliest(alist)
        alist = purge_overlaps(alist, earliest)
        result.append(earliest)
    return result


class ProblemsTest(unittest.TestCase):
    def test_purge_overlaps1(self):
        alist = [(1, 2), (2, 3), (4, 8), (6, 10)]
        interval = (2, 6)
        expected = [(1, 2), (6, 10)]
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)

    def test_purge_overlaps2(self):
        alist = [(1, 2), (2, 3), (4, 8), (6, 10)]
        interval = (1, 10)
        expected = []
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)

    def test_purge_overlaps3(self):
        alist = [(1, 2), (2, 3), (4, 8), (6, 10)]
        interval = (3, 4)
        expected = alist
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)

    def test_purge_overlap4(self):
        alist = [(2, 3), (6, 10)]
        interval = (1, 4)
        expected = [(6, 10)]
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)

    def test_purge_overlap5(self):
        alist = [(1, 4), (4, 8), (6, 10)]
        interval = (2, 3)
        expected = [(4, 8), (6, 10)]
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)

    def test_purge_overlap6(self):
        alist = [(1, 4), (4, 8), (6, 10)]
        interval = (1, 4)
        expected = [(4, 8), (6, 10)]
        actual = purge_overlaps(alist, interval)
        assert (expected == actual)


    def test_interval_schedule(self):
        alist = [(1, 2), (2, 3), (1, 4), (2, 6), (4, 10), (5, 6), (7, 12), (5, 7), (8, 9)]
        expected = [(1, 2), (2, 3), (5, 6), (8, 9)]
        assert (expected == interval_scheduling(alist))


if __name__ == '__main__':
    unittest.main()


